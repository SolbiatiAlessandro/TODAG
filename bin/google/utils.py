"""
utils to work with google  module inside todag
"""
import logging
import json
from datetime import datetime, timedelta
from pytz import timezone
from google.google_calendar_wrapper import GoogleCalendarWrapper as calendar_wrapper

GOOGLEFMT = "%Y-%m-%dT%H:%M:00"
ACTIVITY_METRICS_CONFIG = "./activity_metrics.json" # called from bin
HARDCODED_TIMEZONE = 'Europe/London'

# integration function
def _format_calendar_event_description(
        activity_metrics=None, additional_content=None):
    """all this stuff need to be inside functions
    since I am using calendar like a DB
    
    WARNING: this  is copy pasted both in DATAMONITOR and TODAG"""
    if activity_metrics is None: 
        # put all zeros if None
        configs = json.load(open(ACTIVITY_METRICS_CONFIG,"r"))
        activity_metrics = {metric:0 for metric in configs['activity_metrics']}
    description = _format_card_activity_metrics_to_string(activity_metrics)+'~'
    description += ' \n '*2
    try:
        description += additional_content
    except:
        description += additional_content.decode('utf-8')
    return description

# integration function
def _format_card_activity_metrics_to_string(activity_metrics):
    """
    args:
        activity_metrics : (dict)
    {'asd':0,...} -> "asd : 0 | csd : 1 | kk : 3"

    copy pasted to  TODAG
    """
    string = ""
    for metric, value in activity_metrics.items():
        string  += metric+" : "+str(value)+" |"
    return string[:-1]

def add_checked_time_to_google_calendar(value):
    """
    value: dict {
    checked_time : int 
        (this is the duration as a integer of the time spent on this task)
    checked_task_uuid: str
    checked_task_name : str
    checked_task_description : str
    (optional) timeZone
    }
    """
    # we also add the checked time to google calendar
    # we need to compute the time of the checked task
    if value.get('timeZone') is None:
        value['timeZone'] = HARDCODED_TIMEZONE

    now = datetime.now(timezone(value['timeZone']))
    end_time = now
    start_time = now - timedelta(hours=float(value['checked_time']))
    logging.info("computing todag checked time period")
    logging.info(end_time)
    logging.info(start_time)

    # and we put a default activity metric
    # the next time I work on TODAG I can implement to
    # add custom activity metric while doing the tasks
    configs = json.load(open(ACTIVITY_METRICS_CONFIG,"r"))
    default_todag_activity_metric = \
            {metric:0 for metric in configs['activity_metrics']}
    default_todag_activity_metric['productivity'] = 1
    description  = _format_calendar_event_description(
            default_todag_activity_metric,
            value['checked_task_description']
            )
    calendar = calendar_wrapper(token_pickle_path="./flaskr/google/token.pickle")
    checked_time_event = {
            'summary':'~WORKED ON -{}-'.format(value['checked_task_name']),
            'description':description,
            'start':{
                'dateTime':start_time.strftime(GOOGLEFMT),
                'timeZone': value['timeZone'],
                },
            'end':{
                'dateTime':end_time.strftime(GOOGLEFMT),
                'timeZone': value['timeZone'],
                },
            # 'colorId':'20', -> this is breaking, getting a error 400 from google
            }
    logging.info(checked_time_event)
    calendar.add_event(checked_time_event)
