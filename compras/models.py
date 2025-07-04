import uuid
from django.db import models
from usuarios.models import Negocios

class Proveedores(models.Model):
    proveedor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, editable=False
    )
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='RUC'
    )
    telefono = models.CharField(
        max_length=15, blank=True, null=True, verbose_name='Telefono'
    )
    email = models.EmailField(
        max_length=150, blank=True, null=True, verbose_name='Email'
    )
    direccion = models.CharField(max_length=100, blank=True, null=True, verbose_name='Dirección')
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, editable=False
    )

    def __str__(self):
        return f"Proveedor: {self.nombre}"
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['negocio']
        db_table = 'Proveedores'

class Compras(models.Model):
    compra_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, editable=False
    )
    proveedor = models.ForeignKey(
        Proveedores, on_delete=models.CASCADE, verbose_name='Proveedor'
    )
    fecha = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    metodo_pago = models.CharField(
        max_length=10, verbose_name='Método de Pago', 
        choices=[('EF', 'Efectivo'), ('TR', 'Tarjeta')]
    )
    estado_pago = models.CharField(
        max_length=10, choices=[('PD', 'Pendiente'), ('CT', 'Completado')], 
        verbose_name='Estado de pago'
    )
    estado_envio = models.CharField(
        max_length=10, choices=[('PT', 'Pendiente'), ('EV', 'En envio'), ('ET', 'Entregado')], 
        verbose_name='Estado de envío'
    )
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['fecha']
        db_table = 'Compras'

class DetalleCompra(models.Model):
    detalle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE, editable=False)
    producto = models.ForeignKey('inventario.Productos', on_delete=models.CASCADE, editable=False)
    cantidad = models.PositiveIntegerField(editable=False)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        db_table = 'DetalleCompra'
        verbose_name = 'Detalle de compra'
        verbose_name_plural = 'Detalles de compras'
        ordering = ['detalle_id']

    def __str__(self):
        return f"Detalle {self.detalle_id} - Compra {self.compra.compra_id}"