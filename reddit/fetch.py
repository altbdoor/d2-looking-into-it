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
)

persons = (
    "dmg04",
    "cozmo23",
    "dirtyeffinhippy",
)

joined_queries = urllib.parse.quote_plus("|".join(queries))
joined_persons = urllib.parse.quote_plus(",".join(persons))

print(">> preparing folders")
if not path.exists("data"):
    mkdir("data")

query_url = (
    "https://api.pushshift.io/reddit/comment/search"
    f"?html_decode=true&author={joined_persons}&subreddit=DestinyTheGame"
    f"&q={joined_queries}&size=50"
)

response = urllib.request.urlopen(query_url)
query_data = json.loads(response.read())

filtered_data = []
parent_ids = []

for post in query_data["data"]:
    # gonna exclude submissions for now...
    if not post["parent_id"].startswith("t1_"):
        continue

    parent_ids.append(post["parent_id"])
    filtered_data.append(post)

with open("data/query.json", "w", encoding="utf-8") as fp:
    json.dump(filtered_data, fp)

parent_url = f'https://old.reddit.com/api/info.json?id={",".join(parent_ids)}'

req = urllib.request.Request(
    parent_url,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/79.0.3945.{random.randint(0, 9999)} Safari/537.{random.randint(0, 99)}"
        )
    },
)

with urllib.request.urlopen(req) as response:
    with open("data/parents.json", "wb") as fp:
        fp.write(response.read())
