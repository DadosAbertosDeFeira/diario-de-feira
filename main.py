import os
import tweepy

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv()


auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMOR_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

api.update_status('Hello again')
