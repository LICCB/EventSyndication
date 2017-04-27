from webapp.services.google_calendar import GoogleCalendar
from webapp.services.facebook import Facebook
from webapp.services.mailchimp import MailChimp
services = {
    'GoogleCal': GoogleCalendar(),
    'Facebook': Facebook(),
    'Mailchimp': MailChimp()
}
