"""Definition of models"""
from django.db import models


class EventInfo(models.Model):

    """ This table will store the skeleton information about an event. To allow for
    repeatable events, this is separated from the table with the data about
     an individual trip."""
    EventName = models.CharField(max_length=50)
    EventDescription = models.TextField()
    EventMeetLocation = models.CharField(max_length=50)
    EventDestination = models.CharField(max_length=50)
    EventStart = models.DateTimeField()
    EventEnd = models.DateTimeField()
    def __unicode__(self):
        return self.EventName


class ApiKey(models.Model):
    """Model for an API key"""
    service = models.CharField(max_length=50)
    key = models.TextField()
    lastUpdated = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, service, key):
        apiKey = cls(service = service, key = key)
        return apiKey

class Services(models.Model):
    """Information regarding all available syndication services."""
    Name = models.CharField(max_length=50, blank=False)
    IsEnabled = models.BooleanField(default=True, blank=False)

class Publications(models.Model):
    """New model that keeps track of all instances of event publication"""
    EventID = models.ForeignKey(EventInfo, on_delete=models.CASCADE)
    Service = models.CharField(max_length=50, blank=False)
    Status = models.CharField(max_length=100)
    url = models.CharField(max_length=500)

    @classmethod
    def create(cls, EventID, Service):
        publication=cls(EventID=EventID, Service=Service,Status='Pending')
        return publication
