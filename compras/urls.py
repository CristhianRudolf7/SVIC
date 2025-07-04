from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.listaComprasView.as_view(), name='listaCompras'),
    path('crear/', views.crearCompraView, name='crearCompra'),
    path('<uuid:compra_id>/eliminar', views.eliminarCompraView.as_view(), name='eliminarCompra'),
    path('<uuid:compra_id>/detalle', views.detalleComprasView.as_view(), name='detalleCompra'),
    path('<uuid:compra_id>/pdf', views.pdfCompra, name='pdfCompra'),
    path('proveedores/', views.listaProveedoresView.as_view(), name='listaProveedores'),
    path('proveedores/crear/', views.crearProveedorView.as_view(), name='crearProveedor'),
    path('proveedores/<uuid:proveedor_id>/editar/', views.editarProveedorView.as_view(), name='editarProveedor'),
    path('proveedores/<uuid:proveedor_id>/eliminar/', views.eliminarProveedorView.as_view(), name='eliminarProveedor'),
    path('obtener-proveedores/', views.obtenerProveedores, name='obtenerProveedores'),
]
