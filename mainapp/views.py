from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse


from mainapp.logic.user_logic import save_new_user, login_user
from .forms import LoginForm, RegisterFormConsumer, RegistrationFormUser


class WelcomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('messanger:chat_room'))
        form = LoginForm
        context = {
            'form': form,
        }
        return render(request, 'welcome.html', context)
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login_user(form, request)
            return HttpResponseRedirect(reverse('messanger:chat_room'))
        return render(request, 'login.html', context={'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login_user(form, request)
            return HttpResponseRedirect(reverse('messanger:chat_room'))
        return render(request, 'login.html', context={'form': form})


class RegistrationView(View):

    def get(self, request):
        user_form = RegistrationFormUser
        consumer_form = RegisterFormConsumer
        context = {
            'user_form': user_form,
            'consumer_form': consumer_form,
        }
        return render(request, 'registration.html', context)
    
    def post(self, request):
        user_form = RegistrationFormUser(request.POST)
        consumer_form = RegisterFormConsumer(request.POST)
        if user_form.is_valid() and consumer_form.is_valid():
            save_new_user(user_form, consumer_form)
            messages.add_message(request, messages.INFO, 'Register, now log in')
            return HttpResponseRedirect(reverse('mainapp:login'))

        context = {
            'user_form': user_form,
            'consumer_form': consumer_form
        }
        return render(request, 'registration.html', context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('mainapp:welcome'))
