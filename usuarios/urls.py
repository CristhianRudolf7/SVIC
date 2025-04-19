# usuarios/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import custom_login

app_name = 'usuarios'
urlpatterns = [
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]