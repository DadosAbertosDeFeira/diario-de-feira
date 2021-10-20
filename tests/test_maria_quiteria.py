import pytest
from requests import HTTPError

from diario_bot.apis.maria_quiteria import create_api_token, get_todays_gazette


def test_raise_exception_when_token_is_not_valid(mocker):
    mock_response = mocker.patch("diario_bot.apis.maria_quiteria.requests.post")
    mock_response.return_value.status_code = 401
    mock_response.return_value.raise_for_status.side_effect = HTTPError

    with pytest.raises(HTTPError):
        create_api_token()


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

    mock_token = mocker.patch("diario_bot.apis.maria_quiteria.create_api_token")
    mock_token.return_value = "token-fake"

    mock_response = mocker.patch("diario_bot.apis.maria_quiteria.requests.get")
    mock_response.return_value.ok = True
    mock_response.return_value.json.return_value = expected_result

    result = get_todays_gazette()

    assert mock_response.called
    assert result != []
