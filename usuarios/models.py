
import os
from PIL import Image
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class Negocios(models.Model):
    negocio_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    sector = models.CharField(max_length=50, verbose_name='Sector')
    pais = models.CharField(max_length=50, verbose_name='País')
    region = models.CharField(max_length=50, verbose_name='Región')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(
        max_length=15, verbose_name='Telefono'
    )
    ruc = models.CharField(max_length=20, blank=True, null=True, verbose_name='RUC')
    foto = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Logo de negocio'
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    tipo_suscripcion = models.CharField(
        max_length=8, choices=[('BS', 'Básico'), ('ET', 'Estándar'), ('PR', 'Premium')],
        editable=False
    )
    inicio_suscripcion = models.DateField(editable=False)
    fin_suscripcion = models.DateField(editable=False)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    numero_ventas = models.PositiveIntegerField(
        default=0, editable=False, verbose_name='Número de Ventas'
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        ordering = ['fecha_creacion']
        db_table = 'Negocios'

class Usuarios(AbstractUser):
    usuario_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE
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
            ('OP', 'Trabajador'),
            ('EX', 'Ejecutivo'),
            ('AD', 'Administrador')
        ],
        blank=True,
        max_length=13,
        verbose_name='Rol',
        default='OP'
    )
    telefono = models.CharField(
        max_length=15, null=True, blank=True, verbose_name='Telefono'
    )
    foto = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Foto de perfil'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        choices=[
            ('IN', 'Inactivo'),
            ('AT', 'Activo'),
            ('PM', 'De permiso')
        ],
        max_length=12,
        default='AT',
        verbose_name='Estado'
    )

    USERNAME_FIELD = 'dni'

    def __str__(self):
        return f"Nombre: {self.nombre} {self.apellido} - DNI:({self.dni})"

    class Meta:
        ordering = ['negocio']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Usuarios'

class Pago(models.Model):
    pago_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto', null=True, blank=True)
    numero_celular = models.CharField(
        max_length=15, verbose_name='Número de Celular'
    )
    comprobante_pago = models.ImageField(upload_to='comprobantes/', verbose_name='Comprobante de Pago')
    estado = models.CharField(
        max_length=10, choices=[('PE', 'Pendiente'), ('CO', 'Completado'), ('EL', 'Eliminado')],
        default='PE', verbose_name='Estado'
    )
    codigo_autorizacion = models.CharField(
        max_length=5, null=True, blank=True, verbose_name='Código de Autorización'
    )
    estado_codigo = models.CharField(
        max_length=10, choices=[('PE', 'Pendiente'), ('US', 'Usado')],
        default='PE', verbose_name='Estado del Código'
    )

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        db_table = 'Pagos'
