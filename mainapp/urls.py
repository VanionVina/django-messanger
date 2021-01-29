from django.urls import path

from mainapp.views import WelcomeView


urlpatterns =[
    path('', WelcomeView.as_view(), name='welcome'),
]