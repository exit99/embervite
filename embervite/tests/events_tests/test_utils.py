import pytest
import datetime

from events.models import Event, Member, EventMember
from events.utils import (
    send_invites,
    check_for_replies,
)
from senders.emails import GmailHelper


@pytest.mark.django_db
def test_event_factory(admin_user, event_factory):
    event_factory.create(disabled=True, user=admin_user)
    event_factory.create(user=admin_user)
    assert Event.objects.all().count() == 2
    assert Event.objects.filter(disabled=True).count() == 1


@pytest.mark.django_db
def test_member_factory(admin_user, member_factory):
    member_factory.create(preference="both", user=admin_user)
    member_factory.create(user=admin_user)
    assert Member.objects.all().count() == 2
    assert Member.objects.filter(preference="both").count() == 1


@pytest.mark.django_db
class TestSendInvites:
    def test_it_does_nothing_with_disabled_events(self, admin_user,
                                                  event_factory):
        event_factory.create(disabled=True, user=admin_user)
        send_invites()
        assert Event.objects.filter(needs_reset=True).count() == 0
        assert Event.objects.filter(needs_reset=False).count() == 1

    def test_it_emails_invites(self, admin_user, event_factory, member_factory):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user)
        em = EventMember.objects.create(event=event, member=member)
        assert not em.invite_sent
        send_invites()
        assert EventMember.objects.get(pk=em.pk).invite_sent
        assert Event.objects.get(pk=event.pk).needs_reset

    def test_it_texts_invites(self, admin_user, event_factory, member_factory):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        assert not em.invite_sent
        send_invites()
        assert EventMember.objects.get(pk=em.pk).invite_sent
        assert Event.objects.get(pk=event.pk).needs_reset

    def test_it_resets(self, admin_user, event_factory, member_factory):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        last_date = datetime.datetime.now() - datetime.timedelta(days=7)
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day, needs_reset=True,
                                     last_event_date=last_date)
        member = member_factory.create(user=admin_user)
        em = EventMember.objects.create(event=event, member=member,
                                        invite_sent=True)
        send_invites()
        event = Event.objects.get(pk=event.pk)
        member = Event.objects.get(pk=member.pk)
        em = EventMember.objects.get(pk=em.pk)
        assert not event.needs_reset
        assert event.last_event_date.date() == event.event_date.date()
        assert em.attending is None
        assert not em.invite_sent
        assert not em.follow_up_sent


@pytest.mark.django_db
class TestCheckForReplies:
    def test_it_does_nothing_with_no_unread_emails(self, event_factory,
                                                   member_factory,
                                                   monkeypatch, admin_user):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        monkeypatch.setattr(GmailHelper, 'unread_emails', [])

        check_for_replies()
        assert em.attending is None

    def test_it_does_nothing_with_no_sms_emails(self, event_factory,
                                                member_factory,
                                                monkeypatch, admin_user):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        unread_email = {'type': 'EMAIL'}
        monkeypatch.setattr(GmailHelper, 'unread_emails', [unread_email])

        check_for_replies()
        assert em.attending is None

    def test_it_updates_member_with_yes_reply(self, event_factory,
                                              member_factory,
                                              monkeypatch, admin_user):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        subject = "Hello ID:{}".format(em.unique_hash)
        unread_email = {'type': 'SMS', 'text': 'Yes', 'subject': subject}
        monkeypatch.setattr(GmailHelper, 'unread_emails', [unread_email])

        check_for_replies()
        assert EventMember.objects.get(unique_hash=em.unique_hash).attending

    def test_it_updates_member_with_no_reply(self, event_factory,
                                             member_factory,
                                             monkeypatch, admin_user):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        subject = "Hello ID:{}".format(em.unique_hash)
        unread_email = {'type': 'SMS', 'text': 'Absolutely nO',
                        'subject': subject}
        monkeypatch.setattr(GmailHelper, 'unread_emails', [unread_email])

        check_for_replies()
        assert not EventMember.objects.get(unique_hash=em.unique_hash).attending

    def test_it_does_nothing_with_invalid_reply(self, event_factory,
                                                member_factory,
                                                monkeypatch, admin_user):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        unread_email = {'type': 'SMS', 'text': 'Absolutely bad'}
        monkeypatch.setattr(GmailHelper, 'unread_emails', [unread_email])

        check_for_replies()
        assert EventMember.objects.get(
            unique_hash=em.unique_hash).attending is None

    def test_it_does_nothing_with_both_yes_no(self, event_factory,
                                              member_factory,
                                              monkeypatch, admin_user):
        days = datetime.datetime.now().weekday() + 3
        invite_day = days - 2
        event = event_factory.create(user=admin_user, days=days,
                                     invite_day=invite_day)
        member = member_factory.create(user=admin_user, preference="phone")
        em = EventMember.objects.create(event=event, member=member)
        unread_email = {'type': 'SMS', 'text': 'yesno'}
        monkeypatch.setattr(GmailHelper, 'unread_emails', [unread_email])

        check_for_replies()
        assert em.attending is None
