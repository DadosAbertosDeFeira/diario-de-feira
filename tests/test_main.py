from unittest import mock
from main import tweet
from unittest.mock import call


def test_if_tweet_was_post_on_twitter(mocker):
    mock_tweepy = mocker.patch('main.tweepy')

    tweet('Hi')

    assert mock_tweepy.OAuthHandler.called
    assert mock_tweepy.API.called
    assert call().update_status('Hi') in mock_tweepy.API.mock_calls
