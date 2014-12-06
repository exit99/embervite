from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_email(event_member):
    htmly = get_template('templated_email/event.html')
    plaintext = get_template('templated_email/event.txt')

    context = {
        'event_member': event_member,
    }
    d = Context(context)

    subject = '{}: Your Invited! RSVP'.format(event_member.event.title)
    from_email = settings.EMAIL_HOST_USER
    to = event_member.member.email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
