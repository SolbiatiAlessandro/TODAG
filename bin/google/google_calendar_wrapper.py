from __future__ import print_function
import datetime
import pickle
import os.path
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarWrapper():
    """
    https://developers.google.com/calendar/quickstart/python
    """
    def __init__(self, token_pickle_path='token.pickle'):
        import pdb;pdb.set_trace()
        self.token_pickle_path = token_pickle_path
        self.login()

    def login(self, ):
        """
        from quickstart, needs ./credentials.json or ./token.pkl
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_pickle_path):
            with open(self.token_pickle_path, 'rb') as token:
                creds = pickle.load(token)
        else:
            logging.warning("NO token.pickle FOUND")
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def list_available_colors(self):
        colors = self.service.colors().get().execute()
        # Print available calendarListEntry colors.
        for id, color in colors['calendar'].items():
          print('colorId: %s',id)
          print('  Background: %s' ,color['background'])
          print('  Foreground: %s' ,color['foreground'])
        # Print available event colors.
        for id, color in colors['event'].items():
          print('colorId: %s' ,id)
          print('  Background: %s' ,color['background'])
          print('  Foreground: %s' ,color['foreground'])

    def list_events(self, 
            calendarId='primary',
            start_time=None,
            maxResults=10):
        """
        start_time : datetime.datetime.utcnow().isoformat() + '+01:00' # 'Z' indicates UTC time
        """
        # Call the Calendar API
        if not start_time:
            now = datetime.datetime.utcnow().isoformat() + '+01:00' # 'Z' indicates UTC time
        else:
            now = start_time
        logging.info('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=calendarId, timeMin=now,
                                            maxResults=maxResults, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            logging.info('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            logging.info((start, event['summary']))

        return events

    def add_event(self,
            event=None,
            calendarId='primary'
            ):
        """
        https://developers.google.com/calendar/create-events
        """
        example_event = {
          'summary': 'Google I/O 2015',
          'location': '800 Howard St., San Francisco, CA 94103',
          'description': 'A chance to hear more about Google\'s developer products.',
          'start': {
            'dateTime': '2019-07-20T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': '2019-07-20T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          #'recurrence': [
          #  'RRULE:FREQ=DAILY;COUNT=2'
          #],
          #'attendees': [
          #  {'email': 'lpage@example.com'},
          #  {'email': 'sbrin@example.com'},
          #],
          #'reminders': {
          #  'useDefault': False,
          #  'overrides': [
          #    {'method': 'email', 'minutes': 24 * 60},
          #    {'method': 'popup', 'minutes': 10},
          #  ],
          #},
        }
        if event is None: event = example_event

        logging.info('submitting event to gcloud, body=')
        logging.info(event)
        output_event = self.service.events().insert(calendarId=calendarId, body=event).execute()
        logging.info('Event created: %s', (event.get('htmlLink')))
        return output_event


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    calendar = GoogleCalendarWrapper()
    events = calendar.list_events()
    assert events
    calendar.list_available_colors()
    """
    event = calendar.add_event()
    assert event
    events = calendar.list_events()
    assert events
    """
