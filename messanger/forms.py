from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django import forms

from messanger.models import Consumer, ChatRoom


class ConsumerUpdateProfile(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = Consumer
        exclude = ['avatar', 'user', 'friends']
        widgets = {
            'birth': forms.TextInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, user_t='', user_id='', **kwargs):
        self.user_username = user_t
        self.user_id = user_id
        super(ConsumerUpdateProfile, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        if username == self.user_username:
            pass
        else:
            test_existing_user = User.objects.filter(username=username).first()
            if test_existing_user:
                raise forms.ValidationError('This username is not available')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        birth = self.cleaned_data['birth']
        gender = self.cleaned_data['gender']

        user = User.objects.get(id=self.user_id)
        consumer = Consumer.objects.get(user=user)

        user.username = username
        user.email = email
        consumer.phone = phone
        consumer.birth = birth
        consumer.gender = gender
        user.save()
        consumer.save()


class ConsumerChangeAvatar(forms.Form):
    avatar = forms.ImageField()


class ChatRoomSettingsForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        exclude = ['users', ]


class ChatRoomChangeAvatar(forms.Form):
    image = forms.ImageField()
