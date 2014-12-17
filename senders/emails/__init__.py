from dateutil import parser
import imaplib
import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_invite_email(event_member):
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
    event_member.invite_sent = True
    event_member.save()


class GmailHelper(object):
    def __init__(self, *args, **kwargs):
        """Defaults to selecting Inbox."""
        super(GmailHelper, self).__init__(*args, **kwargs)
        self.connect()

    def connect(self, selected="INBOX"):
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
        data = {}
        for e_id in email_ids:
            _, response = self.imap_server.fetch(e_id, tag)
            data[e_id] = response[0][1]
        return data

    def get_email_data(self, email_id, email):
        date = parser.parse(self._do_regex('Date: .*?:\d\d:\d\d', email)[6:])
        subject = self._do_regex('Subject: .*?\r\n', email)[9:]
        from_addr = self._do_regex('<.*?>', self._do_regex('From: .*?>',
                                                           email))[1:-1]
        if not from_addr:
            data = self._do_regex('Sender: .+', email)
            from_addr = self._do_regex('\d+?@.+?\..+?\r', data)[:-1]
            text = self._do_regex(data + '\n\r\n.+', email)[len(data):]
            msg_type = "SMS"
        else:
            text = email.split('Content-Type: text/html')[-1]
            text = 'Content-Type: text/html' + text
            msg_type = "email"
        return {
            'email_id': email_id,
            'date': date,
            'subject': subject,
            'from': from_addr,
            'text': text,
            'type': msg_type,
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
        return [self.get_email_data(email_id, email)
                for email_id, email in emails.iteritems()]

    def move_to_folder(self, e_id, folder):
        # TODO make this work
        self.connect(folder)
        apply_lbl_msg = self.imap_server.uid('COPY', e_id, folder)
        if apply_lbl_msg[0] == 'OK':
            mov, data = self.imap_server.uid('STORE', e_id, '+FLAGS', '(\Deleted)')
            self.imap_server.expunge()
        self.connect()
