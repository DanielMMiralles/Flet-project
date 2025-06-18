import sqlite3
import os
from pathlib import Path
from models.progress import Progress
from models.product import Product
from models.engineer import Engineer
from utils.database import get_db_connection

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

def add_progress_entry(product_id, engineer_id, date, description, percentage):
    """Añade una entrada de progreso a un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO Avances (id_producto, id_ingeniero, fecha, descripcion, porcentaje) VALUES (?, ?, ?, ?, ?)",
            (product_id, engineer_id, date, description, percentage)
        )
        
        # Si el porcentaje es 100, actualizar el estado del producto a completado
        if percentage == 100:
            cursor.execute(
                "UPDATE Producto SET status = 'completado' WHERE id = ?",
                (product_id,)
            )
        
        conn.commit()
        progress_id = cursor.lastrowid
        conn.close()
        return progress_id
    
    except Exception as e:
        print(f"Error añadiendo entrada de progreso: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_all_project_progress():
    """Obtiene el progreso de todos los proyectos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener todos los productos
        cursor.execute("SELECT * FROM Producto")
        product_rows = cursor.fetchall()
        projects_progress = []
        
        for product_row in product_rows:
            try:
                product = Product.from_db_row(product_row)
                
                # Obtener último avance del proyecto
                cursor.execute("""
                    SELECT a.*, i.nombre as ingeniero_nombre 
                    FROM Avances a
                    JOIN Ingenieros i ON a.id_ingeniero = i.id
                    WHERE a.id_producto = ?
                    ORDER BY a.fecha DESC
                    LIMIT 1
                """, (product.id,))
                
                progress_row = cursor.fetchone()
                percentage = 0
                last_update = None
                engineer_name = None
                
                if progress_row:
                    percentage = progress_row["porcentaje"]
                    last_update = progress_row["fecha"]
                    engineer_name = progress_row["ingeniero_nombre"]
                
                # Obtener ingenieros asignados
                cursor.execute("""
                    SELECT GROUP_CONCAT(i.nombre, ', ') as nombres
                    FROM Ingenieros i
                    JOIN Asignaciones a ON i.id = a.id_ingeniero
                    WHERE a.id_producto = ?
                """, (product.id,))
                
                engineers_row = cursor.fetchone()
                team_name = "Sin asignar"
                
                if engineers_row and engineers_row["nombres"]:
                    team_name = engineers_row["nombres"]
                
                projects_progress.append({
                    "product": product.to_dict(),
                    "percentage": percentage,
                    "last_update": last_update,
                    "engineer_name": engineer_name,
                    "team_name": team_name
                })
            
            except Exception as e:
                print(f"Error procesando progreso del proyecto: {e}")
        
        conn.close()
        return projects_progress
    
    except Exception as e:
        print(f"Error obteniendo progreso de proyectos: {e}")
        import traceback
        traceback.print_exc()
        return []