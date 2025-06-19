import sqlite3
from utils.database import get_db_connection
import datetime

def get_project_progress(project_id):
    """Obtiene el progreso actual de un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla Progreso existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Progreso'")
        if not cursor.fetchone():
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE Progreso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_producto INTEGER,
                    porcentaje INTEGER,
                    fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_producto) REFERENCES Producto(id)
                )
            """)
            conn.commit()
            
            # No hay registros aún
            conn.close()
            return 0
        
        # Verificar las columnas de la tabla Progreso
        cursor.execute("PRAGMA table_info(Progreso)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Determinar el nombre correcto de la columna para el ID del proyecto
        project_id_column = "id_producto" if "id_producto" in columns else "id_proyecto"
        
        # Consulta con el nombre correcto de la columna
        query = f"""
            SELECT porcentaje FROM Progreso
            WHERE {project_id_column} = ?
            ORDER BY fecha_actualizacion DESC
            LIMIT 1
        """
        
        cursor.execute(query, (project_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return 0
        
        progress = row["porcentaje"]
        
        conn.close()
        return progress
    
    except Exception as e:
        print(f"Error obteniendo progreso del proyecto: {e}")
        import traceback
        traceback.print_exc()
        return 0

def update_project_progress(project_id, percentage):
    """Actualiza el progreso de un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla Progreso existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Progreso'")
        if not cursor.fetchone():
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE Progreso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_producto INTEGER,
                    porcentaje INTEGER,
                    fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_producto) REFERENCES Producto(id)
                )
            """)
            conn.commit()
        
        # Verificar las columnas de la tabla Progreso
        cursor.execute("PRAGMA table_info(Progreso)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Determinar el nombre correcto de la columna para el ID del proyecto
        project_id_column = "id_producto" if "id_producto" in columns else "id_proyecto"
        
        # Validar porcentaje
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100
        
        # Insertar nuevo registro de progreso con el nombre correcto de la columna
        query = f"INSERT INTO Progreso ({project_id_column}, porcentaje, fecha_actualizacion) VALUES (?, ?, datetime('now'))"
        cursor.execute(query, (project_id, percentage))
        
        # Si el progreso es 100%, actualizar estado del proyecto
        if percentage == 100:
            cursor.execute(
                "UPDATE Producto SET estado = 'completado' WHERE id = ?",
                (project_id,)
            )
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error actualizando progreso del proyecto: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_project_progress_history(project_id):
    """Obtiene el historial de progreso de un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla Progreso existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Progreso'")
        if not cursor.fetchone():
            conn.close()
            return []
        
        # Verificar las columnas de la tabla Progreso
        cursor.execute("PRAGMA table_info(Progreso)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Determinar el nombre correcto de la columna para el ID del proyecto
        project_id_column = "id_producto" if "id_producto" in columns else "id_proyecto"
        
        # Consulta con el nombre correcto de la columna
        query = f"""
            SELECT porcentaje, fecha_actualizacion FROM Progreso
            WHERE {project_id_column} = ?
            ORDER BY fecha_actualizacion ASC
        """
        
        cursor.execute(query, (project_id,))
        rows = cursor.fetchall()
        
        history = []
        for row in rows:
            entry = {
                "percentage": row["porcentaje"],
                "date": row["fecha_actualizacion"]
            }
            history.append(entry)
        
        conn.close()
        return history
    
    except Exception as e:
        print(f"Error obteniendo historial de progreso del proyecto: {e}")
        import traceback
        traceback.print_exc()
        return []