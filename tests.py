from logger import logger
import markovify
import tweepy
import time
from query import build_tweets
from analyze import tweets_to_corpus, get_tweet, make_mc
import config
from tweet import post_tweet

def test_logger():
    print("Testing Logger")
    logger.new_filepath()
    print("Filepath: " + logger.log_path)
    logger.log_query("query string one", 10, True)
    logger.log_query("query string two", 0, False)
    logger.log_tweet("tweet one", True)
    logger.log_tweet("tweet two", False)
    logger.log_error(ValueError("test error"))
    mc = markovify.Text("dog cat dog. dog dog cat", state_size=1)
    logger.save_mc_chain(mc)
    logger.save_tweets([mc.to_json()])
    logger.save_tweet_set(set([1,2,3,4,5]))
    time.sleep(1)

def test_corpus():
    logger.new_filepath()
    print("Testing corpus building")
    auth = tweepy.AppAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
    app_api = tweepy.API(auth, wait_on_rate_limit=True)
    _, tweets = build_tweets(app_api, [("dog", 200), ("cat", 300)])
    print("Queried tweet: " + tweets[0]["full_text"])
    corp = tweets_to_corpus(tweets)
    print("Generate corpus: " + corp[:200])

def test_sentence():
    logger.new_filepath()
    print("Testing sentence generation")
    auth = tweepy.AppAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
    app_api = tweepy.API(auth, wait_on_rate_limit=True)
    tweet_set, tweets = build_tweets(app_api, [("dog", 200), ("cat", 300)])
    corp = tweets_to_corpus(tweets)
    mc1 = make_mc(corp)
    for i in range(10):
        print("First mc tweet {}: {}".format(i, get_tweet(mc1)))
    new_tweet_set, tweets = build_tweets(app_api, [("Trump", 200), ("Pelosi", 300)], tweet_set=tweet_set)
    print("Tweet set lengths: %d + %d = %d" % (len(tweet_set), len(new_tweet_set), len(tweet_set|new_tweet_set)))
    corp = tweets_to_corpus(tweets)
    mc2 = make_mc(corp, mc1, weights=(1,1))
    for i in range(10):
        print("Combined tweet {}: {}".format(i, get_tweet(mc2)))

def test_tweet():
    logger.new_filepath()
    auth = tweepy.OAuthHandler(config.authen.CONSUMER_TOKEN, config.authen.CONSUMER_SECRET)
    auth.set_access_token(config.authen.OATH_TOKEN, config.authen.OATH_SECRET)
    user_api = tweepy.API(auth)
    post_tweet(user_api, "Current time: {}".format(logger.get_timestamp_string()))

if __name__ == "__main__":
    test_logger()
    test_corpus()
    test_sentence()
    #test_tweet()
