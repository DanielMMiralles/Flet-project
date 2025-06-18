import sys
import os
from pathlib import Path

# Añadir el directorio src al path para poder importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from services.dashboard_service import get_dashboard_data

def test_dashboard():
    """Prueba la obtención de datos para el dashboard"""
    print("Obteniendo datos del dashboard...")
    
    dashboard_data = get_dashboard_data()
    
    print("\nResumen del dashboard:")
    print(f"Proyectos activos: {dashboard_data['active_projects']}")
    print(f"Solicitudes pendientes: {dashboard_data['pending_requests']}")
    print(f"Ingenieros asignados: {dashboard_data['assigned_engineers']}")
    print(f"Proyectos completados: {dashboard_data['completed_projects']}")
    
    print("\nProyectos recientes:")
    for i, project in enumerate(dashboard_data['recent_projects'], 1):
        print(f"\nProyecto {i}:")
        print(f"  Nombre: {project['name']}")
        print(f"  Cliente: {project['client']}")
        print(f"  Ingenieros: {project['team']}")
        print(f"  Progreso: {project['progress'] * 100:.0f}%")
        print(f"  Estado: {project['status']}")

if __name__ == "__main__":
    test_dashboard()