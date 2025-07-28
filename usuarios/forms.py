from django import forms
from .models import Negocios, Usuarios, Pago
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
            'telefono',
            'foto',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del trabajador'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido del trabajador'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el DNI'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo electrónico'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una contraseña',
                'id': 'password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Repita la contraseña',
                'id': 'password'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de teléfono'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['dni']
        if commit:
            user.save()
        return user

class UsuarioEditarForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = [
            'nombre', 
            'apellido', 
            'dni',
            'email',
            'rol',
            'telefono',
            'foto',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del trabajador'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido del trabajador'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el DNI'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo electrónico'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-control'
            }), 
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de teléfono'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='DNI', max_length=8)

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['numero_celular', 'comprobante_pago']