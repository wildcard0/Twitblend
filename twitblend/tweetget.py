#!/usr/bin/env python3
# encoding: utf-8

import csv
import logging
import os
import tweepy

from dataclasses import dataclass


LOG = logging.getLogger(__name__)


@dataclass
class TweetGet:
    user_bundle: dict

    async def get_all_tweets(self, screen_name):
        # Twitter only allows access to a users most recent
        # 3240 tweets with this method

        # authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(
            self.user_bundle["consumer_key"], self.user_bundle["consumer_secret"]
        )
        auth.set_access_token(
            self.user_bundle["access_key"], self.user_bundle["access_secret"]
        )
        api = tweepy.API(auth)

        alltweets = []

        # make initial request for most recent tweets
        # (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)
        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1

        while len(new_tweets) > 0:
            LOG.debug(f"getting tweets before {oldest}")
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(
                screen_name=screen_name, count=200, max_id=oldest
            )
            alltweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            LOG.debug(f"...{len(alltweets)} tweets downloaded so far")

        outtweets = [
            [tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")]
            for tweet in alltweets
        ]

        # write the csv
        tfile = f"{screen_name}_tweets.csv"
        with open(os.path.join(self.user_bundle["cache_dir"], tfile), "w") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])
            writer.writerows(outtweets)
        LOG.debug("done")
