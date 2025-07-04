import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Clientes, Ventas, DetalleVentas
from inventario.models import Productos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView, View
)

from .forms import clienteForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_HALF_UP

@login_required
def crearVentaView(request):
    context = {
        "clientes": [cliente for cliente in Clientes.objects.filter(negocio_id=request.user.negocio.negocio_id)]
    }

    if request.method == 'POST':
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                print(f'DATA: {data}')

                atributos_venta = {
                    "negocio": request.user.negocio,
                    "usuario": request.user,
                    "cliente": Clientes.objects.get(cliente_id=data['cliente']),
                    "total": float(data["total"]),
                    "metodo_pago": data["metodo_pago"],
                    "estado_pago": data["estado_pago"],
                    "estado_envio": data["estado_envio"],
                    "venta_numero": int(request.user.negocio.numero_ventas) + 1,
                }

                with transaction.atomic():
                    venta_nueva = Ventas.objects.create(**atributos_venta)

                    productos = data["productos"]

                    for producto in productos:

                        producto_vendido = Productos.objects.get(producto_id=producto["producto_id"])
                        if producto_vendido.stock < int(producto["quantity"]):
                            raise ValueError(f"No hay suficiente estock para el producto: {producto_vendido.nombre}")

                        detalle_venta = {
                            "venta": venta_nueva,
                            "producto": producto_vendido,
                            "cantidad": int(producto["quantity"]),
                            "precio_unitario": producto_vendido.precio,
                            "subtotal": float(producto["total_product"])
                        }
                        DetalleVentas.objects.create(**detalle_venta)

                        producto_vendido.stock -= int(producto["quantity"])
                        producto_vendido.save()

                return JsonResponse(
                    {
                        'status': 'success',
                        'message': 'Venta creada exitosamente',
                        'redirect': '/ventas/'
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

    return render(request, "ventas/crearVenta.html", context=context)

class listaVentasView(LoginRequiredMixin, ListView):
    model = Ventas
    template_name = "ventas/listaVentas.html"
    context_object_name = "ventas"
    paginate_by = 10
    ordering = ['fecha']

    def get_queryset(self):
        return Ventas.objects.filter(negocio=self.request.user.negocio)

class detalleVentaView(LoginRequiredMixin, DetailView):
    model = Ventas
    template_name = "ventas/detalleVenta.html"
    context_object_name = "detalles"
    pk_url_kwarg = 'venta_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles_venta'] = DetalleVentas.objects.filter(venta=self.object)
        context['igv'] = (self.object.total * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return context

@login_required
def pdf(request, venta_id):
    negocio = request.user.negocio
    venta = Ventas.objects.get(venta_id=venta_id)
    venta_detalle = DetalleVentas.objects.filter(venta_id=venta_id)

    data = {
        "nombre_negocio": negocio.nombre,
        "direccion_negocio": negocio.direccion,
        "venta_numero": venta.venta_numero,
        "cliente": venta.cliente.nombre,
        "total": venta.total,
        "impuesto": (venta.total * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        "fecha_venta": venta.fecha.strftime('%d/%m/%Y %H:%M:%S'),
        "venta_detalle": venta_detalle,
    }
    return render(request, "ventas/pdfVenta.html", data)

class eliminarVentaView(LoginRequiredMixin, View):
    def delete(self, request, venta_id):
        try:
            venta = Ventas.objects.get(venta_id=venta_id)
            
            if venta.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar esta venta'
                }, status=403)
            
            venta.delete()
            return JsonResponse({
                'success': True,
                'message': 'Venta eliminada correctamente'
            })
        except Ventas.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La venta no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)


class listaClientesView(LoginRequiredMixin, ListView):
    model = Clientes
    template_name = "ventas/listaClientes.html"
    context_object_name = "clientes"
    paginate_by = 10
    ordering = ['fecha_creacion']

    def get_queryset(self):
        return Clientes.objects.filter(negocio=self.request.user.negocio)

class crearClienteView(LoginRequiredMixin, CreateView):
    model = Clientes
    template_name = 'ventas/formCliente.html'
    form_class = clienteForm
    success_url = reverse_lazy('listaClientes')

    def form_valid(self, form):
        form.instance.negocio = self.request.user.negocio
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edicion'] = False
        return context

class editarClienteView(LoginRequiredMixin, UpdateView):
    model = Clientes
    template_name = 'ventas/formCliente.html'
    form_class = clienteForm
    success_url = reverse_lazy('listaClientes')
    pk_url_kwarg = 'cliente_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edicion'] = True
        return context

class eliminarClienteView(LoginRequiredMixin, View):
    def delete(self, request, cliente_id):
        try:
            cliente = Clientes.objects.get(cliente_id=cliente_id)
            
            if cliente.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar este cliente'
                }, status=403)
            
            cliente.delete()
            return JsonResponse({
                'success': True,
                'message': 'Cliente eliminado correctamente'
            })
        except Clientes.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El cliente no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)

@csrf_exempt
@require_POST
@login_required
def obtenerClientes(request):
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') and request.method == 'POST':
        term = request.POST.get('term', '')
        clientes = Clientes.objects.filter(
            name__icontains=term
        ).values('cliente_id', 'nombre')
        lista_clientes = list(clientes)
        return JsonResponse(lista_clientes, safe=False)
    return JsonResponse({'error': 'Método inválido'}, status=400)