#from django.conf.urls import url
#from . import views

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
#from . import views
from . import forms
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index')
url(r'^$', views.home, name='home'),
    url(r'^createEvent$', views.createEvent, name='createEvent'),
    url(r'^admin', views.admin, name='admin'),
	url(r'^publish', views.publish, name='publish'),#/(?P<eventName>\d+)/$
	url(r'^pubStatus', views.pubStatus, name='pubStatus'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'webapp/login.html',
            'authentication_form': forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^apiKeys$', views.apiKeys, name='apiKeys'),
    url(r'^EBapiKeys$', views.EBapiKeys, name='EBapiKeys'),
    url(r'^syndicate$', views.syndicate, name='syndicate')
]
