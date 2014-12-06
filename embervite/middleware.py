from django.shortcuts import redirect
import django.utils.timezone

from pytz import timezone


class LoginRequiredMiddleware:
    def process_request(self, request):
        path = request.path
        if not path.startswith('/ev/email/'):
            accepted = ['/', '/login/']
            if not request.user.is_authenticated() and path not in accepted:
                return redirect('index')


class TimeZoneMiddleware:
    def process_request(self, request):
        tz = timezone('US/Eastern')
        django.utils.timezone.activate(tz)
