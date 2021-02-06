from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from messanger.models import Consumer


def save_new_user(user_form, consumer_form):
    user = user_form.save()
    consumer = consumer_form.save(commit=False)
    consumer.user = user
    consumer.save()


def login_user(form, request):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)