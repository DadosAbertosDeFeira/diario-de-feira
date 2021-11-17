from diario_bot.keywords import extract_keywords
from diario_bot.twitter import post_gazette


def test_extract_keywords_from_a_text():
    text = """
    Altera o Decreto Nº 12.312/2021, que “Dispõe sobre novas medidas para o
    enfrentamento da Calamidade Pública de Saúde decorrente do Coronavírus
    (COVID-19).”
    DECRETO N° 12.323, DE 13 DE SETEMBRO DE 2021. (Gabinete do Prefeito):
    Fica aberto Crédito
    DECRETO INDIVIDUAL Nº 725/2021 (Gabinete do Prefeito):
    Nomear LUCIANA CONCEIÇÃO SOUZA SANTOS,
    para o cargo de Coordenadora de Projetos Especiais Nível III, do Gabinete do
    Prefeito, símbolo DA-3.
    DECRETO INDIVIDUAL Nº 724/2021 (Gabinete do Prefeito): JEFERSON SILVA GONÇALVES -
    Exonera, a pedido do cargo de Coordenador de Projetos Especiais Nível III,
    do Gabinete do Prefeito, símbolo DA-3.
    """
    keywords = {
        "decretos": ["decreto"],
        "contratações": ["nomea", "exonera"],
        "pandemia": ["covid", "coronavirus", "pandemia", "Coronavírus", "COVID-19"],
    }

    expected = ["decretos", "contratações", "pandemia"]
    assert extract_keywords(text, keywords) == expected


def test_if_text_empty():
    text = ""
    keywords = {
        "decretos": ["decreto"],
        "contratações": ["nomea", "exonera"],
        "pandemia": ["covid", "coronavirus", "pandemia", "Coronavírus", "COVID-19"],
    }

    assert extract_keywords(text, keywords) == []


def test_if_keywords_empty():
    text = """
    Altera o Decreto Nº 12.312/2021, que “Dispõe sobre novas medidas para o
    enfrentamento da Calamidade Pública de Saúde decorrente do Coronavírus
    (COVID-19).”
    DECRETO N° 12.323, DE 13 DE SETEMBRO DE 2021. (Gabinete do Prefeito):
    Fica aberto Crédito
    DECRETO INDIVIDUAL Nº 725/2021 (Gabinete do Prefeito):
    Nomear LUCIANA CONCEIÇÃO SOUZA SANTOS,
    para o cargo de Coordenadora de Projetos Especiais Nível III, do Gabinete do
    Prefeito, símbolo DA-3.
    DECRETO INDIVIDUAL Nº 724/2021 (Gabinete do Prefeito): JEFERSON SILVA GONÇALVES -
    Exonera, a pedido do cargo de Coordenador de Projetos Especiais Nível III,
    do Gabinete do Prefeito, símbolo DA-3.
    """

    keywords = {}

    assert extract_keywords(text, keywords) == []


def test_read_default_keywords_from_file(mocker, monkeypatch):
    mock_tweet = mocker.patch("diario_bot.twitter.tweet")
    monkeypatch.delenv("KEYWORDS", raising=False)
    gazettes = [
        {
            "crawled_from": "https://diariooficial.feiradesantana.ba.gov.br/",
            "date": "2021-09-25",
            "power": "executivo",
            "year_and_edition": "Ano VII - Edição Nº 1870",
            "events": [
                {
                    "title": "Editais - Auto de Infração nº 127/2021 a 142/2021",
                    "secretariat": "SESP - Serviços Públicos",
                    "summary": "Referente a não retirada de material de construção "
                    "e entulho na via pública e a não construção de muro "
                    "e passeio em terreno baldio.",
                    "published_on": None,
                },
                {
                    "title": "ADITIVOS",
                    "secretariat": "Gabinete do Prefeito",
                    "summary": "ADITIVO Nº 440-2021-12AC.",
                    "published_on": None,
                },
                {
                    "title": "DECRETO Nº 12.347, DE 24 DE SETEMBRO DE 2021.",
                    "secretariat": "Gabinete do Prefeito",
                    "summary": "Abre crédito suplementar ao Orçamento do Município",
                    "published_on": None,
                },
            ],
            "files": [{"url": "http://diariooficial.feiradesantana.ba.gov.br/"}],
        }
    ]
    expected_tweet = "Nele temos: decretos, aditivos, intimação"

    post_gazette(gazettes)

    assert mock_tweet.call_count == 2
    assert expected_tweet in mock_tweet.mock_calls[1].args[0]
