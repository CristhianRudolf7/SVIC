from django.db import models
import uuid
from django.utils import timezone

class Clientes(models.Model):
    cliente_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre
    
class Ventas(models.Model):
    venta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    usuario_id = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    tipo_venta = models.CharField(max_length=50)

    def __str__(self):
        return f"Venta {self.venta_id} - {self.total}"
    
class DetalleVenta(models.Model):
    detalle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto_id = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.detalle_id} - {self.cantidad} unidades"
    
class Descuentos(models.Model):
    descuento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo_descuento = models.CharField(max_length=50)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    activo = models.BooleanField(default=True)
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    producto_id = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
