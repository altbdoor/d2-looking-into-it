#!/usr/bin/env python3

import json
from os import chdir, mkdir, path

from snscrape.base import ScraperException
from snscrape.modules import twitter as sntwitter

chdir(path.dirname(__file__))

queries = (
    "aware",
    "looking into it",
    "look into it",
)

persons = (
    "A_dmg04",
    "cozmo23",
    "DirtyEffinHippy",
)

joined_queries = " OR ".join((f'"{q}"' for q in queries))
joined_persons = " OR ".join((f"from:{p}" for p in persons))

print(">> building query")
full_query = f"({joined_queries}) ({joined_persons}) filter:replies"
print(f"<< {full_query}")
max_results = 40

print(">> preparing folders")
if not path.exists("tweets"):
    mkdir("tweets")

print(">> scraping tweets")
tweet_ids = []
reply_ids = []

for i, data in enumerate(
    sntwitter.TwitterSearchScraper(full_query).get_items(), start=1
):
    tweet: sntwitter.Tweet = data
    print(f">> processing ID {tweet.id}")

    tweet_ids.append(tweet.id)
    reply_ids.append(tweet.inReplyToTweetId)

    fp = open(f"tweets/{tweet.id}.json", "w", encoding="utf-8")
    fp.write(tweet.json())
    fp.close()

    if i >= max_results:
        break

with open("tweets/ids.json", "w", encoding="utf-8") as fp:
    json.dump(tweet_ids, fp)

print(">> scraping replies")
for reply_id in reply_ids:
    try:
        gen = sntwitter.TwitterTweetScraper(reply_id).get_items()
        tweet: sntwitter.Tweet = next(gen)
        print(f">> processing ID {tweet.id}")

        with open(f"tweets/{tweet.id}.json", "w", encoding="utf-8") as fp:
            fp.write(tweet.json())
    except ScraperException as err:
        print(f">> failure on ID:{reply_id}")
