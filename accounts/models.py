from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField


# Define choices for profile status and roles
STATUS_CHOICES = [
    ('INA', 'Inactivo'),
    ('A', 'Activo'),
    ('OL', 'De permiso')
]

ROLE_CHOICES = [
    ('OP', 'Trabajador'),
    ('EX', 'Ejecutivo'),
    ('AD', 'Administrador')
]

class Negocios(models.Model):
    slug = AutoSlugField(
        unique=True,
        populate_from='nombre',
        verbose_name='Slug'
    )
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    sector = models.CharField(max_length=50, verbose_name='Sector')
    pais = models.CharField(max_length=50, verbose_name='País')
    region = models.CharField(max_length=50, verbose_name='Región')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = PhoneNumberField(verbose_name='Número de teléfono', blank=True, null=True)	
    ruc = models.CharField(max_length=20, blank=True, null=True, verbose_name='RUC')
    foto = ProcessedImageField(
        default='usuarios/negocio inicial.png',
        upload_to='',
        format='JPEG',
        processors=[ResizeToFill(150, 150)],
        options={'quality': 100}
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    tipo_suscripcion = models.CharField(
        max_length=20, choices=[('Free', 'Free'), ('Basico', 'Basico'), ('Premium', 'Premium')],
        default='Free', blank=True, verbose_name='Tipo de suscripción'
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

class Profile(models.Model):
    """
    Represents a user profile containing personal and account-related details.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='User'
    )
    slug = AutoSlugField(
        unique=True,
        verbose_name='Account ID',
        populate_from='email'
    )
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, verbose_name='Negocio'
    )
    profile_picture = ProcessedImageField(
        default='images/usuarios/usuario inicial.png',
        upload_to='images/usuarios',
        format='JPEG',
        processors=[ResizeToFill(150, 150)],
        options={'quality': 100}
    )
    telephone = PhoneNumberField(
        null=True, blank=True, verbose_name='Telephone'
    )
    email = models.EmailField(
        max_length=150, blank=True, null=True, verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=30, blank=True, verbose_name='Last Name'
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=12,
        default='INA',
        verbose_name='Status'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Role',
        default='AD',
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


class Vendor(models.Model):
    """
    Represents a vendor with contact and address information.
    """
    name = models.CharField(max_length=50, verbose_name='Name')
    slug = AutoSlugField(
        unique=True,
        populate_from='name',
        verbose_name='Slug'
    )
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, verbose_name='Negocio'
    )
    phone_number = models.BigIntegerField(
        blank=True, null=True, verbose_name='Phone Number'
    )
    address = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Address'
    )

    def __str__(self):
        """
        Returns a string representation of the vendor.
        """
        return self.name

    class Meta:
        """Meta options for the Vendor model."""
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        db_table = 'Proveedores'


class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, verbose_name='Negocio'
    )
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'Clientes'

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item
