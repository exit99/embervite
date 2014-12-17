import pytest
import datetime

from django.contrib.auth.models import User

from events.models import Event, Member


class EventFactory(object):
    @staticmethod
    def create(**kwargs):
        user = User.objects.all().first()
        arguments = {
            'user': user,
            'title': "My Event",
            'occurance': 'weekly',
            'time': datetime.time(12, 1),
            'invite_day': '2',
            'days': u'3',
            'invite_time': datetime.time(1, 0),
        }
        for k, v in kwargs.iteritems():
            arguments[k] = v
        return Event.objects.create(**arguments)


@pytest.fixture
def event_factory():
    """Create Event Models by passing kwargs to create()."""
    return EventFactory


class MemberFactory(object):
    @staticmethod
    def create(**kwargs):
        user = User.objects.all().first()
        arguments = {
            'user': user,
            'first_name': "John",
            'last_name': 'Baptist',
            'email': 'my@email.com',
            'phone': '5555555555',
            'carrier': '@tmomail.net',
            'preference': 'email',
        }
        for k, v in kwargs.iteritems():
            arguments[k] = v
        return Member.objects.create(**arguments)


@pytest.fixture
def member_factory():
    """Create Member Models by passing kwargs to create()."""
    return MemberFactory
