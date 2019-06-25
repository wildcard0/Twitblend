#!/usr/bin/env python3

import csv
import glob
import logging
import random


LOG = logging.getLogger(__name__)


class Markov:
    def __init__(self, open_file):
        self.cache = {}
        self.words = self.sanitize(open_file)
        self.word_size = len(self.words)
        self.database()

    # this is shitty - it could be done like 1000x better
    def sanitize(self, words):
        san = []
        for line in words:
            for word in line.split():
                if "@" in word:
                    continue
                if word == "RT":
                    continue
                if "&" in word:
                    continue
                if "http://" in word:
                    continue
                if "https://" in word:
                    continue
                if ".com" in word:
                    continue
                san.append(word)
        return san

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return self.sanitize(words)

    def triples(self):
        if len(self.words) < 3:
            return
        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size - 3)
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return " ".join(gen_words)
