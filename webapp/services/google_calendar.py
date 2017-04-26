from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

class GoogleCalendar:

    def publish(self, event):
        scopes = ['https://www.googleapis.com/auth/calendar']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'My Project-fe00d781d010.json', scopes=scopes)

        http_auth = credentials.authorize(Http())

        gmt_off = '-04:00'

        event_to_pub = {
            'summary': 'swagu',
            'start': {'dateTime': '2017-04-25T17:00:00%s' % gmt_off},
            'end': {'dateTime': '2017-04-25T18:00:00%s' % gmt_off},
            'attendees': {'email': 'petergoggijr@gmail.com'},
        }

        cal = build('calendar', 'v3', http = http_auth)

        f = cal.events().insert(
            calendarId='primary',
            sendNotifications=True,
            body=event_to_pub
        ).execute()

        print f

