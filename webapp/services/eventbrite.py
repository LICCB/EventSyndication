import json
import sys
from webapp.models import ApiKey
import urllib2

class Eventbrite:
    def publish(self, event, publication):
        access_token = ApiKey.objects.get(service='eventbrite_access_token')
        uri = "https://www.eventbriteapi.com/v3/events/?token={}".format(access_token.key)
        utc_format = '%Y-%m-%dT%H:%M:%S'
        gmt_off = '-04:00'
        startTime = event.EventStart.strftime(utc_format)
        endTime = event.EventEnd.strftime(utc_format)
        description = event.EventDescription + '\n\nMeet Location:' + event.EventMeetLocation + '\n\nDestination: ' + event.EventDestination + '\n\nPoint of Contact: ' + event.PoCName
        post_request = (
            'event.name.html={}'
            '&event.start.utc={}Z'
            '&event.start.timezone=America/New_York'
            '&event.end.utc={}Z'
            '&event.end.timezone=America/New_York'
            '&event.currency=USD'
            '&event.description.html={}'
        ).format(urllib2.quote(event.EventName),
                 startTime,
                 endTime,
                 urllib2.quote(description))
        print(post_request)
        try:
            print "Trying to post"
            response = urllib2.urlopen(uri, post_request)
            print "posted!"
            parsed_response = json.loads(response.read())
            url = parsed_response['url']
        except:
            print("Error posting event:", sys.exc_info()[0])
            publication.Status = 'Failed'
            publication.save()
        else:
            print "made it!"
            publication.Status='Complete'
            publication.url = url
            publication.save()
