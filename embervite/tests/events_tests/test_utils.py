import pytest

from events.models import Event
from events.utils import (
    send_invites,
)


@pytest.mark.django_db
class TestSendInvites:
    def test_it_does_nothing_with_disabled_events(self, admin_user, event_factory):
        event_factory.create(disabled=True)
        assert Event.objects.all().count() == 1
        assert Event.objects.filter(disabled=False).count == 1
