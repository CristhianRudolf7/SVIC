# ceo/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy # Para usar en decoradores

# Función para verificar si el usuario es CEO (rol 1)
def es_ceo(user):
    # Comprueba si está autenticado Y si tiene el atributo rol Y si el rol es 1
    return user.is_authenticated and hasattr(user, 'rol') and user.rol == 1

# Decoradores para proteger la vista:
# 1. @login_required: Asegura que el usuario esté logueado.
#    Si no lo está, redirige a la URL especificada en login_url.
# 2. @user_passes_test: Ejecuta la función es_ceo.
#    Si devuelve False, redirige a la URL especificada en login_url.
@login_required(login_url=reverse_lazy('usuarios:login')) # Usa la URL nombrada del login
@user_passes_test(es_ceo, login_url=reverse_lazy('usuarios:login')) # Redirige al login si no es CEO
def dashboard_ceo(request):
    """Vista para el panel de control del CEO."""
    # Aquí puedes obtener datos específicos que el CEO necesita ver
    context = {
        'nombre_usuario': request.user.nombre,
        # Pasa más datos al contexto si es necesario
        # 'total_ventas': obtener_total_ventas(),
        # 'nuevos_clientes': obtener_nuevos_clientes(),
    }
    # Renderiza la plantilla del dashboard del CEO
    return render(request, 'ceo/dashboard.html', context)

# Puedes añadir más vistas protegidas para CEO aquí
# @login_required(login_url=reverse_lazy('usuarios:login'))
# @user_passes_test(es_ceo, login_url=reverse_lazy('usuarios:login'))
# def ver_reportes(request):
#     # ... lógica para reportes ...
#     return render(request, 'ceo/reportes.html')