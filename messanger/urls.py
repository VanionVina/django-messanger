from django.urls import path

from .views import ChatRoom, BaseView, UserProfile

app_name = 'messanger'
urlpatterns = [
    path('chat-room/', ChatRoom.as_view(), name='chat_room'),
    path('base/', BaseView.as_view(), name='base'),
    path('user-profile/<str:user_id>/', UserProfile.as_view(), name='user_profile'),

]