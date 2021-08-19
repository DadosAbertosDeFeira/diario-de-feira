import os
from requests.models import Response
import tweepy
import requests
import json
import datetime
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def tweet(message: str):
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth)
    api.update_status(message)


def get_todays_gazette():
    official_diary= []

    date_today = datetime.date.today().strftime('%Y-%m-%d')

    url = os.getenv('MARIA_QUITERIA_API_URL')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.getenv('MARIA_QUITERIA_API_TOKEN')
    }
    
    response = requests.get(url, headers=headers)
    response_json = response.json()
    
    for resp in response_json['results']:
        import pdb;pdb.set_trace()
        if resp['date'] == date_today:
            print(resp['date'])
            official_diary.append(resp)

    return official_diary


def post_todays_gazette(official_diary: list):
    date_today = datetime.date.today().strftime('%Y-%m-%d')
    for diary in official_diary:
        tweet_message = f"Saiu uma nova edição do #DiárioOficial do poder {diary['power']} de #FeiradeSantana ({date_today} - {diary['year_and_edition']}).\n{diary['files'][0]['url']}"
        tweet(tweet_message)


if __name__ == '__main__':
    official_diary = get_todays_gazette()
    post_todays_gazette(official_diary)
