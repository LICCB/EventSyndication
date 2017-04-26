# Create your views here.

#def index(request):
#    return render(request, 'webapp/main.html')
# Definition of views.


from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from webapp.forms import AddEventForm
from django.conf import settings
from django.contrib import messages
from webapp.api_helpers import facebook
from webapp.models import ApiKey
from webapp.models import EventInfo
from webapp.models import Publications
from webapp.forms import PublicationsForm

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
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            #CONNECT TO EVERYTHING AND POST EVERYTHING
            #YOLO YOLO
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
