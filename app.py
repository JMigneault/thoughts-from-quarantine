import config
from logger import logger
import tweepy
from query import build_tweets
from analyze import tweets_to_corpus, make_mc, get_tweet
from tweet import post_tweet
import time
import markovify
import json
import pickle

def main():
    # initialize a None markov chain or load an initial one
    mc = None
    if config.param.LOAD_MC_PATH is not None:
        with open(config.param.LOAD_MC_PATH, "r") as f:
            mc = markovify.NewlineText.from_json(json.load(f))
    tweet_set = set()
    if config.param.LOAD_SET_PATH is not None:
        with open(config.param.LOAD_SET_PATH, "rb") as f:
            tweet_set = pickle.load(f)
    while True:
        print("Doing Tweet")
        logger.new_filepath()
        # authorize app
        auth = tweepy.AppAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
        app_api = tweepy.API(auth, wait_on_rate_limit=True)
        # do query
        new_tweet_set, tweets = build_tweets(app_api, config.param.query_list, tweet_set=tweet_set)
        tweet_set = new_tweet_set|tweet_set
        logger.save_tweets(tweets)
        logger.save_tweet_set(tweet_set)
        # build markov chain
        corp = tweets_to_corpus(tweets)
        mc = make_mc(corp, old_mc=mc, weights=(1, 1) if mc is not None else None)
        logger.save_mc_chain(mc)
        # generate tweet
        tweet = get_tweet(mc)
        # authorize user
        auth = tweepy.OAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
        auth.set_access_token(config.authen.OATH_TOKEN, config.authen.OATH_SECRET)
        user_api = tweepy.API(auth)
        # tweet
        post_tweet(user_api, tweet)
        # sleep
        print("Sleeping")
        time.sleep(config.param.TWEET_FREQ)

if __name__ == "__main__":
    main()