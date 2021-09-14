from diario.meaning import extract_keywords


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


# TODO oq acontece se o texto está vazio ou nulo?
# TODO Ou se tem um texto válido mas keywords está vazio ({})?
