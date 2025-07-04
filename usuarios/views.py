from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm, NegocioForm, UsuarioForm, UsuarioEditarForm
from .models import Usuarios
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView, View
)
from django.urls import reverse_lazy
from django.http import JsonResponse

def landing(request):
    return render(request, 'usuarios/landingCuerpo.html')

class LoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

def crearEmpresa(request):
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
            gerente.rol =' Ejecutivo'
            gerente.save()
            return redirect('login')
        else:
            print("Errores negocio_form:", negocio_form.errors)
            print("Errores gerente_form:", gerente_form.errors)
    else:
        negocio_form = NegocioForm(prefix='negocio')
        gerente_form = UsuarioForm(prefix='gerente')

    return render(request, 'usuarios/crearEmpresa.html', {'negocio': negocio_form, 'gerente': gerente_form})

def pagar(request):
    return render(request, 'usuarios/payment.html')

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
        form.instance.rol = 'Trabajador'
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