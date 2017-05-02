from __future__ import print_function

from django.core.urlresolvers import reverse
from django.shortcuts import render,get_object_or_404

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpRequest

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from webapp.api_helpers import facebook
from django.db.models import Q
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

from django import template

from webapp.services.services import services
import logging

register = template.Library()
logger = logging.getLogger(__name__)

def mylogin(request):
    #cleanData()

    ####Uncomment and run the below line to setup the superuser
    createSuperUser(request)

    if(isUserSignedIntoGoogle(request)):
       addIfNewUser(request)
       url = reverse('home')
       return HttpResponseRedirect(url)

    """Renders the login page."""
    #if user click login button
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
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
       if User.objects.filter(username=request.oauth.credentials.id_token['email']).exists():
           updateNameInfo=User.objects.get(username=request.oauth.credentials.id_token['email'])
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
           login(request, user)

def logout_view(request):
   logout(request)
   request.user.auth_token.delete()
   return render(
            request,
            'webapp/logout.html',
            {
                'title':'Syndication Tool',
                'year':datetime.now().year,
                'isLoggedOut':True
            }
        )

@login_required(login_url='/eventsyndication/login')
def home(request,error=''):
    if request.user.has_perm('webapp.CanLogin'):
        """Renders the home page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'webapp/index.html',
            {
                'title':'Syndication Tool',
                'year':datetime.now().year,
                'errorMessage':error
            }
        )
    else:
        return render(
            request,
            'webapp/logout.html',
            {
                'title':'Syndication Tool',
                'year':datetime.now().year,
                'errorMessage':"You don't have permission to be logged in",
                'isLoggedOut':True
            }
        )

def createEvent(request):
  if request.user.has_perm('webapp.CreatePage_View'):  
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
        'form': form,
        'canAction':request.user.has_perm('webapp.CreatePage_Action')
    }
)
  else:
      return loadHomeWithPermError(request,"You don't have permissions to create events")

def publish(request):
    """Renders the publish event page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST" and request.POST.get('delayedSyndication') == "true":
        publicationFormInstance = PublicationsForm(initial={'EventID': request.POST.get('EventID')})
        event = EventInfo.objects.get(id=request.POST.get('EventID'))
    elif request.method == "POST":
        if request.user.has_perm('webapp.CreatePage_Action'):
          form = AddEventForm(request.POST)
          if form.is_valid():
              event = form.save()
              publicationFormInstance = PublicationsForm(initial={'EventID': event.pk})
          else:
              return messages.error(request, "Error")
        else:
            return render(
            request,
            'webapp/createEvent.html',
            {
                'title': 'Syndicate New Event',
                'message':'Your Event Creation page.',
                'year':datetime.now().year,
                'form': AddEventForm(),
                'canAction':request.user.has_perm('webapp.CreatePage_Action')
            })
    if request.user.has_perm('webapp.PublishPage_View'):
        return render(
            request,
            'webapp/publish.html',
            {
                'form': publicationFormInstance,
                'year':datetime.now().year,
                'event': event,
                'canAction':request.user.has_perm('webapp.PublishPage_Action')
            }
        )
    else:
       return render(
        request,
        'webapp/createEvent.html',
        {
            'title': 'Syndicate New Event',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
            'form': AddEventForm(),
            'errorMessage':event.EventName+" was saved successfully, but you don't have access to the publish page",
            'canAction':request.user.has_perm('webapp.CreatePage_Action')
        })

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
                if request.user.has_perm('webapp.StatusPage_View'):
                    return render(
                        request,
                        'webapp/pubStatus.html',
                        {
                            'title': 'Publication Status',
                            'message': 'Event Syndication Status',
                            'year': datetime.now().year,
                            'events': events,
                            'event': event,
                            'publications': postings,
                        }
                    )
                else:   
                    return loadHomeWithPermError(request,"Your event has been syndicated, but you don't have access to view the progress of the syndication")
            else:
                messages.error(request,"Error")
        

def pubStatus(request):
    """Renders the createEvent page."""
    if request.user.has_perm('webapp.StatusPage_View'):
        assert isinstance(request, HttpRequest)
        events = EventInfo.objects.all().order_by('-EventStart')
        if request.method == "POST" and request.POST.get('deleteEvent') == "true":
          if request.user.has_perm('webapp.StatusPage_Delete'):  
            EventInfo.objects.filter(id=request.POST.get('EventID')).delete()
            notice = 'Event deleted successfully.'
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
                'notice': notice,
                'canEdit':request.user.has_perm('webapp.StatusPage_Edit'),
                'canDelete':request.user.has_perm('webapp.StatusPage_Delete')
            })

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
                    'publications': postings,
                    'canEdit':request.user.has_perm('webapp.StatusPage_Edit'),
                    'canDelete':request.user.has_perm('webapp.StatusPage_Delete')
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
                'notice': notice,
                'canEdit':request.user.has_perm('webapp.StatusPage_Edit'),
                'canDelete':request.user.has_perm('webapp.StatusPage_Delete')
            }
        )
    else:
        return loadHomeWithPermError(request,"You do not habe access to view the publish status page" )
     
def loadHomeWithPermError(request,error):
   return home(request,error)

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

def apiKeys(request):
  if request.user.has_perm('webapp.CanChangeAPIKeys'):
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
  else:
      return loadHomeWithPermError(request,"You don't have acces to change the API keys")

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

def group_View(request):

    if request.user.has_perm('webapp.CanChangeGroups'):    
        form = AddGroupForm()
        lastAction=0
        assert isinstance(request, HttpRequest)
        if request.method == "POST":
            form = AddGroupForm(request.POST)
            if form.is_valid():
                    groupInfo=form.cleaned_data
                    if 'deleteGroup' in request.POST:
                        Group.objects.filter(name=groupInfo.get("groupName")).delete()
                        lastAction=3
                    elif 'editGroup' in request.POST:
                        #delete old one and save the update
                        Group.objects.filter(name=groupInfo.get("groupName")).delete()
                        createGroup(groupInfo)
                        lastAction=2

                    else:
                         createGroup(groupInfo) #recalculate permissions 
                         lastAction=1

                    calculatePerms(request)
                    return loadGroupM(request,lastAction)
            else:
                messages.error(request, "Error")
        return loadGroupM(request,lastAction)

    else:
        return loadHomeWithPermError(request,"You do not have access to change groups")

def createGroup(groupInfo):
    userEmails=groupInfo.get('Children').split(",")
    #Creates a group
    new_group, created = Group.objects.get_or_create(name=groupInfo.get('groupName'))
    new_group.save()
    g = Group.objects.get(name=groupInfo.get('groupName')) 
    for userEmail in userEmails:
        user =User.objects.filter(username=userEmail)
        if not user:
            #create a user for the future
            newUser=User.objects.create_user(userEmail,userEmail,'tempPass')
            newUser.save()
        user =User.objects.filter(username=userEmail)
        user.first().groups.add(g)
           


def loadGroupM(request,lastAction):
    return render(
    request,
    'webapp/groupManagement.html',
        {
            'title': 'Manage Groups',
            'message':'Your Group Management page.',
            'year':datetime.now().year,
            'form': AddGroupForm(),
            'groups':Group.objects.all(),
            'lastAction':lastAction
        })

#@permission_required('webapp.CanChangePermissions', login_url='/eventsyndication/')
def role_View(request):
   if request.user.has_perm('webapp.CanChangePermissions'):
        form = AddRoleForm()
        lastAction=0
        assert isinstance(request, HttpRequest)
        if request.method == "POST":
            form = AddRoleForm(request.POST)
            if form.is_valid():
                roleInfo=form.cleaned_data
                if 'deleteRole' in request.POST:
                    LICCB_Role.objects.filter(RoleName=roleInfo.get("RoleName")).delete()
                    lastAction=3
                elif 'editRole' in request.POST:
                    #delete old one and save the update
                    LICCB_Role.objects.filter(RoleName=roleInfo.get("RoleName")).delete()
                    form.save()
                    lastAction=2
                else:
                 form.save()
                 lastAction=1
                calculatePerms(request)
                loadRoleM(request,lastAction)
            else:
                messages.error(request, "Error")
        return loadRoleM(request,lastAction)
   else:
        return loadHomeWithPermError(request,"You do not have access to change roles or permissions")


def loadRoleM(request,lastAction):
    return render(
    request,
    'webapp/roleManagement.html',
    {
        'title': 'Manage Roles',
        'message':'Your Role Management page.',
        'year':datetime.now().year,
        'form': AddRoleForm(),
        'groups':Group.objects.all(),
        'roles':LICCB_Role.objects.filter(~Q(RoleName="BUILTINSUPERUSER")),#return all roles but superuser one
        'lastAction':lastAction
    })

def calculatePerms(request):
    currUser=request.user
    groups=Group.objects.all()
    users=User.objects.all()
    for group in groups:
      group.permissions.clear()
    for user in users:
        user.user_permissions.clear()
    roles=LICCB_Role.objects.all()

    for roleInfo in roles:
             userList=roleInfo.Users.split(",")
             groupList=roleInfo.Groups.split(",")
             if groupList:
              for group in groupList:
                  if group: 
                    group = Group.objects.get(name=group)
                    setGroupPermissions(group,roleInfo)
             if userList:
              for user in userList:
                 if user:
                   if not User.objects.filter(username=user).exists():
                     new_User, created = User.objects.get_or_create(username=user)
                     new_User.set_password('tempPass')
                     new_User.save()
                   
                   nUser = User.objects.get(username=user)
                   if nUser is not None:
                    setUserPermissions(nUser,roleInfo,currUser)
     
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
       if getattr(roleInfo,permName): 
         permission = Permission.objects.get(content_type=content_type, codename=permName)
         myGroup.permissions.add(permission)

def setUserPermissions(myUser,roleInfo,currUser):
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
        #if a role has a permission then add permission to user
       if getattr(roleInfo,permName):
        permission = Permission.objects.get(content_type=content_type, codename=permName)
        myUser.user_permissions.add(permission)
        #used to refresh permission cache
        myUser=get_object_or_404(User, pk=myUser.pk)

#for dev to clean out temp groups and roles, as well as perms and users
def cleanData():
    print('Purging users, groups,, and roles')
    User.objects.all().delete()
    Group.objects.all().delete()
    LICCB_Role.objects.all().delete()  
     
#for Dev to let your user have all perms
def createSuperUser(request):
   if not LICCB_Role.objects.filter(RoleName='BUILTINSUPERUSER').exists():
      role= LICCB_Role(RoleName='BUILTINSUPERUSER',Users=settings.SUPERUSER)
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
          setattr(role,permName,True)
      addIfNewUser(request)
      role.save()
      calculatePerms(request)
    