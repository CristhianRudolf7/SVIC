
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
        default='negocios/negocio inicial.png',
        upload_to='usuarios',
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

    def save(self, *args, **kwargs):
        if self.foto:
            try:
                img_path = self.foto.path
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    if img.size != (224, 224):
                        img = img.resize((224, 224))
                        img.save(img_path)
                    self.ancho, self.alto = img.size
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        
        super().save(*args, **kwargs)

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
        Negocios, on_delete=models.CASCADE, editable=False
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
        default='OP'
    )
    telefono = models.CharField(
        max_length=15, null=True, blank=True, verbose_name='Telefono'
    )
    foto = models.ImageField(
        default='usuarios/usuario inicial.png',
        upload_to='usuarios',
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
    
    def save(self, *args, **kwargs):
        if self.foto:
            try:
                img_path = self.foto.path
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    if img.size != (224, 224):
                        img = img.resize((224, 224))
                        img.save(img_path)
                    self.ancho, self.alto = img.size
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['negocio']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Usuarios'
