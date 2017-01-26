from django.db import models

# This table will store the skeleton information about an event. To allow for
# repeatable events, this is separated from the table with the data about
# an individual trip.
class EventInfo(models.Model):
	EventID = models.AutoField(primary_key=True)
	EventName = models.CharField(max_length=50)
	EventDescription = models.TextField()
	EventLocation = models.CharField(max_length=50)

# This table will store the information about a particular instance of a trip.
# It uses the primary key of the EventInfo table to join the information 
# together, and also includes the PostingID from the Postings table.
class EventLog(models.Model):
	TripID = models.AutoField(primary_key=True)
	EventID = models.ForeignKey(EventInfo,on_delete=models.CASCADE)
	EventStart = models.DateTimeField()
	EventEnd = models.DateTimeField()
	PostingID = models.ForeignKey(Postings, on_delete=models.SET_NULL)

# This table keeps track of where an event has been posted.
class Postings(models.Model):
	PostingID = models.AutoField(primary_key=True)
	TripID = models.ForeignKey(EventLog, on_delete=models.CASCADE)
	Facebook = models.Boolean()
	MeetUp = models.Boolean()
	EventBrite = models.Boolean()
