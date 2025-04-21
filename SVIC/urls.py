from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("super-admin/", admin.site.urls),
    path('ceo/', include('ceo.urls')),
    path('', include('usuarios.urls')),
    path('administrador/', include('administrador.urls')),
    path('inventario/', include('inventario.urls')),
    path('ventas/', include('ventas.urls')),
]