# ceo/views.py (Ejemplo básico)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Decorador para verificar el rol
def es_ceo(user):
    return user.is_authenticated and user.rol == 1

@login_required(login_url='/') # Redirige a login si no está autenticado
@user_passes_test(es_ceo, login_url='/') # Redirige si no es CEO
def dashboard_ceo(request):
    # Lógica de la vista para CEO
    return render(request, 'ceo/dashboard.html') # Crea esta plantilla