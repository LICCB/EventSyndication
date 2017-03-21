# Create your views here.

#def index(request):
#    return render(request, 'webapp/main.html')
# Definition of views.


from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from webapp.forms import AddEventForm
from webapp.forms import PostingsForm
from django.conf import settings
from django.contrib import messages
from webapp.api_helpers import facebook
from webapp.models import ApiKey
#from webapp.models import EvertInfo
from webapp.models import Postings

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
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            newEvent = form.save()
            posting = Postings.create(newEvent)
            #Gotta add event to google calendar here
            postingsFormInstance = PostingsForm(instance=posting)
            return render(request, 'webapp/publish.html', {
                'eventID': newEvent.pk,
                'form': postingsFormInstance,
                'title': 'Publish Event'
            })
        else:
            messages.error(request, "Error")

    return render(
    request,
    'webapp/createEvent.html',
    {
        'title': 'Your Title',
        'message':'Your Event Creation page.',
        'year':datetime.now().year,
        'form': form
    }
)
def publish(request):
    """Renders the publish event page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = PostingsForm(request.POST)
        if form.is_valid():
            #CONNECT TO EVERYTHING AND POST EVERYTHING
            #YOLO YOLO
            #For now let's just save the postings table and call it a day.
            form.save()
            return render(
                request,
                'webapp/pubStatus.html',
                {
                    'form': form,
                    'year':datetime.now().year
                }
            )
def pubStatus(request):
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'webapp/pubStatus.html',
        {
            'title':'Publication Status',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
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
