from main import tweet
from unittest import mock


def test_if_tweet_was_post_on_twitter():
    mock_response = mock.Mock(return_value={'post_tweet': True})

    result = tweet()

    assert result == mock_response.return_value
