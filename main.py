import os
import tweepy

from loguru import logger
from dotenv import load_dotenv


load_dotenv()


def tweet(message: str):
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth)
    api.update_status(message)
