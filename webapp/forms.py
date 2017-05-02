"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from webapp.models import EventInfo
from webapp.models import Services

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




class AddEventForm(ModelForm):
    """ModelForm for Add Event page."""
    class Meta:
        model = EventInfo
        fields = [
            "EventName",
            "EventDescription",
            "PoCName",
            "PoCEmail",
            "PoCNumber",
            "Fee",
            "Availability",
            "EventMeetLocation",
            "EventDestination",
            "EventStart",
            "EventEnd",
            "RegistrationLink"
        ]
        labels = {
            "EventName":"Event Name",
            "EventDescription":"Description",
            "EventMeetLocation" : "Meet Location",
            "EventDestination" : "Destination",
            "EventStart" : "Start Time (MM/DD/YYYY HH:MM)",
            "EventEnd" : "End Time (MM/DD/YYYY HH:MM)",
            "PoCName":"Point of Contact's Name",
            "PoCEmail":"Point of Contact's Email",
            "PoCNumber":"Point of Contact's Number",
            "RegistrationLink":"Registration Link"
        }

class PublicationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PublicationsForm, self).__init__(*args, **kwargs)
        services = Services.objects.values_list('Name', flat=True)
        for service in services:
            self.fields[service] = forms.BooleanField(required=False)
    EventID = forms.IntegerField(widget=forms.HiddenInput())
