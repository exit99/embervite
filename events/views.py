import json

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

from events.forms import EventForm, MemberForm
from events.models import Event, Member


def event_edit(request, pk):
    event = Event.objects.filter(pk=pk).first()
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, "New Event Created!")
        return redirect()

    context = {
        'form': form,
        'event': event,
        'pk': pk,
        'choices': json.dumps(form.fields['occurance'].choices),
    }
    return render(request, 'events/event_edit.html', context)


def member_edit(request, pk):
    member = Member.objects.filter(pk=pk).first()
    form = MemberForm(request.POST or None, instance=member, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "New Event Created!")
        return redirect()

    context = {
        'form': form
    }
    return render(request, 'events/member_edit.html', context)




