import datetime
import os

import requests
import tweepy
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def tweet(message: str):
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

    api = tweepy.API(auth)
    api.update_status(message)
    logger.info("The gazette was posted on twitter!")


def refresh_maria_quiteria_api_token():
    headers = {
        "content_Type": "application/json"
    }
    url = os.getenv("MARIA_QUITERIA_API_URL_TOKEN")
    data = {
        "username":f"{os.getenv('USERNAME_CREDENCIALS')}",
        "password": f"{os.getenv('PASSWORD_CREDENCIALS')}"
    }

    refresh_token_response = requests.post(url, headers=headers, data=data)
    if refresh_token_response.status_code == 200:
        logger.info('New token created')
        new_token = f"Bearer {refresh_token_response.json()['access']}"    

    return new_token


def get_todays_gazette():
    gazettes = []

    date_today = datetime.date.today().strftime("%Y-%m-%d")

    params = {"start_date": date_today}
    url = os.getenv("MARIA_QUITERIA_API_URL")
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv("MARIA_QUITERIA_API_TOKEN"),
    }
    success = False
    number_of_attempts = 0
    while success == False and number_of_attempts < 4:
        try:
            logger.info("Looking for gazettes")
            response = requests.get(url, headers=headers, params=params)

            response_json = response.json()
            for result in response_json["results"]:
                gazettes.append(result)
            success = True
        except KeyError as e:
            logger.exception(e)
            if (response.status_code in [401, 403]) and response.json()['code'] == "token_not_valid":
                logger.info("Token is invalid or expired. Getting new token")
                new_token = refresh_maria_quiteria_api_token()
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": new_token,
                }
            number_of_attempts += 1
            logger.info(f"Trying to get gazettes again. Attempt {number_of_attempts}/3.")
            continue
    
    if gazettes == []:
        logger.debug("Failed to fetch gazettes")
    return gazettes


def post_todays_gazette(gazettes: list):
    date_today = datetime.date.today().strftime("%Y-%m-%d")
    for gazette in gazettes:
        tweet_message = (
            f"Saiu uma nova edição do #DiárioOficial do poder {gazette['power']} "
            f"de #FeiradeSantana ({date_today} - {gazette['year_and_edition']}). 📰\n"
            f"{gazette['files'][0]['url']}"
        )
        tweet(tweet_message)


if __name__ == "__main__":
    gazettes = get_todays_gazette()
    post_todays_gazette(gazettes)
