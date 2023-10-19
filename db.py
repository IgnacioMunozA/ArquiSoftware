import sqlite3
from datetime import datetime
def create_database_and_tables():
    # Esto creará un archivo 'mi_database.db' si no existe, y se conectará a él si ya existe
    conn = sqlite3.connect('db/vise.db')
    
    cursor = conn.cursor()
    
    # Crear la tabla productos si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        estado TEXT NOT NULL,
        ubicacion_bodega TEXT NOT NULL,
        stock_actual INTEGER NOT NULL,
        stock_minimo INTEGER NOT NULL
    );
    ''')

    # Crear la tabla usuarios si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL,
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL                                
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historialcambios (
        id INTEGER PRIMARY KEY,
        id_producto INTEGER NOT NULL,
        fecha_cambio TIMESTAMP NOT NULL,
        detalles_cambio TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedor (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL
    );
    ''')


    
    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect('db/vise.db')
    cursor = conn.cursor()

    # Insertar datos en la tabla 'productos'
    productos = [
        ('Tornillo', 0.5, 'Activo', 'Bodega A', 500, 50),
        ('Martillo', 10.0, 'Activo', 'Bodega B', 100, 10),
        ('Llave inglesa', 25.0, 'Activo', 'Bodega A', 150, 15),
        ('Sierra', 30.0, 'Inactivo', 'Bodega C', 80, 8),
        ('Broca', 5.0, 'Activo', 'Bodega B', 200, 20)
    ]

    cursor.executemany('''
    INSERT INTO productos (nombre, precio, estado, ubicacion_bodega, stock_actual, stock_minimo)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', productos)

    # Insertar datos en la tabla 'usuarios'
    usuarios = [
        ('Juan', 'juan@example.com', 'password_hash1', 'Admin'),
        ('Maria', 'maria@example.com', 'password_hash2', 'Empleado'),
        ('Pedro', 'pedro@example.com', 'password_hash3', 'Empleado'),
        ('Lucia', 'lucia@example.com', 'password_hash4', 'Admin'),
        ('Carlos', 'carlos@example.com', 'password_hash5', 'Empleado')
    ]

    cursor.executemany('''
    INSERT INTO usuarios (nombre, correo, contrasena, rol)
    VALUES (?, ?, ?, ?)
    ''', usuarios)

    # Insertar datos en la tabla 'historialcambios'
    cambios = [
        (1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Cambio de precio de 0.5 a 0.55'),
        (2, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Cambio de ubicación a Bodega C'),
        (3, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Cambio de stock mínimo a 20'),
        (4, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Producto inactivo por falta de stock'),
        (5, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Nuevo producto añadido')
    ]

    cursor.executemany('''
    INSERT INTO historialcambios (id_producto, fecha_cambio, detalles_cambio)
    VALUES (?, ?, ?)
    ''', cambios)

    # Insertar datos en la tabla 'proveedor'
    proveedores = [
        ('ProveeTodo', '555-1234', 'contacto@proveetodo.com'),
        ('Suministros SA', '555-5678', 'info@suministros.com'),
        ('Ferretería Central', '555-9876', 'ventas@fcentral.com'),
        ('Herramientas Elite', '555-4321', 'soporte@helite.com'),
        ('ConstruRápido', '555-1111', 'atencion@construrapido.com')
    ]

    cursor.executemany('''
    INSERT INTO proveedor (nombre, telefono, correo)
    VALUES (?, ?, ?)
    ''', proveedores)

    conn.commit()
    conn.close()

# Ejecutar la función para insertar los datos de ejemplo


# Ejecutar la función para crear la base de datos y las tablas
create_database_and_tables()
insert_sample_data()