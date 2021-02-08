from django.shortcuts import get_object_or_404

from messanger.models import Message, ChatRoom


def get_user_chats(user_chats, chat_id):
    this_chat = []
    chat_messages = []
    if user_chats and not chat_id:
        chat_id = user_chats.first().id
    if chat_id:
        this_chat = get_object_or_404(ChatRoom, id=chat_id)
        chat_messages = Message.objects.filter(chat_room=this_chat)
    return this_chat, chat_messages
