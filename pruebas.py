import google.generativeai as genai
genai.configure(api_key="AIzaSyAAQpaF0tuDW5J7l5HXBJkJCwYoPMvaACM")
model = genai.GenerativeModel('gemini-2.5-flash')
user_msg = "quiero un reporte de los ingresos del ultimo trimestre"
user_msg = f"""Estoy haciendo un agente de IA que brinda reportes y recomendaciones financieras a empresas, por ello la informacion que te doy debes generalizarla. 
Te doy la informacion de la base de datos:
app: compras.models
class Proveedores(models.Model):
    proveedor_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    ruc = models.CharField()
    telefono = models.CharField()
    email = models.EmailField()
    direccion = models.CharField()
    fecha_creacion = models.DateTimeField()
class Compras(models.Model):
    compra_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    proveedor = models.ForeignKey(Proveedores)
    fecha = models.DateTimeField()
    total = models.DecimalField()
    metodo_pago = models.CharField()
    estado_pago = models.CharField()
    estado_envio = models.CharField()
class DetalleCompra(models.Model):
    detalle_id = models.UUIDField()
    compra = models.ForeignKey(Compras)
    producto = models.ForeignKey()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField()
    subtotal = models.DecimalField()
app: inventario.models
class UnidadMedida(models.Model):
    unidad_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    simbolo = models.CharField()
    fecha_creacion = models.DateTimeField()
class Categorias(models.Model):
    categoria_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField()
class Productos(models.Model):
    producto_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categorias)
    precio = models.DecimalField()
    stock = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    unidad = models.ForeignKey(UnidadMedida)
    codigo_barras = models.CharField()
class MovimientosInventario(models.Model):
    movimiento_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    producto = models.ForeignKey(Productos)
    tipo_movimiento = models.CharField(choices=[('in', 'Entrada'),('EX', 'Salida'),('ST', 'Ajuste')])
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField()
    observaciones = models.TextField()
class Alertas(models.Model):
    alerta_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    tipo_alerta = models.CharField(choices=[('ST', 'Stock bajo'),('EX', 'Producto expirado'),('OT', 'Otro')])
    mensaje = models.TextField()
    fecha = models.DateTimeField()
    estado = models.CharField(choices=[('PN', 'Pendiente'),('R', 'Resuelta'),('CN', 'Cancelada')])
app: usuarios.models
class Negocios(models.Model):
    negocio_id = models.UUIDField()
    nombre = models.CharField()
    sector = models.CharField()
    pais = models.CharField()
    region = models.CharField()
    ciudad = models.CharField()
    direccion = models.CharField()
    telefono = models.CharField()
    ruc = models.CharField()
    foto = models.ImageField()
    descripcion = models.TextField()
    tipo_suscripcion = models.CharField(choices=[('BS', 'Básico'), ('ET', 'Estándar'), ('PR', 'Premium')])
    inicio_suscripcion = models.DateField()
    fin_suscripcion = models.DateField()
    fecha_creacion = models.DateTimeField()
    numero_ventas = models.PositiveIntegerField()
class Usuarios(AbstractUser):
    usuario_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    apellido = models.CharField()
    dni = models.CharField()
    email = models.EmailField()
    rol = models.CharField(choices=[('OP', 'Trabajador'),('EX', 'Ejecutivo'),('AD', 'Administrador')])
    telefono = models.CharField()
    foto = models.ImageField()
    fecha_creacion = models.DateTimeField()
    estado = models.CharField(choices=[('IN', 'Inactivo'),('AT', 'Activo'),('PM', 'De permiso')])
app: ventas.models
class Clientes(models.Model):
    cliente_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    apellido = models.CharField()
    dni = models.CharField()
    email = models.EmailField()
    telefono = models.CharField()
    fecha_creacion = models.DateTimeField()
    foto = models.ImageField()
class Descuentos(models.Model):
    descuento_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    nombre = models.CharField()
    descripcion = models.TextField()
    tipo_descuento = models.CharField(choices=[('PR', 'Porcentaje'), ('M', 'Monto Fijo')])
    monto = models.DecimalField()
    porcentaje = models.DecimalField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    activo = models.BooleanField()
    cliente = models.ForeignKey(Clientes)
    productos = models.ManyToManyField('inventario.Productos')
class Ventas(models.Model):
    venta_id = models.UUIDField()
    negocio = models.ForeignKey(Negocios)
    usuario = models.ForeignKey(Usuarios)
    cliente = models.ForeignKey(Clientes)
    fecha = models.DateTimeField()
    total = models.DecimalField()
    metodo_pago = models.CharField(choices=[('EF', 'Efectivo'), ('TR', 'Tarjeta')])
    venta_numero = models.PositiveIntegerField() 
    estado_pago = models.CharField(choices=[('PD', 'Pendiente'), ('CT', 'Completado')])
    estado_envio = models.CharField(choices=[('PT', 'Pendiente'), ('EV', 'En envio'), ('ET', 'Entregado')])
    descuento = models.ManyToManyField( Descuentos)
class DetalleVentas(models.Model):
    detalle_id = models.UUIDField()
    venta = models.ForeignKey(Ventas)
    producto = models.ForeignKey('inventario.Productos')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField()
    subtotal = models.DecimalField()

Dame codigo con el ORM de django y haz que se imprima por consola el resultado, no te olvides de importar las clases (dame solo el codigo): {user_msg}"""
response = model.generate_content(user_msg)
print(response.text)
'''import re

texto = "**texto**"
resultado = re.search(r"\*\*(.*?)\*\*", texto)

if resultado:
    contenido = resultado.group(1)
    print(contenido)  # Salida: texto
'''