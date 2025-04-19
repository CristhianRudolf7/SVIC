import sqlite3

conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()
from datetime import datetime

fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Insertar negocio de prueba si no existe
cursor.execute('''
INSERT INTO negocios (nombre, sector, pais, region, ciudad, direccion, telefono, RUC, foto, descripcion, tipo_suscripcion, fecha_creacion)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', ('Negocio Ejemplo', 'Retail', 'Perú', 'Lima', 'Lima', 'Av. Siempre Viva 123', '123456789', '12345678901', '', 'Negocio de prueba', 'Gratis', fecha_actual))

# Obtener el ID del negocio recién insertado
negocio_id = cursor.lastrowid

# Insertar usuarios con roles del 1 al 4
usuarios = [
    ('Juan Pérez', '12345678', 'juan1@example.com', 'pass1', '1', '900000001'),
    ('Ana López', '87654321', 'ana2@example.com', 'pass2', '2', '900000002'),
    ('Luis Torres', '11223344', 'luis3@example.com', 'pass3', '3', '900000003'),
    ('Carmen Díaz', '44332211', 'carmen4@example.com', 'pass4', '4', '900000004')
]

for nombre, dni, email, password, rol, phone in usuarios:
    cursor.execute('''
    INSERT INTO usuarios (negocio_id, nombre, dni, email, password, rol, PHONE, fecha_creacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (negocio_id, nombre, dni, email, password, rol, phone, fecha_actual))
conexion.commit()
conexion.close()