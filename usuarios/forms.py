from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Usuarios, Negocios

class CrearUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = Usuarios
        fields = [
            'nombre',
            'email',
            'password1',
            'password2'
        ]

class ModificarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class NegociosForm(forms.ModelForm):
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
            'descripcion',
            'tipo_suscripcion'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del negocio'
            }),
            'sector': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el sector del negocio'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el país del negocio'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la región del negocio'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la ciudad del negocio'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección del negocio'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de teléfono del negocio'
            }),
            'tipo_suscripcion': forms.Select(attrs={
                'class': 'form-control'
            }),
        }