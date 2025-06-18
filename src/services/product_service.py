import sqlite3
import os
from pathlib import Path
from models.product import Product
from utils.database import get_db_connection

def get_products(client_id: int = None) -> list[Product]:
    """Obtiene todos los productos de la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Producto'")
        if cursor.fetchone():
            table_name = "Producto"
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
            if cursor.fetchone():
                table_name = "productos"
            else:
                print("¡Error! No se encontró la tabla de productos")
                conn.close()
                return []
        
        query = f"SELECT * FROM {table_name}"
        params = ()
        
        if client_id:
            id_column = "client_id" if "client_id" in get_column_names(cursor, table_name) else "id_cliente"
            query += f" WHERE {id_column} = ?"
            params = (client_id,)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        return [Product.from_db_row(row) for row in rows]
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_product_by_id(product_id: int) -> Product:
    """Obtiene un producto por su ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Producto'")
        if cursor.fetchone():
            table_name = "Producto"
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
            if cursor.fetchone():
                table_name = "productos"
            else:
                print("¡Error! No se encontró la tabla de productos")
                conn.close()
                return None
        
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        product = Product.from_db_row(row)
        conn.close()
        return product
    except Exception as e:
        print(f"Error al obtener producto: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_column_names(cursor, table_name):
    """Obtiene los nombres de las columnas de una tabla"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [col[1] for col in cursor.fetchall()]