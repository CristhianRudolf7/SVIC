from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import uuid

class Negocio(models.Model):
    negocio_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    def create_user(self, dni, password, negocio_id, **extra_fields):
        if not dni:
            raise ValueError('El campo DNI es obligatorio')
        user = self.model(dni=dni, negocio_id=negocio_id, **extra_fields)
        user.set_password(password) # Hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, password, negocio_id, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(dni, password, negocio_id, **extra_fields)

class Usuario(AbstractUser):
    ROL_CHOICES = (
        (1, 'CEO'),
        (2, 'Administrador'),
        (3, 'Empleado'),
    )
    
    username = None     
    usuario_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='static/images/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    negocio_id = models.ForeignKey(Negocio, on_delete=models.CASCADE)
    rol = models.IntegerField(choices=ROL_CHOICES, default=2)
    objects = UsuarioManager() # Asignamos el Manager personalizado
    
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre','negocio_id']
    
    def __str__(self):
        return f"{self.nombre} ({self.dni})"

    @property
    def avatar_url(self):
        return self.foto.url if self.foto else "static/images/avatar.png"
    
    @property
    def negocio_id(self):
       return self.negocio.negocio_id

