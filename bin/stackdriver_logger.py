# module to submit metrics
import requests
import logging
import utils

def submit_metric(
        url="http://127.0.0.1:5000/metric/mood",
        value="6.0"
        ):
    """
    """
    user = utils.readconfig("user","datamonitor")
    password = utils.readconfig("password","datamonitor")
    logging.info("client:logging - submitting metric post request {}".format(url))
    response = requests.post(
            url,
            {
                "user":user,
                "password":password,
                "value":value
                }
            )
    logging.info("client:logger - recieved response")
    logging.info(response)
    logging.info(response.text)

def log_mood(
        value=6.0,
        ):
    submit_metric(
            url="https://todag-239819.appspot.com/metric/mood",
            value=value)

def log_todag_activity(
        value=1
        ):
    submit_metric(
            url="https://todag-239819.appspot.com/metric/todag_activity",
            value=value)

def log_todag_checked_time(
        value=1
        ):
    submit_metric(
            url="https://todag-239819.appspot.com/metric/todag_checked_time",
            value=value)
    
if __name__ == "__main__":
    #log_mood(6.7)
    #log_todag_activity(2)
    log_todag_checked_time(0.5)

