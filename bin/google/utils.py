"""
utils to work with google  module inside todag
"""
import logging
import json
from datetime import datetime, timedelta
from pytz import timezone
import sys
try:
    from google_calendar_wrapper import GoogleCalendarWrapper as calendar_wrapper
except:
    from google.google_calendar_wrapper import GoogleCalendarWrapper as calendar_wrapper

GOOGLEFMT = "%Y-%m-%dT%H:%M:00"
# should add Z for UTC time
# now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
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

# integration function
def _format_activity_metrics_string_to_dict(string):
    """
    "asd : 0 | csd : 1 | kk : 3"-> {'asd':0,...} 

    copied to TODAG
    """
    args = map(lambda x: x.replace(' ',''), string.split("|"))
    # args >>> ['asd:0', 'csd:1', 'kk:3']
    return  {
            arg.split(':')[0]:float(arg.split(':')[1]) for \
                    arg in args
            }

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
    calendar = calendar_wrapper()
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

def compute_activity_metrics_from_calendar(
        datetime_day=None
        ):
    """
    metrics are computed with EVENT DURATION * METRIC WEIGHT
    so if a event has a productivity of 0.8, for 2 hours the productivity
    metric for this event is 1.6 (hours of work)

    Args:
        datetime_day (datetime) to compute the metrics for
        2011-06-03
    example call: compute_activity_metrics_from_calendar("2019-09-01")
    you can compute previous days with 
    datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    timeMax	(datetime)
    Upper bound (exclusive) for an event's start time to filter by. 
    2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. 

    timeMin	(datetime)
    Lower bound (exclusive) for an event's end time to filter by. 
    2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. 
    """
    metrics_keys = json.load(open(ACTIVITY_METRICS_CONFIG,"r"))['activity_metrics']
    total_metrics = {key: 0 for key in metrics_keys}

    if datetime_day is None:
        datetime_day = datetime.today().strftime("%Y-%m-%d")
    timeMin = datetime_day+"T00:01:00+01:00"
    timeMax = datetime_day+"T23:59:00+01:00"
    calendar = calendar_wrapper()
    events = calendar.list_events(start_time=timeMin,
            end_time=timeMax)
    logging.info("found {} events".format(len(events)))
    for event in events:
        logging.info(event['summary'])
        event_start_time = datetime.strptime(
                event['start']['dateTime'],
                #GOOGLEFMT+"+01:00" # UNCOMMENT BELOW FOR LEGAL HOUR CHANGE
                GOOGLEFMT + "Z" # UNCOMMENT ABOVE FOR LEGAL HOUR CHANGE
                )
        event_end_time = datetime.strptime(
                event['end']['dateTime'],
                #GOOGLEFMT+"+01:00" # UNCOMMENT BELOW FOR LEGAL HOUR CHANGE
                GOOGLEFMT + "Z" # UNCOMMENT ABOVE FOR LEGAL HOUR CHANGE
                )
        event_duration_hours = ((event_end_time - event_start_time).seconds)/3600
        logging.info("event duration = {}".format(event_duration_hours))
        if event.get('description'):
            # get metric from description
            activity_metric_string = event['description'].split('~')[0]
            try:
                metrics = _format_activity_metrics_string_to_dict(
                        activity_metric_string
                        )
                logging.info("adding metrics")
                logging.info(metrics)
                for key, metric in metrics.items():
                    # here is the important formula TIME * METRIC
                    total_metrics[key] += metric * event_duration_hours
            except Exception:
                logging.info("COULD NOT FORMAT DESCRIPTION")
                logging.info(activity_metric_string)
    return total_metrics

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    res = compute_activity_metrics_from_calendar("2019-09-01")
    print("\n\nMETRICS FOR THE DAY:")
    print(res)
