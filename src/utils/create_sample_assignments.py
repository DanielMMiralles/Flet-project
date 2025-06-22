import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def create_sample_assignments():
    """Crea asignaciones de ejemplo para que el ingeniero tenga proyectos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existen asignaciones
        cursor.execute("SELECT COUNT(*) FROM Asignaciones")
        existing_assignments = cursor.fetchone()[0]
        
        if existing_assignments > 0:
            print("Ya existen asignaciones en la base de datos")
            conn.close()
            return
        
        # Crear asignaciones de ejemplo (ingeniero ID 1 a varios proyectos)
        sample_assignments = [
            (1, 1, '2024-01-15'),  # Ingeniero 1 -> Proyecto 1
            (2, 1, '2024-01-20'),  # Ingeniero 1 -> Proyecto 2  
            (3, 1, '2024-01-10'),  # Ingeniero 1 -> Proyecto 3
        ]
        
        cursor.executemany("""
            INSERT INTO Asignaciones (id_producto, id_ingeniero, fecha_inicio)
            VALUES (?, ?, ?)
        """, sample_assignments)
        
        # Crear algunos avances de ejemplo
        sample_advances = [
            (1, 1, 75, 'Implementación del módulo de reportes completada', '2024-02-10'),
            (1, 1, 60, 'Base de datos optimizada y pruebas unitarias', '2024-02-08'),
            (2, 1, 45, 'Integración con pasarela de pagos completada', '2024-02-09'),
            (3, 1, 90, 'Módulo de reportes avanzados y exportación completado', '2024-02-11'),
        ]
        
        cursor.executemany("""
            INSERT INTO Avances (id_producto, id_ingeniero, porcentaje, descripcion, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, sample_advances)
        
        # Actualizar tabla Progreso
        sample_progress = [
            (1, 75, '2024-02-10'),
            (2, 45, '2024-02-09'),
            (3, 90, '2024-02-11'),
        ]
        
        cursor.executemany("""
            INSERT OR REPLACE INTO Progreso (id_producto, porcentaje, fecha_actualizacion)
            VALUES (?, ?, ?)
        """, sample_progress)
        
        conn.commit()
        conn.close()
        
        print("Asignaciones y avances de ejemplo creados exitosamente")
        return True
        
    except Exception as e:
        print(f"Error creando asignaciones de ejemplo: {e}")
        return False

if __name__ == "__main__":
    create_sample_assignments()