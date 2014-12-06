from django.conf import settings
from django.core.mail import send_mail


def send_text(number, carrier, event):
    to = number + carrier
    subject = event.title
    msg = 'Will you be attending {} at {} on {}.\n\
        Reply "yes" or "no"'.format(event.title, event.location, event.date)
    send_mail(subject, msg, settings.EMAIL_HOST_USER, [to], fail_silently=False)
