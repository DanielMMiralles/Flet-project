import os
import sys

# Añadir el directorio src al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_db_connection

def check_products():
    """Verifica si la tabla Producto existe y tiene registros"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si la tabla existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Producto';")
    if not cursor.fetchone():
        print("La tabla Producto no existe en la base de datos.")
        conn.close()
        return False
    
    # Obtener la estructura de la tabla
    cursor.execute("PRAGMA table_info(Producto)")
    columns = cursor.fetchall()
    print(f"Columnas en la tabla Producto: {[col[1] for col in columns]}")
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM Producto")
    count = cursor.fetchone()[0]
    print(f"La tabla Producto tiene {count} registros.")
    
    # Mostrar los primeros 5 registros si existen
    if count > 0:
        cursor.execute("SELECT * FROM Producto LIMIT 5")
        products = cursor.fetchall()
        print("\nPrimeros 5 productos:")
        for product in products:
            print(f"ID: {product['id'] if 'id' in product.keys() else 'N/A'}, "
                  f"Nombre: {product['nombre'] if 'nombre' in product.keys() else product['name'] if 'name' in product.keys() else 'N/A'}")
    
    conn.close()
    return count > 0

if __name__ == "__main__":
    print("Verificando productos en la base de datos...")
    has_products = check_products()
    print(f"\nResultado: {'La tabla Producto tiene registros' if has_products else 'La tabla Producto no tiene registros o no existe'}")