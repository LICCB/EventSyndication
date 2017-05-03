"""Definition of models"""
from django.db import models


class EventInfo(models.Model):

    """ This table will store the skeleton information about an event. To allow for
    repeatable events, this is separated from the table with the data about
     an individual trip."""
    EventName = models.CharField(max_length=50)
    EventDescription = models.TextField()
    PoCName = models.CharField(max_length=50, blank=True)
    PoCEmail = models.EmailField(max_length=100, blank=True)
    PoCNumber = models.CharField(max_length=15, blank=True)
    Fee = models.CharField(max_length=50, blank=True)
    Availability = models.CharField(max_length=50, blank=True)
    EventMeetLocation = models.CharField(max_length=50)
    EventDestination = models.CharField(max_length=50)
    EventStart = models.DateTimeField()
    EventEnd = models.DateTimeField()
    RegistrationLink = models.URLField()
    def __unicode__(self):
        return self.EventName


class ApiKey(models.Model):
    """Model for an API key"""
    service = models.CharField(max_length=50)
    key = models.TextField()
    lastUpdated = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, service, key):
        """Method for creating a new API key"""
        apiKey = cls(service=service, key=key)
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
        """Method to create new publication entry. Default status is pending"""
        publication=cls(EventID=EventID, Service=Service,Status='Pending')
        return publication

class LICCB_Role(models.Model):
    """Model for an internal role"""
    RoleName=models.CharField(max_length=256,blank=False)
    Groups=models.CharField(max_length=2048,blank=True)
    Users=models.CharField(max_length=2048,blank=True)
    CanLogin= models.BooleanField(default=True, blank=False)
    CreatePage_View=models.BooleanField(default=False, blank=False)
    CreatePage_Action=models.BooleanField(default=False, blank=False)
    PublishPage_View=models.BooleanField(default=False, blank=False)
    PublishPage_Action=models.BooleanField(default=False, blank=False)
    StatusPage_View=models.BooleanField(default=False, blank=False)
    StatusPage_Edit=models.BooleanField(default=False, blank=False)
    StatusPage_Delete=models.BooleanField(default=False, blank=False)
    CanChangePermissions=models.BooleanField(default=False, blank=False)
    CanChangeGroups=models.BooleanField(default=False, blank=False)
    CanChangeAPIKeys=models.BooleanField(default=False, blank=False) 
    CanViewLogs=models.BooleanField(default=False, blank=False)

#class LICCB_Relationship(models.Model):
#    RoleName=models.CharField(max_length=256)
#    childName=models.CharField(max_length=256)
#    childType=models.IntegerField()

class GlobalPermissions(models.Model):

    class Meta:
        managed = False  # No database table creation or deletion operations \
                         # will be performed for this model. 

        permissions = ( 
            ('CanLogin', 'Allows user to login'),  
            ('CreatePage_View', 'Can view the create page'), 
            ('CreatePage_Action', 'Can create events'), 
            ('PublishPage_View', 'Can view publish page'),  
            ('PublishPage_Action', 'Can publish events'), 
            ('StatusPage_View', 'Can view status of events'), 
            ('StatusPage_Edit', 'Can edit posted events'),  
            ('StatusPage_Delete', 'Can  delete posted events'), 
            ('CanChangePermissions', 'can change permissions'),  
            ('CanChangeGroups', 'Can change groups'), 
            ('CanChangeAPIKeys', 'Can change API keys'),
            ('CanViewLogs', 'Can view logs')
        )