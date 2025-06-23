from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.listaVentasView.as_view(), name='listaVentas'),
    path('crear/', views.crearVentaView, name='crearVenta'),
    path('clientes/', views.listaClientesView.as_view(), name='listaClientes'),
    path('clientes/crear/', views.crearClienteView.as_view(), name='crearCliente'),
    path('clientes/<uuid:cliente_id>/editar/', views.editarClienteView.as_view(), name='editarCliente'),
    path('clientes/<uuid:cliente_id>/eliminar/', views.eliminarClienteView.as_view(), name='eliminarCliente'),
    path('obtener-clientes/', views.obtenerClientes, name='obtenerClientes')
]