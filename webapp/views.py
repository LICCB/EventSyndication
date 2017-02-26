#from django.shortcuts import render

# Create your views here.

#def index(request):
#    return render(request, 'webapp/main.html')
"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from webapp.forms import AddEventForm
from django.shortcuts import get_object_or_404,redirect
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
            form.save()
        return redirect('publish')#,eventName=request.POST['EventName']
    return render(
        request,
        'webapp/createEvent.html',
        {
            'title':'Create Event',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
            'form': form
        }
    )
def publish(request):#,eventName=""
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'webapp/publish.html',
        {
            'title':'Publish event',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
            # 'eventName':eventName,
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
