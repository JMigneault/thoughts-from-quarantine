class Authen:
    def __init__(self):
        self.OATH_TOKEN = "OATH TOKEN GOES HERE"
        self.OATH_SECRET = "OATH SECRET GOES HERE"
        self.CONSUMER_TOKEN = "CONSUMER TOKEN GOES HERE"
        self.CONSUMER_SECRET = "CONSUMER SECRET GOES HERE"

class Param:
    def __init__(self):
        self.API_WAITTIME = 10 # second
        self.API_RETRIES = 6
        self.MC_STATE_SIZE = 3
        self.MAX_CHAR_COUNT = 100
        self.TWEET_FREQ = 3 * (3600) # seconds
        self.LOGGING_PATH = "./logs/"
        self.MC_SAVING_PATH = "./mc_saves/"
        self.TWEET_SAVING_PATH = "./tweet_saves/"
        self.TWEET_SET_SAVING_PATH = "./set_saves/"
        self.LOAD_MC_PATH = None # filepath to initial markov chain or None to start from scratch
        self.LOAD_SET_PATH = None # filepath to initial tweet set or None
        self.query_list = [
            ("isolation+OR+quarantine", 100000),
            ("coronavirus+gaming+OR+coronavirus+cooking+OR+coronavirus+movie+OR+coronavirus+TV+OR+coronavirus+cat+OR+coronavirus+dog+OR+washyourhands+OR+zoom", 30000)]

authen = Authen()
param = Param()