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
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from .forms import clienteForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def crearVentaView(request):
    context = {
        "clientes": [cliente for cliente in Clientes.objects.filter(negocio_id=request.user.negocio.negocio_id)]
    }

    if request.method == 'POST':
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)

                atributos_venta = {
                    "negocio": request.user.negocio,
                    "usuario": request.user,
                    "cliente": Clientes.objects.get(cliente_id=data['cliente']),
                    "total": float(data["total"]),
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

class listaClientesView(LoginRequiredMixin, ListView):
    model = Clientes
    template_name = "ventas/listaClientes.html"
    context_object_name = "clientes"
    paginate_by = 10
    ordering = ['fecha_creacion']

class crearClienteView(LoginRequiredMixin, CreateView):
    model = Clientes
    template_name = 'ventas/formCliente.html'
    form_class = clienteForm
    success_url = reverse_lazy('listaClientes')

    def form_valid(self, form):
        form.instance.negocio = self.request.user.negocio
        return super().form_valid(form)

class editarClienteView(LoginRequiredMixin, UpdateView):
    model = Clientes
    template_name = 'ventas/formCliente.html'
    form_class = clienteForm
    success_url = reverse_lazy('listaClientes')
    pk_url_kwarg = 'cliente_id'

class eliminarClienteView(LoginRequiredMixin, DeleteView):
    model = Clientes
    template_name = 'ventas/eliminarCliente.html'
    success_url = reverse_lazy('listaClientes')

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