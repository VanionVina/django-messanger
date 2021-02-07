from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User

from messanger.forms import ConsumerUpdateProfile, ConsumerChangeAvatar
from messanger.logic.user_change import change_user_avatar
from messanger.models import Consumer


class ChatRoom(View):
    def get(self, request):
        consumer = get_object_or_404(Consumer, user=request.user)
        context = {
            'consumer': consumer,
        }
        return render(request, 'chat_room.html', context)


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
            return HttpResponseRedirect(reverse('messanger:user_profile', kwargs={'user_id': request.user.id}))
        return render(request, 'user_profile_change.html', context={'form': form})

class ChangeUserAvatar(View):
    def post(self, request):
        form = ConsumerChangeAvatar(request.POST, request.FILES)
        if form.is_valid():
            change_user_avatar(request.user, form)
            return HttpResponseRedirect(reverse('messanger:user_profile', kwargs={'user_id': request.user.id}))
        return render(request, 'user_profile_change.html', context={'form': form})

class FriendsView(View):
    def get(self, request):
        consumer = Consumer.objects.get(user=request.user)
        friends = consumer.friends.all()
        context = {
                'friends': friends,
                }
        return render(request, 'friends.html', context)
