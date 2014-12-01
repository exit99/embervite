import datetime

from django import forms

from events.models import Event, Member
from embervite.forms import pop_form_kwarg


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.days, kwargs = pop_form_kwarg('days', kwargs)
        self.time, kwargs = pop_form_kwarg('time', kwargs)
        self.user, kwargs = pop_form_kwarg('user', kwargs)

        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['occurance'].widget = forms.Select(
            choices=self.fields['occurance'].choices,
            attrs={
                'ng-model': 'occurance',
            }
        )
        self.fields['desc'].widget = forms.Textarea(attrs={
            'rows': 4,
        })

    def clean(self, *args, **kwargs):
        if not self.days:
            raise forms.ValidationError('days', "No day selected.")
        elif not self.time:
            raise forms.ValidationError('time', "No time selected.")
        elif not self.user:
            raise forms.ValidationError('time', "You must be logged in.")
        else:
            self.cleaned_data['days'] = self.days
            self.cleaned_data['time'] = self._convert_time(self.time)
            self.cleaned_data['user'] = self.user
            return self.cleaned_data

    def _convert_time(self, time):
        hour_min = map(int, time.split(':'))
        return datetime.time(hour_min[0], hour_min[1])

    class Meta:
        model = Event
        exclude = ['user', 'days', 'follow_up_days', 'time']


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.event = forms.ChoiceField(choices=Event.objects.filter(
            user=self.user),
            required=False
        )
        super(MemberForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        event = self.cleaned_data.get('event')
        if event:
            self.cleaned_data.pop('event')
        super(MemberForm, self).save(*args, **kwargs)

        member = Member.objects.filter(**self.cleaned_data).first()
        if event and member:
            EventMember.objects.get_or_create(event=event, member=member)

    class Meta:
        model = Member
