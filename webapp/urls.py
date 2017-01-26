from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index')
url(r'^$', app.views.home, name='home'),
    url(r'^createEvent$', app.views.createEvent, name='createEvent'),
    url(r'^admin', app.views.admin, name='admin'),
	url(r'^publish', app.views.publish, name='publish'),
	url(r'^pubStatus', app.views.pubStatus, name='pubStatus'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
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

    ]
