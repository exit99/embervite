from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def process_request(self, request):
        accepted = ['/', '/login/']
        if not request.user.is_authenticated() and request.path not in accepted:
            return redirect('index')
