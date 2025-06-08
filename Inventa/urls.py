from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('compras/', include('compras.urls')),
    path('inventario/', include('inventario.urls')),
    path('ventas/', include('ventas.urls'))
]
