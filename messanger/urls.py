from django.urls import path

from .views import ( ChatRoomView, BaseView,
        UserProfile, ChangeProfile, 
        ChangeUserAvatar, FriendsView,
        CreateNewChat, ChatRoomSettings,
        ChatRoomChangeImage, AddFriendToChatView
        )

from .views import delete_chat_room, add_friend_to_chat

app_name = 'messanger'
urlpatterns = [
    path('chat-room/', ChatRoomView.as_view(), name='chat_room'),
    path('chat-room/<str:chat_id>/', ChatRoomView.as_view(), name='chat_room'),
    path('base/', BaseView.as_view(), name='base'),
    path('user-profile/<str:user_id>/', UserProfile.as_view(), name='user_profile'),
    path('change-profile/', ChangeProfile.as_view(), name='change_profile'),
    path('change-user-avatar/', ChangeUserAvatar.as_view(), name='change_user_avatar'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('create-new-chat/', CreateNewChat.as_view(), name='create_new_chat'),
    path('delete-chat-room/<int:room_id>/', delete_chat_room, name='delete_chat_room'),
    path('room-settings/<int:room_id>/', ChatRoomSettings.as_view(), name='chat_room_settings'),
    path('chat-room-image/<int:room_id>/', ChatRoomChangeImage.as_view(), name='chat_room_change_image'),
    path('add-friend-to-chat/<int:room_id>/', AddFriendToChatView.as_view(), name="add_friend_to_chat"),
    path('add-to-chat/<int:room_id>/<int:friend_id>/', add_friend_to_chat, name='add_to_chat'),
]
