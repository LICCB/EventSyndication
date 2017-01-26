#from django.shortcuts import render

# Create your views here.

#def index(request):
#    return render(request, 'webapp/main.html')
"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

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
    return render(
        request,
        'webapp/createEvent.html',
        {
            'title':'Create Event',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
        }
    )
def publish(request):
    """Renders the createEvent page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'webapp/publish.html',
        {
            'title':'Publish event',
            'message':'Your Event Creation page.',
            'year':datetime.now().year,
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
