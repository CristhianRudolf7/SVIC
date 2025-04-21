# usuarios/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView

app_name = 'usuarios'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
]