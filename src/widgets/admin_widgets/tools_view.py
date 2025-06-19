import flet as ft

def create_tool_view(page: ft.Page, title: str, icon: str, description: str):
    """Vista genérica para herramientas en construcción"""
    
    # Paleta de colores
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    
    return ft.Container(
        content=ft.Column(
            controls=[
                # Encabezado
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(title, size=32, weight="bold", color=secondary_color),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.only(bottom=30)
                ),
                
                # Contenido principal
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(icon, size=120, color=ft.Colors.GREY_300),
                            ft.Text(title, size=28, weight="bold", color=ft.Colors.GREY_400),
                            ft.Text(description, size=16, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
                            ft.Text("Esta funcionalidad estará disponible próximamente", 
                                   size=14, color=ft.Colors.GREY_400, italic=True)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            spacing=10,
            expand=True
        ),
        padding=30,
        expand=True,
        bgcolor=background_color
    )

def settings_view(page: ft.Page):
    """Vista de configuración"""
    return create_tool_view(
        page, 
        "Configuración", 
        ft.Icons.SETTINGS,
        "Administra las configuraciones del sistema y preferencias de la aplicación"
    )

def help_view(page: ft.Page):
    """Vista de ayuda"""
    return create_tool_view(
        page, 
        "Ayuda", 
        ft.Icons.HELP_OUTLINE,
        "Encuentra documentación, tutoriales y soporte técnico"
    )

def stats_view(page: ft.Page):
    """Vista de estadísticas"""
    return create_tool_view(
        page, 
        "Estadísticas", 
        ft.Icons.ANALYTICS,
        "Visualiza métricas, reportes y análisis del rendimiento del sistema"
    )

def users_view(page: ft.Page):
    """Vista de usuarios"""
    return create_tool_view(
        page, 
        "Usuarios", 
        ft.Icons.PEOPLE,
        "Gestiona usuarios, permisos y roles del sistema"
    )

def files_view(page: ft.Page):
    """Vista de archivos"""
    return create_tool_view(
        page, 
        "Archivos", 
        ft.Icons.FOLDER,
        "Administra documentos, archivos y recursos del sistema"
    )

def messages_view(page: ft.Page):
    """Vista de mensajes"""
    return create_tool_view(
        page, 
        "Mensajes", 
        ft.Icons.EMAIL,
        "Centro de comunicaciones y notificaciones del sistema"
    )