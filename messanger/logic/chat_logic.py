from django.shortcuts import get_object_or_404

from messanger.models import Message, ChatRoom


def get_user_chats(user_chats, chat_id):
    this_chat = []
    chat_messages = []
    if user_chats and not chat_id:
        chat_id = user_chats.first().id
    if chat_id:
        this_chat = get_object_or_404(ChatRoom, id=chat_id)
        chat_messages = Message.objects.filter(chat_room=this_chat).order_by('-sended')
    return this_chat, chat_messages


def create_chate_room_message(request, chat_id):
    message_text = request.POST.get('sended-message')
    chat = get_object_or_404(ChatRoom, id=chat_id)
    if message_text:
        user = request.user
        Message.objects.create(from_user=user, chat_room=chat, text=message_text)


def create_new_chat_room(request):
    name = request.POST.get('chat_name')
    if name:
        chat = ChatRoom.objects.create(name=name)
        chat.users.add(request.user)
        chat.save()