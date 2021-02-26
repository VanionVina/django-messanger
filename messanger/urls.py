from django.urls import path

from .views import ( ChatRoomView, 
        UserProfile, ChangeProfile, 
        ChangeUserAvatar, FriendsView,
        CreateNewChat, ChatRoomSettings,
        ChatRoomChangeImage, AddFriendToChatView
        )

from .views import ( delete_chat_room, add_friend_to_chat, give_moderator_priveleges,
                     kick_user_from_room, send_friend_request, delete_notification,
                     answer_to_friend_request, delete_friend
                     )

app_name = 'messanger'
urlpatterns = [
    path('chat-room/', ChatRoomView.as_view(), name='chat_room'),
    path('chat-room/<str:chat_id>/', ChatRoomView.as_view(), name='chat_room'),
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
    path('give-moderator-priveleges/<int:room_id>/<int:user_id>/', give_moderator_priveleges, name='give_mod_priv'),
    path('kick-user/<int:room_id>/<int:user_id>/', kick_user_from_room, name='kick_user_from_room'),
    path('send-friend/<int:from_user_id>/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('delete-notification/<int:notification_id>/', delete_notification, name='del_notification'),
    path('answer-to-friend-request/<int:notification_id>/<str:answer>/', answer_to_friend_request, name='answer_friend_request'),
    path('delete-friend/<int:friend_id>/', delete_friend, name='delete_friend'),
]
