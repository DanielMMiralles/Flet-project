import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def create_calendar_table():
    """Crea la tabla de eventos del calendario para ingenieros"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla de eventos del calendario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CalendarioEventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_ingeniero INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_evento DATE NOT NULL,
                tipo_evento TEXT NOT NULL CHECK (tipo_evento IN ('deadline', 'meeting', 'personal')),
                id_proyecto INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id),
                FOREIGN KEY (id_proyecto) REFERENCES Producto(id)
            )
        """)
        
        # Insertar algunos eventos de ejemplo
        sample_events = [
            (1, "Entrega Sistema Inventario", "Fecha límite para la entrega del sistema", "2024-02-15", "deadline", 1),
            (1, "Reunión de equipo", "Reunión semanal del equipo de desarrollo", "2024-02-20", "meeting", 2),
            (1, "Entrega CRM", "Fecha límite para la entrega de la plataforma CRM", "2024-02-25", "deadline", 3),
            (1, "Revisión de código", "Revisión personal del código desarrollado", "2024-02-28", "personal", None)
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO CalendarioEventos 
            (id_ingeniero, titulo, descripcion, fecha_evento, tipo_evento, id_proyecto)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_events)
        
        conn.commit()
        conn.close()
        
        print("Tabla CalendarioEventos creada exitosamente")
        return True
        
    except Exception as e:
        print(f"Error creando tabla CalendarioEventos: {e}")
        return False

if __name__ == "__main__":
    create_calendar_table()