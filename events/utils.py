from datetime import datetime
import re

from senders.emails import send_invite_email, GmailHelper
from senders.sms import send_text
from embervite.models import UserProfile
from events.models import Event, Member, EventMember


def send_invites():
    for event in Event.objects.filter(disabled=False):
        if datetime.now() > event.invite_date and not event.time_to_reset:
            send_event_invites(event)
        elif event.time_to_reset:
            reset_event(event)


def send_event_invites(event, needs_reset=True):
    event_members = event.eventmember_set.filter(invite_sent=False,
                                                 disabled=False)
    for event_member in event_members:
        if event_member.member.preference in ['phone', 'both']:
            send_text(event_member)
        if event_member.member.preference in ['email', 'both']:
            send_invite_email(event_member)
    event.needs_reset = needs_reset
    event.save()


def reset_event(event):
    event.needs_reset = False
    event.last_event_date = event.event_date
    event.save()
    for event_member in event.eventmember_set.all():
        event_member.attending = None
        event_member.invite_sent = False
        event_member.follow_up_sent = False
        event_member.save()


def check_for_replies():
    gmail_inbox = GmailHelper()
    for email in gmail_inbox.unread_emails:
        if email.get('type') == 'SMS':
            yes, no = has_yes_or_no(email.get('text'))
            if yes and not no:
                update_event_member_from_email(email, True)
            elif not yes and no:
                update_event_member_from_email(email, False)
            else:
                # gmail_inbox.move_to_folder(email.get('id'), 'Error')
                pass


def has_yes_or_no(text):
    yes = re.findall('yes', text, re.IGNORECASE)
    no = re.findall('no', text, re.IGNORECASE)
    return yes, no


def update_event_member_from_email(email, attending):
    event_member = get_member_from_subject(email.get('subject'))
    event_member.attending = attending
    event_member.save()


def get_member_from_subject(subject):
    data = subject.split('ID:')
    unique_hash = data[1].strip(' \r\n')
    return EventMember.objects.get(unique_hash=unique_hash)
