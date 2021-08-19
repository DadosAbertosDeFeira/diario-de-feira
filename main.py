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
    gazettes = []

    date_today = datetime.date.today().strftime('%Y-%m-%d')

    params = {'start_date': date_today}
    url = os.getenv('MARIA_QUITERIA_API_URL')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': os.getenv('MARIA_QUITERIA_API_TOKEN')
    }
    
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()

    for result in response_json['results']:
        gazettes.append(result)

    return gazettes


def post_todays_gazette(gazettes: list):
    date_today = datetime.date.today().strftime('%Y-%m-%d')
    for gazette in gazettes:
        tweet_message = f"Saiu uma nova edição do #DiárioOficial do poder {gazette['power']} de #FeiradeSantana ({date_today} - {gazette['year_and_edition']}).\n{gazette['files'][0]['url']}"
        tweet(tweet_message)


if __name__ == '__main__':
    gazettes = get_todays_gazette()
    post_todays_gazette(gazettes)
