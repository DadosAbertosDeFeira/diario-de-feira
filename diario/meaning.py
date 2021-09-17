from typing import Dict


def extract_keywords(text: str, keywords: Dict[str, list]) -> list:
    text = str(text).lower()
    found_topics = []
    for topic, words in keywords.items():
        for word in words:
            if word.lower() in text and topic not in found_topics:
                found_topics.append(topic.lower())
    return found_topics
