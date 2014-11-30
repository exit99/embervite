from django.contrib import messages
from django.contrib.auth import authenticate, login as user_login
from django.views.decorators.http import require_POST
from django.shortcuts import redirect


@require_POST
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            user_login(request, user)
            messages.success(request, "You are logged in.")
        else:
            messages.error(request, "Your account is inactive. \
                             Please contact support.")
    else:
        messages.error(request, "The username and password were incorrect.")
    return redirect(request.META.get('HTTP_REFERER'))
