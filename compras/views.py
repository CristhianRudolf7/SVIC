import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Proveedores, Compras, DetalleCompra
from inventario.models import Productos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView, View
)

from .forms import proveedorForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_HALF_UP

class listaProveedoresView(LoginRequiredMixin, ListView):
    model = Proveedores
    template_name = "compras/listaProveedores.html"
    context_object_name = "proveedores"
    paginate_by = 10

    def get_queryset(self):
        return Proveedores.objects.filter(negocio=self.request.user.negocio)

class crearProveedorView(LoginRequiredMixin, CreateView):
    model = Proveedores
    template_name = 'compras/formProveedores.html'
    form_class = proveedorForm
    success_url = reverse_lazy('listaProveedores')

    def form_valid(self, form):
        form.instance.negocio = self.request.user.negocio
        return super().form_valid(form)

class editarProveedorView(LoginRequiredMixin, UpdateView):
    model = Proveedores
    template_name = 'compras/formProveedores.html'
    form_class = proveedorForm
    success_url = reverse_lazy('listaProveedores')
    pk_url_kwarg = 'proveedor_id'

class eliminarProveedorView(LoginRequiredMixin, View):
    def delete(self, request, proveedor_id):
        try:
            proveedor = Proveedores.objects.get(proveedor_id=proveedor_id)
            
            if proveedor.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar este proveedor'
                }, status=403)
            
            proveedor.delete()
            return JsonResponse({
                'success': True,
                'message': 'Proveedor eliminado correctamente'
            })
        except Proveedores.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El proveedor no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)

@login_required
def crearCompraView(request):
    context = {
        "proveedores": [proveedor for proveedor in Proveedores.objects.filter(negocio_id=request.user.negocio.negocio_id)]
    }

    if request.method == 'POST': 
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)

                atributos_compra = {
                    "negocio": request.user.negocio,
                    "proveedor": Proveedores.objects.get(proveedor_id=data['proveedor']),
                    "total": float(data["total"]),
                    "metodo_pago": data["metodo_pago"],
                    "estado_pago": data["estado_pago"],
                    "estado_envio": data["estado_envio"],
                }

                with transaction.atomic():
                    compra_nueva = Compras.objects.create(**atributos_compra)

                    productos = data["productos"]

                    for producto in productos:

                        producto_comprado = Productos.objects.get(producto_id=producto["producto_id"])

                        detalle_compra = {
                            "compra": compra_nueva,
                            "producto": producto_comprado,
                            "cantidad": int(producto["quantity"]),
                            "precio_unitario": producto_comprado.precio,
                            "subtotal": float(producto["total_product"])
                        }
                        DetalleCompra.objects.create(**detalle_compra)

                        producto_comprado.stock += int(producto["quantity"])
                        producto_comprado.save()

                return JsonResponse(
                    {
                        'status': 'success',
                        'message': 'Compra creada exitosamente',
                        'redirect': '/compras/'
                    }
                )
                
            except Exception as e:
                print(f'Errro: {str(e)}')
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': (
                            f'Errro: {str(e)}'
                        )
                    }, status=500)

    return render(request, "compras/crearCompra.html", context=context)

class listaComprasView(LoginRequiredMixin, ListView):
    model = Compras
    template_name = "compras/listaCompras.html"
    context_object_name = "compras"
    paginate_by = 10
    ordering = ['fecha']

    def get_queryset(self):
        return Compras.objects.filter(negocio=self.request.user.negocio)

class detalleComprasView(LoginRequiredMixin, DetailView):
    model = Compras
    template_name = "compras/detalleCompra.html"
    context_object_name = "detalles"
    pk_url_kwarg = 'compra_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles_compra'] = DetalleCompra.objects.filter(compra=self.object)
        context['igv'] = (self.object.total * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return context

@login_required
def pdfCompra(request, compra_id):
    negocio = request.user.negocio
    compra = Compras.objects.get(compra_id=compra_id)
    compra_detalle = DetalleCompra.objects.filter(compra_id=compra_id)
    proveedor = Proveedores.objects.get(proveedor_id=compra.proveedor.proveedor_id)

    data = {
        "nombre_proveedor": proveedor.nombre,
        "nombre_negocio": negocio.nombre,
        "direccion_proveedor": proveedor.direccion,
        "total": compra.total,
        "impuesto": (compra.total * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        "fecha_venta": compra.fecha.strftime('%d/%m/%Y %H:%M:%S'),
        "compra_detalle": compra_detalle,
    }
    return render(request, "ventas/pdfVenta.html", data)

class eliminarCompraView(LoginRequiredMixin, View):
    def delete(self, request, compra_id):
        try:
            compra = Compras.objects.get(compra_id=compra_id)
            
            if compra.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar esta compra'
                }, status=403)
            
            compra.delete()
            return JsonResponse({
                'success': True,
                'message': 'Compra eliminada correctamente'
            })
        except Compras.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La compra no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)

@csrf_exempt
@require_POST
@login_required
def obtenerProveedores(request):
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') and request.method == 'POST':
        term = request.POST.get('term', '')
        proveedores = Proveedores.objects.filter(
            name__icontains=term
        ).values('proveedor_id', 'nombre')
        lista_proveedores = list(proveedores)
        return JsonResponse(lista_proveedores, safe=False)
    return JsonResponse({'error': 'Método inválido'}, status=400)