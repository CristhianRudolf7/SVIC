from django import forms
from .models import Negocios, Usuarios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class NegocioForm(forms.ModelForm):
    class Meta:
        model = Negocios
        fields = [
            'nombre',
            'sector',
            'pais',
            'region',
            'ciudad',
            'direccion',
            'telefono',
            'ruc',
            'foto',
            'descripcion'
        ]

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = [
            'nombre', 
            'apellido', 
            'dni',
            'email',
            'password1', 
            'password2',
            'rol',
            'telefono',
            'foto',
        ]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='DNI', max_length=8)
