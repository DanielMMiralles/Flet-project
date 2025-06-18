import sqlite3
import os
from pathlib import Path
from models.engineer import Engineer
from models.assignment import Assignment
from utils.database import get_db_connection

def get_all_engineers():
    """Obtiene todos los ingenieros"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Ingenieros ORDER BY nombre")
        rows = cursor.fetchall()
        engineers = []
        
        for row in rows:
            try:
                engineer = Engineer.from_db_row(row)
                engineers.append(engineer)
            except Exception as e:
                print(f"Error procesando ingeniero: {e}")
        
        conn.close()
        return engineers
    
    except Exception as e:
        print(f"Error obteniendo ingenieros: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_available_engineers():
    """Obtiene los ingenieros disponibles"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Ingenieros WHERE disponible = 1 ORDER BY nombre")
        rows = cursor.fetchall()
        engineers = []
        
        for row in rows:
            try:
                engineer = Engineer.from_db_row(row)
                engineers.append(engineer)
            except Exception as e:
                print(f"Error procesando ingeniero: {e}")
        
        conn.close()
        return engineers
    
    except Exception as e:
        print(f"Error obteniendo ingenieros disponibles: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_engineer_by_id(engineer_id):
    """Obtiene un ingeniero por su ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Ingenieros WHERE id = ?", (engineer_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        engineer = Engineer.from_db_row(row)
        conn.close()
        return engineer
    
    except Exception as e:
        print(f"Error obteniendo ingeniero: {e}")
        import traceback
        traceback.print_exc()
        return None

def assign_engineer_to_project(engineer_id, product_id, start_date):
    """Asigna un ingeniero a un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya está asignado
        cursor.execute(
            "SELECT * FROM Asignaciones WHERE id_ingeniero = ? AND id_producto = ?",
            (engineer_id, product_id)
        )
        
        if cursor.fetchone():
            conn.close()
            return False  # Ya está asignado
        
        # Crear asignación
        cursor.execute(
            "INSERT INTO Asignaciones (id_ingeniero, id_producto, fecha_inicio) VALUES (?, ?, ?)",
            (engineer_id, product_id, start_date)
        )
        
        # Actualizar disponibilidad del ingeniero
        cursor.execute(
            "UPDATE Ingenieros SET disponible = 0 WHERE id = ?",
            (engineer_id,)
        )
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error asignando ingeniero a proyecto: {e}")
        import traceback
        traceback.print_exc()
        return False

def complete_engineer_assignment(engineer_id, product_id, end_date):
    """Marca como completada la asignación de un ingeniero a un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Actualizar fecha de fin
        cursor.execute(
            "UPDATE Asignaciones SET fecha_fin = ? WHERE id_ingeniero = ? AND id_producto = ?",
            (end_date, engineer_id, product_id)
        )
        
        # Actualizar disponibilidad del ingeniero
        cursor.execute(
            "UPDATE Ingenieros SET disponible = 1 WHERE id = ?",
            (engineer_id,)
        )
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error completando asignación: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_engineers_by_project(product_id):
    """Obtiene los ingenieros asignados a un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.*, a.fecha_inicio, a.fecha_fin
            FROM Ingenieros i
            JOIN Asignaciones a ON i.id = a.id_ingeniero
            WHERE a.id_producto = ?
            ORDER BY i.nombre
        """, (product_id,))
        
        rows = cursor.fetchall()
        engineers = []
        
        for row in rows:
            try:
                engineer = Engineer.from_db_row(row)
                engineer_dict = engineer.to_dict()
                engineer_dict["start_date"] = row["fecha_inicio"]
                engineer_dict["end_date"] = row["fecha_fin"] if "fecha_fin" in row.keys() else None
                engineers.append(engineer_dict)
            except Exception as e:
                print(f"Error procesando ingeniero: {e}")
        
        conn.close()
        return engineers
    
    except Exception as e:
        print(f"Error obteniendo ingenieros por proyecto: {e}")
        import traceback
        traceback.print_exc()
        return []