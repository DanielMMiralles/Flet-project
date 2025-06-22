import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import get_db_connection

def populate_realistic_data():
    """Limpia y pobla la base de datos con datos realistas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("Limpiando datos existentes (excepto Producto)...")
        
        # Limpiar todas las tablas excepto Producto
        cursor.execute("DELETE FROM CalendarioEventos")
        cursor.execute("DELETE FROM Progreso")
        cursor.execute("DELETE FROM Avances")
        cursor.execute("DELETE FROM Asignaciones")
        cursor.execute("DELETE FROM Solicitudes")
        cursor.execute("DELETE FROM Ingenieros")
        cursor.execute("DELETE FROM Clientes")
        cursor.execute("DELETE FROM Usuarios")
        
        print("Creando usuarios realistas...")
        
        # Usuarios realistas
        usuarios = [
            (1, 'admin', 'admin123', 'admin'),
            (2, 'maria.garcia', 'maria2024', 'cliente'),
            (3, 'carlos.lopez', 'carlos2024', 'cliente'),
            (4, 'ana.rodriguez', 'ana2024', 'cliente'),
            (5, 'juan.perez', 'juan2024', 'ingeniero'),
            (6, 'sofia.martinez', 'sofia2024', 'ingeniero'),
            (7, 'diego.torres', 'diego2024', 'ingeniero'),
            (8, 'lucia.fernandez', 'lucia2024', 'ingeniero'),
            (9, 'miguel.santos', 'miguel2024', 'ingeniero')
        ]
        
        cursor.executemany("INSERT INTO Usuarios (id, usuario, password, rol) VALUES (?, ?, ?, ?)", usuarios)
        
        print("Creando clientes realistas...")
        
        # Clientes realistas
        clientes = [
            (1, 2, 'TechCorp Solutions', 'contacto@techcorp.com', '+1-555-0101'),
            (2, 3, 'Innovate Business Group', 'info@innovate.com', '+1-555-0102'),
            (3, 4, 'Digital Ventures LLC', 'hello@digitalventures.com', '+1-555-0103')
        ]
        
        cursor.executemany("INSERT INTO Clientes (id, id_usuario, nombre, email, telefono) VALUES (?, ?, ?, ?, ?)", clientes)
        
        print("Creando ingenieros realistas...")
        
        # Ingenieros realistas
        ingenieros = [
            (1, 5, 'Juan Pérez', 'Full Stack Developer', 0),
            (2, 6, 'Sofía Martínez', 'Frontend Specialist', 0),
            (3, 7, 'Diego Torres', 'Backend Developer', 0),
            (4, 8, 'Lucía Fernández', 'Mobile Developer', 1),
            (5, 9, 'Miguel Santos', 'DevOps Engineer', 1)
        ]
        
        cursor.executemany("INSERT INTO Ingenieros (id, id_usuario, nombre, especialidad, disponible) VALUES (?, ?, ?, ?, ?)", ingenieros)
        
        print("Creando solicitudes realistas...")
        
        # Solicitudes realistas
        solicitudes = [
            (1, 1, 1, '2024-01-15', 'Necesitamos un sistema de gestión empresarial completo para optimizar nuestros procesos internos', 'aprobada'),
            (2, 1, 2, '2024-01-20', 'Requerimos una aplicación móvil para mejorar la experiencia de nuestros clientes', 'aprobada'),
            (3, 2, 3, '2024-01-25', 'Buscamos una plataforma de e-learning moderna para capacitar a nuestro personal', 'aprobada'),
            (4, 2, 5, '2024-02-01', 'Necesitamos una tienda online robusta para expandir nuestro negocio digital', 'aprobada'),
            (5, 3, 6, '2024-02-05', 'Queremos implementar un CRM empresarial para gestionar mejor nuestros clientes', 'aprobada'),
            (6, 3, 8, '2024-02-10', 'Requerimos una plataforma de análisis de datos para tomar mejores decisiones', 'pendiente')
        ]
        
        cursor.executemany("INSERT INTO Solicitudes (id, id_cliente, id_producto, fecha_solicitud, detalles, estado) VALUES (?, ?, ?, ?, ?, ?)", solicitudes)
        
        print("Creando asignaciones realistas...")
        
        # Asignaciones realistas (proyectos con equipos)
        asignaciones = [
            (1, 1, 1, '2024-01-20', None),  # Juan -> Sistema de Gestión
            (2, 2, 1, '2024-01-20', None),  # Sofía -> Sistema de Gestión
            (3, 3, 2, '2024-01-25', None),  # Diego -> App Móvil
            (4, 4, 2, '2024-01-25', None),  # Lucía -> App Móvil
            (5, 1, 3, '2024-01-30', None),  # Juan -> Plataforma E-learning
            (6, 2, 3, '2024-01-30', None),  # Sofía -> Plataforma E-learning
            (7, 3, 3, '2024-01-30', None),  # Diego -> Plataforma E-learning
            (8, 2, 5, '2024-02-05', None),  # Sofía -> Tienda Online
            (9, 3, 5, '2024-02-05', None),  # Diego -> Tienda Online
            (10, 1, 6, '2024-02-10', None), # Juan -> CRM Empresarial
            (11, 4, 6, '2024-02-10', None)  # Lucía -> CRM Empresarial
        ]
        
        cursor.executemany("INSERT INTO Asignaciones (id, id_ingeniero, id_producto, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?, ?)", asignaciones)
        
        print("Creando avances realistas...")
        
        # Avances realistas
        avances = [
            # Sistema de Gestión (ID: 1) - 85% total
            (1, 1, 1, '2024-02-01', 'Configuración inicial del proyecto y arquitectura base', 15),
            (2, 1, 2, '2024-02-15', 'Desarrollo del módulo de usuarios y autenticación', 25),
            (3, 1, 1, '2024-03-01', 'Implementación de dashboard principal y navegación', 20),
            (4, 1, 2, '2024-03-15', 'Desarrollo de módulos de inventario y reportes', 25),
            
            # App Móvil (ID: 2) - 70% total
            (5, 2, 3, '2024-02-05', 'Configuración del proyecto React Native', 10),
            (6, 2, 4, '2024-02-20', 'Desarrollo de pantallas principales y navegación', 30),
            (7, 2, 3, '2024-03-05', 'Integración con APIs y servicios backend', 20),
            (8, 2, 4, '2024-03-20', 'Implementación de funcionalidades avanzadas', 10),
            
            # Plataforma E-learning (ID: 3) - 60% total
            (9, 3, 1, '2024-02-10', 'Análisis de requerimientos y diseño de arquitectura', 15),
            (10, 3, 2, '2024-02-25', 'Desarrollo del sistema de gestión de cursos', 20),
            (11, 3, 3, '2024-03-10', 'Implementación del reproductor de video y evaluaciones', 25),
            
            # Tienda Online (ID: 5) - 45% total
            (12, 5, 2, '2024-02-15', 'Configuración de la plataforma e-commerce', 15),
            (13, 5, 3, '2024-03-01', 'Desarrollo del catálogo de productos', 20),
            (14, 5, 2, '2024-03-15', 'Integración con pasarela de pagos', 10),
            
            # CRM Empresarial (ID: 6) - 30% total
            (15, 6, 1, '2024-02-20', 'Configuración inicial y base de datos', 15),
            (16, 6, 4, '2024-03-05', 'Desarrollo del módulo de contactos', 15)
        ]
        
        cursor.executemany("INSERT INTO Avances (id, id_producto, id_ingeniero, fecha, descripcion, porcentaje) VALUES (?, ?, ?, ?, ?, ?)", avances)
        
        print("Calculando y actualizando progreso...")
        
        # Calcular progreso por proyecto
        proyectos_progreso = [
            (1, 85),  # Sistema de Gestión
            (2, 70),  # App Móvil
            (3, 60),  # Plataforma E-learning
            (5, 45),  # Tienda Online
            (6, 30)   # CRM Empresarial
        ]
        
        for proyecto_id, progreso in proyectos_progreso:
            cursor.execute("""
                INSERT OR REPLACE INTO Progreso (id_producto, porcentaje, fecha_actualizacion)
                VALUES (?, ?, datetime('now'))
            """, (proyecto_id, progreso))
        
        print("Creando eventos de calendario realistas...")
        
        # Eventos de calendario realistas
        eventos = [
            (1, 1, 'Entrega Sistema de Gestión', 'Fecha límite para la entrega del sistema completo', '2024-04-15', 'deadline', 1),
            (2, 1, 'Reunión de seguimiento', 'Reunión semanal del equipo de desarrollo', '2024-04-01', 'meeting', 1),
            (3, 2, 'Demo App Móvil', 'Presentación del prototipo al cliente', '2024-04-10', 'meeting', 2),
            (4, 3, 'Entrega E-learning', 'Fecha límite para la plataforma educativa', '2024-04-20', 'deadline', 3),
            (5, 2, 'Capacitación técnica', 'Sesión de capacitación en nuevas tecnologías', '2024-04-05', 'personal', None),
            (6, 4, 'Revisión de código', 'Revisión de código del proyecto móvil', '2024-04-08', 'personal', None)
        ]
        
        cursor.executemany("INSERT INTO CalendarioEventos (id, id_ingeniero, titulo, descripcion, fecha_evento, tipo_evento, id_proyecto) VALUES (?, ?, ?, ?, ?, ?, ?)", eventos)
        
        # Resetear secuencias
        cursor.execute("UPDATE sqlite_sequence SET seq = 9 WHERE name = 'Usuarios'")
        cursor.execute("UPDATE sqlite_sequence SET seq = 3 WHERE name = 'Clientes'")
        cursor.execute("UPDATE sqlite_sequence SET seq = 5 WHERE name = 'Ingenieros'")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Base de datos poblada exitosamente con datos realistas!")
        print("\n📊 RESUMEN:")
        print("- 9 usuarios (1 admin, 3 clientes, 5 ingenieros)")
        print("- 3 clientes empresariales")
        print("- 5 ingenieros especializados")
        print("- 6 solicitudes de proyectos")
        print("- 5 proyectos con equipos asignados")
        print("- 16 avances de desarrollo registrados")
        print("- 6 eventos de calendario")
        print("\n🔑 Credenciales de acceso:")
        print("Admin: admin / admin123")
        print("Cliente: maria.garcia / maria2024")
        print("Ingeniero: juan.perez / juan2024")
        
        return True
        
    except Exception as e:
        print(f"Error poblando base de datos: {e}")
        return False

if __name__ == "__main__":
    populate_realistic_data()