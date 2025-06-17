from django.shortcuts import render, redirect
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView, View
)
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from usuarios.models import Usuarios, Negocios
from ventas.models import Ventas
from .models import Categorias, Productos, UnidadMedida
from .tables import ProductosTable, CategoriasTable, UnidadesTable
from .forms import ProductoForm, CategoriaForm
from django.http import JsonResponse
import json

@login_required
def dashboard(request):
    negocio = request.user.negocio
    usuarios = Usuarios.objects.filter(negocio=negocio)
    productos = Productos.objects.all()
    total_productos = (
        Productos.objects.all()
        .aggregate(Sum("stock"))
        .get("cantidad", 0.00)
    )
    cantidad_productos = productos.count()
    cantidad_usuarios = usuarios.count()

    context = {
        "productos": productos,
        "usuarios": usuarios,
        "cantidad_usuarios": cantidad_usuarios,
        "cantidad_productos": cantidad_productos,
        "total_productos": total_productos,
        "ventas": Ventas.objects.all(),
    }
    return render(request, "inventario/dashboard.html", context)

class ListaProductosViews(LoginRequiredMixin, ExportMixin, SingleTableView):
    model = Productos
    table_class = ProductosTable
    template_name = "inventario/listaProductos.html"
    context_object_name = "productos"
    paginate_by = 10
    SingleTableView.table_pagination = False

    def post(self, request):
        # Verificar si es una solicitud AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8'))
                nombre = data.get('nombre')
                descripcion = data.get('descripcion', '')
                precio = data.get('precio')
                stock = data.get('stock')
                fecha_expiracion = data.get('fecha_expiracion')
                foto = data.get('foto')
                codigo_barras = data.get('codigo_barras')
                
                # Validar que el nombre no esté vacío
                if not nombre:
                    return JsonResponse({
                        'success': False,
                        'message': 'El nombre es obligatorio'
                    }, status=400)
                
                nuevo_producto = Productos(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    stock=stock,
                    fecha_expiracion=fecha_expiracion,
                    foto=foto,
                    codigo_barras=codigo_barras,
                    negocio_id=request.user.negocio.negocio_id,
                    categoria_id="",
                    unidad_id=""
                )
                nuevo_producto.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Producto creada con éxito',
                    'producto': {
                        'producto_id': nuevo_producto.producto_id,
                        'nombre': nuevo_producto.nombre,
                        'categoria': nuevo_producto.categoria,
                        'precio': nuevo_producto.fecha_creacion,
                        'stock': nuevo_producto.stock,
                        "unidad": nuevo_producto.unidad
                    }
                })
            except Exception as e:
                print(f'Error al guardar: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Error al guardar: {str(e)}'
                }, status=500)
        else:
            # Si no es AJAX, mantener el comportamiento original
            return super().get(request)
        
class ProductoDetalleViews(LoginRequiredMixin, View):
    def put(self, request, categoria_id):
        try:
            data = json.loads(request.body.decode('utf-8'))
            categoria = Categorias.objects.get(categoria_id=categoria_id)
            if categoria.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para modificar esta categoria'
                }, status=403)
            
            categoria.nombre = data.get('nombre')
            categoria.descripcion = data.get('descripcion', '')
            
            categoria.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Categoria actualizada correctamente',
                'categoria': {
                    'categoria_id': categoria.categoria_id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'fecha_creacion': categoria.fecha_creacion
                }
            })
        except Categorias.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Categoria no encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        
    def get(self, request, categoria_id):
        try:
            categoria = Categorias.objects.get(categoria_id=categoria_id)
            return JsonResponse({
                'success': True,
                'categoria': {
                    'categoria_id': categoria.categoria_id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'fecha_creacion': categoria.fecha_creacion
                }
            })
        except Categorias.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Categoria no encontrada'
            }, status=404)
        
    def delete(self, request, categoria_id):
        try:
            categoria = Categorias.objects.get(categoria_id=categoria_id)
            
            # Verificar que la categoría pertenece al negocio del usuario
            if categoria.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar esta categoría'
                }, status=403)
            
            categoria.delete()
            return JsonResponse({
                'success': True,
                'message': 'Categoría eliminada correctamente'
            })
        except Categorias.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La categoría no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)

class ListaCategoriasViews(LoginRequiredMixin, ExportMixin, SingleTableView):
    model = Categorias
    table_class = CategoriasTable
    template_name = "inventario/listaCategorias.html"
    context_object_name = "categorias"
    paginate_by = 10
    SingleTableView.table_pagination = False
    
    def post(self, request):
        # Verificar si es una solicitud AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8'))
                nombre = data.get('nombre')
                descripcion = data.get('descripcion', '')
                
                # Validar que el nombre no esté vacío
                if not nombre:
                    return JsonResponse({
                        'success': False,
                        'message': 'El nombre es obligatorio'
                    }, status=400)
                
                nueva_categoria = Categorias(
                    nombre=nombre,
                    descripcion=descripcion,
                    negocio_id=request.user.negocio.negocio_id
                )
                nueva_categoria.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Categoría creada con éxito',
                    'categoria': {
                        'id': nueva_categoria.categoria_id,
                        'nombre': nueva_categoria.nombre,
                        'descripcion': nueva_categoria.descripcion,
                        'fecha_creacion': nueva_categoria.fecha_creacion
                    }
                })
            except Exception as e:
                print(f'Error al guardar: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Error al guardar: {str(e)}'
                }, status=500)
        else:
            # Si no es AJAX, mantener el comportamiento original
            return super().get(request)
        
class CategoriaDetalleViews(LoginRequiredMixin, View):
    def put(self, request, categoria_id):
        try:
            data = json.loads(request.body.decode('utf-8'))
            categoria = Categorias.objects.get(categoria_id=categoria_id)
            if categoria.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para modificar esta categoria'
                }, status=403)
            
            categoria.nombre = data.get('nombre')
            categoria.descripcion = data.get('descripcion', '')
            
            categoria.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Categoria actualizada correctamente',
                'categoria': {
                    'categoria_id': categoria.categoria_id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'fecha_creacion': categoria.fecha_creacion
                }
            })
        except Categorias.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Categoria no encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        
    def get(self, request, categoria_id):
        try:
            categoria = Categorias.objects.get(categoria_id=categoria_id)
            return JsonResponse({
                'success': True,
                'categoria': {
                    'categoria_id': categoria.categoria_id,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'fecha_creacion': categoria.fecha_creacion
                }
            })
        except Categorias.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Categoria no encontrada'
            }, status=404)
        
    def delete(self, request, categoria_id):
        try:
            categoria = Categorias.objects.get(categoria_id=categoria_id)
            
            # Verificar que la categoría pertenece al negocio del usuario
            if categoria.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar esta categoría'
                }, status=403)
            
            categoria.delete()
            return JsonResponse({
                'success': True,
                'message': 'Categoría eliminada correctamente'
            })
        except Categorias.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La categoría no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)
        
class ListaUnidadesViews(LoginRequiredMixin, ExportMixin, SingleTableView):
    model = UnidadMedida
    table_class = UnidadesTable
    template_name = "inventario/listaUnidad.html"
    context_object_name = "unidades"
    paginate_by = 10
    SingleTableView.table_pagination = False
    
    def post(self, request):
        # Verificar si es una solicitud AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8'))
                nombre = data.get('nombre')
                simbolo = data.get('simbolo', '')
                
                # Validar que el nombre no esté vacío
                if not nombre:
                    return JsonResponse({
                        'success': False,
                        'message': 'El nombre es obligatorio'
                    }, status=400)
                
                nueva_unidad = UnidadMedida(
                    nombre=nombre,
                    simbolo=simbolo,
                    negocio_id=request.user.negocio.negocio_id
                )
                nueva_unidad.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Unidad creada con éxito',
                    'unidad': {
                        'id': nueva_unidad.unidad_id,
                        'nombre': nueva_unidad.nombre,
                        'simbolo': nueva_unidad.simbolo,
                        'fecha_creacion': nueva_unidad.fecha_creacion
                    }
                })
            except Exception as e:
                print(f'Error al guardar: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'message': f'Error al guardar: {str(e)}'
                }, status=500)
        else:
            # Si no es AJAX, mantener el comportamiento original
            return super().get(request)
        
class UnidadDetalleViews(LoginRequiredMixin, View):
    def put(self, request, unidad_id):
        try:
            data = json.loads(request.body.decode('utf-8'))
            unidad = UnidadMedida.objects.get(unidad_id=unidad_id)
            if unidad.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para modificar esta unidad'
                }, status=403)
            
            unidad.nombre = data.get('nombre')
            unidad.simbolo = data.get('simbolo', '')
            
            unidad.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Unidad actualizada correctamente',
                'unidad': {
                    'unidad_id': unidad.unidad_id,
                    'nombre': unidad.nombre,
                    'simbolo': unidad.simbolo,
                    'fecha_creacion': unidad.fecha_creacion
                }
            })
        except UnidadMedida.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Unidad no encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        
    def get(self, request, unidad_id):
        try:
            unidad = UnidadMedida.objects.get(unidad_id=unidad_id)
            return JsonResponse({
                'success': True,
                'unidad': {
                    'unidad_id': unidad.unidad_id,
                    'nombre': unidad.nombre,
                    'simbolo': unidad.simbolo,
                    'fecha_creacion': unidad.fecha_creacion
                }
            })
        except UnidadMedida.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Unidad no encontrada'
            }, status=404)
        
    def delete(self, request, unidad_id):
        try:
            unidad = UnidadMedida.objects.get(unidad_id=unidad_id)
            
            # Verificar que la categoría pertenece al negocio del usuario
            if unidad.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar esta unidad'
                }, status=403)
            
            unidad.delete()
            return JsonResponse({
                'success': True,
                'message': 'Unidad eliminada correctamente'
            })
        except UnidadMedida.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La unidad no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)
    