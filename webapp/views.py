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
#from oauth2client.contrib import xsrfutil
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.contrib.django_orm import Storage
#from webapp.models import CredentialsModel

from django.conf import settings
from syndication import settings
from django.contrib import messages
from webapp.api_helpers import facebook


#Our models and forms
from webapp.models import ApiKey
from webapp.models import EventInfo
from webapp.models import Publications
from webapp.models import GlobalPermissions
from webapp.models import LICCB_Role
from webapp.forms import AddGroupForm
from webapp.forms import AddEventForm
from webapp.forms import PublicationsForm
from webapp.forms import AddRoleForm
#Needed for google auth
from oauth2client.contrib.django_util import decorators
#needed for user control and authentication
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
# Needed for permission control
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


import pdb; 



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

@login_required(login_url='/eventsyndication/login')
@permission_required('webapp.CanLogin', login_url='/eventsyndication/logout')
def home(request):
       #cleanData()
       #print('hit home')
       #print(request.user)
       #print('Does user have canlogin perm?',request.user.has_perm('webapp.CanLogin'))
       assert isinstance(request, HttpRequest)
       return render(
        request,
        'webapp/index.html',
        {
            'title':'Syndication Tool',
            'year':datetime.now().year,
        }
    )
 
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
        return True
    else: return False


@decorators.oauth_enabled
def addIfNewUser(request):
    if request.oauth.has_credentials():
       #print(request.oauth.credentials.id_token.items())
       if User.objects.filter(username=request.oauth.credentials.id_token['email']).exists():
           updateNameInfo=User.objects.get(username=request.oauth.credentials.id_token['email'])
           print('user exists') 
           updateNameInfo.set_first_name=request.oauth.credentials.id_token['given_name']
           updateNameInfo.set_last_name=request.oauth.credentials.id_token['family_name']
           updateNameInfo.save()         
       else:
         newUser=User.objects.create_user(request.oauth.credentials.id_token['email'],request.oauth.credentials.id_token['email'],'tempPass')
         newUser.first_name=request.oauth.credentials.id_token['given_name']
         newUser.last_name=request.oauth.credentials.id_token['family_name']
         newUser.save()
       user = authenticate(username=request.oauth.credentials.id_token['email'], password='tempPass')
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
@permission_required('webapp.StatusPage_View', login_url='/eventsyndication/')
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

@permission_required('webapp.CanChangeGroups', login_url='/eventsyndication/')
def group_View(request):
    print('My groups ',request.user.groups.all())
    form = AddGroupForm()
    print('hit right view')
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        print('Hit post')
        form = AddGroupForm(request.POST)
        if form.is_valid():
            #new_group, created = Group.objects.get_or_create(name=form.groupName)
            print(form.cleaned_data.get('groupName'))
            print(form.cleaned_data.get('Children'))
            userEmails=form.cleaned_data.get('Children').split(",")
            print('About to create group')
            #Creates a group if its new
            #stanislavgrozny@gmail.com
            new_group, created = Group.objects.get_or_create(name=form.cleaned_data.get('groupName'))
            new_group.save()
            for userEmail in userEmails:
               if User.objects.filter(username=userEmail).exists():
                  user =User.objects.filter(username=userEmail)
                  print('about to add group')
                  group = Group.objects.get(name=form.cleaned_data.get('groupName'))
                  request.user.groups.add(group)
               else:
                   #create a user for the future
                  newUser=User.objects.create_user(userEmail,userEmail,'tempPass')
                  newUser.save()
            return HttpResponseRedirect('groupManagement') 
        else:
            messages.error(request, "Error")
    return render(
    request,
    'webapp/groupManagement.html',
    {
        'title': 'Manage Groups',
        'message':'Your Group Management page.',
        'year':datetime.now().year,
        'form': form,
        'groups':Group.objects.all()
    })

@permission_required('webapp.CanChangePermissions', login_url='/eventsyndication/')
def role_View(request):
    #print('My groups ',request.user.groups.all())
    form = AddRoleForm()
    print(LICCB_Role.objects.all())
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        #print('Hit role post')
        form = AddRoleForm(request.POST)
        if form.is_valid():
            #print('valid form')
            roleInfo=form.cleaned_data
            print(roleInfo.items())
            userList=roleInfo.get('Users').split(",")
            groupList=roleInfo.get('Groups').split(",")
            for group in groupList:
                   print(group)
                   new_group, created = Group.objects.get_or_create(name=group)
                   #group = Group.objects.get(name=group)
                   setGroupPermissions(new_group,roleInfo)
            for user in userList:
                   print(user)
                   new_User, created = User.objects.get_or_create(username=user)
                   new_User.set_password('tempPass')
                   new_User.save()
                   nUser = User.objects.get(username=user)
                   print(nUser)
                   setUserPermissions(nUser,roleInfo)
            form.save()

            return HttpResponseRedirect('roleManagement') 
        else:
            print('error message')
            messages.error(request, "Error")
    return render(
    request,
    'webapp/roleManagement.html',
    {
        'title': 'Manage Roles',
        'message':'Your Role Management page.',
        'year':datetime.now().year,
        'form': form,
        'groups':Group.objects.all()
    })

def setGroupPermissions(myGroup,roleInfo):
    myGroup.permissions.clear()
    content_type = ContentType.objects.get_for_model(GlobalPermissions)
    
    for permName in ['CanLogin',  
           'CreatePage_View', 
            'CreatePage_Action',
            'PublishPage_View', 
            'PublishPage_Action', 
            'StatusPage_View',
            'StatusPage_Edit', 
            'StatusPage_Delete',
            'CanChangePermissions', 
            'CanChangeGroups', 
            'CanChangeAPIKeys', 
            'CanViewLogs']:
       if(roleInfo.get(permName)):
         print(mygroup,' has ' ,permName) 
         permission = Permission.objects.get(content_type=content_type, codename=permName)
         myGroup.permissions.add(permission)

def setUserPermissions(myUser,roleInfo):
    myUser.user_permissions.clear()
    content_type = ContentType.objects.get_for_model(GlobalPermissions)
    
    for permName in ['CanLogin',  
           'CreatePage_View', 
            'CreatePage_Action',
            'PublishPage_View', 
            'PublishPage_Action', 
            'StatusPage_View',
            'StatusPage_Edit', 
            'StatusPage_Delete',
            'CanChangePermissions', 
            'CanChangeGroups', 
            'CanChangeAPIKeys', 
            'CanViewLogs']:
       if(roleInfo.get(permName)):
        print(myUser,' has ' ,permName) 
        permission = Permission.objects.get(content_type=content_type, codename=permName)
        myUser.user_permissions.add(permission)

def cleanData():
    User.objects.all().delete()
    Group.objects.all().delete()
    LICCB_Role.objects.all().delete()     