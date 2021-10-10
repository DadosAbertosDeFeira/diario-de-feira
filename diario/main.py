import json
import os
from datetime import date, datetime

import requests
import tweepy
from dotenv import load_dotenv
from loguru import logger

from diario.meaning import extract_keywords, split_tweets

load_dotenv()

CHARACTER_LIMIT = 270


def tweet(message: str, tweet_id=None):
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

    api = tweepy.API(auth)
    try:
        tweet = api.update_status(message, tweet_id)
        tweet_id = tweet._json["id_str"]
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
    date_today = date.today().strftime("%Y-%m-%d")
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
        logger.debug(response)
        response_json = response.json()

        gazettes = [result for result in response_json["results"]]
        logger.info(f"Number of gazettes found: {len(gazettes)}")
    except KeyError as e:
        logger.exception(e)
        raise KeyError

    return gazettes


def read_keywords():
    keywords = os.getenv("KEYWORDS") or open("default_keywords.json").read()
    logger.info(f"Keywords:\n{keywords}")
    return json.loads(keywords)


def post_todays_gazette(gazettes: list):
    for gazette in gazettes:
        date_br = datetime.strptime(gazette["date"], "%Y-%m-%d").strftime("%d/%m/%y")
        tweet_message = (
            f"Saiu uma nova edição do #DiárioOficial do poder {gazette['power']} "
            f"de #FeiradeSantana ({date_br} - {gazette['year_and_edition']}). "
            f"📰\n{gazette['files'][0]['url']}"
        )
        tweet_id = tweet(tweet_message)
        if tweet_id is None:
            continue
        logger.info("The gazette was posted on twitter!")

        keywords = read_keywords()
        if keywords:
            logger.info("Keywords found.")
        events_text = "".join(
            f"{event['title']} {event['summary']}" for event in gazette["events"]
        )

        found_topics = extract_keywords(events_text, keywords)
        logger.info(f"Number of found topics: {len(found_topics)}")
        if found_topics:
            character_number = sum(len(topic_len) for topic_len in found_topics)
            if character_number > CHARACTER_LIMIT:
                tweets = split_tweets(found_topics, CHARACTER_LIMIT)
                for index, post in enumerate(tweets):
                    if index == 0:
                        reply_message = f"Nele temos: {', '.join(post)}"
                    else:
                        reply_message = f"Temos também: {', '.join(post)}"
                    tweet_id = tweet(reply_message, tweet_id)
                    logger.info("The thread was posted")
            else:
                reply_message = f"Nele temos: {', '.join(found_topics)}"
                tweet(reply_message, tweet_id)
                logger.info("The thread was posted")


if __name__ == "__main__":
    gazettes = get_todays_gazette()
    post_todays_gazette(gazettes)
