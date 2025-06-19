import sqlite3
from utils.database import get_db_connection
from services.engineer_service import get_engineer_by_id, update_engineer_availability

def assign_engineers_to_project(project_id, engineer_ids):
    """Asigna ingenieros a un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Iniciar transacción
        conn.execute("BEGIN TRANSACTION")
        
        # Verificar que el proyecto existe
        cursor.execute("SELECT * FROM Producto WHERE id = ?", (project_id,))
        project = cursor.fetchone()
        if not project:
            print(f"Proyecto {project_id} no existe")
            conn.rollback()
            conn.close()
            return False
        
        # Verificar que todos los ingenieros existen y están disponibles (menos de 5 proyectos)
        for engineer_id in engineer_ids:
            engineer = get_engineer_by_id(engineer_id)
            if not engineer:
                print(f"Ingeniero {engineer_id} no existe")
                conn.rollback()
                conn.close()
                return False
            
            # Verificar si el ingeniero tiene menos de 5 proyectos activos
            if "active_projects" in engineer and engineer["active_projects"] >= 5:
                print(f"Ingeniero {engineer_id} ya tiene 5 o más proyectos activos")
                conn.rollback()
                conn.close()
                return False
        
        # Verificar si la tabla Asignaciones existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Asignaciones'")
        if not cursor.fetchone():
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE Asignaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_producto INTEGER,
                    id_ingeniero INTEGER,
                    fecha_inicio TEXT DEFAULT CURRENT_TIMESTAMP,
                    fecha_fin TEXT,
                    FOREIGN KEY (id_producto) REFERENCES Producto(id),
                    FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id)
                )
            """)
        
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
        
        # Crear asignaciones con fecha_inicio explícita
        for engineer_id in engineer_ids:
            cursor.execute(
                "INSERT INTO Asignaciones (id_producto, id_ingeniero, fecha_inicio) VALUES (?, ?, datetime('now'))",
                (project_id, engineer_id)
            )
        
        # Verificar si existe la columna estado en la tabla Producto
        cursor.execute("PRAGMA table_info(Producto)")
        product_columns = [col[1] for col in cursor.fetchall()]
        
        # Actualizar estado del proyecto si la columna existe
        if "estado" in product_columns:
            cursor.execute(
                "UPDATE Producto SET estado = 'en_progreso' WHERE id = ?",
                (project_id,)
            )
        elif "status" in product_columns:
            cursor.execute(
                "UPDATE Producto SET status = 'en_progreso' WHERE id = ?",
                (project_id,)
            )
        
        # Crear registro de progreso inicial
        cursor.execute(
            "INSERT INTO Progreso (id_producto, porcentaje, fecha_actualizacion) VALUES (?, ?, datetime('now'))",
            (project_id, 0)
        )
        
        # Confirmar transacción
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error asignando ingenieros al proyecto: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return False

def get_project_engineers(project_id):
    """Obtiene los ingenieros asignados a un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla Asignaciones existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Asignaciones'")
        if not cursor.fetchone():
            conn.close()
            return []
        
        # Verificar las columnas de la tabla Asignaciones
        cursor.execute("PRAGMA table_info(Asignaciones)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Determinar el nombre correcto de la columna para el ID del proyecto
        project_id_column = "id_producto" if "id_producto" in columns else "id_proyecto"
        
        # Verificar las columnas de la tabla Ingenieros
        cursor.execute("PRAGMA table_info(Ingenieros)")
        engineer_columns = {col[1]: True for col in cursor.fetchall()}
        
        # Consulta con el nombre correcto de la columna
        query = f"""
            SELECT i.* FROM Ingenieros i
            JOIN Asignaciones a ON i.id = a.id_ingeniero
            WHERE a.{project_id_column} = ?
        """
        
        cursor.execute(query, (project_id,))
        rows = cursor.fetchall()
        
        engineers = []
        for row in rows:
            try:
                # Contar proyectos activos del ingeniero
                try:
                    cursor.execute("""
                        SELECT COUNT(*) as proyecto_count 
                        FROM Asignaciones 
                        WHERE id_ingeniero = ? AND fecha_fin IS NULL
                    """, (row["id"],))
                    
                    count_row = cursor.fetchone()
                    project_count = count_row["proyecto_count"] if count_row else 0
                except Exception as e:
                    print(f"Error al contar proyectos: {e}")
                    project_count = 0
                
                engineer = {
                    "id": row["id"],
                    "name": row["nombre"] if "nombre" in engineer_columns else "Sin nombre",
                    "specialty": row["especialidad"] if "especialidad" in engineer_columns else "Sin especialidad",
                    "experience": row["experiencia"] if "experiencia" in engineer_columns else 0,
                    "available": project_count < 5,
                    "active_projects": project_count
                }
                engineers.append(engineer)
            except Exception as e:
                print(f"Error procesando ingeniero en get_project_engineers: {e}")
                import traceback
                traceback.print_exc()
        
        conn.close()
        return engineers
    
    except Exception as e:
        print(f"Error obteniendo ingenieros del proyecto: {e}")
        import traceback
        traceback.print_exc()
        return []

def remove_engineer_from_project(project_id, engineer_id):
    """Elimina un ingeniero de un proyecto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Iniciar transacción
        conn.execute("BEGIN TRANSACTION")
        
        # Verificar las columnas de la tabla Asignaciones
        cursor.execute("PRAGMA table_info(Asignaciones)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Determinar el nombre correcto de la columna para el ID del proyecto
        project_id_column = "id_producto" if "id_producto" in columns else "id_proyecto"
        
        # Eliminar asignación con el nombre correcto de la columna
        query = f"DELETE FROM Asignaciones WHERE {project_id_column} = ? AND id_ingeniero = ?"
        cursor.execute(query, (project_id, engineer_id))
        
        # Ya no necesitamos actualizar la disponibilidad
        # Los ingenieros pueden tener hasta 5 proyectos activos
        
        # Confirmar transacción
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error eliminando ingeniero del proyecto: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()
        return False