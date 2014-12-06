import re
import datetime

from django import forms

from events.models import Event, Member, EventMember
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
        exclude = ['user', 'days', 'time', 'send_delta']


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user, kwargs = pop_form_kwarg('user', kwargs)
        self.event = forms.ChoiceField(choices=Event.objects.filter(
            user=self.user),
            required=False
        )
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['desc'].widget = forms.Textarea(attrs={
            'rows': 4,
        })

    def clean_preference(self):
        pref = self.cleaned_data['preference']
        if pref == 'email' and not self.cleaned_data.get('email'):
            raise forms.ValidationError('No email specified above.')
        if pref == 'phone' and not self.cleaned_data.get('phone'):
            raise forms.ValidationError('No phone specified above.')
        return pref

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = re.sub('[()-]', '', phone)
        if len(phone) not in [10, 0]:
            raise forms.ValidationError('Invalid phone number length.')
        return phone

    def clean_carrier(self):
        carrier = self.cleaned_data.get('carrier')
        if self.cleaned_data.get('phone') and not carrier:
            raise forms.ValidationError('No carrier selected for phone.')
        return carrier

    def clean(self, *args, **kwargs):
        self.cleaned_data['user'] = self.user
        return self.cleaned_data

    class Meta:
        model = Member
        exclude = ['user']
