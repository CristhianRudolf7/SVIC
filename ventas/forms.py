from .models import Clientes
from django import forms

class clienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nombre',
            'apellido',
            'dni',
            'email',
            'telefono',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido del cliente'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su número dni'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su email'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su número de teléfono'
            }),
        }

