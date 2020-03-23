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
    tweet_num = 0
    while True:
        new_query = tweet_num % config.param.QUERY_EVERY == 0
        print("Doing Tweet")
        logger.new_filepath()
        if new_query:
            # authorize app
            auth = tweepy.AppAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
            app_api = tweepy.API(auth, wait_on_rate_limit=True)
            # do query
            tweets = build_tweets(app_api, config.param.query_list)
            # build markov chain
            corp = tweets_to_corpus(tweets)
            mc = make_mc(corp)
            # save
            mc_fp = logger.save_mc_chain(mc)
            del(auth, app_api, tweets, corp)
        else:
            with open(mc_fp, "r") as f:
                mc = markovify.NewlineText.from_json(json.load(f))
        # generate tweet
        tweet = get_tweet(mc)
        # authorize user
        auth = tweepy.OAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
        auth.set_access_token(config.authen.OATH_TOKEN, config.authen.OATH_SECRET)
        user_api = tweepy.API(auth)
        # tweet
        post_tweet(user_api, tweet)
        # sleep
        del(auth, user_api, tweet, mc)
        print("Sleeping")
        time.sleep(config.param.TWEET_FREQ)
        tweet_num += 1

if __name__ == "__main__":
    main()