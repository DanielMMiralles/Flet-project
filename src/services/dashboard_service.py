import sqlite3
import os
from pathlib import Path
from models.product import Product
from models.client import Client
from models.engineer import Engineer
from models.request import Request
from models.assignment import Assignment
from models.progress import Progress

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    base_dir = Path(__file__).parent.parent.parent
    db_path = os.path.join(base_dir, "storage", "data", "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_dashboard_data():
    """Obtiene los datos necesarios para el dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Datos para el dashboard
        dashboard_data = {
            "active_projects": 0,
            "pending_requests": 0,
            "assigned_engineers": 0,
            "completed_projects": 0,
            "recent_projects": []
        }
        
        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"Tablas disponibles: {tables}")
        
        # Contar proyectos activos
        if 'Producto' in tables or 'productos' in tables:
            table_name = 'Producto' if 'Producto' in tables else 'productos'
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE status='activo'")
            dashboard_data["active_projects"] = cursor.fetchone()[0]
        
        # Contar solicitudes pendientes
        if 'Solicitudes' in tables:
            cursor.execute("SELECT COUNT(*) FROM Solicitudes WHERE estado='pendiente'")
            dashboard_data["pending_requests"] = cursor.fetchone()[0]
        
        # Contar ingenieros asignados
        if 'Asignaciones' in tables:
            cursor.execute("SELECT COUNT(DISTINCT id_ingeniero) FROM Asignaciones WHERE fecha_fin IS NULL")
            dashboard_data["assigned_engineers"] = cursor.fetchone()[0]
        
        # Contar proyectos completados
        if 'Producto' in tables or 'productos' in tables:
            table_name = 'Producto' if 'Producto' in tables else 'productos'
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE status='completado'")
            dashboard_data["completed_projects"] = cursor.fetchone()[0]
        
        # Obtener proyectos recientes
        if 'Producto' in tables or 'productos' in tables:
            table_name = 'Producto' if 'Producto' in tables else 'productos'
            cursor.execute(f"""
                SELECT p.*, c.nombre as cliente_nombre 
                FROM {table_name} p
                LEFT JOIN Clientes c ON p.client_id = c.id
                ORDER BY p.id DESC LIMIT 5
            """)
            
            rows = cursor.fetchall()
            projects = []
            
            for row in rows:
                try:
                    # Crear objeto Product
                    product = None
                    try:
                        product = Product.from_db_row(row)
                    except Exception as e:
                        print(f"Error creando Product: {e}")
                        product = Product(
                            id=row["id"],
                            name=row["nombre"] if "nombre" in row.keys() else "",
                            description=row["descripcion"] if "descripcion" in row.keys() else "",
                            status=row["status"] if "status" in row.keys() else "pendiente"
                        )
                    
                    # Obtener cliente
                    client_name = row["cliente_nombre"] if "cliente_nombre" in row.keys() else "Cliente no asignado"
                    
                    # Obtener ingenieros asignados
                    engineers_assigned = "Sin asignar"
                    if 'Asignaciones' in tables and 'Ingenieros' in tables:
                        cursor.execute("""
                            SELECT GROUP_CONCAT(i.nombre, ', ') as nombres
                            FROM Ingenieros i
                            JOIN Asignaciones a ON i.id = a.id_ingeniero
                            WHERE a.id_producto = ?
                        """, (product.id,))
                        engineers_row = cursor.fetchone()
                        if engineers_row and engineers_row["nombres"]:
                            engineers_assigned = engineers_row["nombres"]
                    
                    # Obtener progreso
                    progress = 0.0
                    if 'Avances' in tables:
                        cursor.execute("""
                            SELECT MAX(porcentaje) as maximo FROM Avances
                            WHERE id_producto = ?
                        """, (product.id,))
                        progress_row = cursor.fetchone()
                        if progress_row and progress_row["maximo"]:
                            progress = float(progress_row["maximo"]) / 100.0
                    
                    # Crear diccionario del proyecto
                    project_dict = {
                        "id": product.id,
                        "name": product.name,
                        "client": client_name,
                        "team": engineers_assigned,  # Ahora muestra los ingenieros asignados
                        "progress": progress,
                        "status": product.status
                    }
                    
                    projects.append(project_dict)
                except Exception as e:
                    print(f"Error procesando proyecto: {e}")
            
            dashboard_data["recent_projects"] = projects
        
        conn.close()
        return dashboard_data
    
    except Exception as e:
        print(f"Error obteniendo datos del dashboard: {e}")
        import traceback
        traceback.print_exc()
        return {
            "active_projects": 0,
            "pending_requests": 0,
            "assigned_engineers": 0,
            "completed_projects": 0,
            "recent_projects": []
        }

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

def get_available_engineers():
    """Obtiene los ingenieros disponibles"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM Ingenieros
            WHERE disponible = 1
            ORDER BY nombre
        """)
        
        rows = cursor.fetchall()
        engineers = []
        
        for row in rows:
            try:
                engineer = Engineer.from_db_row(row)
                engineers.append(engineer.to_dict())
            except Exception as e:
                print(f"Error procesando ingeniero: {e}")
        
        conn.close()
        return engineers
    
    except Exception as e:
        print(f"Error obteniendo ingenieros disponibles: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_project_progress(product_id):
    """Obtiene el progreso de un proyecto específico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener información del producto
        cursor.execute("SELECT * FROM Producto WHERE id = ?", (product_id,))
        product_row = cursor.fetchone()
        if not product_row:
            conn.close()
            return None
        
        product = Product.from_db_row(product_row)
        
        # Obtener ingenieros asignados
        cursor.execute("""
            SELECT i.*, a.fecha_inicio, a.fecha_fin
            FROM Ingenieros i
            JOIN Asignaciones a ON i.id = a.id_ingeniero
            WHERE a.id_producto = ?
        """, (product_id,))
        
        engineer_rows = cursor.fetchall()
        engineers = []
        
        for row in engineer_rows:
            engineer = Engineer.from_db_row(row)
            engineer_dict = engineer.to_dict()
            engineer_dict["start_date"] = row["fecha_inicio"]
            engineer_dict["end_date"] = row["fecha_fin"] if "fecha_fin" in row.keys() else None
            engineers.append(engineer_dict)
        
        # Obtener avances del proyecto
        cursor.execute("""
            SELECT a.*, i.nombre as ingeniero_nombre 
            FROM Avances a
            JOIN Ingenieros i ON a.id_ingeniero = i.id
            WHERE a.id_producto = ?
            ORDER BY a.fecha DESC
        """, (product_id,))
        
        progress_rows = cursor.fetchall()
        progress_entries = []
        
        for row in progress_rows:
            progress = Progress.from_db_row(row)
            progress_dict = progress.to_dict()
            progress_dict["engineer_name"] = row["ingeniero_nombre"]
            progress_entries.append(progress_dict)
        
        # Calcular porcentaje total
        total_percentage = 0
        if progress_entries:
            total_percentage = progress_entries[0]["percentage"]
        
        conn.close()
        
        return {
            "product": product.to_dict(),
            "engineers": engineers,
            "progress_entries": progress_entries,
            "total_percentage": total_percentage
        }
    
    except Exception as e:
        print(f"Error obteniendo progreso del proyecto: {e}")
        import traceback
        traceback.print_exc()
        return None