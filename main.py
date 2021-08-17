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


def get_todays_official_diary():
    official_diary= []

    url = os.getenv('URL_API_MARIA_QUITERIA')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.getenv('TOKEN')
    }
    
    response = requests.get(url, headers=headers)
    response_json = response.json()
    
    date_today = datetime.date.today()
    for resp in response_json['results']:
        if resp['date'] == '2021-08-14': #date_today:
            official_diary.append(resp)

    return official_diary


def post_todays_official_diary(official_diary: list):
    for diary in official_diary:
        tweet_message = f"Saiu uma nova edição do #DiárioOficial do poder {diary['power']} de #FeiradeSantana ({'2021-08-14'} - {diary['year_and_edition']}).\n{diary['files'][0]['url']}"
        tweet(tweet_message)


if __name__ == '__main__':
    official_diary = get_todays_official_diary()
    post_todays_official_diary(official_diary)