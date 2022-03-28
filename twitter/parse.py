#!/usr/bin/env python3

import json
from os import chdir, path
from typing import Any, List

chdir(path.dirname(__file__))

with open("tweets/ids.json", "r", encoding="utf-8") as fp:
    tweet_ids: List[int] = json.load(fp)


def convert_json_to_dict(data: Any, dict_type: str):
    if dict_type == "user":
        return {
            "username": data["username"],
            "id": str(data["id"]),
            "url": data["url"],
            "imageUrl": data["profileImageUrl"],
        }
    elif dict_type == "tweet":
        return {
            "id": str(data["id"]),
            "url": data["url"],
            "date": data["date"],
            "content": data["content"],
        }


processed_tweets = []

for tweet_id in tweet_ids:
    with open(f"tweets/{tweet_id}.json", "r", encoding="utf-8") as fp:
        json_tweet = json.load(fp)

    current_tweet = convert_json_to_dict(json_tweet, "tweet")
    current_tweet["user"] = convert_json_to_dict(json_tweet["user"], "user")
    current_tweet["replying_to"] = None
    current_tweet["platform"] = "twitter"

    replying_to_id = json_tweet["inReplyToTweetId"]
    if path.exists(f"tweets/{replying_to_id}.json"):
        with open(f"tweets/{replying_to_id}.json", "r", encoding="utf-8") as fp:
            json_replying_to_tweet = json.load(fp)

        replying_to_tweet = convert_json_to_dict(json_replying_to_tweet, "tweet")
        replying_to_tweet["user"] = convert_json_to_dict(
            json_replying_to_tweet["user"], "user"
        )
        current_tweet["replying_to"] = replying_to_tweet

    processed_tweets.append(current_tweet)

with open("tweets/compiled.json", "w", encoding="utf-8") as fp:
    json.dump(processed_tweets, fp, ensure_ascii=False)
