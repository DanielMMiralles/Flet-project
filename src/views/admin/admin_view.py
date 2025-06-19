import flet as ft
import time
from widgets.admin_widgets.admin_navigation_panel import admin_navigation_panel
from widgets.admin_widgets.dashboard_view import dashboard_view

def admin_view(page: ft.Page):
    """Vista principal del panel de administrador"""
    
    # Estado actual de la vista
    current_view = "dashboard"
    
    # Mostrar snackbars de bienvenida al cargar la vista
    def show_welcome_snackbars():
        from widgets.snackbar_design import modern_snackbar
        
        # Snackbar de bienvenida
        page.snackbar = modern_snackbar(
            "¡Bienvenido al Panel de Administración!",
            "success",
            3000
        )
        page.open(page.snackbar)
        page.update()
        
        # Esperar y mostrar segundo snackbar con estadísticas
        def show_stats_snackbar():
            from services.request_service import get_pending_requests
            from services.product_service import get_approved_products
            from services.assignment_service import get_project_engineers
            
            # Obtener estadísticas
            pending_requests = len(get_pending_requests())
            projects = get_approved_products()
            unassigned_projects = 0
            
            for project in projects:
                engineers = get_project_engineers(project["id"])
                if not engineers or len(engineers) == 0:
                    unassigned_projects += 1
            
            stats_message = f"📊 {pending_requests} solicitudes pendientes • {unassigned_projects} proyectos sin equipo"
            
            page.snackbar = modern_snackbar(
                stats_message,
                "info",
                4000
            )
            page.open(page.snackbar)
            page.update()
        
        # Programar el segundo snackbar después de 3.5 segundos
        import threading
        timer = threading.Timer(3.5, show_stats_snackbar)
        timer.start()
    
    # Mostrar snackbars de bienvenida
    show_welcome_snackbars()
    
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
                from widgets.admin_widgets.progress_view import progress_view
                content_area.content = progress_view(page)
            elif view_name == "settings":
                from widgets.admin_widgets.tools_view import settings_view
                content_area.content = settings_view(page)
            elif view_name == "help":
                from widgets.admin_widgets.tools_view import help_view
                content_area.content = help_view(page)
            elif view_name == "stats":
                from widgets.admin_widgets.tools_view import stats_view
                content_area.content = stats_view(page)
            elif view_name == "users":
                from widgets.admin_widgets.tools_view import users_view
                content_area.content = users_view(page)
            elif view_name == "files":
                from widgets.admin_widgets.tools_view import files_view
                content_area.content = files_view(page)
            elif view_name == "messages":
                from widgets.admin_widgets.tools_view import messages_view
                content_area.content = messages_view(page)
            else:
                # Vista por defecto o placeholder
                content_area.content = ft.Text(f"Vista {view_name} en construcción", size=30, color=ft.Colors.GREY_400)
            
            # Solo actualizar el contenido sin recrear el panel de navegación
            # El panel se mantiene igual, solo cambia la selección visual
            
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