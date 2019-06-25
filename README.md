# Twitblend
Twitblend downloads tweets from one or more user and uses markov chains to blend them into new tweets, poorly.

This requires twitter API access. This can be added as command line options or from a file. The file is better. Here's an example:

~~~~
{
      "consumer_key": "ckey3dfsfsfs",
      "consumer_secret": "csecret3dfsfsfsf",
      "access_key": "akey234242-fknasklff323io3r23",
      "access_secret": "asecret3sdfaf3fa3rfafwsf"
}
~~~~

--username can be used multiple times, for example:
twitblend --key-file ../twitter_secrets --cache-dir . --username user1 --username user2 --username user3

--cache-dir is required and is where it still store tweets.  It will keep using these unless the file is removed or --refresh-cache is added.


