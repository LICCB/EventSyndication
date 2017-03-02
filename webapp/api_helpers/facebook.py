from django.conf import settings
from webapp.models import ApiKey
import urllib2
import json

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
    response = urllib2.urlopen(uri)
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
