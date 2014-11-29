from django.contrib.auth.models import User
from django.db import models

from embervite.constants import STATES

OCCURANCE_CHOICES = (
    ('once', 'Once'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
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
    occurance = models.ChoiceField(max_length=8, choices=OCCURANCE_CHOICES)
    days = models.CommaSeperatedIntgerField(max_length=1000)
    follow_up_days = models.CommaSeperatedIntgerField(max_length=1000)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.title

    @property
    def invited(self):
        EventMember.objects.filter(event=self).count()

    @property
    def attending(self):
        EventMember.objects.filter(event=self, attending=True).count()

    @property
    def not_attending(self):
        EventMember.objects.filter(event=self, attending=False).count()


class Members(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=555, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.ChoiceField(max_length=2, choices=STATES, blank=True,
                               null=True)
    preference = models.ChoiceField(max_length=10, choices=PREFERENCE_CHOICES)

    def __unicode__(self):
        return "{} {}".format(self.first_name, self.last_name)


class EventMember(models.Model):
    event = models.ForeignKey(Event)
    member = models.ForeignKey(Members)
    invite_sent = models.BooleanField(default=False)
    follow_up_sent = models.BooleanField(default=False)
    attending = models.BooleanField(blank=True, null=True)

    def __unicode__(self):
        return "{} at {}".format(self.member, self.event)
