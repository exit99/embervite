from django.conf import settings
from django.core.mail import send_mail

from embervite.models import UserProfile


def send_text(event_member):
    member = event_member.member
    event = event_member.event
    to = str(member.phone) + member.carrier
    user_hash = UserProfile.objects.filter(user=event.user).first().unique_hash
    subject = event.title + " ID:{}".format(user_hash)
    msg = 'Will you be attending {} at {} on {}.\nReply "yes" or "no"\n'.format(
        event.title,
        event.location,
        event.event_date,
    )
    send_mail(subject, msg, settings.EMAIL_HOST_USER, [to], fail_silently=False)
