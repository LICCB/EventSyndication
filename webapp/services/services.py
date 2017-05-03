from webapp.services.google_calendar import GoogleCalendar
from webapp.services.facebook import Facebook
from webapp.services.mailchimp import MailChimp
from webapp.services.wordpress import Wordpress
services = {
    'Google Calendar': GoogleCalendar(),
    'Wordpress': Wordpress(),
    'Facebook': Facebook(),
    'Mailchimp': MailChimp()
}
