# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class Negocio(models.Model):
    nombre = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='negocios/fotos/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_suscripcion = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError('El campo DNI es obligatorio')
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password) # Hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(dni, password, **extra_fields)

class Usuario(AbstractUser):
    username = None
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'negocio'] # Agrega otros campos obligatorios aquí

    nombre = models.CharField(max_length=255) # Si prefieres este a first_name
    rol = models.IntegerField() # 1: CEO, 2: Admin, 3: Inventario, 4: Ventas
    phone = models.CharField(max_length=20) # Renombrado desde PHONE
    foto = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='usuarios')

    objects = UsuarioManager() # Asignamos el Manager personalizado

    def __str__(self):
        return f"{self.nombre} ({self.dni})"

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set", # Cambiado de user_set
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set", # Cambiado de user_set
        related_query_name="usuario",
    )
