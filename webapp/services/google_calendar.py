from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
import sys

class GoogleCalendar:

    def publish(self, event, publication):
        scopes = ['https://www.googleapis.com/auth/calendar']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'My Project-fe00d781d010.json', scopes=scopes
        )
        http_auth = credentials.authorize(Http())
        gmt_off = '-04:00'
        utc_format = '%Y-%m-%dT%H:%M:%S'
        description = event.EventDescription + '\n\nDestination: ' + event.EventDestination

        event_to_pub = {
            'summary': event.EventName,
            'start': {'dateTime': event.EventStart.strftime(utc_format) + gmt_off},
            'end': {'dateTime': event.EventEnd.strftime(utc_format) + gmt_off},
            'description': description,
            'location': event.EventMeetLocation,
        }

        cal = build('calendar', 'v3', http = http_auth)

        try:
            f = cal.events().insert(
                calendarId='primary',
                sendNotifications=True,
                body=event_to_pub
            ).execute()

            publication.Status = 'Complete'
            publication.url = f[u'htmlLink']
            publication.save()
        except:
            print "Error posting google calendar event: ", event, "error: ", sys.exc_info()[0]
            publication.Status = 'Failed'
            publication.save()


