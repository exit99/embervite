from django import forms

from events.models import Event, Member


class EventForm(forms.ModelForm):
    class Meta:
        model = Event


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
