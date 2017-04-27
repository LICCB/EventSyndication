from __future__ import print_function

from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpRequest

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from webapp.api_helpers import facebook
#our models
from webapp.models import ApiKey
from webapp.models import EventInfo
from webapp.models import Publications
from webapp.models import GlobalPermissions
from webapp.models import LICCB_Role
#our forms
from webapp.forms import AddGroupForm
from webapp.forms import AddEventForm
from webapp.forms import PublicationsForm
from webapp.forms import AddRoleForm

#Needed for google auth
from oauth2client.contrib.django_util import decorators
#needed for user control and authentication
from django.contrib.auth import authenticate, login, logout
# Needed for permission control
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType


from webapp.services.services import services
import logging

logger = logging.getLogger(__name__)

def mylogin(request):
    if(isUserSignedIntoGoogle(request)):
       addIfNewUser(request)
       #print('logged in, redirect to home')
       url = reverse('home')
       return HttpResponseRedirect(url)

    """Renders the login page."""
    #if user click login button
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
       #print('Entered post')
       return get_profile_required(request)
       return HttpResponseRedirect('home')
   #load login page
    return render(
        request,
        'webapp/login.html',
        {
            'title':'Login',
            'message':'Your application description page.',
            'year':datetime.now().year,
            
        })

@decorators.oauth_required
def get_profile_required(request):
    resp, content = request.oauth.http.request(
        'https://www.googleapis.com/plus/v1/people/me')
    return http.HttpResponse(content)

@decorators.oauth_enabled
def isUserSignedIntoGoogle(request):
    if request.oauth.has_credentials():
        return True
    else: return False


@decorators.oauth_enabled
def addIfNewUser(request):
    if request.oauth.has_credentials():
       #print(request.oauth.credentials.id_token.items())
       if User.objects.filter(username=request.oauth.credentials.id_token['email']).exists():
           updateNameInfo=User.objects.get(username=request.oauth.credentials.id_token['email'])
           # print('user exists') 
		   ## Update the users name ( in the case that the user was created through group/role management pages)
           updateNameInfo.set_first_name=request.oauth.credentials.id_token['given_name']
           updateNameInfo.set_last_name=request.oauth.credentials.id_token['family_name']
           updateNameInfo.save()         
       else:
	   #Create a new user from the logged in google info
         newUser=User.objects.create_user(request.oauth.credentials.id_token['email'],request.oauth.credentials.id_token['email'],'tempPass')
         newUser.first_name=request.oauth.credentials.id_token['given_name']
         newUser.last_name=request.oauth.credentials.id_token['family_name']
         newUser.save()
       user = authenticate(username=request.oauth.credentials.id_token['email'], password='tempPass')
       if user is not None:
           #print('logging in user')
           login(request, user)


@login_required(login_url='/eventsyndication/login')
@permission_required('webapp.CanLogin', login_url='/eventsyndication/logout')
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'webapp/index.html',
        {
            'title':'Syndication Tool',
            'year':datetime.now().year,
        }
    )


@permission_required('webapp.CreatePage_View', login_url='/eventsyndication/')
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

@permission_required('webapp.PublishPage_View', login_url='/eventsyndication/')
def publish(request):
    """Renders the publish event page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST" and request.POST.get('delayedSyndication') == "true":
        publicationFormInstance = PublicationsForm(initial={'EventID': request.POST.get('EventID')})
        event = EventInfo.objects.get(id=request.POST.get('EventID'))
    elif request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            publicationFormInstance = PublicationsForm(initial={'EventID': event.pk})
        else:
            return messages.error(request, "Error")
    return render(
        request,
        'webapp/publish.html',
        {
            'form': publicationFormInstance,
            'year':datetime.now().year,
            'event': event
        }
    )

def syndicate(request):
    """Renders the pubStatus page for a newly created event and attempts syndication"""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = PublicationsForm(request.POST)
        if form.is_valid():
            serviceList = request.POST.copy()
            serviceList.pop("csrfmiddlewaretoken")
            serviceList.pop("EventID")
            events = EventInfo.objects.all().order_by('-EventStart')
            event = events.get(id=request.POST.get('EventID'))
            for service in serviceList:
                publication = Publications.create(event, service)
                publication.save()
                publishService = services[service]
                publishService.publish(event, publication)
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

            
@permission_required('webapp.StatusPage_View', login_url='/eventsyndication/')
def pubStatus(request):
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)
    events = EventInfo.objects.all().order_by('-EventStart')
    if request.method == "POST" and request.POST.get('deleteEvent') == "true":
        EventInfo.objects.filter(id=request.POST.get('EventID')).delete()
        notice = 'Event deleted successfully.'
    elif request.method == "POST":
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
    else:
        notice = None
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
            'publications': postings,
            'notice': notice
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
            'year':datetime.now().year
        }
    )
@permission_required('webapp.CanChangeAPIKeys', login_url='/eventsyndication/')
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
            'hostname': settings.SERVER_HOSTNAME,
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
