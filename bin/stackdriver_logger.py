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
    logging.warning("client:logging - submitting metric post request {}".format(url))
    response = requests.post(
            url,
            {
                "user":user,
                "password":password,
                "value":value
                }
            )
    logging.warning("client:logger - recieved response")
    logging.warning(response)
    logging.warning(response.text)

def log_mood(
        value=6.0,
        ):
    submit_metric(
            url="https://todag-239819.appspot.com/metric/mood",
            value=value)

if __name__ == "__main__":
    log_mood(6.7)

