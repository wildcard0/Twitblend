#!/usr/bin/env python3

import click
import json
import logging

from .twitblend import Twitblend


LOG = logging.getLogger(__name__)


def get_secrets(key_file):
    with open(key_file) as jfile:
        data = json.load(jfile)
        return data


@click.command()
@click.option("--cache-dir", required=True, type=str, help="Storage for tweets")
@click.option("--refresh-cache", default=False, is_flag=True, help="refresh cache")
@click.option(
    "--username",
    multiple=True,
    required=True,
    type=str,
    help="tweeters, can do multiple",
)
@click.option("--consumer-key", default=None, type=str)
@click.option("--consumer-secret", default=None, type=str)
@click.option("--access-key", default=None, type=str)
@click.option("--access-secret", default=None, type=str)
@click.option(
    "--key-file",
    default=None,
    type=str,
    help="json file { 'consumer_key': 'blah' ... }",
)
@click.option(
    "--num-generated", default=1000, type=int, help="number of items generated"
)
@click.option("--verbose", default=False, is_flag=True, help="logging on/off")
def blend(
    cache_dir,
    refresh_cache,
    username,
    consumer_key,
    consumer_secret,
    access_key,
    access_secret,
    key_file,
    num_generated,
    verbose,
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    if key_file is None:
        if (
            consumer_key is None
            or consumer_secret is None
            or access_key is None
            or access_secret is None
        ):
            click.echo("full key set or key file is needed")
            return
    else:
        if (
            consumer_key is None
            and consumer_secret is None
            and access_key is None
            and access_secret is None
        ):
            user_bundle = get_secrets(key_file)
        else:
            click.echo("key set and key file are mutually exclusive")
            return
    user_bundle["cache_dir"] = cache_dir
    user_bundle["num_generated"] = num_generated
    user_bundle["verbose"] = verbose
    tb = Twitblend(username, user_bundle)
    tb.pull_cache(False)
    values = tb.blend()
    for v in values:
        print(v)


if __name__ == "__main__":
    blend()
