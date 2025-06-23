from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('compras/', include('compras.urls')),
    path('inventario/', include('inventario.urls')),
    path('ventas/', include('ventas.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)