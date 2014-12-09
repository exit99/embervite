import csv
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from events.forms import EventForm, MemberForm
from events.models import Event, Member, EventMember


@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)
    context = {
        'events': events,
    }
    return render(request, 'events/event_list.html', context)


@login_required
def event_attendance(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    attending = EventMember.objects.filter(event=event, attending=True)
    not_attending = EventMember.objects.filter(event=event, attending=False)
    invited = EventMember.objects.filter(event=event, attending=None)
    context = {
        'invited': invited,
        'attending': attending,
        'not_attending': not_attending,
    }
    return render(request, 'events/event_attendance.html', context)


@login_required
def event_disable(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    event.disabled = not event.disabled
    event.save()
    msg = {True: 'disabled', False: 'enabled'}
    messages.success(request, "{} is {}.".format(event.title,
                                                msg[event.disabled]))
    return redirect('event-list')


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    event.delete()
    messages.success(request, "Event Deleted.")
    return redirect('event-list')


@login_required
def event_edit(request, pk):
    event = Event.objects.filter(pk=pk, user=request.user).first()
    if not event and pk != '0':
        raise Http404

    if request.method == "POST":
        days = request.POST.get('days')
        time = request.POST.get('time')
        invite_day = request.POST.get('invite_day')
        invite_time = request.POST.get('invite_time')
        form = EventForm(request.POST, instance=event, days=days, time=time,
                         user=request.user, invite_day=invite_day,
                         invite_time=invite_time)
    else:
        form = EventForm(instance=event)
    if form.is_valid():
        # TODO form can be submitted without a proper day
        if not event:
            Event.objects.create(**form.cleaned_data)
            messages.success(request, "New Event Created!")
        else:
            for attr, value in form.cleaned_data.iteritems():
                setattr(event, attr, value)
            event.save()
            messages.success(request, "Event Information Updated!")
        return redirect('event-list')

    context = {
        'form': form,
        'event': event,
        'pk': pk,
        'choices': json.dumps(form.fields['occurance'].choices),
    }
    return render(request, 'events/event_edit.html', context)


@login_required
def event_add(request, pk):
    event = Event.objects.filter(pk=pk, user=request.user).first()
    if not event and pk != '0':
        raise Http404
    if request.method == "POST":
        primary_keys = [v for k, v in request.POST.iteritems()
                        if k != "csrfmiddlewaretoken" ]
        invited = event.update_members(primary_keys)
        msg = "{} Members are now invited to {}.".format(invited, event.title)
        messages.success(request, msg)
        return redirect('event-list')

    members = Member.objects.filter(user=request.user).order_by('first_name')
    event_members = event.event_members(pks=True)
    context = {
        'event': event,
        'members': members,
        'event_members': json.dumps(event_members),
    }
    return render(request, 'events/event_add.html', context)


@login_required
def member_list(request):
    members = Member.objects.filter(user=request.user)
    context = {
        'members': members,
    }
    return render(request, 'events/member_list.html', context)


@login_required
def member_edit(request, pk):
    member = Member.objects.filter(pk=pk, user=request.user).first()
    if not member and pk != '0':
        raise Http404

    form = MemberForm(request.POST or None, instance=member, user=request.user)
    if form.is_valid():
        if not member:
            Member.objects.create(**form.cleaned_data)
            messages.success(request, "New Member Created!")
        else:
            for attr, value in form.cleaned_data.iteritems():
                setattr(member, attr, value)
            member.save()
            messages.success(request, "Member Information Updated!")
        return redirect('member-list')

    context = {
        'form': form,
        'pk': pk,
    }
    return render(request, 'events/member_edit.html', context)


@login_required
def download_backup(request):
    members = Member.objects.filter(user=request.user)
    if not members:
        return HttpResponse(200)
    json_members = serializers.serialize('json', members)

    response = HttpResponse(content_type='text/json')
    content = 'attachment; filename="embervite-backups-{}.json"'.format(
        request.user.username
    )
    response['Content-Disposition'] = content
    response.write(json_members)

    return response


# TODO ask Keene about a more secure way to do this
def email_yes(request, unique_hash):
    return _email_update(request, unique_hash, True)


def email_no(request, unique_hash):
    return _email_update(request, unique_hash, False)


def _email_update(request, unique_hash, attending):
    event_member = _update_event_member(unique_hash, attending)
    context = {
        'event_member': event_member
    }
    return render(request, 'events/confirmation.html', context)


def _update_event_member(unique_hash, attending):
    event_member = get_object_or_404(EventMember, unique_hash=unique_hash)
    event_member.attending = attending
    event_member.save()
    return event_member

