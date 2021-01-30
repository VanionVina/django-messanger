from django.urls import path

from mainapp.views import WelcomeView, RegistrationView, LoginView


app_name = 'mainapp'
urlpatterns =[
    path('', WelcomeView.as_view(), name='welcome'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login')
]