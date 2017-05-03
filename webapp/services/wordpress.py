import base64
import json
import logging
import urllib
import urllib2
from django.conf import settings

logger = logging.getLogger(__name__)

class Wordpress:
    hostname = settings.WORDPRESS_HOSTNAME
    username = settings.WORDPRESS_USERNAME
    password = settings.WORDPRESS_PASSWORD

    def log_error(self, message, publication):
        logger.error("Failed to update wordpress. Ex: " + message)


    def publish(self, event, publication):

        time_format = '%b %d, %Y %X'

        event_to_pub = {
            'content': (
                '' + event.EventDescription + '\n\n Meet Location: '
                '' + event.EventMeetLocation + '\nDestination: '
                '' + event.EventDestination + '\n\n Start Time: '
                '' + event.EventStart.strftime(time_format) + '\n End Time: '
                '' + event.EventEnd.strftime(time_format)
            ),
            'title': event.EventName,
            'excerpt': event.EventDescription,
            'status': 'publish'
        }
        encoded_event = urllib.urlencode(event_to_pub)
        uri = self.hostname + "/wp-json/wp/v2/posts"
        request = urllib2.Request(uri, encoded_event)
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            response = urllib2.urlopen(request)
            content = json.load(response)
            if(response.getcode() == 201):
                publication.Status = 'Complete'
                publication.url = content[u'link']
            else:
                self.log_error(response[u'message'], publication)

        except Exception, e:
            self.log_error(str(e), publication)

        publication.save()


        def __init__(self):
            "hi"
