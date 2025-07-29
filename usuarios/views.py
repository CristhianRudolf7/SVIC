from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm, NegocioForm, UsuarioForm, UsuarioEditarForm, PagoForm
from django.contrib.auth.decorators import login_required
from .models import Usuarios, Pago
from datetime import date, timedelta
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView, View
)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
import random

def crear_pago(request):
    pago_exitoso = False

    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pago_exitoso = True
    else:
        form = PagoForm()

    return render(request, 'usuarios/payment.html', {
        'form': form,
        'pago_exitoso': pago_exitoso
    })

@login_required
def vista_comprobantes(request):
    if request.user.dni != '77235743':
        return redirect('dashboard')

    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'usuarios/listaPagos.html', {'pagos': pagos})

@login_required
def aprobar_pago(request, pago_id):
    if request.method == 'POST':
        pago = get_object_or_404(Pago, pago_id=pago_id)
        pago.estado = 'CO'
        pago.codigo_autorizacion = str(random.randint(10000, 99999))
        pago.estado_codigo = 'PE'
        pago.save()
    return redirect('comprobantes')

@login_required
def desaprobar_pago(request, pago_id):
    if request.method == 'POST':
        pago = get_object_or_404(Pago, pago_id=pago_id)
        pago.estado = 'EL'
        pago.codigo_autorizacion = None
        pago.estado_codigo = 'PE' 
        pago.save()
    return redirect('comprobantes')

def landing(request):
    return render(request, 'usuarios/landingCuerpo.html')

class LoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

def crearEmpresa(request):
    if not request.session.get('codigo_validado'):
        if request.method == 'POST' and 'codigo_autorizacion' in request.POST:
            codigo = request.POST['codigo_autorizacion']
            pago = Pago.objects.filter(codigo_autorizacion=codigo, estado_codigo='PE').first()
            if pago:
                request.session['codigo_validado'] = True
                request.session['codigo_pago'] = pago.codigo_autorizacion
                return redirect('crearEmpresa')
            else:
                return render(request, 'usuarios/codigo_verificacion.html', {'error': 'Código inválido o ya usado'})

        return render(request, 'usuarios/codigo_verificacion.html')

    # Si el código ya fue validado
    if request.method == 'POST':
        negocio_form = NegocioForm(request.POST, request.FILES, prefix='negocio')
        gerente_form = UsuarioForm(request.POST, prefix='gerente')
        if negocio_form.is_valid() and gerente_form.is_valid():
            negocio = negocio_form.save(commit=False)
            negocio.inicio_suscripcion = date.today()
            negocio.fin_suscripcion = date.today() + relativedelta(months=1)
            negocio.tipo_suscripcion = 'Básico'
            negocio.save()

            gerente = gerente_form.save(commit=False)
            gerente.negocio = negocio
            gerente.rol = 'EX'
            gerente.save()

            # Marcar código como usado
            Pago.objects.filter(codigo_autorizacion=request.session.get('codigo_pago')).update(estado_codigo='US')

            # Limpiar sesión
            request.session.pop('codigo_validado')
            request.session.pop('codigo_pago')

            return redirect('login')
    else:
        negocio_form = NegocioForm(prefix='negocio')
        gerente_form = UsuarioForm(prefix='gerente')

    return render(request, 'usuarios/crearEmpresa.html', {'negocio': negocio_form, 'gerente': gerente_form})

def crearAdmi(request):
    if request.method == 'POST':
        negocio_form = NegocioForm(request.POST, request.FILES, prefix='negocio')
        gerente_form = UsuarioForm(request.POST, prefix='gerente')
        if negocio_form.is_valid() and gerente_form.is_valid():
            negocio = negocio_form.save(commit=False)
            negocio.inicio_suscripcion = date.today()
            negocio.fin_suscripcion = date.today() + relativedelta(months=1)
            negocio.tipo_suscripcion = 'Básico'
            negocio.save()
            gerente = gerente_form.save(commit=False)
            gerente.negocio = negocio
            gerente.rol ='AD'
            gerente.save()
            return redirect('login')
        else:
            print("Errores negocio_form:", negocio_form.errors)
            print("Errores gerente_form:", gerente_form.errors)
    else:
        negocio_form = NegocioForm(prefix='negocio')
        gerente_form = UsuarioForm(prefix='gerente')

    return render(request, 'usuarios/crearAdmi.html', {'negocio': negocio_form, 'gerente': gerente_form})

class listaTrabajadoresView(LoginRequiredMixin, ListView):
    model = Usuarios
    template_name = "usuarios/listaTrabajadores.html"
    context_object_name = "trabajadores"
    paginate_by = 10

    def get_queryset(self):
        return Usuarios.objects.filter(negocio=self.request.user.negocio).exclude(usuario_id=self.request.user.usuario_id)

class crearTrabajadorView(LoginRequiredMixin, CreateView):
    model = Usuarios
    template_name = 'usuarios/formTrabajadores.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('listaTrabajadores')

    def form_valid(self, form):
        form.instance.negocio = self.request.user.negocio
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edicion'] = False
        return context

class editarTrabajadorView(LoginRequiredMixin, UpdateView):
    model = Usuarios
    template_name = 'usuarios/formTrabajadores.html'
    form_class = UsuarioEditarForm
    success_url = reverse_lazy('listaTrabajadores')
    pk_url_kwarg = 'usuario_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edicion'] = True
        return context
    
    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)
        return super().form_invalid(form)

class eliminarTrabajadorView(LoginRequiredMixin, View):
    def delete(self, request, usuario_id):
        try:
            trabajador = Usuarios.objects.get(usuario_id=usuario_id)
            
            if trabajador.negocio != request.user.negocio:
                return JsonResponse({
                    'success': False,
                    'message': 'No tienes permiso para eliminar este trabajador'
                }, status=403)
            
            trabajador.delete()
            return JsonResponse({
                'success': True,
                'message': 'Trabajador eliminado correctamente'
            })
        except Usuarios.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El trabajador no existe'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar: {str(e)}'
            }, status=500)