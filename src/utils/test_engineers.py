import sys
import os
from pathlib import Path

# Añadir el directorio src al path para poder importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from services.engineer_service import get_all_engineers, get_available_engineers, get_engineers_by_project

def test_engineers():
    """Prueba los servicios relacionados con ingenieros"""
    print("Obteniendo todos los ingenieros...")
    
    engineers = get_all_engineers()
    
    print(f"\nTotal de ingenieros: {len(engineers)}")
    for i, engineer in enumerate(engineers, 1):
        print(f"\nIngeniero {i}:")
        print(f"  ID: {engineer.id}")
        print(f"  Nombre: {engineer.name}")
        print(f"  Especialidad: {engineer.specialty}")
        print(f"  Disponible: {'Sí' if engineer.available else 'No'}")
    
    print("\nObteniendo ingenieros disponibles...")
    available_engineers = get_available_engineers()
    
    print(f"\nTotal de ingenieros disponibles: {len(available_engineers)}")
    for i, engineer in enumerate(available_engineers, 1):
        print(f"\nIngeniero disponible {i}:")
        print(f"  ID: {engineer.id}")
        print(f"  Nombre: {engineer.name}")
        print(f"  Especialidad: {engineer.specialty}")
    
    print("\nObteniendo ingenieros por proyecto...")
    project_id = 1  # ID del Sistema de Gestión
    project_engineers = get_engineers_by_project(project_id)
    
    print(f"\nIngenieros asignados al proyecto {project_id}: {len(project_engineers)}")
    for i, engineer in enumerate(project_engineers, 1):
        print(f"\nIngeniero asignado {i}:")
        print(f"  ID: {engineer['id']}")
        print(f"  Nombre: {engineer['name']}")
        print(f"  Especialidad: {engineer['specialty']}")
        print(f"  Fecha inicio: {engineer['start_date']}")
        print(f"  Fecha fin: {engineer['end_date'] or 'En progreso'}")

if __name__ == "__main__":
    test_engineers()