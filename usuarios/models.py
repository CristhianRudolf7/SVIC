from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=20, unique=True)
    rol = models.IntegerField()
    
    # Agrega estos campos para resolver el conflicto
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set",  # Nombre único
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set",  # Nombre único
        related_query_name="usuario",
    )
    
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuarios'
        # Si estás usando una tabla existente:
        # managed = False
        # Si estás creando una nueva tabla:
        managed = True