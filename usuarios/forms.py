from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Negocios, Usuarios
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class NegocioForm(forms.ModelForm):
    """
    Formulario para la creación y actualización de Negocios.
    """
    # Definimos explícitamente los campos de teléfono para usar el widget adecuado si es necesario.
    # Si el widget por defecto de PhoneNumberField es suficiente, no necesitas redefinirlo aquí.
    telefono = PhoneNumberField(
        label='Número de teléfono',
        required=True,
        initial='+51'
    )
    # Hacemos los campos de fecha más amigables con un DateInput
    inicio_suscripcion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label='Inicio de suscripción'
    )
    fin_suscripcion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label='Fin de suscripción'
    )

    class Meta:
        model = Negocios
        fields = [
            'nombre', 'sector', 'pais', 'region', 'ciudad', 'direccion',
            'telefono', 'ruc', 'foto', 'descripcion', 'tipo_suscripcion',
            'inicio_suscripcion', 'fin_suscripcion'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mi Super Tienda'}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Retail'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Perú'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lima'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Miraflores'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Av. Larco 123'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 20123456789'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe brevemente tu negocio...'}),
            'tipo_suscripcion': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre del Negocio',
            'ruc': 'RUC (Opcional)',
            # Puedes añadir más etiquetas personalizadas si lo deseas
        }

    def clean_ruc(self):
        """
        Validación personalizada para el RUC (ejemplo).
        Asegúrate de que tenga 11 dígitos si no está vacío.
        """
        ruc = self.cleaned_data.get('ruc')
        if ruc and not ruc.isdigit():
            raise forms.ValidationError("El RUC debe contener solo números.")
        if ruc and len(ruc) != 11:
            raise forms.ValidationError("El RUC debe tener 11 dígitos.")
        return ruc

    def clean_nombre(self):
        """
        Validación para asegurar que el nombre no contenga caracteres no deseados.
        """
        nombre = self.cleaned_data.get('nombre')
        # Ejemplo: permitir solo alfanuméricos y espacios. Ajusta según necesidad.
        if not nombre.replace(' ', '').isalnum():
             # Esto es un ejemplo, podrías ser más específico o usar regex
            if any(not c.isalnum() and not c.isspace() for c in nombre):
                raise forms.ValidationError("El nombre solo puede contener letras, números y espacios.")
        return nombre
        
    # Puedes añadir más métodos clean_<fieldname>() para validaciones específicas


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de Usuarios de Django (auth.User).
    Hereda de UserCreationForm para manejar contraseñas de forma segura.
    Podemos añadir campos adicionales del modelo User aquí si es necesario (email, first_name, last_name).
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    # Los campos 'nombre' y 'apellido' de tu modelo Usuarios se manejarán en UsuarioProfileForm
    # pero es buena práctica también pedir first_name y last_name para el modelo User de Django.
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'})
    )
    last_name = forms.CharField(
        max_length=30, # El modelo User tiene last_name con max_length=150, ajustamos a tu modelo Usuarios
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )

    class Meta(UserCreationForm.Meta):
        model = User # Se refiere al modelo User de Django
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UsuarioProfileForm(forms.ModelForm):
    """
    Formulario para los campos adicionales del perfil de Usuario (modelo Usuarios).
    Este formulario se usará en conjunto con CustomUserCreationForm.
    """
    # El campo 'negocio_id' será un ModelChoiceField
    negocio_id = forms.ModelChoiceField(
        queryset=Negocios.objects.all(), # Podrías filtrar esto en la vista si es necesario
        label="Negocio Asignado",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    telefono = PhoneNumberField(
        label='Número de teléfono',
        required=True,
        initial='+51'
    )
    # El campo email de Usuarios es opcional, el de User es el principal para login
    email = forms.EmailField(
        required=False, # Ya que el modelo lo permite (blank=True, null=True)
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo.secundario@ejemplo.com (Opcional)'})
    )

    class Meta:
        model = Usuarios
        fields = [
            'negocio_id', 'nombre', 'apellido', 'dni', 'email', 'rol',
            'telefono', 'foto', 'estado'
        ]
        # 'user' se asignará en la vista después de crear el User con CustomUserCreationForm
        # 'usuario_id' es autogenerado
        # 'fecha_creacion' es auto_now_add

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del empleado'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del empleado'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombres (Perfil)',
            'apellido': 'Apellidos (Perfil)',
            'dni': 'DNI',
            'email': 'Email de Contacto (Perfil)',
            'foto': 'Foto de Perfil',
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni and not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        if dni and len(dni) != 8:
            raise forms.ValidationError("El DNI debe tener 8 dígitos.")
        # Verificar unicidad (aunque el modelo ya lo hace a nivel de DB, es bueno validar en el form)
        # Si estás actualizando una instancia, debes excluir la propia instancia de la verificación
        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     if Usuarios.objects.filter(dni=dni).exclude(pk=instance.pk).exists():
        #         raise forms.ValidationError("Este DNI ya está registrado.")
        # elif Usuarios.objects.filter(dni=dni).exists():
        #     raise forms.ValidationError("Este DNI ya está registrado.")
        return dni

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(not c.isalpha() and not c.isspace() for c in nombre): # Solo letras y espacios
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if any(not c.isalpha() and not c.isspace() for c in apellido): # Solo letras y espacios
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        return apellido