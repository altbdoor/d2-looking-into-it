#!/usr/bin/env python3

import json
import random
import urllib.parse
import urllib.request
from os import chdir, mkdir, path

chdir(path.dirname(__file__))

queries = (
    "aware",
    "looking into it",
    "look into it",
    "looking into this",
    "look into this",
)

persons = (
    "dmg04",
    "cozmo23",
    "dirtyeffinhippy",
)

joined_queries = urllib.parse.quote_plus("|".join(queries))
joined_persons = urllib.parse.quote_plus(",".join(persons))


def prepare_reddit_request(url: str):
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/79.0.3945.{random.randint(0, 9999)} Safari/537.{random.randint(0, 99)}"
            )
        },
    )


print(">> preparing folders")
if not path.exists("data"):
    mkdir("data")

print(">> building query")
query_url = (
    "https://api.pushshift.io/reddit/comment/search"
    f"?html_decode=true&author={joined_persons}&subreddit=DestinyTheGame"
    f"&q={joined_queries}&size=50"
)
print(f"<< {query_url}")

print(">> fetching posts")
with urllib.request.urlopen(query_url) as response:
    response_text = response.read()

    with open("data/posts.json", "wb") as fp:
        fp.write(response_text)

query_data = json.loads(response_text)
parent_ids = [post["parent_id"] for post in query_data["data"]]

print(">> fetching replies")
parent_url = f'https://old.reddit.com/api/info.json?id={",".join(parent_ids)}'
req = prepare_reddit_request(parent_url)

with urllib.request.urlopen(req) as response:
    with open("data/replies.json", "wb") as fp:
        fp.write(response.read())
