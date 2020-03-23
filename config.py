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
        self.TWEET_FREQ = 4 * (3600) # seconds
        self.QUERY_EVERY = 5 # make new mc every nth tweet
        self.LOGGING_PATH = "./logs/"
        self.MC_SAVING_PATH = "./mc_saves/"
        self.query_list = [
            ("isolation+OR+quarantine", 200000),
            ("coronavirus+video+game+OR+coronavirus+movie+OR+coronavirus+cat+OR+coronavirus+dog+OR+washyourhands+OR+zoom", 68000)]

authen = Authen()
param = Param()