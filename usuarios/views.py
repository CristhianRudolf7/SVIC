from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.urls import reverse
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, UpdateView


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'usuarios/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'rol') and request.user.rol == 1:
                return HttpResponseRedirect(reverse('ceo:dashboard'))
            else:
                return HttpResponseRedirect(reverse('/'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        messages.success(self.request, f"Bienvenido {user.nombre}")
        if user.rol == 1:
            return redirect(reverse('ceo:dashboard'))
        else:
            messages.warning(self.request, "Rol no definido o sin página de inicio asignada.")
            return redirect('/')
        
    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario. Por favor, corrige los campos indicados.")
        return super().form_invalid(form)