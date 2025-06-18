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

def update_db_structure():
    """Actualiza la estructura de la base de datos"""
    conn, db_path = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Actualizando estructura de la base de datos en: {db_path}")
    
    # Verificar tablas existentes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    print(f"Tablas existentes: {tables}")
    
    # 1. Eliminar tablas antiguas y duplicadas
    old_tables = ["Cliente", "Ingeniero", "Asignacion", "Avance", "Solicitud"]
    for table in old_tables:
        if table in tables:
            print(f"Eliminando tabla antigua: {table}")
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # 2. Actualizar la tabla Asignaciones para usar ingenieros directamente
    if "Asignaciones" in tables:
        print("Actualizando tabla Asignaciones...")
        
        # Verificar si ya tiene la estructura correcta
        cursor.execute("PRAGMA table_info(Asignaciones)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "id_equipo" in columns and "id_ingeniero" not in columns:
            print("Creando nueva tabla Asignaciones con la estructura correcta...")
            
            # Crear tabla temporal con la estructura correcta
            cursor.execute("""
            CREATE TABLE Asignaciones_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_ingeniero INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT,
                FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id),
                FOREIGN KEY (id_producto) REFERENCES Producto(id)
            )
            """)
            
            # Migrar datos si es posible (usando Miembros_Equipo para obtener ingenieros)
            if "Miembros_Equipo" in tables:
                print("Migrando datos de asignaciones...")
                cursor.execute("""
                INSERT INTO Asignaciones_new (id_ingeniero, id_producto, fecha_inicio, fecha_fin)
                SELECT me.id_ingeniero, a.id_producto, a.fecha_inicio, a.fecha_fin
                FROM Asignaciones a
                JOIN Miembros_Equipo me ON a.id_equipo = me.id_equipo
                """)
            
            # Eliminar tabla antigua y renombrar la nueva
            cursor.execute("DROP TABLE Asignaciones")
            cursor.execute("ALTER TABLE Asignaciones_new RENAME TO Asignaciones")
            
            print("Tabla Asignaciones actualizada correctamente")
        else:
            print("La tabla Asignaciones ya tiene la estructura correcta")
    else:
        print("Creando tabla Asignaciones...")
        cursor.execute("""
        CREATE TABLE Asignaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ingeniero INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT,
            FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id),
            FOREIGN KEY (id_producto) REFERENCES Producto(id)
        )
        """)
    
    # 3. Eliminar tablas de equipos si ya no se necesitan
    team_tables = ["Equipos", "Miembros_Equipo"]
    for table in team_tables:
        if table in tables:
            print(f"Eliminando tabla de equipos: {table}")
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # 4. Verificar y crear tablas necesarias si no existen
    # Tabla Usuarios
    if "Usuarios" not in tables:
        print("Creando tabla Usuarios...")
        cursor.execute("""
        CREATE TABLE Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """)
    
    # Tabla Clientes
    if "Clientes" not in tables:
        print("Creando tabla Clientes...")
        cursor.execute("""
        CREATE TABLE Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            nombre TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
        )
        """)
    
    # Tabla Ingenieros
    if "Ingenieros" not in tables:
        print("Creando tabla Ingenieros...")
        cursor.execute("""
        CREATE TABLE Ingenieros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            nombre TEXT NOT NULL,
            especialidad TEXT,
            disponible BOOLEAN DEFAULT 1,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
        )
        """)
    
    # Tabla Producto
    if "Producto" not in tables:
        print("Creando tabla Producto...")
        cursor.execute("""
        CREATE TABLE Producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dias INTEGER NOT NULL,
            cantidad_ing INTEGER NOT NULL,
            imagen TEXT,
            descripcion TEXT,
            status TEXT DEFAULT 'propuesta',
            client_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES Clientes(id)
        )
        """)
    
    # Tabla Solicitudes
    if "Solicitudes" not in tables:
        print("Creando tabla Solicitudes...")
        cursor.execute("""
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
        """)
    
    # Tabla Avances
    if "Avances" not in tables:
        print("Creando tabla Avances...")
        cursor.execute("""
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
        """)
    
    conn.commit()
    conn.close()
    print("Estructura de la base de datos actualizada correctamente.")

if __name__ == "__main__":
    update_db_structure()