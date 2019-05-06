"""utils for TODAG scripts"""

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
