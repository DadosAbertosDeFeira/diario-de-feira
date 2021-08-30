import pytest
from unittest.mock import call

from main import get_todays_gazette, tweet


def test_if_tweet_was_post_on_twitter(mocker):
    mock_tweepy = mocker.patch("main.tweepy")
    tweet("Hi")

    assert mock_tweepy.OAuthHandler.called
    assert mock_tweepy.API.called
    assert call().update_status("Hi") in mock_tweepy.API.mock_calls


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

    mock_response = mocker.patch("main.requests.get")
    mock_response.return_value.ok = True
    mock_response.return_value.json.return_value = expected_result

    result = get_todays_gazette()

    assert mock_response.called
    assert result != []


def test_get_todays_gazette_token_not_valid(mocker):
    expected_result = {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }

    mock_response = mocker.patch("main.requests.get")
    mock_response.return_value.raise_for_status.side_effect = KeyError
    mock_response.return_value.json.return_value = expected_result

    with pytest.raises(KeyError) as exc:
        get_todays_gazette()
        assert exc('results')
        assert expected_result['code'] == "token_not_valid"
        assert mock_response.status_code in [401, 403]
