import sqlite3
import os
from pathlib import Path
from models.request import Request
from models.product import Product
from models.client import Client
from utils.database import get_db_connection

def get_all_requests():
    """Obtiene todas las solicitudes de la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, c.nombre as cliente_nombre, p.nombre as producto_nombre 
            FROM Solicitudes s
            JOIN Clientes c ON s.id_cliente = c.id
            JOIN Producto p ON s.id_producto = p.id
            ORDER BY s.fecha_solicitud DESC
        """)
        
        rows = cursor.fetchall()
        requests = []
        
        for row in rows:
            try:
                request = Request.from_db_row(row)
                request_dict = request.to_dict()
                request_dict["client_name"] = row["cliente_nombre"]
                request_dict["product_name"] = row["producto_nombre"]
                requests.append(request_dict)
            except Exception as e:
                print(f"Error procesando solicitud: {e}")
        
        conn.close()
        return requests
    
    except Exception as e:
        print(f"Error obteniendo solicitudes: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_pending_requests():
    """Obtiene las solicitudes pendientes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, c.nombre as cliente_nombre, p.nombre as producto_nombre 
            FROM Solicitudes s
            JOIN Clientes c ON s.id_cliente = c.id
            JOIN Producto p ON s.id_producto = p.id
            WHERE s.estado = 'pendiente'
            ORDER BY s.fecha_solicitud DESC
        """)
        
        rows = cursor.fetchall()
        requests = []
        
        for row in rows:
            try:
                request = Request.from_db_row(row)
                request_dict = request.to_dict()
                request_dict["client_name"] = row["cliente_nombre"]
                request_dict["product_name"] = row["producto_nombre"]
                requests.append(request_dict)
            except Exception as e:
                print(f"Error procesando solicitud: {e}")
        
        conn.close()
        return requests
    
    except Exception as e:
        print(f"Error obteniendo solicitudes pendientes: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_request_details(request_id):
    """Obtiene los detalles de una solicitud específica"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.*, c.nombre as cliente_nombre, c.email as cliente_email, c.telefono as cliente_telefono,
                   p.nombre as producto_nombre, p.descripcion as producto_descripcion, p.dias, p.cantidad_ing
            FROM Solicitudes s
            JOIN Clientes c ON s.id_cliente = c.id
            JOIN Producto p ON s.id_producto = p.id
            WHERE s.id = ?
        """, (request_id,))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        request_details = {
            "id": row["id"],
            "client_id": row["id_cliente"],
            "product_id": row["id_producto"],
            "request_date": row["fecha_solicitud"],
            "details": row["detalles"],
            "status": row["estado"],
            "client_name": row["cliente_nombre"],
            "client_email": row["cliente_email"],
            "client_phone": row["cliente_telefono"],
            "product_name": row["producto_nombre"],
            "product_description": row["producto_descripcion"],
            "product_days": row["dias"],
            "product_engineers": row["cantidad_ing"]
        }
        
        conn.close()
        return request_details
    
    except Exception as e:
        print(f"Error obteniendo detalles de la solicitud: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_request_status(request_id, new_status):
    """Actualiza el estado de una solicitud"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE Solicitudes SET estado = ? WHERE id = ?",
            (new_status, request_id)
        )
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error actualizando estado de solicitud: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_request(client_id, product_id, details, desired_date=None):
    """Crea una nueva solicitud"""
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
        request_date = desired_date or datetime.datetime.now().strftime("%Y-%m-%d")
        
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