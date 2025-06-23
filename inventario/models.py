import os
import uuid
from PIL import Image
from django.db import models
from usuarios.models import Negocios
from django.forms import model_to_dict
from ventas.models import Clientes

class UnidadMedida(models.Model):
    unidad_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE, editable=False
    )
    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UnidadMedida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return f"{self.nombre} ({self.simbolo})"

class Categorias(models.Model):
    categoria_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    producto_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(
        Negocios, on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(
        Categorias, on_delete=models.CASCADE, blank=True, null=True
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField(blank=True, null=True)
    unidad = models.ForeignKey(
        UnidadMedida, on_delete=models.CASCADE, blank=True, null=True
    )
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre

    def to_json(self):
        product = model_to_dict(self)
        product['id'] = str(self.producto_id)
        product['text'] = self.nombre
        product['category'] = self.categoria.nombre
        product['quantity'] = 1
        product['total_product'] = 0
        return product
    
class MovimientosInventario(models.Model):
    movimiento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(
        max_length=7,
        choices=[
            ('in', 'Entrada'),
            ('EX', 'Salida'),
            ('ST', 'Ajuste')
        ]
    )
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'MovimientosInventario'
        verbose_name = 'Movimiento de inventario'
        verbose_name_plural = 'Movimientos de inventario'

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} ({self.cantidad})"
    
class Alertas(models.Model):
    alerta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocios, on_delete=models.CASCADE)
    tipo_alerta = models.CharField(
        max_length=10,
        choices=[
            ('ST', 'Stock bajo'),
            ('EX', 'Producto expirado'),
            ('OT', 'Otro')
        ]
    )
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=10,
        choices=[
            ('PN', 'Pendiente'),
            ('R', 'Resuelta'),
            ('CN', 'Cancelada')
        ],
        default='pendiente'
    )

    class Meta:
        db_table = 'Alertas'
        verbose_name = 'Alerta de inventario'
        verbose_name_plural = 'Alertas de inventario'
