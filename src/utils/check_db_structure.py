import sqlite3
import os
from pathlib import Path

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    base_dir = Path(__file__).parent.parent.parent
    db_path = os.path.join(base_dir, "storage", "data", "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn, db_path

def check_db_structure():
    """Verifica la estructura de la base de datos"""
    conn, db_path = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Verificando estructura de la base de datos en: {db_path}")
    
    # Obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\nTablas en la base de datos:")
    for table in tables:
        print(f"- {table['name']}")
    
    print("\nEstructura de las tablas:")
    for table in tables:
        table_name = table['name']
        print(f"\nTabla: {table_name}")
        print("-" * 40)
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"{col['cid']}: {col['name']} ({col['type']})")
    
    # Verificar compatibilidad con los modelos
    print("\nVerificando compatibilidad con los modelos:")
    
    # Verificar tabla Usuarios
    if any(table['name'] == 'Usuarios' for table in tables):
        print("\nModelo User es compatible con la tabla Usuarios")
    else:
        print("\nAdvertencia: No se encontró la tabla Usuarios para el modelo User")
    
    # Verificar tabla Clientes
    if any(table['name'] == 'Clientes' for table in tables):
        print("Modelo Client es compatible con la tabla Clientes")
    else:
        print("Advertencia: No se encontró la tabla Clientes para el modelo Client")
    
    # Verificar tabla Ingenieros
    if any(table['name'] == 'Ingenieros' for table in tables):
        print("Modelo Engineer es compatible con la tabla Ingenieros")
    else:
        print("Advertencia: No se encontró la tabla Ingenieros para el modelo Engineer")
    
    # Verificar tabla Producto
    if any(table['name'] == 'Producto' for table in tables) or any(table['name'] == 'productos' for table in tables):
        print("Modelo Product es compatible con la tabla Producto/productos")
    else:
        print("Advertencia: No se encontró la tabla Producto/productos para el modelo Product")
    
    # Verificar tabla Solicitudes
    if any(table['name'] == 'Solicitudes' for table in tables):
        print("Modelo Request es compatible con la tabla Solicitudes")
    else:
        print("Advertencia: No se encontró la tabla Solicitudes para el modelo Request")
    
    # Verificar tabla Asignaciones
    if any(table['name'] == 'Asignaciones' for table in tables):
        print("Modelo Assignment es compatible con la tabla Asignaciones")
    else:
        print("Advertencia: No se encontró la tabla Asignaciones para el modelo Assignment")
    
    # Verificar tabla Avances
    if any(table['name'] == 'Avances' for table in tables):
        print("Modelo Progress es compatible con la tabla Avances")
    else:
        print("Advertencia: No se encontró la tabla Avances para el modelo Progress")
    
    conn.close()

if __name__ == "__main__":
    check_db_structure()