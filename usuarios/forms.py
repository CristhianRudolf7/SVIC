from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=8)
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['dni'].widget.attrs.update({'placeholder': 'Ingrese su DNI'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Ingrese su contraseña'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")
        password = cleaned_data.get("password")

        if dni and password:
            self.user = authenticate(username=dni, password=password)

            if self.user is None:
                raise forms.ValidationError("El usuario no existe.")

        return cleaned_data

    def get_user(self):
        return self.user