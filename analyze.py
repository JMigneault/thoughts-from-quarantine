import re
import markovify
import config

def tweets_to_corpus(tweet_list):
    corpus = ""
    for json in tweet_list:
        corpus += json["full_text"].replace("\n", "") + "\n"
    corpus = re.sub(r"\&amp", "", corpus) # remove amp symbols
    corpus = re.sub(r"@\S*", "", corpus) # remove @s
    corpus = re.sub(r"http\S*", "", corpus) # remove links
    corpus = re.sub(r" ; ", " ", corpus)
    return corpus

def make_mc(corpus, old_mc=None, weights=None):
    new_mc = markovify.NewlineText(corpus, well_formed=False, state_size=config.param.MC_STATE_SIZE, retain_original=False)
    if old_mc is None:
        return new_mc
    else:
        return markovify.combine((old_mc, new_mc), weights=weights)

def get_tweet(mc):
    sentence = None
    while sentence is None:
        sentence = mc.make_short_sentence(config.param.MAX_CHAR_COUNT)
    return sentence
    
