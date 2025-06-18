import sqlite3
import os
from pathlib import Path

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    base_dir = Path(__file__).parent.parent.parent
    db_path = os.path.join(base_dir, "storage", "data", "database.db")
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn, db_path

def setup_database():
    """Configura la estructura de la base de datos"""
    conn, db_path = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Configurando base de datos en: {db_path}")
    
    # Verificar tablas existentes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    print(f"Tablas existentes: {tables}")
    
    # Crear tabla de Usuarios si no existe
    if 'Usuarios' not in tables:
        print("Creando tabla Usuarios...")
        cursor.execute('''
        CREATE TABLE Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        ''')
        
        # Insertar usuarios de prueba
        cursor.execute('''
        INSERT INTO Usuarios (usuario, password, rol) VALUES 
        ('admin', 'admin123', 'admin'),
        ('cliente', 'cliente123', 'cliente'),
        ('ingeniero', 'ingeniero123', 'ingeniero')
        ''')
    
    # Crear tabla de Clientes si no existe
    if 'Clientes' not in tables:
        print("Creando tabla Clientes...")
        cursor.execute('''
        CREATE TABLE Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            nombre TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
        )
        ''')
        
        # Insertar cliente de prueba
        cursor.execute('''
        INSERT INTO Clientes (id_usuario, nombre, email, telefono) VALUES 
        (2, 'Cliente Ejemplo', 'cliente@ejemplo.com', '123456789')
        ''')
    
    # Crear tabla de Ingenieros si no existe
    if 'Ingenieros' not in tables:
        print("Creando tabla Ingenieros...")
        cursor.execute('''
        CREATE TABLE Ingenieros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            nombre TEXT NOT NULL,
            especialidad TEXT,
            disponible BOOLEAN DEFAULT 1,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
        )
        ''')
        
        # Insertar ingeniero de prueba
        cursor.execute('''
        INSERT INTO Ingenieros (id_usuario, nombre, especialidad, disponible) VALUES 
        (3, 'Ingeniero Ejemplo', 'Desarrollo Web', 1)
        ''')
    
    # Crear tabla de Productos si no existe
    product_table = None
    if 'Producto' in tables:
        product_table = 'Producto'
    elif 'productos' in tables:
        product_table = 'productos'
    
    if not product_table:
        print("Creando tabla Producto...")
        cursor.execute('''
        CREATE TABLE Producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dias INTEGER NOT NULL,
            cantidad_ing INTEGER NOT NULL,
            imagen TEXT,
            descripcion TEXT,
            status TEXT DEFAULT 'propuesta',
            client_id INTEGER,
            requirements TEXT,
            FOREIGN KEY (client_id) REFERENCES Clientes(id)
        )
        ''')
        product_table = 'Producto'
        
        # Insertar productos de prueba
        cursor.execute('''
        INSERT INTO Producto (nombre, dias, cantidad_ing, imagen, descripcion, status, client_id) VALUES 
        ('Sistema de Gestión', 30, 3, '/assets/productos/sistema.jpg', 'Sistema de gestión empresarial', 'activo', 1),
        ('App Móvil', 45, 4, '/assets/productos/app.jpg', 'Aplicación móvil multiplataforma', 'pendiente', 1),
        ('Plataforma E-learning', 60, 5, '/assets/productos/elearning.jpg', 'Plataforma de aprendizaje en línea', 'completado', 1)
        ''')
    
    # Verificar y actualizar estructura de la tabla Producto si es necesario
    cursor.execute(f"PRAGMA table_info({product_table})")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'status' not in columns:
        print(f"Añadiendo columna 'status' a la tabla {product_table}...")
        cursor.execute(f"ALTER TABLE {product_table} ADD COLUMN status TEXT DEFAULT 'propuesta'")
    
    if 'client_id' not in columns:
        print(f"Añadiendo columna 'client_id' a la tabla {product_table}...")
        cursor.execute(f"ALTER TABLE {product_table} ADD COLUMN client_id INTEGER REFERENCES Clientes(id)")
    
    # Crear tabla de Solicitudes si no existe
    if 'Solicitudes' not in tables:
        print("Creando tabla Solicitudes...")
        cursor.execute('''
        CREATE TABLE Solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            fecha_solicitud TEXT NOT NULL,
            detalles TEXT,
            estado TEXT DEFAULT 'pendiente',
            FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
            FOREIGN KEY (id_producto) REFERENCES Producto(id)
        )
        ''')
        
        # Insertar solicitudes de prueba
        cursor.execute('''
        INSERT INTO Solicitudes (id_cliente, id_producto, fecha_solicitud, detalles, estado) VALUES 
        (1, 1, '2023-05-15', 'Necesito un sistema de gestión para mi empresa', 'aprobada'),
        (1, 2, '2023-06-20', 'Requiero una app móvil para mi negocio', 'pendiente')
        ''')
    
    # Crear tabla de Asignaciones si no existe
    if 'Asignaciones' not in tables:
        print("Creando tabla Asignaciones...")
        cursor.execute('''
        CREATE TABLE Asignaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ingeniero INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT,
            FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id),
            FOREIGN KEY (id_producto) REFERENCES Producto(id)
        )
        ''')
        
        # Insertar asignaciones de prueba
        cursor.execute('''
        INSERT INTO Asignaciones (id_ingeniero, id_producto, fecha_inicio, fecha_fin) VALUES 
        (1, 1, '2023-05-20', NULL),
        (1, 3, '2023-03-10', '2023-05-10')
        ''')
    
    # Crear tabla de Avances si no existe
    if 'Avances' not in tables:
        print("Creando tabla Avances...")
        cursor.execute('''
        CREATE TABLE Avances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            id_ingeniero INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            porcentaje INTEGER NOT NULL,
            FOREIGN KEY (id_producto) REFERENCES Producto(id),
            FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id)
        )
        ''')
        
        # Insertar avances de prueba
        cursor.execute('''
        INSERT INTO Avances (id_producto, id_ingeniero, fecha, descripcion, porcentaje) VALUES 
        (1, 1, '2023-05-25', 'Inicio del desarrollo', 10),
        (1, 1, '2023-06-10', 'Desarrollo de módulos principales', 40),
        (1, 1, '2023-06-25', 'Implementación de funcionalidades avanzadas', 70),
        (3, 1, '2023-03-15', 'Inicio del desarrollo', 20),
        (3, 1, '2023-04-10', 'Desarrollo de módulos principales', 50),
        (3, 1, '2023-05-05', 'Finalización del proyecto', 100)
        ''')
    
    conn.commit()
    conn.close()
    print("Base de datos configurada correctamente.")

if __name__ == "__main__":
    setup_database()