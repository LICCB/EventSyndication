from django.db import models

# This table will store the skeleton information about an event. To allow for
# repeatable events, this is separated from the table with the data about
# an individual trip.
class EventInfo(models.Model):
    EventID = models.AutoField(primary_key=True)
    EventName = models.CharField(max_length=50)
    EventDescription = models.TextField()
    EventMeetLocation = models.CharField(max_length=50)
    EventDestination = models.CharField(max_length=50)
    EventStart = models.DateTimeField()
    EventEnd = models.DateTimeField()
    PostingID = models.IntegerField()
    def __unicode__(self):
        return self.EventName

# This table keeps track of where an event has been posted.
class Postings(models.Model):
    PostingID = models.AutoField(primary_key=True)
    Facebook = models.BooleanField()
    MeetUp = models.BooleanField()
    EventBrite = models.BooleanField()
