"""Definition of models"""
from django.db import models


class EventInfo(models.Model):

    """ This table will store the skeleton information about an event. To allow for
    repeatable events, this is separated from the table with the data about
     an individual trip."""
    EventID = models.AutoField(primary_key=True)
    EventName = models.CharField(max_length=50)
    EventDescription = models.TextField()
    EventMeetLocation = models.CharField(max_length=50)
    EventDestination = models.CharField(max_length=50)
    EventStart = models.DateTimeField()
    EventEnd = models.DateTimeField()
    PostingID = models.IntegerField(default=0)
    def __unicode__(self):
        return self.EventName


class Postings(models.Model):
    """This table keeps track of where an event has been posted"""
    PostingID = models.AutoField(primary_key=True)
    Facebook = models.BooleanField()
    MeetUp = models.BooleanField()
    EventBrite = models.BooleanField()

class ApiKey(models.Model):
    """Model for an API key"""
    service = models.CharField(max_length=50)
    key = models.TextField()
    lastUpdated = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, service, key):
        apiKey = cls(service = service, key = key)
        return apiKey

