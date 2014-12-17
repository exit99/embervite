import pytest

from events.models import EventDateHelper, EventMember


class TestEventDateHelper:
    def test_it_calcs_dates_when_days_is_less(self, admin_user, event_factory):
        event = event_factory.create(user=admin_user, days='3', invite_day='5')
        helper = EventDateHelper(model=event)
        assert helper.calc_event_date().day - 5 == helper.calc_invite_date().day

    def test_it_calcs_dates_when_days_is_less_and_1(self, admin_user,
                                                    event_factory):
        event = event_factory.create(user=admin_user, days='1', invite_day='5')
        helper = EventDateHelper(model=event)
        assert helper.calc_event_date().day - 5 == helper.calc_invite_date().day

    def test_it_calcs_dates_when_days_is_less_and_7(self, admin_user,
                                                    event_factory):
        event = event_factory.create(user=admin_user, days='7', invite_day='5')
        helper = EventDateHelper(model=event)
        assert helper.calc_event_date().day - 5 == helper.calc_invite_date().day

    def test_it_calcs_dates_when_days_is_more(self, admin_user, event_factory):
        event = event_factory.create(user=admin_user, days='5', invite_day='2')
        helper = EventDateHelper(model=event)
        assert helper.calc_event_date().day - 2 == helper.calc_invite_date().day

    def test_it_calcs_dates_when_days_is_more_and_1(self, admin_user,
                                                    event_factory):
        event = event_factory.create(user=admin_user, days='1', invite_day='2')
        helper = EventDateHelper(model=event)
        assert helper.calc_event_date().day - 2 == helper.calc_invite_date().day

    def test_it_calcs_dates_when_days_is_more_and_7(self, admin_user,
                                                    event_factory):
        event = event_factory.create(user=admin_user, days='7', invite_day='2')
        helper = EventDateHelper(model=event)
        assert helper.calc_event_date().day - 2 == helper.calc_invite_date().day


@pytest.mark.django_db
class TestEventModel:
    def test_its_update_member_property_creates(self, event_factory,
                                                member_factory, admin_user):
        event = event_factory.create(user=admin_user)
        member_pks = []
        for i in range(0, 4):
            member_pks.append(member_factory.create(user=admin_user).pk)
        assert not EventMember.objects.all().count()
        event.update_members(primary_keys=member_pks)
        assert EventMember.objects.all().count() == 4

    def test_its_update_member_property_disables(self, event_factory,
                                                 member_factory, admin_user):
        event = event_factory.create(user=admin_user)
        pks = []
        for i in range(0, 4):
            member = member_factory.create(user=admin_user)
            pks.append(member.pk)
            EventMember.objects.create(member=member, event=event)
        event.update_members(primary_keys=pks[1:])
        assert EventMember.objects.all().count() == 4
        assert EventMember.objects.filter(disabled=True).count() == 1
        assert EventMember.objects.filter(disabled=False).count() == 3
