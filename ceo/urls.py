from django.urls import path
from . import views

app_name = 'ceo'
urlpatterns = [
    path('', views.home, name='home'),
]