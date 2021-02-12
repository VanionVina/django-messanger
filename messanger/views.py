from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User

from messanger.forms import ConsumerUpdateProfile, ConsumerChangeAvatar, ChatRoomSettingsForm
from messanger.logic.user_change import change_user_avatar
from messanger.logic.chat_logic import get_user_chats, create_chate_room_message, create_new_chat_room, save_chat_settings
from messanger.models import Consumer, ChatRoom, Message
from .mixins import FriendsListMixin


class ChatRoomView(View):
    def get(self, request, **kwargs):
        chat_id = kwargs.get('chat_id')
        consumer = get_object_or_404(Consumer, user=request.user)
        user_chats = ChatRoom.objects.filter(users=request.user)
        this_chat, chat_messages = get_user_chats(user_chats, chat_id)
        context = {
            'consumer': consumer,
            'user_chats': user_chats,
            'this_chat': this_chat,
            'chat_messages': chat_messages,
        }
        return render(request, 'chat_room.html', context)
    
    def post(self, request, chat_id):
        create_chate_room_message(request, chat_id)
        chat = get_object_or_404(ChatRoom, id=chat_id)
        return HttpResponseRedirect(chat.get_absolute_url())


class FriendsView(FriendsListMixin, View):
    def get(self, request):
        context = {
                'friends': self.friends,
                }
        return render(request, 'friends.html', context)

    def post(self, request):
        context = {
            'friends': self.friends,
        }
        search_qwr = request.POST.get('search-friends')
        if search_qwr:
            searched = User.objects.filter(username__icontains=search_qwr)
            context['searched'] = searched
        return render(request, 'friends.html', context)


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


class ChangeProfile(View):
    def get(self, request):
        form = ConsumerUpdateProfile
        form_image = ConsumerChangeAvatar
        context = {
            'form': form,
            'form_image': form_image,
        }
        return render (request, 'user_profile_change.html', context)

    def post(self, request):
        form = ConsumerUpdateProfile(data=request.POST, user_t=request.user.username, user_id=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.user.consumer.get_absolute_url())
        return render(request, 'user_profile_change.html', context={'form': form})


class ChangeUserAvatar(View):
    def post(self, request):
        form = ConsumerChangeAvatar(request.POST, request.FILES)
        if form.is_valid():
            change_user_avatar(request.user, form)
            return HttpResponseRedirect(reverse('messanger:user_profile', kwargs={'user_id': request.user.id}))
        return render(request, 'user_profile_change.html', context={'form': form})


class CreateNewChat(View):
    def post(self, request):
        create_new_chat_room(request)
        return HttpResponseRedirect(reverse('messanger:chat_room'))


class ChatRoomSettings(View):
    def get(self, request, room_id):
        user_chats = ChatRoom.objects.filter(users=request.user)
        this_chat = get_object_or_404(ChatRoom, id=room_id)
        settings = ChatRoomSettingsForm
        context = {
            'user_chats': user_chats,
            'this_chat': this_chat,
            'settings': settings,
        }
        return render(request, 'chat_room_settings.html', context)

    def post(self, request, room_id):
        form = ChatRoomSettingsForm(request.POST)
        if form.is_valid():
            save_chat_settings(form, room_id)
            return HttpResponseRedirect(reverse('messanger:chat_room'))
        return render(request, 'chat_room_settings.html', context={'settings': form})


def delete_chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    room.delete()
    return HttpResponseRedirect(reverse('messanger:chat_room'))
