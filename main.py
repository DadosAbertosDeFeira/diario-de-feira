import ast
import datetime
import json
import os
import pdb
from typing import Optional

import requests
import tweepy
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def tweet(message: str, tweet_id=None):
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

    api = tweepy.API(auth)
    try:
        tweet = api.update_status(message, tweet_id)
        tweet_id = tweet._json["id_str"]
        logger.info("The gazette was posted on twitter!")
        return tweet_id
    except tweepy.TweepError as e:
        logger.exception(e)


def create_maria_quiteria_api_token():
    url = f"{os.getenv('MARIA_QUITERIA_API_HOST')}/token/"
    data = {
        "username": f"{os.getenv('MARIA_QUITERIA_USERNAME')}",
        "password": f"{os.getenv('MARIA_QUITERIA_PASSWORD')}",
    }

    logger.info("Getting token from Maria Quitéria")
    token_response = requests.post(url, data=data)
    token_response.raise_for_status()

    return token_response.json()["access"]


def get_todays_gazette():
    date_today = datetime.date.today().strftime("%Y-%m-%d")
    token_maria_quiteria = create_maria_quiteria_api_token()

    params = {"start_date": date_today}
    url = f"{os.getenv('MARIA_QUITERIA_API_HOST')}/gazettes/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_maria_quiteria}",
    }

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


def post_todays_gazette(gazettes: list):
    for gazette in gazettes:
        tweet_message = (
            f"Saiu uma nova edição do #DiárioOficial do poder {gazette['power']} "
            f"de #FeiradeSantana ({gazette['date']} - {gazette['year_and_edition']}). "
            f"📰\n{gazette['files'][0]['url']}"
        )

        tweet_id = tweet(tweet_message)

        number_of_events = len(gazette["events"])
        logger.info(f"Quantidade de events encontrados: {number_of_events}")

        mapped_keywords = {}
        keywords = ast.literal_eval(os.getenv("KEYWORDS"))
        for event in gazette["events"]:
            for keyword in keywords:
                if keyword in event["title"].lower():
                    number_of_events -= 1
                    if keyword in mapped_keywords:
                        mapped_keywords[keyword] += 1
                        break
                    else:
                        mapped_keywords[keyword] = 1
                        break

        list_events = []
        for key, value in mapped_keywords.items():
            message = f"{key}({value})"
            list_events.append(message)

        reply_message = f"Nele temos: {', '.join(list_events)}"
        tweet_id = tweet(reply_message, tweet_id)

        mapped_subjects = []
        subject_keywords = ast.literal_eval(os.getenv("SUBJECT_KEYWORDS"))
        for event in gazette["events"]:
            for subject in subject_keywords:
                if (
                    subject in event["secretariat"].lower()
                    and subject not in mapped_subjects
                ):
                    mapped_subjects.append(subject)

        if mapped_subjects != []:
            reply_message_subject = (
                f"Alguns assuntos tratados foram: {', '.join(mapped_subjects)}"
            )
            tweet_id = tweet(reply_message_subject, tweet_id)


if __name__ == "__main__":
    gazettes = get_todays_gazette()
    post_todays_gazette(gazettes)
