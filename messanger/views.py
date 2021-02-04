from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User

from messanger.models import Consumer


class ChatRoom(View):
    def get(self, request):
        # consumer = Consumer.objects.get(user=request.user)
        consumer = get_object_or_404(Consumer, user=request.user)
        context = {
            'consumer': consumer,
        }
        return render(request, 'chat_room.html', context)

class BaseView(View):
    def get(self, request):
        return render(request, 'base.html')

class UserProfile(View):
    def get(self, request, user_id):
        user_c = get_object_or_404(User, id=user_id)
        context = {
            'user_c': user_c,
        }
        return render(request, 'user_profile.html', context)