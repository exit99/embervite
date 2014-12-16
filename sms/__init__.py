from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from embervite.models import UserProfile


def send_text(event_member):
    member = event_member.member
    event = event_member.event
    to = str(member.phone) + member.carrier
    user_hash = UserProfile.objects.filter(user=event.user).first().unique_hash
    subject = event.title + " ID:{}".format(user_hash)
    msg = '\n\nWill you be attending {} at {} on {}.\n'.format(
        event.title,
        event.location,
        datetime.strftime(event.event_date, '%a, %D @ %l:%M %p'),
    )
    msg += '\nIf you are attending reply "Yes"'
    msg += ' or follow this link: http://68.233.232.239:9000{}'.format(
        reverse('email-yes', args=(event_member.unique_hash,))
    )
    msg += '\n\nOtherwise, reply "No"'
    msg += ' or follow this link: http://68.233.232.239:9000{}'.format(
        reverse('email-no', args=(event_member.unique_hash,))
    )
    send_mail(subject, msg, settings.EMAIL_HOST_USER, [to],
              fail_silently=True)
    event_member.invite_sent = True
    event_member.save()
