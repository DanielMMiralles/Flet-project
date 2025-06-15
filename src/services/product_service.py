import sqlite3
import os
from pathlib import Path
from models.product import Product

def get_products(client_id: int = None) -> list[Product]:
    """Obtiene todos los productos de la base de datos"""
    try:
        # Obtener la ruta base del proyecto
        base_dir = Path(__file__).parent.parent.parent
        
        # Construir la ruta a la base de datos
        db_path = os.path.join(base_dir, "storage", "data", "database.db")
        
        print(f"Conectando a la base de datos en: {db_path}")
        
        # Verificar si el archivo existe
        if not os.path.exists(db_path):
            print(f"¡Advertencia! La base de datos no existe en: {db_path}")
            # Buscar la base de datos en ubicaciones alternativas
            alt_path = os.path.join(base_dir, "data", "storage", "database.db")
            if os.path.exists(alt_path):
                db_path = alt_path
                print(f"Base de datos encontrada en ubicación alternativa: {db_path}")
        
        conn = sqlite3.connect(db_path)
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
                return []
        
        print(f"Usando tabla: {table_name}")
        
        # Obtener la estructura de la tabla
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"Estructura de la tabla {table_name}:")
        for i, col in enumerate(columns):
            print(f"  {i}: {col[1]} ({col[2]})")
        
        query = f"SELECT * FROM {table_name}"
        params = ()
        
        if client_id:
            id_column = "client_id" if "client_id" in [col[1] for col in columns] else "id_cliente"
            query += f" WHERE {id_column} = ?"
            params = (client_id,)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        print(f"Productos encontrados: {len(rows)}")
        
        # Imprimir la primera fila para depuración
        if rows:
            print(f"Primera fila: {rows[0]}")
        
        conn.close()
        
        return [Product.from_db_row(row) for row in rows]
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        import traceback
        traceback.print_exc()
        return []
