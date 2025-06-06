
import os
from PIL import Image
from django.db import models
import uuid
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

STATUS_CHOICES = [
    ('INA', 'Inactivo'),
    ('A', 'Activo'),
    ('OL', 'De permiso')
]

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
        default='usuarios/negocio inicial.png',
        upload_to='usuarios',
        width_field='ancho',
        height_field='alto',
        blank=True,
        verbose_name='Logo de negocio'
    )
    ancho = models.PositiveIntegerField(editable=False, default=224)
    alto = models.PositiveIntegerField(editable=False, default=224)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_path = self.imagen.path
        if os.path.exists(img_path):
            img = Image.open(img_path)
            if img.size != (224, 224):
                img = img.resize((224, 224))
                img.save(img_path)

            self.ancho, self.alto = img.size
            super().save(update_fields=['ancho', 'alto'])

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        ordering = ['fecha_creacion']
        unique_together = ('nombre', 'sector', 'pais', 'region', 'ciudad')
        db_table = 'Negocios'

class Usuarios(AbstractUser):
    usuario_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    negocio_id = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, verbose_name='Negocio'
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
        max_length=13,
        verbose_name='Rol',
        default='OP',
        verbose_name='Rol'
    )
    telefono = models.CharField(
        null=True, blank=True, verbose_name='Telefono'
    )
    foto = models.ImageField(
        default='usuarios/negocio inicial.png',
        upload_to='usuarios',
        width_field='ancho',
        height_field='alto',
        verbose_name='Foto de perfil'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=12,
        default='INA',
        verbose_name='Status'
    )
    

    @property
    def image_url(self):
        """
        Returns the URL of the profile picture.
        Returns an empty string if the image is not available.
        """
        try:
            return self.profile_picture.url
        except AttributeError:
            return ''

    def __str__(self):
        """
        Returns a string representation of the profile.
        """
        return f"{self.user.username} Profile"

    class Meta:
        """Meta options for the Profile model."""
        ordering = ['slug']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'Usuarios'
