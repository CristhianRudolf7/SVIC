from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Negocios(models.Model):
    negocio_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    sector = models.CharField(max_length=50, verbose_name='Sector')
    pais = models.CharField(max_length=50, verbose_name='País')
    region = models.CharField(max_length=50, verbose_name='Región')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = PhoneNumberField(verbose_name='Número de teléfono')	
    ruc = models.CharField(max_length=20, blank=True, null=True, verbose_name='RUC')
    foto = ProcessedImageField(
        default='usuarios/negocio inicial.png',
        upload_to='usuarios',
        format='JPEG',
        processors=[ResizeToFill(300, 200)],
        options={'quality': 100},
        blank=True,
        null=True
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    tipo_suscripcion = models.CharField(
        max_length=20, choices=[('Free', 'Free'), ('Basico', 'Basico'), ('Premium', 'Premium')],
        default='Free', verbose_name='Tipo de suscripción'
    )
    inicio_suscripcion = models.DateField(
        blank=True, null=True, verbose_name='Inicio de suscripción')
    fin_suscripcion = models.DateField(
        blank=True, null=True, verbose_name='Fin de suscripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        ordering = ['fecha_creacion']
        unique_together = ('nombre', 'sector', 'pais', 'region', 'ciudad')
        db_table = 'Negocios'

class Usuarios(models.Model):
    usuario_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuarios'
    )
    negocio_id = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, verbose_name='Negocio', related_name='usuarios'
    )
    nombre = models.CharField(
        max_length=30, verbose_name='Nombre'
    )
    apellido = models.CharField(
        max_length=30, verbose_name='Apellido'
    )
    dni = models.CharField(
        max_length=8, unique=True, verbose_name='DNI'
    )
    email = models.EmailField(
        max_length=150, blank=True, null=True, verbose_name='Email'
    )
    rol = models.CharField(
        choices=[
            ('Gerente', 'Gerente'),
            ('Trabajador', 'Trabajador')],
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Rol'
    )
    telefono = PhoneNumberField(
        null=True, blank=True, verbose_name='Telefono'
    )
    foto = ProcessedImageField(
        default='usuarios/usuario inicial.jpg',
        upload_to='usuarios',
        format='JPEG',
        processors=[ResizeToFill(150, 150)],
        options={'quality': 100}
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        choices=[
            ('Inactivo', 'Inactivo'),
            ('Activo', 'Activo'),
            ('Despedido', 'Despedido')],
        max_length=12,
        default='Activo',
        verbose_name='Estado'
    )

    def __str__(self):
        return f"Nombre: {self.apellido} - Rol: {self.rol}"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Usuarios'