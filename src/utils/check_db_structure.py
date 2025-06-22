import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def check_database_structure():
    """Revisa la estructura de la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("=== ESTRUCTURA DE LA BASE DE DATOS ===")
        
        for table in tables:
            table_name = table[0]
            print(f"\n--- TABLA: {table_name} ---")
            
            # Obtener estructura de la tabla
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("Columnas:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Mostrar algunos datos de ejemplo
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            
            if rows:
                print("Datos de ejemplo:")
                for row in rows:
                    print(f"  {dict(row)}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error revisando estructura: {e}")

if __name__ == "__main__":
    check_database_structure()