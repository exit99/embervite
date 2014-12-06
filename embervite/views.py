from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as login_user,
    logout as logout_user,
)
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect


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
