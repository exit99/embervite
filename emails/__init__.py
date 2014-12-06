from django.conf import settings
from django.core.mail import send_mail


def send_email(email, event):
    subject = event.title
    msg = 'Will you be attending {} at {} on {}.\n\
        Reply "yes" or "no"'.format(event.title, event.location, event.date)
    send_mail(subject, msg, settings.EMAIL_HOST_USER, [email], fail_silently=False)
