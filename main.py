import os
import tweepy

from loguru import logger
from dotenv import load_dotenv


load_dotenv()

def tweet():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    try:
        api = tweepy.API(auth)
        tweet_message = 'test'
        api.update_status(tweet_message)

        logger.info(f"Tweet posted with the message: {tweet_message}")
        return {'post_tweet': True}  
    except Exception as e:
        logger.error(e)
