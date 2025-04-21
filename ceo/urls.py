# ceo/urls.py
from django.urls import path
from . import views # Asegúrate de crear views.py en la app ceo

app_name = 'ceo' # Define el namespace

urlpatterns = [
    path('', views.dashboard_ceo, name='dashboard'),
]