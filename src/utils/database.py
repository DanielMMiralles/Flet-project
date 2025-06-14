import sqlite3
import os
from pathlib import Path

def get_db_connection():
    # Obtener la ruta base del proyecto (independiente de dónde se ejecute)
    base_dir = Path(__file__).parent.parent.parent
    
    # Usar específicamente la ruta storage/data/database.db
    db_path = os.path.join(base_dir, "storage", "data", "database.db")
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def list_all_users():
    """Función para listar todos los usuarios en la base de datos"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buscar la tabla de usuarios
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios';")
    if not cursor.fetchone():
        print("No se encontró la tabla Usuarios")
        conn.close()
        return []
    
    # Obtener todos los usuarios
    cursor.execute("SELECT * FROM Usuarios")
    users = cursor.fetchall()
    
    # Mostrar información detallada
    print(f"Se encontraron {len(users)} usuarios en la base de datos:")
    for user in users:
        print(f"ID: {user['id']}, Usuario: {user['usuario']}, Password: {user['password']}, Rol: {user['rol']}")
    
    conn.close()
    return users

def authenticate_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar la estructura de la tabla
    cursor.execute("PRAGMA table_info(Usuarios)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print(f"Columnas en la tabla Usuarios: {column_names}")
    
    # Primero, listar todos los usuarios para diagnóstico
    cursor.execute("SELECT * FROM Usuarios")
    all_users = cursor.fetchall()
    print(f"Total de usuarios en la base de datos: {len(all_users)}")
    
    # Ejecutar la consulta sin el filtro de rol primero para ver si el usuario y contraseña son correctos
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = ? AND password = ?", (username, password))
    user_without_role = cursor.fetchone()
    
    if user_without_role:
        print(f"Usuario encontrado con credenciales correctas. Rol en la BD: {user_without_role['rol']}, Rol proporcionado: {role}")
    
    # Ahora ejecutar la consulta completa con el rol
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = ? AND password = ? AND rol = ?", 
                  (username, password, role))
    user = cursor.fetchone()
    
    conn.close()
    return user

def register_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el usuario ya existe
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False  # Usuario ya existe

    # Insertar el nuevo usuario
    cursor.execute("INSERT INTO Usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                   (username, password, role))
    conn.commit()
    conn.close()
    return True  # Registro exitoso