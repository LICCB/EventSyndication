import json
import logging
import sys
from django.conf import settings
from webapp.models import ApiKey
import urllib2

logger = logging.getLogger(__name__)

def get_user_access_token(EventbriteCode):
    uri = (
        'https://www.eventbrite.com/oauth/token'
    )
    post_request = ('code={}'
                    '&client_secret={}'
                    '&client_id={}'
                    '&grant_type=authorization_code').format(EventbriteCode,
                                                             settings.EVENTBRITE_SETTINGS['client_secret'],
                                                             settings.EVENTBRITE_SETTINGS['client_key'])
    try:
        response = urllib2.urlopen(uri, post_request)
        parsed_response = json.loads(response.read())
        access_token = parsed_response['access_token']
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        newApiKey = ApiKey.create('eventbrite_access_token', access_token)
        if(ApiKey.objects.filter(service='eventbrite_access_token').exists()):
            oldApiKey = ApiKey.objects.get(service='eventbrite_access_token')
        else:
            oldApiKey = None
        """save the new guy"""
        newApiKey.save()
        """delete the old guy"""
        if(oldApiKey is not None):
            oldApiKey.delete()


def get_user_info():
    if(ApiKey.objects.filter(service='eventbrite_access_token').exists()):
        access_token = ApiKey.objects.get(service='eventbrite_access_token')
        uri = "https://www.eventbriteapi.com/v3/users/me?token={}".format(access_token.key)
        try:
            response = urllib2.urlopen(uri)
            parsed_response = json.loads(response.read())
            name = parsed_response['name']
        except:
            return 'unknown'
        else:
            return name
    else:
        return 'unknown'

