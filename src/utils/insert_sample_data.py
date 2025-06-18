import sqlite3
import os
from pathlib import Path
import datetime

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    base_dir = Path(__file__).parent.parent.parent
    db_path = os.path.join(base_dir, "storage", "data", "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn, db_path

def insert_sample_data():
    """Inserta datos de ejemplo en las tablas"""
    conn, db_path = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Insertando datos de ejemplo en: {db_path}")
    
    try:
        # Limpiar datos existentes
        cursor.execute("DELETE FROM Avances")
        cursor.execute("DELETE FROM Asignaciones")
        cursor.execute("DELETE FROM Solicitudes")
        cursor.execute("DELETE FROM Producto")
        cursor.execute("DELETE FROM Ingenieros")
        cursor.execute("DELETE FROM Clientes")
        cursor.execute("DELETE FROM Usuarios")
        
        # Reiniciar secuencias
        cursor.execute("DELETE FROM sqlite_sequence")
        
        print("Datos existentes eliminados")
        
        # 1. Insertar usuarios
        print("Insertando usuarios...")
        usuarios = [
            (1, "admin", "admin123", "admin"),
            (2, "cliente1", "cliente123", "cliente"),
            (3, "cliente2", "cliente123", "cliente"),
            (4, "ingeniero1", "ingeniero123", "ingeniero"),
            (5, "ingeniero2", "ingeniero123", "ingeniero"),
            (6, "ingeniero3", "ingeniero123", "ingeniero")
        ]
        cursor.executemany(
            "INSERT INTO Usuarios (id, usuario, password, rol) VALUES (?, ?, ?, ?)",
            usuarios
        )
        
        # 2. Insertar clientes
        print("Insertando clientes...")
        clientes = [
            (1, 2, "Empresa ABC", "contacto@abc.com", "555-1234"),
            (2, 3, "Corporación XYZ", "info@xyz.com", "555-5678")
        ]
        cursor.executemany(
            "INSERT INTO Clientes (id, id_usuario, nombre, email, telefono) VALUES (?, ?, ?, ?, ?)",
            clientes
        )
        
        # 3. Insertar ingenieros
        print("Insertando ingenieros...")
        ingenieros = [
            (1, 4, "Juan Pérez", "Desarrollo Web", 1),
            (2, 5, "Ana Gómez", "Desarrollo Móvil", 1),
            (3, 6, "Carlos Rodríguez", "Base de Datos", 1)
        ]
        cursor.executemany(
            "INSERT INTO Ingenieros (id, id_usuario, nombre, especialidad, disponible) VALUES (?, ?, ?, ?, ?)",
            ingenieros
        )
        
        # 4. Insertar productos
        print("Insertando productos...")
        productos = [
            (1, "Sistema de Gestión", 30, 2, "/assets/productos/sistema.jpg", "Sistema de gestión empresarial completo", "activo", 1),
            (2, "App Móvil", 45, 2, "/assets/productos/app.jpg", "Aplicación móvil multiplataforma", "pendiente", 1),
            (3, "Plataforma E-learning", 60, 3, "/assets/productos/elearning.jpg", "Plataforma de aprendizaje en línea", "completado", 2),
            (4, "Sistema de Inventario", 20, 1, "/assets/productos/inventario.jpg", "Sistema de control de inventario", "propuesta", 2)
        ]
        cursor.executemany(
            "INSERT INTO Producto (id, nombre, dias, cantidad_ing, imagen, descripcion, status, client_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            productos
        )
        
        # 5. Insertar solicitudes
        print("Insertando solicitudes...")
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        solicitudes = [
            (1, 1, 1, "2023-05-15", "Necesito un sistema de gestión para mi empresa", "aprobada"),
            (2, 1, 2, "2023-06-20", "Requiero una app móvil para mi negocio", "pendiente"),
            (3, 2, 3, "2023-03-10", "Necesitamos una plataforma de e-learning", "aprobada"),
            (4, 2, 4, "2023-07-05", "Sistema de inventario para nuestra tienda", "pendiente")
        ]
        cursor.executemany(
            "INSERT INTO Solicitudes (id, id_cliente, id_producto, fecha_solicitud, detalles, estado) VALUES (?, ?, ?, ?, ?, ?)",
            solicitudes
        )
        
        # 6. Insertar asignaciones
        print("Insertando asignaciones...")
        asignaciones = [
            (1, 1, 1, "2023-05-20", None),  # Juan Pérez asignado al Sistema de Gestión (activo)
            (2, 2, 1, "2023-05-20", None),  # Ana Gómez asignada al Sistema de Gestión (activo)
            (3, 3, 3, "2023-03-15", "2023-05-10")  # Carlos Rodríguez asignado a la Plataforma E-learning (completado)
        ]
        cursor.executemany(
            "INSERT INTO Asignaciones (id, id_ingeniero, id_producto, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?, ?)",
            asignaciones
        )
        
        # 7. Insertar avances
        print("Insertando avances...")
        avances = [
            (1, 1, 1, "2023-05-25", "Inicio del desarrollo", 10),
            (2, 1, 1, "2023-06-10", "Desarrollo de módulos principales", 40),
            (3, 1, 1, "2023-06-25", "Implementación de funcionalidades avanzadas", 70),
            (4, 2, 1, "2023-05-25", "Diseño de la interfaz", 15),
            (5, 2, 1, "2023-06-15", "Implementación de la interfaz", 50),
            (6, 3, 3, "2023-03-20", "Inicio del desarrollo", 20),
            (7, 3, 3, "2023-04-10", "Desarrollo de módulos principales", 50),
            (8, 3, 3, "2023-05-05", "Finalización del proyecto", 100)
        ]
        cursor.executemany(
            "INSERT INTO Avances (id, id_producto, id_ingeniero, fecha, descripcion, porcentaje) VALUES (?, ?, ?, ?, ?, ?)",
            avances
        )
        
        # Actualizar disponibilidad de ingenieros según asignaciones
        print("Actualizando disponibilidad de ingenieros...")
        cursor.execute("""
        UPDATE Ingenieros SET disponible = 0
        WHERE id IN (
            SELECT DISTINCT id_ingeniero FROM Asignaciones WHERE fecha_fin IS NULL
        )
        """)
        
        conn.commit()
        print("Datos de ejemplo insertados correctamente")
        
        # Verificar datos insertados
        print("\nVerificando datos insertados:")
        
        cursor.execute("SELECT COUNT(*) FROM Usuarios")
        print(f"Usuarios: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Clientes")
        print(f"Clientes: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Ingenieros")
        print(f"Ingenieros: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Producto")
        print(f"Productos: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Solicitudes")
        print(f"Solicitudes: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Asignaciones")
        print(f"Asignaciones: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Avances")
        print(f"Avances: {cursor.fetchone()[0]}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error al insertar datos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    insert_sample_data()