import os
from datetime import date

import requests
from loguru import logger


def create_api_token():
    url = f"{os.getenv('MARIA_QUITERIA_API_HOST')}/token/"
    data = {
        "username": f"{os.getenv('MARIA_QUITERIA_USERNAME')}",
        "password": f"{os.getenv('MARIA_QUITERIA_PASSWORD')}",
    }

    logger.info("Getting token from Maria Quitéria")
    token_response = requests.post(url, data=data)
    token_response.raise_for_status()

    return token_response.json()["access"]


def get_todays_gazette(gazette_date=None):
    token_maria_quiteria = create_api_token()

    params = {"start_date": date.today().strftime("%Y-%m-%d")}
    url = f"{os.getenv('MARIA_QUITERIA_API_HOST')}/gazettes/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_maria_quiteria}",
    }

    if gazette_date:
        params = {"start_date": gazette_date, "end_date": gazette_date}

    try:
        logger.info("Looking for gazettes")
        response = requests.get(url, headers=headers, params=params)
        response_json = response.json()

        gazettes = [result for result in response_json["results"]]
        logger.info(f"Number of gazettes found: {len(gazettes)}")
    except KeyError as e:
        logger.exception(e)
        raise KeyError

    return gazettes
