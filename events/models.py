import datetime
from dateutil import parser
import json
import timedelta

from django.contrib.auth.models import User
from django.db import models

from embervite.constants import STATES
from embervite.carriers import CARRIER_CHOICES


OCCURANCE_CHOICES = (
    # ('once', 'Once'),
    ('weekly', 'Weekly'),
    # ('monthly', 'Monthly'),
    # ('yearly', 'Yearly'),
)

PREFERENCE_CHOICES = (
    ('email', 'Email'),
    ('phone', 'Phone'),
    # ('twitter', 'Twitter'),
    # ('facebook', 'Facebook'),
)


class Event(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    occurance = models.CharField(max_length=8, choices=OCCURANCE_CHOICES)
    days = models.CommaSeparatedIntegerField(max_length=1000)
    time = models.TimeField()
    send_delta = timedelta.fields.TimedeltaField()

    def __unicode__(self):
        return self.title

    ##############
    # PROPERTIES #
    ##############

    @property
    def invited(self):
        count = EventMember.objects.filter(event=self).count()
        if not count:
            return 0
        return count

    @property
    def attending(self):
        count = EventMember.objects.filter(event=self, attending=True).count()
        if not count:
            return 0
        return count

    @property
    def not_attending(self):
        count = EventMember.objects.filter(event=self, attending=False).count()
        if not count:
            return 0
        return count

    @property
    def send_date(self):
        return parser.parse(self.send_date)

    @send_date.setter
    def send_date(self):
        self._send_date = datetime.strftime('%d %H:%M:%S')

    ########
    # JSON #
    ########

    @property
    def days_json(self):
        if not self.days:
            return "false"
        return json.dumps(self.days)

    @property
    def time_json(self):
        if not self.time:
            return "false"
        return json.dumps(str(self.time).strip('0:'))

    @property
    def occurance_json(self):
        if not self.occurance:
            return "false"
        return json.dumps(self.occurance)

    #################
    # EVENT MEMBERS #
    #################

    def update_members(self, primary_keys):
        """Delete EventMember not in primary_keys.
        Add EventMember in primary_keys. Return new count of Event Members"""
        for event_member in EventMember.objects.filter(event=self):
            if event_member.pk not in primary_keys:
                event_member.delete()
            else:
                primary_keys.pop(event_member.pk)
        for pk in primary_keys:
            member = Member.objects.get(pk=pk)
            EventMember.objects.create(member=member, event=self)
        return self.invited

    def event_members(self, pks=False):
        event_members = EventMember.objects.filter(event=self)
        if not pks:
            return event_members
        return [event_member.member.pk for event_member in event_members]


class Member(models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=555, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    carrier = models.CharField(choices=CARRIER_CHOICES, max_length=4,
                               blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATES, blank=True,
                               null=True)
    zip = models.IntegerField(blank=True, null=True)
    preference = models.CharField(max_length=10, choices=PREFERENCE_CHOICES)

    def __unicode__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class EventMember(models.Model):
    event = models.ForeignKey(Event)
    member = models.ForeignKey(Member)
    invite_sent = models.BooleanField(default=False)
    follow_up_sent = models.BooleanField(default=False)
    attending = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return "{} at {}".format(self.member, self.event)
