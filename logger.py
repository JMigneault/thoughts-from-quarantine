import json
import datetime
import os
import config
import pickle

class Logger:

    def get_timestamp_string(self):
        current_time = datetime.datetime.now()
        return "{}{}{}_{}{}{}".format(
            current_time.year,
            current_time.month if len(str(current_time.month)) == 2 else '0' + str(current_time.month),
            current_time.day if len(str(current_time.day)) == 2 else '0' + str(current_time.day),
            current_time.hour if len(str(current_time.hour)) == 2 else '0' + str(current_time.hour),
            current_time.minute if len(str(current_time.minute)) == 2 else '0' + str(current_time.minute),
            current_time.second if len(str(current_time.second)) == 2 else '0' + str(current_time.second))

    def new_filepath(self):
        self.log_path = config.param.LOGGING_PATH + self.get_timestamp_string() + ".log"
        with open(self.log_path, 'a') as f:
            f.write(self.get_timestamp_string() + "; ")
            f.write("BEGINNING CYCLE\n")

    def log_query(self, q, n_queried, worked):
        with open(self.log_path, 'a') as f:
            f.write(self.get_timestamp_string() + "; ")
            f.write("QUERY: {}; ".format("SUCCESS" if worked else "INCOMPLETE"))
            f.write("QUERYSTRING: %s; " % q)
            f.write("NUMQUERIED: %d\n" % n_queried)

    def log_tweet(self, text, worked):
        with open(self.log_path, 'ab') as f:
            f.write((self.get_timestamp_string() + "; ").encode("utf8"))
            f.write("TWEET: {}; ".format("SUCCESS" if worked else "FAILURE").encode("utf8"))
            f.write("TEXT: {}\n".format(text).encode("utf8"))

    def log_error(self, err):
        with open(self.log_path, 'a') as f:
            f.write(self.get_timestamp_string() + "; ")
            f.write("ERROR; ")
            f.write("MESSAGE: {}\n".format(str(err)))

    def save_mc_chain(self, mc):
        fp = config.param.MC_SAVING_PATH + self.get_timestamp_string() + "_chain.json"
        with open(fp, "w") as f:
            json.dump(mc.to_json(), f)
        return fp

logger = Logger()
