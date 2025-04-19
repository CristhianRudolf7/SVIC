# mi_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Importa las vistas de login/logout directamente aquí porque el login es la raíz
from usuarios.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Login/Logout ---
    # La URL raíz ('') apunta directamente a la vista de login
    path('', login_view, name='login'), # Nombrar la URL es buena práctica
    path('logout/', logout_view, name='logout'),

    # --- Apps por Rol ---
    # Incluye las URLs de tus otras apps con prefijos
    # El namespace permite usar reverse('ceo:dashboard')
    path('ceo/', include('ceo.urls', namespace='ceo')),
    path('administrador/', include('administrador.urls', namespace='administrador')),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    # Agrega otras apps aquí...

]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)