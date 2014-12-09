import re
import datetime

from django import forms

from events.models import Event, Member
from embervite.forms import pop_form_kwarg


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.days, kwargs = pop_form_kwarg('days', kwargs)
        self.invite_day, kwargs = pop_form_kwarg('invite_day', kwargs)
        self.time, kwargs = pop_form_kwarg('time', kwargs)
        self.invite_time, kwargs = pop_form_kwarg('invite_time', kwargs)
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

    def clean_title(self):
        if re.findall('ID:', self.cleaned_data.get('title')):
            raise forms.ValidationError("Cannot hav ID: in title.")
        return self.cleaned_data.get('title').strip(' ')

    def clean(self, *args, **kwargs):
        if not self.days:
            raise forms.ValidationError('days', "No day selected.")
        elif not self.time:
            raise forms.ValidationError('time', "No time selected.")
        elif not self.user:
            raise forms.ValidationError('time', "You must be logged in.")
        elif not self.invite_time:
            raise forms.ValidationError('invite_time', "No prior time selected.")
        elif not self.invite_day:
            raise forms.ValidationError('invite_day', "No prior days selected.")
        else:
            data = self.cleaned_data
            data['days'] = self.days
            data['time'] = self._convert_time(self.time)
            data['user'] = self.user
            data['invite_day'] = self.invite_day
            data['invite_time'] = self._convert_time(self.invite_time)
            return data

    def _convert_time(self, time):
        hour_min = map(int, time.split(':'))
        return datetime.time(hour_min[0], hour_min[1])

    class Meta:
        model = Event
        exclude = ['user', 'days', 'time', 'invite_day', 'invite_time']


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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Member.objects.filter(user=self.user, email=email).exists():
            raise forms.ValidationError('One of your members has this \
                                        email already.')
        return email

    def clean_preference(self):
        pref = self.cleaned_data['preference']

        if pref in ['email', 'both'] and not self.cleaned_data.get('email'):
            raise forms.ValidationError('No email specified above.')
        if pref in ['phone', 'both'] and not self.cleaned_data.get('phone'):
            raise forms.ValidationError('No phone specified above.')
        return pref

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = re.sub('[()-]', '', phone)
        if len(phone) not in [10, 0]:
            raise forms.ValidationError('Invalid phone number length.')
        if Member.objects.filter(user=self.user, phone=phone).exists():
            raise forms.ValidationError('One of your members has this \
                                        number already.')
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
