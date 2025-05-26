import django_tables2 as tables
from django.shortcuts import render
from .models import Usuarios

class ProfileTable(tables.Table):
    class Meta:
        model = Usuarios
        template_name = "django_tables2/semantic.html"
        fields = (
            'nombre',
            'apellido'
            'dni',
            'email',
            'rol',
            'estado',
            'fecha_creacion',
        )
        order_by_field = 'sort'
