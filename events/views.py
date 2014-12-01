import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from events.forms import EventForm, MemberForm
from events.models import Event, Member


@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)
    context = {
        'events': events,
    }
    return render(request, 'events/event_list.html', context)


@login_required
def event_edit(request, pk):
    event = Event.objects.filter(pk=pk).first()
    if request.POST:
        days = request.POST.get('days')
        time = request.POST.get('time')
        form = EventForm(request.POST, instance=event, days=days, time=time,
                         user=request.user)
    else:
        form = EventForm(instance=event)
    if form.is_valid():
        # TODO when the form is submitted it can be submitted without a proper
        # day
        if not event:
            Event.objects.create(**form.cleaned_data)
            messages.success(request, "New Event Created!")
        else:
            for attr, value in form.cleaned_data.iteritems():
                setattr(event, attr, value)
            event.save()
            messages.success(request, "Event Updated!")
        return redirect('event-list')

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




