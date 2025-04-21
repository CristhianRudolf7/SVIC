from django.db import models
import uuid

class UnidadMedida(models.Model):
    unidad_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    categoria_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    producto_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    categorita = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='static/images/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    @property
    def avatar_url(self):
        return self.foto.url if self.foto else "static/images/avatar.png"

class movimientoInventario(models.Model):
    movimiento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo_movimiento = models.CharField(max_length=50)  # 'entrada' o 'salida'
    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.tipo_movimiento} - {self.cantidad}"
    
class Proveedores(models.Model):
    proveedor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Compras(models.Model):
    compra_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)
    proveedor_id = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Compra {self.compra_id} - {self.total}"
    
class DetalleCompra(models.Model):
    detalle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compra_id = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    negocio_id = models.ForeignKey('usuarios.Negocio', on_delete=models.CASCADE)

    def __str__(self):
        return f"Detalle {self.detalle_id} - {self.cantidad} unidades"