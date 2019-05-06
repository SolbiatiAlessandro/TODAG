"""utils for TODAG scripts"""
import pickle 
import os
from google.cloud import storage

class Logger():
    """
    logger for the TODAG to build custom metrics
    """
    def __init__(self):
        self.location = self.populate_location()

    def log_action(self, action, arg):
        """
        log action for metric reports

        action: str to be written in action column
        arg: str to be written in action column
        """
        from time import ctime
        with open("logs.csv","a") as f:
            f.write(ctime()+','+str(self.location)+','+str(action)+','+str(arg)+'\n')

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
            read_location = subprocess.check_output('/Users/lessandro/coding/SCRIPTS/whereami')
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
            self.gcs_load()
        self.cards = self.load_cards()

    def __del__(self):
        """
        clean env after ending
        """
        os.system("rm cards.pkl")

    def load_cards(self):
        """
        load cards from pickle to global variable CARDS

        Exception:
            to be used after having imported card, otherwise
            will raise exception
        """
        with open('cards.pkl', 'rb') as data:
            return pickle.load(data)

    def write_cards(self):
        """
        write current cards to CARDS
        """
        with open('cards.pkl', 'wb') as data:
            pickle.dump(self.cards, data)
        self.gcs_write()

    def gcs_load(self):
        """
        loads cards from gcs

        need key in ../gcskey.json
        """
        print("[Logger.gcs_load] interacting with Google Cloud Storage to retrieve data ")
        os.system("export GOOGLE_APPLICATION_CREDENTIALS='../gcskey.json'")
        client = storage.Client()
        bucket = client.get_bucket('todag-bucket')
        blob = bucket.get_blob('cards.pkl')
        blob.download_to_filename('cards.pkl')

    def gcs_write(self):
        """
        write cards to gcs

        need key in ../gcskey.json
        """
        print("[Logger.gcs_load] interacting with Google Cloud Storage to upload data ")
        os.system("export GOOGLE_APPLICATION_CREDENTIALS='../gcskey.json'")
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('todag-bucket')
        blob = bucket.blob('cards.pkl')

        blob.upload_from_filename('cards.pkl')
