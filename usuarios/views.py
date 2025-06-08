from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm, NegocioForm, UsuarioForm
from .models import Usuarios
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

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
            gerente.rol =' Administrador'
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