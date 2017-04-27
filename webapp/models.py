"""Definition of models"""
import pickle
import base64

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
#from oauth2client.contrib.django_orm import FlowField
#from oauth2client.contrib.django_util.models import CredentialsField

#class CredentialsModel(models.Model):
#  id = models.ForeignKey(User, primary_key=True)
#  credential = CredentialsField()


#class CredentialsAdmin(admin.ModelAdmin):
#    pass

class LICCB_User(models.Model):
    """Model for an internal user"""
    FullName=models.CharField(max_length=256)
    Email= models.CharField(max_length=256)
    FirstName=models.CharField(max_length=256)
    LastName=models.CharField(max_length=256)
class LICCB_Group(models.Model):
    """Model for an internal group"""
    GroupName=models.CharField(max_length=256)
    Email= models.CharField(max_length=256)
class LICCB_Role(models.Model):
    """Model for an internal role"""
    RoleName=models.CharField(max_length=256)
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
    CanAssignRoles=models.BooleanField(default=False, blank=False)

class LICCB_Relationship(models.Model):
    parentId=models.IntegerField()
    parentType=models.IntegerField()
    childId=models.IntegerField()
    childType=models.IntegerField()

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

    

#admin.site.register(CredentialsModel, CredentialsAdmin)