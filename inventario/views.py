from django.shortcuts import render, redirect
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView, View
)
from django_tables2 import SingleTableView
from django.views.decorators.csrf import csrf_exempt
import django_tables2 as tables
from django.views.decorators.http import require_POST
from django_tables2.export.views import ExportMixin
from usuarios.models import Usuarios, Negocios
from .models import Categorias, Productos, UnidadMedida
from .tables import ProductosTable, CategoriasTable, UnidadesTable
from ventas.models import Ventas, DetalleVentas
from inventario.models import Productos, MovimientosInventario, Alertas
from .forms import ProductoForm, CategoriaForm
from django.http import JsonResponse
import json
from compras.models import Compras
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.db.models.functions import TruncDate

@login_required
def dashboard(request):
    negocio = request.user.negocio
    ventas = Ventas.objects.filter(negocio=negocio)
    compras = Compras.objects.filter(negocio=negocio)
    productos = Productos.objects.filter(negocio=negocio)
    inventario = MovimientosInventario.objects.filter(negocio=negocio)
    alertas = Alertas.objects.filter(negocio=negocio, estado='PN')
    total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
    total_compras = compras.aggregate(total=Sum('total'))['total'] or 0
    productos_bajo_stock = productos.filter(stock__lte=5).count()
    productos_total = productos.count()
    alertas_pendientes = alertas.count()
    ventas_mes_actual = ventas.filter(fecha__month=now().month).aggregate(total=Sum('total'))['total'] or 0

    hoy = timezone.localdate()
    hace_30_dias = hoy - timedelta(days=30)

    cantidad_ventas = Ventas.objects.filter(negocio=negocio).count()
    ventas_actual = Ventas.objects.filter(
        negocio=negocio,
        fecha__lte=hoy
    ).count()
    ventas_anterior = Ventas.objects.filter(
        negocio=negocio,
        fecha__lte=hace_30_dias
    ).count()
    if ventas_anterior > 0:
        porcentaje_ventas = ((ventas_actual - ventas_anterior) / ventas_anterior) * 100
    else:
        porcentaje_ventas = 0

    cantidad_empleados = Usuarios.objects.filter(negocio=negocio, rol='Trabajador').count()
    empleados_actual = Usuarios.objects.filter(
        negocio=negocio,
        rol='Trabajador',
        fecha_creacion__lte=hoy
    ).count()
    empleados_periodo_anterior = Usuarios.objects.filter(
        negocio=negocio,
        rol='Trabajador',
        fecha_creacion__lte=hace_30_dias
    ).count()
    if empleados_periodo_anterior > 0:
        porcentaje_empleados = ((empleados_actual - empleados_periodo_anterior) / empleados_periodo_anterior) * 100
    else:
        porcentaje_empleados = 0

    hace_15_dias = hoy - timedelta(days=14)
    ventas = (
        Ventas.objects
        .filter(fecha__date__range=(hace_15_dias, hoy))
        .annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(cantidad=Count('venta_id'))
    )
    ventas_dict = {v['dia']: v['cantidad'] for v in ventas}
    lista_cantidades = [
        ventas_dict.get(hace_15_dias + timedelta(days=i), 0)
        for i in range(15)
    ]

    context = {
        "total_ventas": total_ventas,
        "total_compras": total_compras,
        "productos_total": productos_total,
        "productos_bajo_stock": productos_bajo_stock,
        "alertas_pendientes": alertas_pendientes,
        "ventas_mes_actual": ventas_mes_actual,
        "cantidad_empleados": cantidad_empleados,
        "cantidad_ventas": cantidad_ventas,
        "porcentaje_empleados": {'porcentaje': abs(round(porcentaje_empleados, 2)),
                                            'signo': 'P' if porcentaje_empleados >= 0 else 'N'},
        "porcentaje_ventas": {'porcentaje': abs(round(porcentaje_ventas, 2)),
                                            'signo': 'P' if porcentaje_ventas >= 0 else 'N'},
        "ventas_dia": lista_cantidades
    }
    print(lista_cantidades)
    return render(request, "inventario/dashboard.html", context)

class ListaProductosViews(LoginRequiredMixin, ExportMixin, SingleTableView):
    model = Productos
    table_class = ProductosTable
    template_name = "inventario/listaProductos.html"
    context_object_name = "productos"
    paginate_by = 10
    SingleTableView.table_pagination = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        negocio_id = self.request.user.negocio.negocio_id
        
        context['categorias'] = Categorias.objects.filter(negocio_id=negocio_id)
        context['unidades'] = UnidadMedida.objects.filter(negocio_id=negocio_id)
        return context
    
    def get_queryset(self):
        return Productos.objects.filter(negocio=self.request.user.negocio)
    
    def post(self, request):
        # Verificar si es una solicitud AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body.decode('utf-8'))
                negocio_id = request.user.negocio.negocio_id
                nombre = data.get('nombre')
                # Validar que el nombre no esté vacío
                if not nombre:
                    return JsonResponse({
                        'success': False,
                        'message': 'El nombre es obligatorio'
                    }, status=400)
                
                descripcion = data.get('descripcion', '')
                precio = data.get('precio')
                stock = data.get('stock')
                fecha_expiracion = data.get('fecha_expiracion')
                codigo_barras = data.get('codigo_barras')
                categoria_id = data.get('categoria_id')
                try:
                    categoria = Categorias.objects.get(
                        categoria_id=categoria_id,
                        negocio_id=negocio_id
                    )
                except Categorias.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'Categoría inválida o no pertenece a tu negocio'
                    }, status=400)
                
                unidad_id = data.get('unidad_id')
                unidad = None
                if unidad_id:
                    try:
                        unidad = UnidadMedida.objects.get(
                            unidad_id=unidad_id,
                            negocio_id=negocio_id
                        )
                    except UnidadMedida.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'message': 'Unidad inválida o no pertenece a tu negocio'
                        }, status=400)
                    
                nuevo_producto = Productos(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    stock=stock,
                    fecha_expiracion=fecha_expiracion if fecha_expiracion else None,
                    codigo_barras=codigo_barras,
                    negocio_id=request.user.negocio.negocio_id,
                    categoria_id=categoria.categoria_id,
                    unidad_id=unidad.unidad_id if unidad else None
                )
                nuevo_producto.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Producto creada con éxito',
                    'producto': {
                        'producto_id': nuevo_producto.producto_id,
                        'nombre': nuevo_producto.nombre,
                        'categoria': nuevo_producto.categoria.nombre if nuevo_producto.categoria else '',
                        'categoria_id': nuevo_producto.categoria.categoria_id if nuevo_producto.categoria else '',
                        'precio': nuevo_producto.precio,
                        'stock': nuevo_producto.stock,
                        'unidad': nuevo_producto.unidad.nombre if nuevo_producto.unidad else '',
                        'unidad_id': nuevo_producto.unidad.unidad_id if nuevo_producto.unidad else ''
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
    def put(self, request, producto_id):
        try:
            data = json.loads(request.body.decode('utf-8'))
            producto = Productos.objects.get(producto_id=producto_id)
            if producto.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para modificar este producto'
                }, status=403)
            
            producto.nombre = data.get('nombre')
            producto.descripcion = data.get('descripcion')
            categoria_id = data.get('categoria_id')
            if categoria_id:
                producto.categoria = Categorias.objects.get(categoria_id=categoria_id)
            producto.precio = data.get('precio')
            producto.stock = data.get('stock')
            producto.fecha_expiracion = data.get('fecha_expiracion') if data.get('fecha_expiracion') else None
            producto.unidad = data.get('unidad')
            unidad_id = data.get('unidad_id')
            if unidad_id:
                producto.unidad = UnidadMedida.objects.get(unidad_id=unidad_id)
            producto.codigo_barras = data.get('codigo_barras')
            
            producto.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Producto actualizado correctamente',
                'producto': {
                    'producto_id': producto.producto_id,
                    'nombre': producto.nombre,
                    'categoria': producto.categoria.nombre if producto.categoria else '',
                    'precio': producto.precio,
                    'stock': producto.stock,
                    'unidad': producto.unidad.nombre if producto.unidad else '',
                }
            })
        except Productos.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Producto no encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
        
    def get(self, request, producto_id):
        try:
            producto = Productos.objects.get(
                producto_id=producto_id,
                negocio=request.user.negocio.negocio_id
            )
            return JsonResponse({
                'success': True,
                'message': 'Producto actualizado correctamente',
                'producto': {
                    'producto_id': producto.producto_id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'categoria_id': producto.categoria.categoria_id if producto.categoria else '',
                    'precio': producto.precio,
                    'stock': producto.stock,
                    'codigo_barras': producto.codigo_barras,
                    'fecha_expiracion': producto.fecha_expiracion,
                    'unidad_id': producto.unidad.unidad_id if producto.unidad else None
                }
            })
        except Productos.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Producto no encontrada'
            }, status=404)
        
    def delete(self, request, producto_id):
        try:
            producto = Productos.objects.get(producto_id=producto_id)
            
            # Verificar que la categoría pertenece al negocio del usuario
            if producto.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar este producto'
                }, status=403)
            
            producto.delete()
            return JsonResponse({
                'success': True,
                'message': 'Producto eliminado correctamente'
            })
        except Productos.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El producto no existe'
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

    def get_queryset(self):
        return Categorias.objects.filter(negocio=self.request.user.negocio)
    
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

    def get_queryset(self):
        return UnidadMedida.objects.filter(negocio=self.request.user.negocio)
    
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
    
@csrf_exempt
@require_POST
@login_required
def obtenerProductos(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            term = request.POST.get("term", "")
            data = []

            productos = Productos.objects.filter(nombre__icontains=term, negocio=request.user.negocio)
            for producto in productos[:10]:
                data.append(producto.to_json())

            return JsonResponse(data, safe=False)
        except Exception as e:
            print(f'Error al obtener productos: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No es un request AJAX'}, status=400)