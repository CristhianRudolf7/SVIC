import uuid
from django.db import models
from usuarios.models import Negocios, Usuarios
from inventario.models import Productos

class Clientes(models.Model):
    cliente_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE, editable=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    dni = models.CharField(max_length=8, unique=True, verbose_name='DNI')
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='Email')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Descuentos(models.Model):
    descuento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE, editable=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Descuento')
    descripcion = models.TextField(verbose_name='Descripción del Descuento', blank=True, null=True)
    tipo_descuento = models.CharField(max_length=20, choices=[('PR', 'Porcentaje'), ('M', 'Monto Fijo')], default='PR', verbose_name='Tipo de Descuento')
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Monto de descuento')
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Porcentaje de descuento')
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de inicio', blank=True, null=True)
    fecha_fin = models.DateTimeField(verbose_name='Fecha de fin', blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name='Activo')
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Cliente')
    productos = models.ManyToManyField(Productos, blank=True, verbose_name='Productos Aplicables')

    class Meta:
        db_table = 'Descuentos'
        verbose_name = 'Descuento de venta'
        verbose_name_plural = 'Descuentos de ventas'
        ordering = ['descuento_id']

    def __str__(self):
        return f"Descuento {self.nombre}"

class Ventas(models.Model):
    venta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE, editable=False)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, editable=False)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
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
    descuento = models.ManyToManyField(
        Descuentos, blank=True, verbose_name='Descuento aplicado'
    )

    class Meta:
        db_table = 'Ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['fecha']

    def __str__(self):
        return f"Venta {self.venta_id} - {self.cliente.nombre} {self.cliente.apellido}"

class DetalleVentas(models.Model):
    detalle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, editable=False)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, editable=False)
    cantidad = models.PositiveIntegerField(editable=False)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        db_table = 'DetalleVentas'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
        ordering = ['detalle_id']

    def __str__(self):
        return f"Detalle {self.detalle_id} - Venta {self.venta.venta_id}"
