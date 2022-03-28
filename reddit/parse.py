#!/usr/bin/env python3

import json
from os import chdir, path
from datetime import datetime
from typing import Any

chdir(path.dirname(__file__))

with open("data/posts.json", "r", encoding="utf-8") as fp:
    posts = json.load(fp)

with open("data/replies.json", "r", encoding="utf-8") as fp:
    replies = json.load(fp)


def convert_json_to_dict(data: Any, dict_type: str):
    if dict_type == "user":
        return {
            "username": data["author"],
            "id": data.get("author_fullname", ""),
            "url": f'https://www.reddit.com/user/{data["author"]}',
            "imageUrl": None,
        }
    elif dict_type == "post":
        return {
            "id": data["id"],
            "url": f'https://www.reddit.com{data["permalink"]}',
            "date": datetime.utcfromtimestamp(data["created_utc"]).isoformat(),
            "content": data["body"] if "body" in data else data["selftext"],
        }


processed_posts = []

for post in posts["data"]:
    replying_to_data = next(
        filter(
            lambda child: child["data"]["name"] == post["parent_id"],
            replies["data"]["children"],
        ),
        None,
    )

    current_post = convert_json_to_dict(post, "post")
    current_post["user"] = convert_json_to_dict(post, "user")
    current_post["replying_to"] = None
    current_post["platform"] = "reddit"

    if replying_to_data:
        replying_to_post = convert_json_to_dict(replying_to_data["data"], "post")
        replying_to_post["user"] = convert_json_to_dict(
            replying_to_data["data"], "user"
        )
        current_post["replying_to"] = replying_to_post

    processed_posts.append(current_post)

with open("data/compiled.json", "w", encoding="utf-8") as fp:
    json.dump(processed_posts, fp, ensure_ascii=False)
