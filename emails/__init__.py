import imaplib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_rsvp_email(event_member):
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


class GmailHelper(object):
    def __init__(self, *args, **kwargs):
        """Defaults to selecting Inbox."""
        try:
            selected = kwargs.pop('selected')
        except KeyError:
            selected = "INBOX"
        super(GmailHelper, self).__init__(*args, **kwargs)
        # Move this to a refresh function
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.imap_server.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
        self.imap_server.select(selected)

    def get_email_ids(self, tag="(UNSEEN)"):
        """Defaults to unread."""
        status, email_ids = self.imap_server.search(None, tag)
        return email_ids

    def get_emails(self, email_ids=None):
        """Defaults to unread."""
        if not email_ids:
            email_ids = self.get_email_ids()

        data = []
        for e_id in email_ids:
            _, response = self.imap_server.fetch(e_id, '(UID BODY[TEXT])')
            data.append(response[0][1])
        return data

    def get_subjects(self, email_ids=None):
        """Defaults to unread."""
        if not email_ids:
            email_ids = self.get_email_ids()

        subjects = []
        for e_id in email_ids:
            _, response = self.imap_server.fetch(e_id, '(body[header.fields (subject)])')
            subjects.append( response[0][1][9:] )
        return subjects
