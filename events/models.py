import os
import datetime
from dateutil import parser
import json

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
    ('both', 'Both'),
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
    invite_day = models.CommaSeparatedIntegerField(max_length=1000)
    invite_time = models.TimeField()
    disabled = models.BooleanField(default=False)
    needs_reset = models.BooleanField(default=False)
    last_event_date = models.DateTimeField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.helper = EventDateHelper(model=self)

    def save(self, *args, **kwargs):
        """Defualt to first event date if not active.  (Avoids breaking
        send_invites.)"""
        if not self.last_event_date:
            self.last_event_date = self.event_date
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    ##############
    # PROPERTIES #
    ##############

    @property
    def invited(self):
        count = EventMember.objects.filter(event=self, invite_sent=True).count()
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

    @property
    def event_date(self):
        return self.helper.calc_event_date()

    @property
    def invite_date(self):
        return self.helper.calc_invite_date()

    @property
    def time_to_reset(self):
        last = self.last_event_date
        date = datetime.datetime(last.year, last.month, last.day,
                                 last.hour, last.minute)
        return datetime.datetime.now() > date and self.needs_reset

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

    @property
    def to_json(self):
        data = {
            'pk': self.pk,
            'title': self.title,
            'event_date': str(self.event_date.strftime('%A %B %d, %Y %I:%M %p')),
            'invite_date': str(self.invite_date.strftime(
                '%A %B %d, %Y at %I:%M %p')),
            'location': self.location,
            'invited': self.invited,
            'attending': self.attending,
            'not_attending': self.not_attending,
        }
        return json.dumps(data)

    #################
    # EVENT MEMBERS #
    #################

    def update_members(self, primary_keys):
        """Disable EventMember not in primary_keys.
        Add EventMember in primary_keys. Return new count of Event Members"""
        for event_member in EventMember.objects.filter(event=self):
            if event_member.pk not in primary_keys:
                event_member.disabled = True
                event_member.save()
        for pk in primary_keys:
            member = Member.objects.get(pk=pk)
            em, created = EventMember.objects.get_or_create(member=member,
                                                            event=self)
            em.disabled = False
            em.save()
        return self.invited

    def event_members(self, pks=False):
        event_members = EventMember.objects.filter(event=self, disabled=False)
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
    carrier = models.CharField(choices=CARRIER_CHOICES, max_length=50,
                               blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATES, blank=True,
                               null=True)
    zip = models.IntegerField(blank=True, null=True)
    preference = models.CharField(max_length=10, choices=PREFERENCE_CHOICES)
    tags = models.CharField(max_length=255, blank=True, null=True)

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
    unique_hash = models.TextField(blank=True, null=True)
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return "{} at {}".format(self.member, self.event)

    def save(self, *args, **kwargs):
        if not self.unique_hash:
            self.unique_hash = self._create_hash()
        super(EventMember, self).save(*args, **kwargs)

    def _create_hash(self):
        new_hash = os.urandom(4).encode('hex')
        if EventMember.objects.filter(unique_hash=new_hash):
            return self._create_hash()
        else:
            return new_hash


class EventDateHelper(object):
    """Helps convert Event fields to human readable, and usable datetimes."""
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super(EventDateHelper, self).__init__(*args, **kwargs)
        self.now = datetime.datetime.now()

    def calc_invite_date(self):
        event_date = self.calc_event_date()
        invite_date = event_date - datetime.timedelta(days=int(
            self.model.invite_day)
        )
        return self.update_time(invite_date, self.model.invite_time)

    def calc_event_date(self):
        return self.calc_date(int(self.model.days)-1, self.model.time)

    def calc_date(self, day, time):
        return self.update_time(self.calc_day(day), time)

    def calc_day(self, day):
        """We save with 1-7 not 0-6 like datetime.weekday()."""
        weekday = self.now.weekday() + 1
        if weekday >= day:
            days = (7 - weekday) + day
        else:
            days = day - weekday
        return self.now + datetime.timedelta(days=days)

    def update_time(self, date, time):
        return datetime.datetime(date.year, date.month, date.day, time.hour,
                                 time.minute)



