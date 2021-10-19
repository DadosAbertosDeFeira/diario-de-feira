import os
from datetime import datetime

import tweepy
from loguru import logger

from diario.keywords import extract_keywords, read_keywords

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


def split_tweets(found_topics: list, character_limit: int):
    tweet = []
    tweet_list = []
    character_sum = 0

    for word in found_topics:
        if character_sum + len(word) >= character_limit:
            tweet_list.append(tweet)
            tweet = []
        tweet.append(word)
        character_sum = sum(len(item) for item in tweet)

    tweet_list.append(tweet)
    return tweet_list


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
