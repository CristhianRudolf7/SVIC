from django import forms
from .models import Productos, Categorias, UnidadMedida

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'stock',
            'fecha_expiracion',
            'unidad',
            'foto',
            'codigo_barras'
        ]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = [
            'nombre',
            'descripcion'
        ]

'''
class UnidadForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = [
            'item',
            'customer_name',
            'phone_number',
            'location',
            'date',
            'is_delivered'
        ]
        widgets = {
            'item': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select item',
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter delivery location',
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Select delivery date and time',
                'type': 'datetime-local'
            }),
            'is_delivered': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'label': 'Mark as delivered',
            }),
        }
'''