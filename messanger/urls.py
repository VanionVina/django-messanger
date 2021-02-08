from django.urls import path

from .views import ( ChatRoomView, BaseView,
        UserProfile, ChangeProfile, 
        ChangeUserAvatar, FriendsView
        )

app_name = 'messanger'
urlpatterns = [
    path('chat-room/', ChatRoomView.as_view(), name='chat_room'),
    path('chat-room/<str:chat_id>/', ChatRoomView.as_view(), name='chat_room'),
    path('base/', BaseView.as_view(), name='base'),
    path('user-profile/<str:user_id>/', UserProfile.as_view(), name='user_profile'),
    path('change-profile/', ChangeProfile.as_view(), name='change_profile'),
    path('change-user-avatar/', ChangeUserAvatar.as_view(), name='change_user_avatar'),
    path('friends/', FriendsView.as_view(), name='friends'),
]
