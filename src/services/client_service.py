import sqlite3
import os
from pathlib import Path
import datetime
from models.client import Client
from models.request import Request
from utils.database import get_db_connection

def get_client_by_user_id(user_id):
    """Obtiene un cliente por su ID de usuario"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Clientes WHERE id_usuario = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        client = Client.from_db_row(row)
        conn.close()
        return client
    
    except Exception as e:
        print(f"Error obteniendo cliente: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_request(client_id, product_id, details, desired_date=None):
    """Crea una nueva solicitud de un cliente para un producto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que el cliente existe
        cursor.execute("SELECT * FROM Clientes WHERE id = ?", (client_id,))
        if not cursor.fetchone():
            print(f"Error: Cliente con ID {client_id} no existe")
            conn.close()
            return False
        
        # Verificar que el producto existe
        cursor.execute("SELECT * FROM Producto WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            print(f"Error: Producto con ID {product_id} no existe")
            conn.close()
            return False
        
        # Obtener fecha actual si no se proporciona una fecha deseada
        request_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Insertar la solicitud
        cursor.execute(
            "INSERT INTO Solicitudes (id_cliente, id_producto, fecha_solicitud, detalles, estado) VALUES (?, ?, ?, ?, ?)",
            (client_id, product_id, request_date, details, "pendiente")
        )
        
        conn.commit()
        request_id = cursor.lastrowid
        conn.close()
        
        print(f"Solicitud creada con ID: {request_id}")
        return True
    
    except Exception as e:
        print(f"Error creando solicitud: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_client_requests(client_id):
    """Obtiene todas las solicitudes de un cliente"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, p.nombre as producto_nombre, p.descripcion as producto_descripcion
            FROM Solicitudes s
            JOIN Producto p ON s.id_producto = p.id
            WHERE s.id_cliente = ?
            ORDER BY s.fecha_solicitud DESC
        """, (client_id,))
        
        rows = cursor.fetchall()
        requests = []
        
        for row in rows:
            request = Request.from_db_row(row)
            request_dict = request.to_dict()
            request_dict["product_name"] = row["producto_nombre"]
            request_dict["product_description"] = row["producto_descripcion"]
            requests.append(request_dict)
        
        conn.close()
        return requests
    
    except Exception as e:
        print(f"Error obteniendo solicitudes del cliente: {e}")
        import traceback
        traceback.print_exc()
        return []