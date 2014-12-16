from datetime import datetime
import re

from emails import send_invite_email, GmailHelper
from sms import send_text
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
    event, user = get_info_from_subject(email.get('subject'))
    if not event or not user:
        # TODO probably want to log here as well
        return
    phone = email.get('from', ' @ ').split('@')[0]
    while len(phone) > 10:
        phone = phone[1:]
    members = Member.objects.filter(user=user, phone=phone)

    try:
        event_member = EventMember.objects.get(member=members.first(),
                                               event=event)
    except EventMember.DoesNotExist:
        # TODO probably want to log here as well
        pass
    else:
        event_member.attending = attending
        event_member.save()


def get_info_from_subject(subject):
    if subject.startswith('RE:'):
        subject = subject[3:]
    data = subject.split('ID:')
    title = data[0].strip(' \r\n')
    unique_hash = data[1][:11]
    user = None
    profile = UserProfile.objects.filter(unique_hash=unique_hash)
    if profile:
        user = profile.first().user
    try:
        event = Event.objects.get(user=user, title=title)
    except Event.DoesNotExist:
        return False, user
    else:
        return event, user
