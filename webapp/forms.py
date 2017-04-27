"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from webapp.models import EventInfo
from webapp.models import Services
from webapp.models import LICCB_Role

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class AddGroupForm(forms.Form):
    """ModelForm for Add group page."""
    groupName=forms.CharField(label='Group Name', max_length=50)
    Children=forms.CharField(label='Comma delimited users',max_length=256)   


class AddEventForm(ModelForm):
    """ModelForm for Add Event page."""
    class Meta:
        model = EventInfo
        fields = [
            "EventName",
            "EventDescription",
            "EventMeetLocation",
            "EventDestination",
            "EventStart",
            "EventEnd"
        ]
        labels = {
            "EventName":"Event Name",
            "EventDescription":"Description",
            "EventMeetLocation" : "Meet Location",
            "EventDestination" : "Destination",
            "EventStart" : "Start Time (MM/DD/YYYY HH:MM)",
            "EventEnd" : "End Time (MM/DD/YYYY HH:MM)"
        }

class AddRoleForm(ModelForm):
    """ModelForm for Add Event page."""
    class Meta:
        model = LICCB_Role
        fields = [
        "RoleName",
    "Groups",
    "Users",
    "CanLogin",
    "CreatePage_View",
   "CreatePage_Action",
    "PublishPage_View",
    "PublishPage_Action",
    "StatusPage_View",
    "StatusPage_Edit",
    "StatusPage_Delete",
    "CanChangePermissions",
    "CanChangeGroups",
    "CanChangeAPIKeys",
    "CanViewLogs"
    ]
        #labels = {
        #    "RoleName":"Role Name",
        #    "EventDescription":"Description",
        #    "EventMeetLocation" : "Meet Location",
        #    "EventDestination" : "Destination",
        #    "EventStart" : "Start Time (MM/DD/YYYY HH:MM)",
        #    "EventEnd" : "End Time (MM/DD/YYYY HH:MM)"
        #}

class PublicationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PublicationsForm, self).__init__(*args, **kwargs)
        services = Services.objects.values_list('Name', flat=True)
        for service in services:
            self.fields[service] = forms.BooleanField(required=False)
    EventID = forms.IntegerField(widget=forms.HiddenInput())
