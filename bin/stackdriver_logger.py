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
    payload = {
                "user":user,
                "password":password,
                "value":value
                }
    logging.info("client:logging - submitting metric post request {}, payload: ".format(url))
    logging.info(payload)
    response = requests.post(
            url,
            json=payload
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
        value={
            'checked_time' : 1,
            'checked_task_uuid': "test",
            'checked_task_name' : "test",
            'checked_task_description' : "test",
            },
        local=False,
        ):
    url = "https://todag-239819.appspot.com/metric/todag_checked_time" if \
            not local else\
            "http://127.0.0.1:5000/metric/todag_checked_time"
    logging.info("stackriver_logger:log_todag_checked_time submitting metric")
    value['timeZone'] = 'America/Los_Angeles'
    #value['timeZone'] = 'Europe/London'
    submit_metric(
            url=url,
            value=value)
    
if __name__ == "__main__":
    #log_mood(6.7)
    #log_todag_activity(2)
    log_todag_checked_time(0.5)

