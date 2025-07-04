from .models import Proveedores
from django import forms

class proveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = [
            'nombre',
            'ruc',
            'telefono',
            'email',
            'direccion',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del proveedor'
            }),
            'ruc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el RUC del proveedor'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el telefono del proveedor'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el email del proveedor'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección del proveedor'
            }),
        }

