#!/usr/bin/env python3

import asyncio
import csv
import glob
import logging
import os

from dataclasses import dataclass
from pathlib import Path

from .tweetget import TweetGet
from .markov import Markov

LOG = logging.getLogger(__name__)


@dataclass
class Twitblend:
    usernames: list
    user_bundle: dict

    def __post_init__(self, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop

    async def check_cache(self, username):
        p = Path(os.path.join(self.user_bundle["cache_dir"], f"{username}_tweets.csv"))
        if not p.is_file():
            return username

    def require_file(self):
        check_tasks = [self.check_cache(user) for user in self.usernames]
        return self.loop.run_until_complete(asyncio.gather(*check_tasks))

    def pull_cache(self, full):
        cusers = self.usernames if full else self.require_file()
        cusers = list(set(cusers))
        if None in cusers:
            cusers.remove(None)
        LOG.debug(f"pulling {cusers}")
        if len(cusers) < 1:
            return
        tg = TweetGet(self.user_bundle)
        gat = [tg.get_all_tweets(user) for user in cusers]
        self.loop.run_until_complete(asyncio.gather(*gat))

    def blend(self):
        files = glob.glob(os.path.join(self.user_bundle["cache_dir"], "*.csv"))
        words = []
        for fl in files:
            with open(fl, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    LOG.debug(f"row {row}")
                    words.append(row[2])
        generated = []
        markov = Markov(words)
        for i in range(self.user_bundle["num_generated"]):
            text = markov.generate_markov_text()
            #text = bytes(text, "utf8")
            generated.append(text)
        return generated
