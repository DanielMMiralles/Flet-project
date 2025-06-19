import flet as ft
import time
from widgets.admin_widgets.admin_navigation_panel import admin_navigation_panel
from widgets.admin_widgets.dashboard_view import dashboard_view

def admin_view(page: ft.Page):
    """Vista principal del panel de administrador"""
    
    # Estado actual de la vista
    current_view = "dashboard"
    
    # Contenedor para el contenido dinámico con animación
    content_area = ft.Container(
        content=dashboard_view(page),  # Vista inicial
        expand=True,
        padding=20,
        bgcolor=ft.Colors.BLUE_GREY_50,
        border_radius=15,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),  # Animación suave
        opacity=1  # Opacidad inicial
    )
    
    # Función para cambiar de vista con animación
    def change_view(view_name):
        nonlocal current_view, nav_panel
        
        # Solo hacer algo si la vista seleccionada es diferente a la actual
        if view_name != current_view:
            current_view = view_name
            
            # Animar la salida del contenido actual
            content_area.opacity = 0
            page.update()
            
            # Actualizar el contenido según la vista seleccionada
            if view_name == "dashboard":
                content_area.content = dashboard_view(page)
            elif view_name == "requests":
                from widgets.admin_widgets.requests_view import requests_view
                content_area.content = requests_view(page)
            elif view_name == "teams":
                from widgets.admin_widgets.teams_view import teams_view
                content_area.content = teams_view(page)
            elif view_name == "progress":
                content_area.content = ft.Text("Vista de Progreso y Avances", size=30, color=ft.Colors.GREY_400)
            else:
                # Vista por defecto o placeholder
                content_area.content = ft.Text(f"Vista {view_name} en construcción", size=30, color=ft.Colors.GREY_400)
            
            # Recrear el panel de navegación con la nueva vista seleccionada
            old_nav_panel = nav_panel
            nav_panel = admin_navigation_panel(page, current_view, change_view)
            
            # Reemplazar el panel antiguo con el nuevo en el layout
            layout_idx = layout.controls.index(old_nav_panel)
            layout.controls[layout_idx] = nav_panel
            
            # Mostrar el contenido inmediatamente
            content_area.opacity = 1
            
            # Actualizar la página
            page.update()
        
    # Panel de navegación
    nav_panel = admin_navigation_panel(page, current_view, change_view)
    
    # Layout principal con panel de navegación y área de contenido
    layout = ft.Row(
        controls=[
            nav_panel,  # Panel de navegación a la izquierda
            content_area  # Área de contenido a la derecha
        ],
        spacing=0,
        expand=True
    )
    
    return layout