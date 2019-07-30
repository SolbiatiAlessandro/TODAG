"""utils for TODAG scripts"""
import pickle 
import os
from google.cloud import storage
import stackdriver_logger
import socket
from uuid import getnode
import configparser
import datetime
from time import ctime
CONFIG_PATH = "../config.ini"
import logging
TIME_FORMAT = "%Y/%m/%d-%H:%M:%S"

def readconfig(arg, section="bin"):
    """
    read from config file inside CONFIG_PATH
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    try: return config[section][arg]
    except:
        print("[utils:readconfig] warning couldn't read '{}' from config gile in {}".format(arg, CONFIG_PATH))
        return None

def open_termdown():
    """
    open termdown stopwatch
    """
    cmd="""osascript -e 'tell application "Terminal" to activate' -e 'tell application "Terminal" to do script "termdown"'"""
    os.system(cmd)

class Logger():
    """
    logger for the TODAG to build custom metrics
    """
    def __init__(self, location=None, time_format=TIME_FORMAT):
        """
        args:
            location = [0.1, 0.13] forces location (home or work) instead of reading from GPS
            time_format = you can specify how the time is logged
        """
        self.location = self.populate_location() if location is None else location
        self.machine = str(getnode())+":"+socket.gethostname()

        self.refactor_time = lambda s: datetime.datetime.strptime(s, "%a %b %d %H:%M:%S %Y").strftime(time_format)

    def log_action(self, action, *arg, verbose=False):
        """
        log action for metric reports

        action: str to be written in action column
        *arg: will be casted to strings and logged
        """
        arg = list(arg) # might need to overwrite
        if verbose: print("[utils:logger.py] logging {}, {}".format(str(action), str(arg)))

        # TODAG GAE
        # log todag activity to stackdriver
        stackdriver_logger.log_todag_activity(1)

        # log mood to stackdriver 
        if action == "mood":
            stackdriver_logger.log_mood(arg[0])

        # log checked_todo to stackdriver
        if action == "checked_todo":
            todo_information = arg[0]
            duration = arg[1]
            """ since we want more information on the checking process
            we need to send a value like the following 
            value={
                'checked_time' : 1,
                'checked_task_uuid': "test",
                'checked_task_name' : "test",
                'checked_task_description' : "test",
                },
            """
            logging.info("logger: preparing payload checking_todo metric")
            formatted_value_to_send = todo_information
            formatted_value_to_send['checked_time'] = duration
            logging.info(formatted_value_to_send)
            stackdriver_logger.log_todag_checked_time(
                    formatted_value_to_send
                    )
            arg[0] = '' # this is not to break the log.csv

        """
        this is used to see when a card was last checked
        """

        with open("logs.csv","a") as f:
            # if there is no logs.csv means that Loader wasn't loaded yet (it download logs.csv ftom gcp)

            # logs.csv FORMAT
            # time, location, machine, action, arg1, arg2, arg3

            arg0 = arg[0] if len(arg) > 0 else ""
            arg1 = arg[1] if len(arg) > 1 else ""
            arg2 = arg[2] if len(arg) > 2 else ""

            to_print = [self.refactor_time(ctime()), self.location, self.machine, action, arg0, arg1, arg2] 

            f.write(','.join(map(str, to_print)) + "\n")

    def populate_location(self):
        """
        routine to populate location on my local machine

        returns location as a longitude value
        """
        try: # reading location from phyiscal machine

            # this are the lines to change when on different machines you need to change
            # how to get geographical location of the machine
            import subprocess
            print("[Logger.populate_location] loading machine location")
            WHEREAMI_PATH = readconfig('whereami')
            read_location = subprocess.check_output(WHEREAMI_PATH)
            read_location = str(read_location)
            start = read_location.find('Longitude')+len("Longitude: -")
            end = start + 4
            location = float(read_location[start:end])
            return location
        
        except Exception as e:
            print("warning: couldn't get location of machine\n'")
            print(e)
            return None

class Loader():
    """
    loads and write cards locally or from cloud
    """
    def __init__(self, local=False):
        if not local:
            self.proxy = GCSproxy() 
            self.proxy.gcs_load('cards.pkl')
            self.proxy.gcs_load('logs.csv')
        self.cards = self.load_cards()

    def __del__(self):
        """
        clean env after ending
        """
        try:
            os.system("rm cards.pkl")
            os.system("rm logs.csv")
        except: pass

    def load_cards(self):
        """
        load cards from pickle to global variable CARDS

        Exception:
            to be used after having imported card, otherwise
            will raise exception
        """
        with open('cards.pkl', 'rb') as data:
            return pickle.load(data)

    def write(self):
        """
        write current cards to CARDS
        """
        with open('cards.pkl', 'wb') as data:
            pickle.dump(self.cards, data)
        self.proxy.gcs_write('logs.csv')
        self.proxy.gcs_write('cards.pkl')

class GCSproxy():
    """basic proxy to handle gcs APIs"""

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../gcskey.json'
        self.client = storage.Client()
        BUCKET_NAME = readconfig('bucketid')
        self.bucket = self.client.get_bucket(BUCKET_NAME)

    def gcs_load(self, filename):
        """
        loads cards from gcs
        args:
            filename [cards.pkl, logs.csv]

        need key in ../gcskey.json
        """
        print("[GCSproxy.gcs_load] interacting with Google Cloud Storage to retrieve data: {}".format(filename))
        blob = self.bucket.get_blob(filename)
        blob.download_to_filename(filename)

    def gcs_write(self, filename):
        """
        write cards to gcs
        args:
            filename [cards.pkl, logs.csv]

        need key in ../gcskey.json
        """
        print("[GCSproxy.gcs_load] interacting with Google Cloud Storage to upload data: {}".format(filename))
        blob = self.bucket.blob(filename)
        blob.upload_from_filename(filename)
