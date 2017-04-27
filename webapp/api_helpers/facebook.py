from django.conf import settings
from webapp.models import ApiKey
import urllib2
import json
import logging
import sys

logger = logging.getLogger(__name__)

def get_user_access_token(code, redirect_url):
    uri = (
        'https://graph.facebook.com/v2.8/oauth/access_token'
        '?client_id={}'
        '&redirect_uri={}'
        '&client_secret={}'
        '&code={}'
    ).format(
        settings.FACEBOOK_SETTINGS['client_id'],
        redirect_url,
        settings.FACEBOOK_SETTINGS['client_secret'],
        code
    )
    try:
        response = urllib2.urlopen(uri)
    except:
        logger.error("error getting facebook api key for uri: ", uri, "error: ", sys.exc_info()[0])
    else:
        parsedResponse = json.load(response)
        newApiKey = ApiKey.create('facebook_user_access_token', parsedResponse[u'access_token'])
        if(ApiKey.objects.filter(service = 'facebook_user_access_token').exists()):
            oldApiKey = ApiKey.objects.get(service = 'facebook_user_access_token')
        else:
            oldApiKey = None
        """save the new guy"""
        newApiKey.save()
        """delete the old guy"""
        if(oldApiKey is not None):
            oldApiKey.delete()


def get_user_info():
    if(ApiKey.objects.filter(service = 'facebook_user_access_token').exists()):
        access_token = ApiKey.objects.get(service = 'facebook_user_access_token')
        uri = "https://graph.facebook.com/v2.8/me?access_token={}".format(access_token.key)
        try:
            response = urllib2.urlopen(uri)
        except:
            return 'unknown'
        else:
            userInfo = json.load(response)
            return userInfo[u'name']
    else:
        return 'unknown'

