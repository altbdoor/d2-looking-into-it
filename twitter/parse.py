#!/usr/bin/env python3

import json
from dataclasses import asdict, fields
from os import chdir, path
from typing import Any, List

from models import BaseTweet, Tweet, User

chdir(path.dirname(__file__))

with open("tweets/ids.json", "r", encoding="utf-8") as fp:
    tweet_ids: List[int] = json.load(fp)

user_keys = [(f.name, f.type) for f in fields(User)]
base_keys = [(f.name, f.type) for f in fields(BaseTweet)]


def convert_json_to_class(data: Any, custom_class_name: str):
    re_data = {}
    check_keys = user_keys

    if custom_class_name == "tweet":
        check_keys = base_keys

    for (key, key_type) in check_keys:
        if key not in data:
            continue

        if key_type is str:
            re_data[key] = str(data[key])
        else:
            re_data[key] = data[key]

    if custom_class_name == "user":
        return User(**re_data)
    elif custom_class_name == "tweet":
        return Tweet(**re_data)


processed_tweets = []

for tweet_id in tweet_ids:
    with open(f"tweets/{tweet_id}.json", "r", encoding="utf-8") as fp:
        json_tweet = json.load(fp)

    current_user = convert_json_to_class(json_tweet["user"], "user")
    current_tweet = convert_json_to_class(json_tweet, "tweet")
    current_tweet.custom_user = current_user

    replying_to_id = json_tweet["inReplyToTweetId"]

    if path.exists(f"tweets/{replying_to_id}.json"):
        with open(f"tweets/{replying_to_id}.json", "r", encoding="utf-8") as fp:
            json_replying_to_tweet = json.load(fp)

        replying_to_user = convert_json_to_class(json_replying_to_tweet["user"], "user")
        replying_to_tweet = convert_json_to_class(json_replying_to_tweet, "tweet")
        replying_to_tweet.custom_user = replying_to_user

        current_tweet.custom_replying_to = replying_to_tweet

    processed_tweets.append(asdict(current_tweet))

with open("tweets/compiled.json", "w", encoding="utf-8") as fp:
    json.dump(processed_tweets, fp, ensure_ascii=False)
