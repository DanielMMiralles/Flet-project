import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def update_product_images():
    """Asigna todas las imágenes disponibles a los productos sin imagen"""
    
    # Lista de todas las imágenes disponibles
    available_images = [
        "/assets/productos/artesanal.jpg",
        "/assets/productos/delivery.jpg", 
        "/assets/productos/elearning.jpg",
        "/assets/productos/finanzas.jpg",
        "/assets/productos/fitness.jpg",
        "/assets/productos/flotas.jpg",
        "/assets/productos/hotel.jpg",
        "/assets/productos/inventario.jpg",
        "/assets/productos/iot.jpg",
        "/assets/productos/noticias.jpg",
        "/assets/productos/redsocial.jpg",
        "/assets/productos/rh.jpg",
        "/assets/productos/riego.jpg",
        "/assets/productos/turismo.jpg",
        "/assets/productos/turnos.jpg"
    ]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener todos los productos
        cursor.execute("SELECT id, nombre, imagen FROM Producto")
        products = cursor.fetchall()
        
        updated_count = 0
        image_index = 0
        
        for product in products:
            product_id = product["id"]
            product_name = product["nombre"]
            current_image = product["imagen"]
            
            # Asignar imagen a todos los productos para usar todas las imágenes
            if image_index < len(available_images):
                new_image = available_images[image_index]
                cursor.execute(
                    "UPDATE Producto SET imagen = ? WHERE id = ?",
                    (new_image, product_id)
                )
                print(f"Asignado: {product_name} -> {new_image}")
                updated_count += 1
                image_index += 1
        
        conn.commit()
        conn.close()
        
        print(f"\nActualizacion completada: {updated_count} productos actualizados")
        return True
        
    except Exception as e:
        print(f"Error actualizando imagenes: {e}")
        return False

if __name__ == "__main__":
    update_product_images()