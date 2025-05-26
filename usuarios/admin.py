from django.contrib import admin
from .models import Negocios, Usuarios

@admin.register(Negocios)
class NegociosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'tipo_suscripcion', 'fecha_creacion')

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    fields = ('negocio_id', 'apellido', 'rol', 'nombre', 'user', 'telefono', 'email', 'foto')
    list_display = ('negocio_id', 'apellido', 'rol', 'nombre', 'user', 'telefono', 'email', 'foto')
    search_fields = ('negocio_id', 'apellido', 'rol', 'nombre', 'user', 'telefono', 'email', 'foto')
