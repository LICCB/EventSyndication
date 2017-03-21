"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from webapp.models import EventInfo
from webapp.models import Postings

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

class PostingsForm(ModelForm):
    """Form for the user to select where the event should syndicate to"""
    class Meta:
        model = Postings
        fields = [
            "Facebook",
            "MeetUp",
            "EventBrite",
            "GoogleCal",
            "LICCB"
        ]
