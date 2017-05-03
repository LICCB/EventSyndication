from webapp.services.google_calendar import GoogleCalendar
from webapp.services.facebook import Facebook
from webapp.services.mailchimp import MailChimp
from webapp.services.eventbrite import Eventbrite
services = {
    'Google Calendar': GoogleCalendar(),
    'Facebook': Facebook(),
    'Mailchimp': MailChimp(),
    'Eventbrite': Eventbrite()
}
