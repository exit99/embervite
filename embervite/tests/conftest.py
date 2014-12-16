import pytest

from django.contrib.auth.models import User

from events.models import Event


class EventFactory(object):
    @staticmethod
    def create(**kwargs):
        user = User.objects.all().first()
        arguments = {
            'user': user,
            'title': "My Event",
            'occurance': 'weekly',
            'time': '12:01',
            'invite_day': '2',
            'days': u'3',
            'invite_time': u'1:00',
        }
        for k, v in kwargs.iteritems():
            arguments[k] = v
        return Event.objects.create(**arguments)


@pytest.fixture
def event_factory():
    """Create Event Models by passing kwargs to create()."""
    return EventFactory
