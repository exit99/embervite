from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as login_user,
    logout as logout_user,
)
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


@require_POST
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login_user(request, user)
        else:
            messages.error(request, "Your account is inactive. \
                             Please contact support.")
    else:
        messages.error(request, "The username and password were incorrect.")
        return redirect('index')
    return redirect('event-list')


@require_POST
def logout(request):
    logout_user(request)
    return redirect('index')


def debug_view(request):
    from events.utils import check_for_replies, send_invites
    if not settings.DEBUG:
        raise Http404
    send_invites()
    check_for_replies()
