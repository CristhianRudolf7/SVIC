import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

#### Tablas de usuarios ####
# Crear tabla negocios
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS negocios (
    negocio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    sector TEXT NOT NULL,
    pais TEXT NOT NULL,
    region TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL,
    RUC TEXT,
    foto TEXT,
    descripcion TEXT,
    tipo_suscripcion TEXT NOT NULL,
    inicio_suscripcion TEXT,
    fin_suscripcion TEXT,
    fecha_creacion TEXT NOT NULL
)
"""
)
# Crear tabla usuarios
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    email TEXT,
    password TEXT NOT NULL,
    rol INTEGER NOT NULL,
    telefono TEXT NOT NULL,
    foto TEXT,
    fecha_creacion TEXT NOT NULL,
    estado TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)


#### Tablas de inventario ####
# Tabla unidades_medida
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS unidades_medida (
    unidad_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    simbolo TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)

# Tabla productos
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS productos (
    producto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria_id TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    fecha_creacion TEXT NOT NULL,
    unidad_id INTEGER NOT NULL,
    foto TEXT,
    codigo_barras TEXT,
    FOREIGN KEY (unidad_id) REFERENCES unidades_medida (unidad_id),
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id),
    FOREIGN KEY (categoria_id) REFERENCES categorias (categoria_id)
)
"""
)

# Tabla categorias
cursor.execute(
    """ 
CREATE TABLE IF NOT EXISTS categorias (
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    fecha_creacion TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)

# Tabla movimientos_inventario
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS movimientos_inventario (
    movimiento_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    tipo_movimiento TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id),
    FOREIGN KEY (producto_id) REFERENCES productos (producto_id)
)
"""
)

# Tabla alertas
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS alertas (
    alerta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    tipo_alerta TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TEXT NOT NULL,
    estado INTEGER NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)


#### Ventas ####
# Tabla clientes
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    tipo_cliente_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    email TEXT,
    telefono TEXT,
    foto TEXT,
    fecha_creacion TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id),
    FOREIGN KEY (tipo_cliente_id) REFERENCES tipos_clientes (tipo_cliente_id
)
"""
)

# Tabla tipos_clientes
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tipos_clientes (
    tipo_cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    fecha_creacion TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)

# Tabla ventas
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS ventas (
    venta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    total REAL NOT NULL,
    metodo_pago TEXT NOT NULL,
    estado_pago TEXT NOT NULL,
    estado_envio TEXT NOT NULL,               
    tipo_venta TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (usuario_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes (cliente_id)
)
"""
)

# Tabla detalle_venta
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS detalle_venta (
    detalle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas (venta_id),
    FOREIGN KEY (producto_id) REFERENCES productos (producto_id)
)
"""
)

# Tabla descuentos
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS descuentos (
    descuento_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    tipo_descuento TEXT,
    porcentaje REAL NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    activo INTEGER NOT NULL,
    cliente_id INTEGER,
    producto_id INTEGER,
    FOREIGN KEY (producto_id) REFERENCES productos (producto_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes (cliente_id),
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)


#### Compras ####
# Tabla proveedores
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS proveedores (
    proveedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    ruc TEXT,
    telefono TEXT NOT NULL,
    email TEXT,
    foto TEXT,
    direccion TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id)
)
"""
)

# Tabla compras
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS compras (
    compra_id INTEGER PRIMARY KEY AUTOINCREMENT,
    negocio_id INTEGER NOT NULL,
    proveedor_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    total REAL NOT NULL,
    metodo_pago TEXT NOT NULL,
    estado_pago TEXT NOT NULL,
    estado_envio TEXT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id),
    FOREIGN KEY (proveedor_id) REFERENCES proveedores (proveedor_id)
)
"""
)

# Tabla detalle_compra
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS detalle_compra (
    detalle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    negocio_id INTEGER NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES negocios (negocio_id),
    FOREIGN KEY (compra_id) REFERENCES compras (compra_id),
    FOREIGN KEY (producto_id) REFERENCES productos (producto_id)
)
"""
)


# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()
