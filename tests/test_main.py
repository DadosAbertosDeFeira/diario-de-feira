from unittest.mock import call

import pytest
from requests import HTTPError

from diario.main import (
    create_maria_quiteria_api_token,
    get_todays_gazette,
    post_todays_gazette,
    tweet,
)


def test_if_tweet_was_posted_on_twitter(mocker):
    mock_tweepy = mocker.patch("diario.main.tweepy")
    tweet("Hi")

    assert mock_tweepy.OAuthHandler.called
    assert mock_tweepy.API.called
    assert call().update_status("Hi", None) in mock_tweepy.API.mock_calls


def test_if_get_todays_gazette_return_result(mocker):
    expected_result = {
        "count": 249,
        "next": "...",
        "previous": None,
        "results": [
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
        ],
    }

    mock_token = mocker.patch("diario.main.create_maria_quiteria_api_token")
    mock_token.return_value = "token-fake"

    mock_response = mocker.patch("diario.main.requests.get")
    mock_response.return_value.ok = True
    mock_response.return_value.json.return_value = expected_result

    result = get_todays_gazette()

    assert mock_response.called
    assert result != []


def test_raise_exception_when_token_is_not_valid(mocker):
    mock_response = mocker.patch("diario.main.requests.post")
    mock_response.return_value.status_code = 401
    mock_response.return_value.raise_for_status.side_effect = HTTPError

    with pytest.raises(HTTPError):
        create_maria_quiteria_api_token()


def test_thread_creation_when_there_are_events(mocker, monkeypatch):
    monkeypatch.setenv("KEYWORDS", '{"rh": ["folha de pagamento"]}')
    mock_tweet = mocker.patch("diario.main.tweet")
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

    post_todays_gazette(gazettes)

    assert mock_tweet.called
    assert "Nele temos: rh" in mock_tweet.mock_calls[1].args[0]
