#from django.conf.urls import url
#from . import views

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
#from . import views

import oauth2client.contrib.django_util.site as django_util_site
from django.conf import urls
from . import forms
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index')
url(r'^$', views.home, name='home'),
    url(r'^createEvent$', views.createEvent, name='createEvent'),
    url(r'^admin', views.admin, name='admin'),
	url(r'^publish', views.publish, name='publish'),#/(?P<eventName>\d+)/$
	url(r'^pubStatus', views.pubStatus, name='pubStatus'),
    url(r'^login$', views.mylogin, name='login'),
    url(r'^logout$',views.logout_view,name='logout'),
    url(r'^apiKeys$', views.apiKeys, name='apiKeys'),
    url(r'^EBapiKeys$', views.EBapiKeys, name='EBapiKeys'),
    url(r'^syndicate$', views.syndicate, name='syndicate'),
    url(r'^profile_required$', views.get_profile_required),
    url(r'^groupManagement$',views.group_View, name='groupManagement'),
    url(r'^roleManagement$',views.role_View, name='roleManagement'),
    url(r'^oauth2/', urls.include(django_util_site.urls))

]
