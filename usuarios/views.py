# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # AuthenticationForm valida usuario/contraseña
            # Obtiene el usuario autenticado del formulario
            user = form.get_user()

            # Inicia sesión al usuario
            login(request, user)
            messages.success(request, f"Bienvenido, {user.nombre}")

            # Redirigir basado en el rol
            return redirect_based_on_role(user)
        else:
            # Mensaje de error si el formulario no es válido (credenciales incorrectas)
            messages.error(request, "DNI o contraseña incorrectos.")
    else:
        # Si es GET, muestra el formulario vacío
        form = AuthenticationForm()

    # Renderiza la plantilla de login con el formulario
    return render(request, 'login.html', {'form': form})

def redirect_based_on_role(user):
    # Lógica de redirección basada en el campo 'rol'
    if user.rol == 1:
        # Redirigir a la vista principal de CEO
        # Asegúrate de tener una URL nombrada 'dashboard' en ceo/urls.py
        return redirect(reverse('ceo:dashboard')) # Ejemplo: 'nombre_app:nombre_url'
    elif user.rol == 2:
        # Redirigir a la vista principal de Administrador
        return redirect(reverse('administrador:dashboard'))
    elif user.rol == 3:
        # Redirigir a la vista principal de Inventario
        return redirect(reverse('inventario:dashboard'))
    elif user.rol == 4:
        # Redirigir a la vista principal de Ventas
        return redirect(reverse('ventas:dashboard'))
    else:
        # Rol desconocido o no asignado, redirigir a una página por defecto o de error
        # O quizás al perfil del usuario si tienes uno
        messages.warning(user.request, "Rol no definido, contacte al administrador.")
        # Podrías redirigir a una vista de perfil o a la misma página de login
        return redirect('/') # O a una URL específica de 'perfil'

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect(reverse('login')) # Redirige a la URL nombrada 'login'