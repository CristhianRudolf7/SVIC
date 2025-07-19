from django.urls import path
from django.http import HttpResponse
from inventario import views as inventario_views
from .views import (
    ListaProductosViews, ListaCategoriasViews, CategoriaDetalleViews, 
    ListaUnidadesViews, UnidadDetalleViews, ProductoDetalleViews, obtenerProductos, dashboard_data
)

urlpatterns = [
    path('', inventario_views.dashboard, name='dashboard'),
    path('productos/', ListaProductosViews.as_view(), name='listaProductos'),
    path('productos/<uuid:producto_id>/', ProductoDetalleViews.as_view(), name='metodosProductos'),
    path('categorias/', ListaCategoriasViews.as_view(), name='listaCategorias'),
    path('categorias/<uuid:categoria_id>/', CategoriaDetalleViews.as_view(), name='metodosCategorias'),
    path('unidades/', ListaUnidadesViews.as_view(), name='listaUnidades'),
    path('unidades/<uuid:unidad_id>/', UnidadDetalleViews.as_view(), name='metodosUnidades'),
    path('api/dashboard-data/', dashboard_data, name='dashboard-data'),
    path('obtener-productos/', obtenerProductos, name='obtenerProductos')
]