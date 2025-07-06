from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.chatView, name='chat'),
    path('api/', views.chatApi, name='chat_api'),
]