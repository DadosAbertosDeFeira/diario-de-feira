import json
import os
from typing import Dict

from loguru import logger


def extract_keywords(text: str, keywords: Dict[str, list]) -> list:
    text = text.lower()
    found_topics = []
    for topic, words in keywords.items():
        for word in words:
            if word.lower() in text and topic not in found_topics:
                found_topics.append(topic.lower())
    return found_topics


def read_keywords():
    keywords = os.getenv("KEYWORDS") or open("default_keywords.json").read()
    logger.info(f"Keywords:\n{keywords}")
    return json.loads(keywords)
