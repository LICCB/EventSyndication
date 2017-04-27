# Create your views here.

#def index(request):
#    return render(request, 'webapp/main.html')
# Definition of views.

#from __future__ import print_function

from __future__ import print_function
import traceback
import sys
import os
import logging
import httplib2

from django import http
#from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from datetime import datetime
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
#from oauth2client.contrib.django_orm import Storage
#from webapp.models import CredentialsModel
from webapp.models import LICCB_User
from webapp.forms import AddEventForm
from django.conf import settings
from syndication import settings
from django.contrib import messages
from webapp.api_helpers import facebook
from webapp.models import ApiKey
from webapp.models import EventInfo
from webapp.models import Publications
from webapp.forms import PublicationsForm
from oauth2client.contrib.django_util import decorators
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login

import pdb; 

from django.contrib.auth.models import User

#SECRETS_JSON = os.path.join(os.path.dirname(__file__), 'google_secret.json')

#FLOW = flow_from_clientsecrets(
#    SECRETS_JSON,
#    scope='https://www.googleapis.com/auth/plus.me',
#    redirect_uri='http://localhost:8000/oauth2callback')


def mylogin(request):
    if(isUserLoggedIn(request)):
       addIfNewUser(request)
       print('logged in, redirect to home')
       url = reverse('home')
       return HttpResponseRedirect(url)
       #return render(
       #  request,
       # 'webapp/index.html',
       # {
       #     'title':'Syndication Tool',
       #     'year':datetime.now().year,
       # })
       #home(request)
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
       #print('Entered post')
       return get_profile_required(request)
       return render(
         request,
        'webapp/index.html',
        {
            'title':'Syndication Tool',
            'year':datetime.now().year,
        })
    return render(
        request,
        'webapp/login.html',
        {
            'title':'Login',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })


@login_required(login_url='/eventsyndication/login')
def home(request):

  #print >>sys.stderr, 'Goodbye, cruel world!'
  #storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  #credential = storage.get()
  #if credential is None or credential.invalid == True:
  #  FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
  #                                                 request.user)
  #  authorize_url = FLOW.step1_get_authorize_url()
  #  #print (authorize_url)
  #  return HttpResponseRedirect(authorize_url)
  #else:
  #  http = httplib2.Http()
  #  http = credential.authorize(http)
  #  service = build("plus", "v1", http=http)
  #  activities = service.activities()
  #  activitylist = activities.list(collection='public',
  #                                 userId='me').execute()
  #  logging.info(activitylist)
    #if User.objects.filter(username='test').exists():
    #    print('user exists')
    #else:
    # x=User.objects.create_user('test')
    # x.save()
    #print(isUserLoggedIn(request))
    #print(User.is_authenticated)

    #if(isUserLoggedIn(request)):
       print('hit home')
       assert isinstance(request, HttpRequest)
       return render(
        request,
        'webapp/index.html',
        {
            'title':'Syndication Tool',
            'year':datetime.now().year,
        }
    )
    #else:
        #return get_profile_required(request)
        #return render(
        #request,
        #'webapp/index.html',
        #{
        #    'title':'Syndication Tool',
        #    'year':datetime.now().year,
        #})
        #return render(
        #request,
        #'webapp/index.html',
        #{
        #    'title':'Syndication Tool',
        #    'year':datetime.now().year,
        #    'user':get_profile_required(request)
        #})

@decorators.oauth_required
def get_profile_required(request):
    resp, content = request.oauth.http.request(
        'https://www.googleapis.com/plus/v1/people/me')
    #
    print('calling addIfNewUser')
    #addIfNewUser(request)
    #return content
    return http.HttpResponse(content)

@decorators.oauth_enabled
def isUserLoggedIn(request):
    if request.oauth.has_credentials():
        # this could be passed into a view
        # request.oauth.http is also initialized
        #return http.HttpResponse('User email: {}'.format(
        #    request.oauth.credentials.id_token['email']))
        return True
    #render(request,"webapp/index.html",{'email':request.oauth.credentials.id_token['email'],'name':request.oauth.credentials.id_token['displayName']})
    else: return False
        #return http.HttpResponse(
        #    'Follow the link to login via google:<a href="{}">Login</a>'
        #    .format(request.oauth.get_authorize_redirect()))

@decorators.oauth_enabled
def addIfNewUser(request):
    if request.oauth.has_credentials():
       #print(request.oauth.credentials.id_token.items())
       if User.objects.filter(username=request.oauth.credentials.id_token['email']).exists():
          print('user exists')
       else:
         newUser=User.objects.create_user(request.oauth.credentials.id_token['email'],request.oauth.credentials.id_token['email'],'hashedEmail')
         newUser.first_name=request.oauth.credentials.id_token['given_name']
         newUser.last_name=request.oauth.credentials.id_token['family_name']
         newUser.save()
       user = authenticate(username=request.oauth.credentials.id_token['email'], password='hashedEmail')
       if user is not None:
           print('logging in user')
           login(request, user)
    
#@login_required
#def auth_return(request):
#  if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
#                                 request.user):
#    return  HttpResponseBadRequest()
#  credential = FLOW.step2_exchange(request.REQUEST)
#  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
#  storage.put(credential)
#  return HttpResponseRedirect("/")

def createEvent(request):
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)
    form = AddEventForm()

    return render(
    request,
    'webapp/createEvent.html',
    {
        'title': 'Syndicate New Event',
        'message':'Your Event Creation page.',
        'year':datetime.now().year,
        'form': form
    }
)
def publish(request):
    """Renders the publish event page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            #CONNECT TO EVERYTHING AND POST EVERYTHING
            #For now let's just save the postings table and call it a day.
            newEvent = form.save()
            publicationFormInstance = PublicationsForm(initial={'EventID': newEvent.pk})
            return render(
                request,
                'webapp/publish.html',
                {
                    'form': publicationFormInstance,
                    'year':datetime.now().year,
                    'eventID':newEvent.pk,
                    'event': request.POST.get('EventID'),
                    'events': EventInfo.objects.all()
                }
            )
        else:
            messages.error(request, "Error")

def syndicate(request):
    """Renders the pubStatus page for a newly created event and attempts syndication"""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = PublicationsForm(request.POST)
        if form.is_valid():
            serviceList = request.POST.copy()
            serviceList.pop("csrfmiddlewaretoken")
            serviceList.pop("EventID")
            events = EventInfo.objects.all()
            event = events.get(id=request.POST.get('EventID'))
            for service in serviceList:
                service = Publications.create(event, service)
                service.save()
            #SYNDDDDDIDCAATEEEEEEEEEEEEEE
            postings = Publications.objects.filter(EventID = event)
            return render(
                request,
                'webapp/pubStatus.html',
                {
                    'title': 'Publication Status',
                    'message': 'Event Syndication Status',
                    'year': datetime.now().year,
                    'events': events,
                    'event': event,
                    'publications': postings
                }
            )
        else:
            messages.error(request,"Error")

def pubStatus(request):
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)
    events = EventInfo.objects.all().order_by('-EventStart')
    if request.method == "POST":
        event = events.get(id=request.POST.get('EventID'))
        postings = Publications.objects.filter(EventID=event)
        return render(
            request,
            'webapp/pubStatus.html',
            {
                'title':'Publication Status',
                'message':'Your status',
                'year':datetime.now().year,
                'event': event,
                'events': events,
                'publications': postings
            }
        )

    event = events.first()
    postings = Publications.objects.filter(EventID=event)
    return render(
        request,
        'webapp/pubStatus.html',
        {
            'title':'Publication Status',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
            'events': events,
            'event': event,
            'publications': postings
        }
    )

def admin(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'webapp/admin.html',
        {
            'title':'Administration',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def apiKeys(request):
    """Renders the API keys page"""
    assert isinstance(request, HttpRequest)
    facebook_code = request.GET.get('code')
    logout = request.GET.get('logout')
    if(facebook_code is not None):
        """Update facebook user access token with code"""
        facebook.get_user_access_token(facebook_code, 'http://loopback.pizza:8000/eventsyndication/apiKeys')
    if(logout is not None):
        ApiKey.objects.filter(service = 'facebook_user_access_token').delete()
    return render(
            request,
            'webapp/apiKeys.html',
            {
            'client_id': settings.FACEBOOK_SETTINGS['client_id'],
            'name': facebook.get_user_info()
            }
            )

def add(request):
    """Saves form to db"""
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "webapp/createEvent.html",
                          {
                              'title': 'Create Event',
                              'message': 'Your Event Creation Page',
                              'year': datetime.now().year
                          })

def logout_view(request):
   logout(request)
   return HttpResponseRedirect('login')