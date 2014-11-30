from django import forms

from events.models import Event, Member


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['occurance'].widget = forms.Select(
            choices = self.fields['occurance'].choices,
            attrs={
                'ng-model': 'occurance',
                'ng-change': 'doThat()',
            }
        )
        self.fields['desc'].widget = forms.Textarea(attrs={
            'rows': 4,
        });

    class Meta:
        model = Event
        exclude = ['user', 'days', 'follow_up_days', 'time']


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.event = forms.ChoiceField(choices=Event.objects.filter(user=user),
                                       required=False)
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
