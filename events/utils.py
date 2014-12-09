import re

from emails import GmailHelper
from embervite.models import UserProfile
from events.models import Event, Member, EventMember


def send_invites():
    for event in Event.objects.all()
        EventM


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
