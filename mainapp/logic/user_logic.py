from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from messanger.models import Consumer


def save_new_user(user_form, consumer_form):
    username = user_form.cleaned_data['username']
    passwd = user_form.cleaned_data['password']
    phone = consumer_form.cleaned_data['phone']
    birth = consumer_form.cleaned_data['birth']
    gender = consumer_form.cleaned_data['gender']
    user = User.objects.create(username=username)
    user.set_password(passwd)
    user.save()
    Consumer.objects.create(user=user, phone=phone, birth=birth, gender=gender)

def login_user(form, request):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)