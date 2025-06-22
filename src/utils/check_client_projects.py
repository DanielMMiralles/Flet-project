import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def check_client_projects():
    """Verifica los proyectos de los clientes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("=== VERIFICACIÓN DE PROYECTOS DE CLIENTES ===\n")
        
        # Ver todos los clientes
        cursor.execute("SELECT * FROM Clientes")
        clients = cursor.fetchall()
        
        print("CLIENTES:")
        for client in clients:
            print(f"  ID: {client['id']}, Usuario: {client['id_usuario']}, Nombre: {client['nombre']}")
        
        print("\nSOLICITUDES:")
        cursor.execute("SELECT * FROM Solicitudes")
        requests = cursor.fetchall()
        
        for req in requests:
            print(f"  ID: {req['id']}, Cliente: {req['id_cliente']}, Producto: {req['id_producto']}, Estado: {req['estado']}")
        
        print("\nPROYECTOS CON SOLICITUDES APROBADAS:")
        cursor.execute("""
            SELECT p.nombre, s.id_cliente, s.estado, c.nombre as cliente_nombre
            FROM Producto p
            INNER JOIN Solicitudes s ON p.id = s.id_producto
            INNER JOIN Clientes c ON s.id_cliente = c.id
            WHERE s.estado = 'aprobada'
        """)
        
        approved_projects = cursor.fetchall()
        for proj in approved_projects:
            print(f"  Proyecto: {proj['nombre']}, Cliente: {proj['cliente_nombre']} (ID: {proj['id_cliente']})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_client_projects()