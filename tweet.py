import time
import tweepy
import config
from logger import logger

def post_tweet(api, tweet_text):
    retries = 0
    while retries < config.param.API_RETRIES:
        try:
            api.update_status(tweet_text.encode("utf8"))
            break
        except tweepy.TweepError as err:
            logger.log_error(err)
            retries += 1
            time.sleep(config.param.API_WAITTIME)
    logger.log_tweet(tweet_text, retries < config.param.API_RETRIES)
