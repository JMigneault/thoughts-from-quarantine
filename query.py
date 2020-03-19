import tweepy
import time
import config
from logger import logger

def build_tweets(api, query_list, tweet_set=set()):
    tweet_map = {}
    total_queried = 0
    for q, n_items in query_list:
        n_queried = query(q, n_items, tweet_map, api)
        logger.log_query(q, n_queried, n_queried == n_items)
        total_queried += n_queried
    return set(tweet_map.keys()), list(tweet_map.values())

def query(q, n_items, tweet_map, api, tweet_set=set()):
    n_queried = 0
    retries = 0
    tweet_iter = tweepy.Cursor(
        api.search, 
        q=q, 
        tweet_mode="extended",
        lang="en",
        count=100
        ).items(n_items)

    while n_queried < n_items and retries < config.param.API_RETRIES:
        try:
            for tweet in tweet_iter:
                n_queried += 1
                try:
                    tweet_id = tweet.retweeted_status.id
                    tweet_json = tweet.retweeted_status._json
                except AttributeError:
                    tweet_id = tweet.id
                    tweet_json = tweet._json
                if tweet_id not in tweet_map and tweet_id not in tweet_set:
                    tweet_map[tweet_id] = tweet_json
        except tweepy.error.TweepError as err:
            logger.log_error(err)
            retries += 1
            time.sleep(config.param.API_WAITTIME)
    return n_queried