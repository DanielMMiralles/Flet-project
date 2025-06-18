import sys
import os
from pathlib import Path

# Añadir el directorio src al path para poder importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from services.progress_service import get_project_progress, get_all_project_progress

def test_progress():
    """Prueba los servicios relacionados con el progreso de proyectos"""
    print("Obteniendo progreso de todos los proyectos...")
    
    all_progress = get_all_project_progress()
    
    print(f"\nTotal de proyectos con progreso: {len(all_progress)}")
    for i, project in enumerate(all_progress, 1):
        print(f"\nProyecto {i}:")
        print(f"  Nombre: {project['product']['name']}")
        print(f"  Porcentaje: {project['percentage']}%")
        print(f"  Última actualización: {project['last_update'] or 'Sin actualizaciones'}")
        print(f"  Ingeniero: {project['engineer_name'] or 'Sin asignar'}")
        print(f"  Equipo: {project['team_name']}")
    
    print("\nObteniendo detalles de progreso para un proyecto específico...")
    project_id = 1  # ID del Sistema de Gestión
    project_progress = get_project_progress(project_id)
    
    if project_progress:
        print(f"\nDetalles del proyecto {project_id}:")
        print(f"  Nombre: {project_progress['product']['name']}")
        print(f"  Descripción: {project_progress['product']['description']}")
        print(f"  Estado: {project_progress['product']['status']}")
        print(f"  Porcentaje total: {project_progress['total_percentage']}%")
        
        print(f"\n  Ingenieros asignados: {len(project_progress['engineers'])}")
        for i, engineer in enumerate(project_progress['engineers'], 1):
            print(f"\n  Ingeniero {i}:")
            print(f"    Nombre: {engineer['name']}")
            print(f"    Especialidad: {engineer['specialty']}")
            print(f"    Fecha inicio: {engineer['start_date']}")
            print(f"    Fecha fin: {engineer['end_date'] or 'En progreso'}")
        
        print(f"\n  Avances registrados: {len(project_progress['progress_entries'])}")
        for i, entry in enumerate(project_progress['progress_entries'], 1):
            print(f"\n  Avance {i}:")
            print(f"    Fecha: {entry['date']}")
            print(f"    Ingeniero: {entry['engineer_name']}")
            print(f"    Descripción: {entry['description']}")
            print(f"    Porcentaje: {entry['percentage']}%")
    else:
        print(f"No se encontró información de progreso para el proyecto {project_id}")

if __name__ == "__main__":
    test_progress()