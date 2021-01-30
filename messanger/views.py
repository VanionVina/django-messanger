from django.shortcuts import render
from django.views.generic import View


class ChatRoom(View):
    def get(self, request):
        return render(request, 'chat_room.html')

class BaseView(View):
    def get(self, request):
        return render(request, 'base.html')