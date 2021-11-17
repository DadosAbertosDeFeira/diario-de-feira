from unittest.mock import call

from diario_bot.twitter import post_gazette, split_tweets, tweet


def test_split_tweets_return_list():
    expected_found_topics = [
        "decretos",
        "contratações",
        "dispensa de licitação",
        "pandemia",
        "portaria",
    ]
    character_limit = 30
    tweet_list = split_tweets(expected_found_topics, character_limit)

    assert tweet_list != []
    assert len(tweet_list) == 3


def test_thread_creation_when_there_are_events(mocker, monkeypatch):
    monkeypatch.setenv("KEYWORDS", '{"rh": ["folha de pagamento"]}')
    mock_tweet = mocker.patch("diario_bot.twitter.tweet")
    gazettes = [
        {
            "crawled_from": "https://diariooficial.feiradesantana.ba.gov.br",
            "date": "2021-09-07",
            "power": "executivo",
            "year_and_edition": "Ano VII - Edição Nº 1851",
            "events": [
                {
                    "title": "INEXIGIBILIDADE DE LICITAÇÃO Nº 219-2021-05I",
                    "secretariat": "Gabinete do Prefeito",
                    "summary": "INSCRIÇÃO DE CURSO PRESENCIAL DE CAPACITAÇÃO.",
                    "published_on": None,
                },
                {
                    "title": "DISPENSA DE CHAMAMENTO PÚBLICO Nº 276-2021-12D",
                    "secretariat": "Gabinete do Prefeito",
                    "summary": "PAGAMENTO DE FOLHA DE PAGAMENTO.",
                    "published_on": None,
                },
            ],
            "files": [{"url": "http://diariooficial.feiradesantana.ba.gov.br/"}],
        }
    ]

    post_gazette(gazettes)
    assert mock_tweet.called
    assert "Nele temos: rh" in mock_tweet.mock_calls[1].args[0]


def test_if_tweet_was_posted_on_twitter(mocker):
    mock_tweepy = mocker.patch("diario_bot.twitter.tweepy")
    tweet("Hi")

    assert mock_tweepy.OAuthHandler.called
    assert mock_tweepy.API.called
    assert call().update_status("Hi", None) in mock_tweepy.API.mock_calls


def test_when_need_post_multiple_threads(mocker, monkeypatch):
    mock_tweet = mocker.patch("diario_bot.twitter.tweet")
    monkeypatch.setenv(
        "KEYWORDS",
        """
        {
            "INEXIGIBILIDADE DE LICITAÇÃO": ["CURSO"],
            "DISPENSA DE CHAMAMENTO PÚBLICO": ["PAGAMENTO"],
            "EXTRATO RESUMO DE ADITIVOS": ["Aditivos"]
        }
        """,
    )
    monkeypatch.setattr("diario_bot.twitter.CHARACTER_LIMIT", 40)

    gazettes = [
        {
            "crawled_from": "https://diariooficial.feiradesantana.ba.gov.br",
            "date": "2021-09-07",
            "power": "executivo",
            "year_and_edition": "Ano VII - Edição Nº 1851",
            "events": [
                {
                    "title": "INEXIGIBILIDADE DE LICITAÇÃO Nº 219-2021-05I",
                    "secretariat": "Gabinete do Prefeito",
                    "summary": "INSCRIÇÃO DE CURSO PRESENCIAL DE CAPACITAÇÃO.",
                    "published_on": None,
                },
                {
                    "title": "DISPENSA DE CHAMAMENTO PÚBLICO",
                    "secretariat": "Gabinete do Prefeito",
                    "summary": "PAGAMENTO DE FOLHA DE PAGAMENTO.",
                    "published_on": None,
                },
                {
                    "title": "EXTRATO RESUMO DE ADITIVOS",
                    "secretariat": "CÂMARA MUNICIPAL",
                    "summary": "Extrato Resumo dos Aditivos Firmados em setembro",
                    "published_on": None,
                },
            ],
            "files": [{"url": "http://diariooficial.feiradesantana.ba.gov.br/"}],
        }
    ]

    post_gazette(gazettes)
    assert mock_tweet.call_count == 4
    assert (
        "Nele temos: inexigibilidade de licitação" in mock_tweet.mock_calls[1].args[0]
    )
    assert (
        "Temos também: dispensa de chamamento público"
        in mock_tweet.mock_calls[2].args[0]
    )
    assert (
        "Temos também: extrato resumo de aditivos" in mock_tweet.mock_calls[3].args[0]
    )


def test_date_format_is_correct(mocker):
    mock_tweet = mocker.patch("diario_bot.twitter.tweet")

    gazettes = [
        {
            "crawled_from": "...",
            "date": "2021-08-14",
            "power": "legislativo",
            "year_and_edition": "Ano xxx - Edição Nº xxx",
            "events": [
                {
                    "title": "TEXT",
                    "secretariat": "TEXT",
                    "summary": "TEXT",
                    "published_on": None,
                }
            ],
            "files": [{"url": "..."}],
        }
    ]

    expected_date = "14/08/21"

    post_gazette(gazettes)

    assert expected_date in mock_tweet.mock_calls[0].args[0]
