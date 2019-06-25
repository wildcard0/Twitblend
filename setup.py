#!/usr/bin/env python3

from setuptools import setup
from sys import version_info


assert version_info >= (3, 7, 0), "twitblend.py requires >= Python 3.7"


setup(
    name="twitblend",
    version='1',
    description=("blend tweets"),
    long_description="blend tweets",
    packages=["twitblend"],
    url="http://github.com/wildcard0",
    author="wildcard0",
    author_email="wildcard0@illuminatus.org",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
    ),
    python_requires=">=3.7",
    install_requires=["click", "tweepy"],
    entry_points={
        "console_scripts": ["twitblend = twitblend.cli:blend"]
    },
)
