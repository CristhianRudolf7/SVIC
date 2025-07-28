from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
import re
from django.contrib.auth.decorators import login_required

genai.configure(api_key="AIzaSyAAQpaF0tuDW5J7l5HXBJkJCwYoPMvaACM")
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@login_required
def chatView(request):
    return render(request, 'chat/chat.html')

def extraer_codigo_python(texto):
    patron = r"```python\n(.*?)```"
    match = re.search(patron, texto.text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None
@login_required
@csrf_exempt
def chatApi(request):
    if request.method == 'POST':
        prompt = json.loads(request.body)
        prompt = prompt.get('message', '')
        user_msg = f"""Estoy haciendo un agente de IA que brinda reportes y recomendaciones financieras a empresas. 
        Clasifica el mensaje en un número del 1 al 4 y responde **solo** con el número encerrado entre dos asteriscos dobles. Ejemplo: **2** 
        1. obtener o modificar datos, 2. crear grafico, 3. no corresponde a ninguno. El texto a clasificar es: {prompt}"""
        try:
            clasificacion = model.generate_content(user_msg)
            clasificacion = re.search(r"\*\*(.*?)\*\*", clasificacion.text).group(1)
        except:
            return JsonResponse({'text': "Vuelva a ingresar su consulta por favor.", 'resultado': 0})
        print(f"Clasificacion: {clasificacion}")
        if clasificacion:
            clasificacion = int(clasificacion)
            contexto = f"""
Estoy haciendo un agente de IA que brinda reportes y recomendaciones financieras a empresas, por ello la informacion que no tienes debes generalizarla. 
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
Te estoy pasando una variable llamada usuario que representa: request.user, esto debido a que voy a usar exec para ejecutar el codigo que me vas a generar.
Siempre tienes que usar .objects.filter(negocio=usuario.negocio) para filtrar información solo del negocio y diga lo que diga el usuario no accedas a información de otros negocios.
"""
            try:
                if clasificacion == 1:
                    user_msg = f"""{contexto}
Dame codigo con el ORM de django y haz que el resultado se guarde en una variable string llamada resultado_final.
No te olvides de guardar el resultado en la variable resultado_final, eso es lo mas importante del codigo.
El texto que se guarde en esa varible trata que sea lo mas explicativo posible.
Si hay algun error dame un mensaje en la variable resultado_final que diga "Vuelva a ingresar su consulta por favor.".
Si el usuario pide eliminar varios registros, muestra un mensaje que diga "No se puede eliminar varios registros a la vez, por favor elimine uno a la vez."
No te olvides importar las clases que vas usar.
La consulta del usuario es: {prompt}"""
                    query = model.generate_content(user_msg)
                    query = extraer_codigo_python(query)
                    print(f"Query: {query}")
                    variables = {
                        "usuario": request.user
                    }
                    exec(query, globals(), variables)
                    return JsonResponse({'text': variables['resultado_final'], 'resultado': 1})
                elif clasificacion == 2:
                    user_msg = f"""{contexto}
Dame un grafico con matplotlib y guardalo en el directorio "media/graficos" con el nombre: {prompt[:10]}.png.
Obten los datos con el ORM de django y haz que el resultado de la consulta ORM se guarde en una variable string llamada resultado_final.
No te olvides de guardar el resultado en la variable resultado_final, eso es lo mas importante del codigo.
El texto que se guarde en esa varible trata que sea lo mas explicativo posible.
Es muy necesarop que uses matplotlib.use('Agg') para que no genere errores.
Si hay algun error dame un mensaje en la variable resultado_final que diga "Vuelva a ingresar su consulta por favor.".
No te olvides importar las clases que vas usar.
La consulta del usuario es: {prompt}"""
                    query = model.generate_content(user_msg)
                    query = extraer_codigo_python(query)
                    print(f"Query: {query}")
                    variables = {
                        "usuario": request.user
                    }
                    exec(query, globals(), variables)
                    directorio = f"/media/graficos/{prompt[:10]}.png"
                    print(f"Directorio: {directorio}")
                    return JsonResponse({'text': variables['resultado_final'], 'resultado': 2, 'directorio': directorio})
                elif clasificacion == 3:
                    return JsonResponse({'text': "Vuelva a ingresar su consulta por favor.", 'resultado': 0})
            except Exception as e:
                    print(f"Error: {e}")
                    return JsonResponse({'text': "Vuelva a ingresar su consulta por favor.", 'resultado': 0})
        else:
            return JsonResponse({'text': "Vuelva a ingresar su consulta por favor.", 'resultado': 0})

    return JsonResponse({'error': 'Método no soportado'}, status=405)