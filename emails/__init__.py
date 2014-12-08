import imaplib
import re

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
        super(GmailHelper, self).__init__(*args, **kwargs)
        self.refresh()

    def refresh(self, selected="INBOX"):
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.imap_server.login(settings.EMAIL_HOST_USER,
                               settings.EMAIL_HOST_PASSWORD)
        self.imap_server.select(selected)

    def get_email_ids(self, tag="(UNSEEN)"):
        status, email_ids = self.imap_server.search(None, tag)
        if email_ids:
            return email_ids[0].split()
        return None

    def get_emails(self, email_ids=None, tag="(RFC822)"):
        """Defaults to unread."""
        data = []
        for e_id in email_ids:
            _, response = self.imap_server.fetch(e_id, tag)
            data.append(response[0][1])
        return data

    def get_email_data(self, email):
        date = self._do_regex('Date: .*?:\d\d:\d\d', email)[6:]
        subject = self._do_regex('Subject: .*?\r\n', email)[9:]
        from_email = self._do_regex('<.*?>',
                              self._do_regex('From: .*?>', email))[1:-1]
        text = email.split('Content-Type: text/html')[-1]
        text = 'Content-Type: text/html' + text
        return {
            'date': date,
            'subject': subject,
            'from': from_email,
            'text': text,
        }

    def _do_regex(self, regex, data):
        cleaned_data = re.findall(regex, data)
        try:
            cleaned_data = cleaned_data[0]
        except IndexError:
            return ""
        else:
            return cleaned_data

    @property
    def unread_emails(self):
        emails = self.get_emails(self.get_email_ids())
        return [self.get_email_data(email) for email in emails]

