"""utils for TODAG scripts"""
import pickle 

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
            read_location = subprocess.check_output('/Users/lessandro/coding/SCRIPTS/whereami')
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
    def __init__(self, local=True):
        self.local = local
        self.cards = self.load_cards()

    def load_cards(self, local=None):
        """
        load cards from pickle to global variable CARDS

        Exception:
            to be used after having imported card, otherwise
            will raise exception
        """
        if local is None: local = self.local
        with open('cards.pkl', 'rb') as data:
            return pickle.load(data)

    def write_cards(self, local=None):
        """
        write current cards to CARDS
        """
        if local is None: local = self.local
        with open('cards.pkl', 'wb') as data:
            pickle.dump(self.cards, data)
