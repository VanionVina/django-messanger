from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User

from messanger.forms import (
        ConsumerUpdateProfile, ConsumerChangeAvatar,
        ChatRoomSettingsForm, ChatRoomChangeAvatar
        )
from messanger.logic.user_change import change_user_avatar
from messanger.logic.chat_logic import (
        get_user_chats,
        create_new_chat_room, save_chat_settings,
        save_chat_image
        )
from messanger.models import Consumer, ChatRoom, AddToFriendNotification
from .mixins import FriendsListMixin, NotificationsMixin


class ChatRoomView(NotificationsMixin, View):
    def get(self, request, **kwargs):
        chat_id = kwargs.get('chat_id')
        consumer = get_object_or_404(Consumer, user=request.user)
        user_chats = ChatRoom.objects.filter(users=request.user)
        this_chat, chat_messages = get_user_chats(user_chats, chat_id)
        if this_chat:
            if request.user not in this_chat.users.all():
                return HttpResponseRedirect(reverse('messanger:chat_room'))
        context = {
            'consumer': consumer,
            'user_chats': user_chats,
            'this_chat': this_chat,
            'chat_messages': chat_messages,
        }
        context.update(self.context_notif)
        return render(request, 'chat_room.html', context)

    # def post(self, request, chat_id):
    #     create_chate_room_message(request, chat_id)
    #     chat = get_object_or_404(ChatRoom, id=chat_id)
    #     return HttpResponseRedirect(chat.get_absolute_url())


class FriendsView(FriendsListMixin, NotificationsMixin, View):
    def get(self, request):
        context = {
                'friends': self.friends,
                }
        context.update(self.context_notif)
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


class UserProfile(NotificationsMixin, View):
    def get(self, request, user_id):
        user_c = get_object_or_404(User, id=user_id)
        sended_requests_to_friends_users = [notif.send_to for notif in self.notifications]
        sended_requests_to_me_users = [notif.send_from for notif in self.notif_to_me]
        context = {
            'user_c': user_c,
            'sended_requests_to_friends': sended_requests_to_friends_users,
            'sended_request_to_me_users': sended_requests_to_me_users,
        }
        context.update(self.context_notif)
        return render(request, 'user_profile.html', context)


class ChangeProfile(NotificationsMixin, View):
    def get(self, request):
        form = ConsumerUpdateProfile
        form_image = ConsumerChangeAvatar
        context = {
            'form': form,
            'form_image': form_image,
        }
        context.update(self.context_notif)
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


class ChatRoomSettings(NotificationsMixin, View):
    def get(self, request, room_id):
        user_chats = ChatRoom.objects.filter(users=request.user)
        this_chat = get_object_or_404(ChatRoom, id=room_id)
        settings = ChatRoomSettingsForm
        change_image = ChatRoomChangeAvatar
        context = {
            'user_chats': user_chats,
            'this_chat': this_chat,
            'settings': settings,
            'change_image': change_image,
        }
        context.update(self.context_notif)
        return render(request, 'chat_room_settings.html', context)

    def post(self, request, room_id):
        form = ChatRoomSettingsForm(request.POST)
        if form.is_valid():
            save_chat_settings(form, room_id)
            return HttpResponseRedirect(reverse('messanger:chat_room'))
        return render(request, 'chat_room_settings.html', context={'settings': form})


class ChatRoomChangeImage(View):
    def post(self, request, room_id):
        form = ChatRoomChangeAvatar(request.POST, request.FILES)
        if form.is_valid():
            save_chat_image(form, room_id)
            return HttpResponseRedirect(reverse('messanger:chat_room_settings', kwargs={'room_id': room_id}))
        return render(request, 'chat_room_settings.html', context={'settings': form})


def delete_chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    room.delete()
    return HttpResponseRedirect(reverse('messanger:chat_room'))


class AddFriendToChatView(NotificationsMixin, View):
    def get(self, request, room_id):
        chat = get_object_or_404(ChatRoom, id=room_id)
        friends = request.user.consumer.friends.all()
        context = {
            'friends': friends,
            'chat': chat,
        }
        context.update(self.context_notif)
        return render(request, 'add_friend_to_chat.html', context)


def add_friend_to_chat(request, friend_id, room_id):
    chat = get_object_or_404(ChatRoom, id=room_id)
    friend = get_object_or_404(Consumer, id=friend_id)
    chat.users.add(friend.user)
    chat.save()
    return HttpResponseRedirect(reverse('messanger:add_friend_to_chat', kwargs={'room_id': chat.id}))


def give_moderator_priveleges(requets, user_id, room_id):
    chat = get_object_or_404(ChatRoom, id=room_id)
    user = get_object_or_404(User, id=user_id)
    chat.moderators.add(user)
    chat.save()
    return HttpResponseRedirect(reverse('messanger:chat_room_settings', kwargs={'room_id': room_id}))


def kick_user_from_room(request, user_id, room_id):
    chat = get_object_or_404(ChatRoom, id=room_id)
    user = get_object_or_404(User, id=user_id)
    if user in chat.moderators.all():
        chat.moderators.remove(user)
    chat.users.remove(user)
    chat.save()
    return HttpResponseRedirect(reverse('messanger:add_friend_to_chat', kwargs={'room_id': room_id}))


def send_friend_request(request, from_user_id, to_user_id):
    send_from = get_object_or_404(User, id=from_user_id)
    send_to = get_object_or_404(User, id=to_user_id)
    AddToFriendNotification.objects.create(send_from=send_from, send_to=send_to)
    return HttpResponseRedirect(reverse('messanger:chat_room'))


def answer_to_friend_request(request, notification_id, answer):
    notification = get_object_or_404(AddToFriendNotification, id=notification_id)
    notification.agreed = answer
    notification.save()
    print(answer, type(answer))
    if answer == 'True':
        from_user = notification.send_from
        request.user.consumer.friends.add(from_user.consumer)
        from_user.consumer.friends.add(request.user.consumer)
    return HttpResponseRedirect('/')


def delete_notification(request, notification_id):
    notification = get_object_or_404(AddToFriendNotification, id=notification_id)
    notification.delete()
    return HttpResponseRedirect('/')


def delete_friend(request, friend_id):
    friend = get_object_or_404(Consumer, id=friend_id)
    request.user.consumer.friends.remove(friend)
    friend.friends.remove(request.user.consumer)
    return HttpResponseRedirect(reverse('messanger:friends'))
