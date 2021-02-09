import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

class LoginRequiredMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func,  view_args, view_kwargs):
        if request.user.is_authenticated:
            return None

        for url in self.required:
            if url.match(request.path):
                messages.add_message(request, messages.INFO, 'You need to do login thing for this')
                return login_required(view_func, login_url=reverse('mainapp:login'))(request, *view_args, **view_kwargs)
        
        return None
   