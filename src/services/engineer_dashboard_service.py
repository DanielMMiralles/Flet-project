import sqlite3
from utils.database import get_db_connection
import datetime

def get_engineer_dashboard_data(engineer_id=1):
    """Obtiene datos del dashboard para un ingeniero específico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener proyectos asignados al ingeniero
        cursor.execute("""
            SELECT DISTINCT p.*, a.fecha_inicio
            FROM Producto p
            INNER JOIN Asignaciones a ON p.id = a.id_producto
            WHERE a.id_ingeniero = ?
            ORDER BY a.fecha_inicio DESC
        """, (engineer_id,))
        
        projects_rows = cursor.fetchall()
        projects = []
        
        for row in projects_rows:
            # Obtener progreso del proyecto (suma de todos los avances)
            cursor.execute("""
                SELECT COALESCE(SUM(porcentaje), 0) as total_progress
                FROM Avances
                WHERE id_producto = ?
            """, (row["id"],))
            
            progress_row = cursor.fetchone()
            # Limitar progreso a máximo 100% para mostrar
            raw_progress = progress_row["total_progress"] if progress_row else 0
            current_progress = min(100, raw_progress)
            
            if raw_progress > 100:
                print(f"ADVERTENCIA: Proyecto {row['nombre']} tiene {raw_progress}% (limitado a 100% para mostrar)")
            
            # Debug: Ver todos los avances del proyecto
            cursor.execute("""
                SELECT porcentaje, descripcion, fecha
                FROM Avances
                WHERE id_producto = ?
                ORDER BY fecha DESC
            """, (row["id"],))
            
            debug_advances = cursor.fetchall()
            print(f"\n=== DEBUG PROYECTO {row['nombre']} (ID: {row['id']}) ===")
            print(f"Avances encontrados: {len(debug_advances)}")
            for adv in debug_advances:
                print(f"  - {adv['porcentaje']}% | {adv['descripcion'][:50]}... | {adv['fecha']}")
            print(f"Suma calculada: {current_progress}%")
            print(f"=======================================\n")
            
            # Obtener tamaño del equipo
            cursor.execute("""
                SELECT COUNT(*) as team_count
                FROM Asignaciones
                WHERE id_producto = ?
            """, (row["id"],))
            
            team_row = cursor.fetchone()
            team_size = team_row["team_count"] if team_row else 1
            
            # Obtener avances del proyecto
            cursor.execute("""
                SELECT a.*, i.nombre as engineer_name
                FROM Avances a
                JOIN Ingenieros i ON a.id_ingeniero = i.id
                WHERE a.id_producto = ?
                ORDER BY a.fecha DESC
                LIMIT 5
            """, (row["id"],))
            
            advances_rows = cursor.fetchall()
            advances = []
            
            for advance_row in advances_rows:
                advances.append({
                    "engineer": advance_row["engineer_name"],
                    "date": advance_row["fecha"],
                    "progress": advance_row["porcentaje"],
                    "description": advance_row["descripcion"]
                })
            
            projects.append({
                "id": row["id"],
                "name": row["nombre"],
                "client": "Cliente Asignado",  # Simplificado
                "progress": current_progress,
                "team_size": team_size,
                "start_date": row["fecha_inicio"][:10] if row["fecha_inicio"] else "2024-01-01",
                "advances": advances
            })
        
        # Calcular métricas
        projects_count = len(projects)
        pending_tasks = sum(1 for p in projects if p["progress"] < 100)
        avg_progress = sum(p["progress"] for p in projects) // len(projects) if projects else 0
        
        conn.close()
        
        return {
            "projects_count": projects_count,
            "pending_tasks": pending_tasks,
            "avg_progress": avg_progress,
            "projects": projects
        }
        
    except Exception as e:
        print(f"Error obteniendo datos del dashboard del ingeniero: {e}")
        # Retornar datos por defecto si hay error
        return {
            "projects_count": 0,
            "pending_tasks": 0,
            "avg_progress": 0,
            "projects": []
        }

def register_progress(engineer_id, project_id, percentage, description):
    """Registra un nuevo avance para un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que el ingeniero esté asignado al proyecto
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Asignaciones
            WHERE id_ingeniero = ? AND id_producto = ?
        """, (engineer_id, project_id))
        
        assignment_row = cursor.fetchone()
        if not assignment_row or assignment_row["count"] == 0:
            conn.close()
            return False, "No tienes asignado este proyecto"
        
        # Validar que el porcentaje no sea negativo
        if percentage < 0:
            conn.close()
            return False, "El porcentaje no puede ser negativo"
        
        # Verificar progreso actual del proyecto
        cursor.execute("""
            SELECT COALESCE(SUM(porcentaje), 0) as current_progress
            FROM Avances
            WHERE id_producto = ?
        """, (project_id,))
        
        current_row = cursor.fetchone()
        current_progress = current_row["current_progress"] if current_row else 0
        
        # Debug: Ver avances actuales
        cursor.execute("""
            SELECT porcentaje, descripcion, fecha, id_ingeniero
            FROM Avances
            WHERE id_producto = ?
            ORDER BY fecha DESC
        """, (project_id,))
        
        debug_advances = cursor.fetchall()
        print(f"\n=== DEBUG REGISTRO AVANCE ===")
        print(f"Proyecto ID: {project_id}")
        print(f"Nuevo porcentaje a agregar: {percentage}%")
        print(f"Avances actuales: {len(debug_advances)}")
        for adv in debug_advances:
            print(f"  - {adv['porcentaje']}% | Ing: {adv['id_ingeniero']} | {adv['descripcion'][:30]}...")
        print(f"Progreso actual calculado: {current_progress}%")
        print(f"Nuevo total sería: {current_progress + percentage}%")
        print(f"==============================\n")
        
        # Validar que no se exceda el 100%
        if current_progress + percentage > 100:
            remaining = 100 - current_progress
            conn.close()
            return False, f"Solo puedes agregar {remaining}% más. Progreso actual: {current_progress}%"
        
        # Insertar nuevo avance
        cursor.execute("""
            INSERT INTO Avances (id_producto, id_ingeniero, porcentaje, descripcion, fecha)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (project_id, engineer_id, percentage, description))
        
        # Calcular progreso total (suma de todos los avances)
        cursor.execute("""
            SELECT COALESCE(SUM(porcentaje), 0) as total_progress
            FROM Avances
            WHERE id_producto = ?
        """, (project_id,))
        
        total_row = cursor.fetchone()
        total_progress = total_row["total_progress"] if total_row else 0
        
        print(f"\n=== DEBUG DESPUÉS DE INSERTAR ===")
        print(f"Progreso total calculado: {total_progress}%")
        print(f"Actualizando tabla Progreso...")
        print(f"===================================\n")
        
        # Actualizar progreso en tabla Progreso
        cursor.execute("""
            INSERT OR REPLACE INTO Progreso (id_producto, porcentaje, fecha_actualizacion)
            VALUES (?, ?, datetime('now'))
        """, (project_id, total_progress))
        
        conn.commit()
        conn.close()
        
        return True, "Avance registrado correctamente"
        
    except Exception as e:
        print(f"Error registrando avance: {e}")
        return False, f"Error: {str(e)}"

def get_engineer_projects_for_dropdown(engineer_id=1):
    """Obtiene proyectos del ingeniero para el dropdown"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT p.id, p.nombre
            FROM Producto p
            INNER JOIN Asignaciones a ON p.id = a.id_producto
            WHERE a.id_ingeniero = ?
            ORDER BY p.nombre
        """, (engineer_id,))
        
        rows = cursor.fetchall()
        projects = []
        
        for row in rows:
            projects.append({
                "id": row["id"],
                "name": row["nombre"]
            })
        
        conn.close()
        return projects
        
    except Exception as e:
        print(f"Error obteniendo proyectos para dropdown: {e}")
        return []