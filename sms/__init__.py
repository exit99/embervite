from django.conf import settings
from django.core.mail import send_mail


def send_text(event_member):
    member = event_member.member
    event = event_member.event
    to = str(member.phone) + member.carrier
    subject = event.title
    msg = 'Will you be attending {} at {} on {}.\n\
        Reply "yes" or "no"'.format(event.title, event.location, event.event_date)
    send_mail(subject, msg, settings.EMAIL_HOST_USER, [to], fail_silently=False)
