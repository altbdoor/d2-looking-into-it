#!/usr/bin/env python3

import json
from datetime import datetime
from os import chdir, path
from typing import Any

chdir(path.dirname(__file__))

with open("reddit/data/compiled.json", "r", encoding="utf-8") as fp:
    reddit = json.load(fp)

with open("twitter/tweets/compiled.json", "r", encoding="utf-8") as fp:
    twitter = json.load(fp)

compiled = [*reddit, *twitter]


def get_data_date(data: Any):
    return datetime.fromisoformat(data["date"]).timestamp()


compiled_sorted = sorted(compiled, key=get_data_date, reverse=True)
with open("website/_data/compiled.json", "w", encoding="utf-8") as fp:
    json.dump(compiled_sorted, fp, ensure_ascii=False)
