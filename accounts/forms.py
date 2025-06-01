from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Customer, Vendor, Negocios

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
            'tipo_suscripcion',
            'inicio_suscripcion',
            'fin_suscripcion',
        ]

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'telephone',
            'email',
            'first_name',
            'last_name',
            'profile_picture'
        ]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'address',
            'email',
            'phone',
            'loyalty_points'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu apellido',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu dirección',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu correo electrónico'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu número de teléfono'
            }),
            'loyalty_points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu cantidad de puntos'
            }),
        }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'phone_number', 'address']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingresa el nombre del proveedor'}
            ),
            'phone_number': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de teléfono del proveedor'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingresa la dirección del proveedor'}
            ),
        }
