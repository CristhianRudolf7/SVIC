# ceo/urls.py
from django.urls import path
from . import views # Asegúrate de crear views.py en la app ceo

app_name = 'ceo' # Define el namespace

urlpatterns = [
    # Define una URL para la vista principal de CEO
    path('', views.dashboard_ceo, name='dashboard'),
    # Otras URLs específicas de CEO...
]