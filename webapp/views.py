from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from webapp.forms import AddEventForm
from django.conf import settings
from django.contrib import messages
from webapp.api_helpers import facebook
from webapp.api_helpers import eventbrite
from webapp.models import ApiKey
from webapp.models import EventInfo
from webapp.models import Publications
from webapp.forms import PublicationsForm
from webapp.services.services import services
import logging

logger = logging.getLogger(__name__)

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

def pubStatus(request):
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)

    """Populates the events variables with the list of all events in the db"""
    events = EventInfo.objects.all().order_by('-EventStart')

    """If the request came from the deleteEvent button, delete and fire notice text"""
    """Else, gather info on selected event."""
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

def apiKeys(request):
    """Renders the API keys page"""
    assert isinstance(request, HttpRequest)
    facebook_code = request.GET.get('code')
    FBlogout = request.GET.get('FBlogout')
    if(facebook_code is not None):
        """Update facebook user access token with code"""
        facebook.get_user_access_token(facebook_code, 'http://loopback.pizza:8000/eventsyndication/apiKeys')
    if(FBlogout is not None):
        ApiKey.objects.filter(service = 'facebook_user_access_token').delete()
    return render(
            request,
            'webapp/apiKeys.html',
            {
            'FBclient_id': settings.FACEBOOK_SETTINGS['client_id'],
            'hostname': settings.SERVER_HOSTNAME,
            'FBname': facebook.get_user_info(),
            'EBname': eventbrite.get_user_info(),
            'EBclient_id':settings.EVENTBRITE_SETTINGS['client_key']
            }
            )

def EBapiKeys(request):
    """Handles the response from eventbrite and renders API keys page."""
    assert isinstance(request, HttpRequest)
    eventbrite_code = request.GET.get('code')
    EBlogout = request.GET.get('EBlogout')
    if (eventbrite_code is not None):
        """Use code to get oauth token"""
        eventbrite.get_user_access_token(eventbrite_code)
    if (EBlogout is not None):
        ApiKey.objects.filter(service='eventbrite_access_token').delete()
    return apiKeys(request)
"""
    return render(
            request,
            'webapp/apiKeys.html',
            {
            'FBclient_id': settings.FACEBOOK_SETTINGS['client_id'],
            'hostname': settings.SERVER_HOSTNAME,
            'FBname': facebook.get_user_info(),
            'EBname': eventbrite.get_user_info(),
            'EBclient_id': settings.EVENTBRITE_SETTINGS['client_key']
            }
            )
"""

