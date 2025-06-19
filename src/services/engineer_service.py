import sqlite3
from utils.database import get_db_connection
from models.engineer import Engineer

def get_all_engineers():
    """Obtiene todos los ingenieros de la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla Ingenieros existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Ingenieros'")
        if not cursor.fetchone():
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE Ingenieros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    especialidad TEXT,
                    experiencia INTEGER DEFAULT 0,
                    disponible INTEGER DEFAULT 1
                )
            """)
            
            # Insertar algunos ingenieros de ejemplo
            sample_engineers = [
                ("Juan Pérez", "Frontend", 5, 1),
                ("María García", "Backend", 3, 1),
                ("Carlos Rodríguez", "DevOps", 4, 1),
                ("Ana Martínez", "UX/UI", 2, 1),
                ("Luis Sánchez", "Fullstack", 6, 1)
            ]
            
            cursor.executemany(
                "INSERT INTO Ingenieros (nombre, especialidad, experiencia, disponible) VALUES (?, ?, ?, ?)",
                sample_engineers
            )
            
            conn.commit()
        
        # Verificar las columnas de la tabla Ingenieros
        cursor.execute("PRAGMA table_info(Ingenieros)")
        columns = {col[1]: True for col in cursor.fetchall()}
        
        cursor.execute("SELECT * FROM Ingenieros")
        rows = cursor.fetchall()
        
        engineers = []
        for row in rows:
            try:
                engineer = {
                    "id": row["id"],
                    "name": row["nombre"] if "nombre" in columns else "Sin nombre",
                    "specialty": row["especialidad"] if "especialidad" in columns else "Sin especialidad",
                    "experience": row["experiencia"] if "experiencia" in columns else 0,
                    "available": row["disponible"] == 1 if "disponible" in columns else True
                }
                engineers.append(engineer)
            except Exception as e:
                print(f"Error procesando ingeniero: {e}")
                import traceback
                traceback.print_exc()
        
        conn.close()
        return engineers
    
    except Exception as e:
        print(f"Error obteniendo ingenieros: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_available_engineers():
    """Obtiene los ingenieros disponibles (con menos de 5 proyectos activos)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla Ingenieros existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Ingenieros'")
        if not cursor.fetchone():
            # Si no existe, crear la tabla y los ingenieros de ejemplo
            get_all_engineers()
            conn = get_db_connection()
            cursor = conn.cursor()
        
        # Verificar si la tabla Asignaciones existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Asignaciones'")
        if not cursor.fetchone():
            # Si no existe, todos los ingenieros están disponibles
            return get_all_engineers()
        
        # Verificar las columnas de la tabla Ingenieros
        cursor.execute("PRAGMA table_info(Ingenieros)")
        columns = {col[1]: True for col in cursor.fetchall()}
        
        # Obtener todos los ingenieros
        cursor.execute("SELECT * FROM Ingenieros")
        rows = cursor.fetchall()
        
        engineers = []
        for row in rows:
            try:
                # Verificar cuántos proyectos activos tiene el ingeniero
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
                
                # Si tiene menos de 5 proyectos activos, está disponible
                if project_count < 5:
                    engineer = {
                        "id": row["id"],
                        "name": row["nombre"] if "nombre" in columns else "Sin nombre",
                        "specialty": row["especialidad"] if "especialidad" in columns else "Sin especialidad",
                        "experience": row["experiencia"] if "experiencia" in columns else 0,
                        "available": True,
                        "active_projects": project_count
                    }
                    engineers.append(engineer)
            except Exception as e:
                print(f"Error procesando ingeniero disponible: {e}")
                import traceback
                traceback.print_exc()
        
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
        
        # Verificar las columnas de la tabla Ingenieros
        cursor.execute("PRAGMA table_info(Ingenieros)")
        columns = {col[1]: True for col in cursor.fetchall()}
        
        cursor.execute("SELECT * FROM Ingenieros WHERE id = ?", (engineer_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        try:
            # Verificar cuántos proyectos activos tiene el ingeniero
            try:
                cursor.execute("""
                    SELECT COUNT(*) as proyecto_count 
                    FROM Asignaciones 
                    WHERE id_ingeniero = ? AND fecha_fin IS NULL
                """, (engineer_id,))
                
                count_row = cursor.fetchone()
                project_count = count_row["proyecto_count"] if count_row else 0
            except Exception as e:
                print(f"Error al contar proyectos: {e}")
                project_count = 0
            
            engineer = {
                "id": row["id"],
                "name": row["nombre"] if "nombre" in columns else "Sin nombre",
                "specialty": row["especialidad"] if "especialidad" in columns else "Sin especialidad",
                "experience": row["experiencia"] if "experiencia" in columns else 0,
                "available": project_count < 5,  # Disponible si tiene menos de 5 proyectos
                "active_projects": project_count
            }
        except Exception as e:
            print(f"Error procesando ingeniero en get_engineer_by_id: {e}")
            import traceback
            traceback.print_exc()
            conn.close()
            return None
        
        conn.close()
        return engineer
    
    except Exception as e:
        print(f"Error obteniendo ingeniero: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_engineer_availability(engineer_id, available):
    """Actualiza la disponibilidad de un ingeniero"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE Ingenieros SET disponible = ? WHERE id = ?",
            (1 if available else 0, engineer_id)
        )
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error actualizando disponibilidad del ingeniero: {e}")
        import traceback
        traceback.print_exc()
        return False