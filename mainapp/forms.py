from django.contrib.auth.models import User
from django import forms

from messanger.models import Consumer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Wrong username {username}') 
        if not user.check_password(password):
            raise forms.ValidationError('Wrong password')
        return self.cleaned_data


class RegisterFormConsumer(forms.ModelForm):

    class Meta:
        model = Consumer
        exclude = ('user', 'friends')
        widgets = {
            'birth': forms.TextInput(attrs={'type': 'date'}),
        }


class RegistrationFormUser(forms.ModelForm):

    confirm_passwd = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        username = self.cleaned_data['username']
        passwd = self.cleaned_data['password']
        confirm_passwd = self.cleaned_data['confirm_passwd']
        check = User.objects.filter(username=username).first()
        if check:
            raise forms.ValidationError('This username is taken')
        if passwd != confirm_passwd:
            raise forms.ValidationError('Passwords don\'t math')
        return self.cleaned_data
    
    def save(self):
        username = self.cleaned_data['username']
        passwd = self.cleaned_data['password']
        email = self.cleaned_data['email']
        user = User.objects.create(username=username, email=email)
        user.set_password(passwd)
        user.save()
        return user
