from django.urls import path

from .views import ChatRoom

app_name = 'messanger'
urlpatterns = [
    path('chat-room', ChatRoom.as_view(), name='chat_room')
]