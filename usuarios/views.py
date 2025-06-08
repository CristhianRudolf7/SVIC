from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import LoginForm

def landing(request):
    return render(request, 'usuarios/landingCuerpo.html')

class LoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True