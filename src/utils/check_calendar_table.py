import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def check_calendar_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("=== ESTRUCTURA DE CalendarioEventos ===")
        cursor.execute("PRAGMA table_info(CalendarioEventos)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"Columna: {col[1]} | Tipo: {col[2]} | NOT NULL: {bool(col[3])}")
        
        print("\n=== SCHEMA COMPLETO ===")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='CalendarioEventos'")
        schema = cursor.fetchone()
        if schema:
            print(schema[0])
        
        print("\n=== INTENTAR INSERTAR EVENTO DE PRUEBA ===")
        try:
            cursor.execute("""
                INSERT INTO CalendarioEventos (id_ingeniero, titulo, descripcion, fecha_evento, tipo_evento, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (1, "Evento Prueba", "Descripcion prueba", "2025-06-30", "meeting"))
            
            conn.commit()
            print("✅ Inserción exitosa")
            
            # Verificar inserción
            cursor.execute("SELECT * FROM CalendarioEventos WHERE titulo = 'Evento Prueba'")
            result = cursor.fetchone()
            if result:
                print(f"✅ Evento encontrado: {dict(result)}")
            else:
                print("❌ Evento no encontrado después de insertar")
                
        except Exception as e:
            print(f"❌ Error en inserción: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    check_calendar_table()