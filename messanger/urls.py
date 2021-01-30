from django.urls import path

from .views import ChatRoom, BaseView

app_name = 'messanger'
urlpatterns = [
    path('chat-room/', ChatRoom.as_view(), name='chat_room'),
    path('base/', BaseView.as_view(), name='base')
]