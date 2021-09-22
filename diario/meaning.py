from typing import Dict


def extract_keywords(text: str, keywords: Dict[str, list]) -> list:
    text = text.lower()
    found_topics = []
    for topic, words in keywords.items():
        for word in words:
            if word.lower() in text and topic not in found_topics:
                found_topics.append(topic.lower())
    return found_topics


def split_tweets(found_topics: list, character_limit: int):
    tweet = []
    tweet_list = []
    character_sum = 0

    for word in found_topics:
        if character_sum + len(word) < character_limit:
            tweet.append(word)
        else:
            tweet_list.append(tweet)
            tweet = []
            tweet.append(word)

        character_sum = sum([len(item) for item in tweet])

    tweet_list.append(tweet)
    return tweet_list
