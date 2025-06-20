import flet as ft
from widgets.snackbar_design import modern_snackbar

def app_bar(page: ft.Page, user_role: str, user_name: str = "Usuario") -> ft.AppBar:
    # Configuración de colores para tema oscuro
    BG_COLOR = ft.Colors.BLACK12
    TEXT_COLOR = ft.Colors.ON_SURFACE

    # Configuración por rol
    role_config = {
        "admin": {
            "icon": ft.Icons.ADMIN_PANEL_SETTINGS,
            "title": "Admin",
            "color": ft.Colors.PURPLE
        },
        "engineer": {
            "icon": ft.Icons.ENGINEERING,
            "title": "Ingeniero",
            "color": ft.Colors.TEAL
        },
        "client": {
            "icon": ft.Icons.PERSON,
            "title": "Cliente",
            "color": ft.Colors.AMBER
        }
    }
    
    config = role_config.get(user_role, role_config["client"])
    
    # Avatar simple pero efectivo
    avatar = ft.CircleAvatar(
        content=ft.Text(user_name[0].upper(), size=20, color=ft.Colors.WHITE),
        bgcolor=config["color"],
        radius=18
    )
    
    return ft.AppBar(
        title=ft.Row(
            controls=[
                ft.Icon(config["icon"], size=24, color=config["color"]),
                ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                ft.Text(
                    "ProjectFlow", 
                    size=20, 
                    weight="bold",
                    color=TEXT_COLOR
                )
            ],
            spacing=10
        ),
        center_title=False,
        bgcolor=BG_COLOR,
        elevation=2,
        toolbar_height=60,
        leading=ft.Container(
            content=ft.Row(
                controls=[
                    avatar,
                    ft.Column(
                        controls=[
                            ft.Text(
                                user_name,
                                size=14,
                                weight="bold",
                                color=TEXT_COLOR
                            ),
                            ft.Text(
                                config["title"],
                                size=12,
                                color=ft.Colors.with_opacity(0.7, TEXT_COLOR)
                            )
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            margin=ft.margin.only(left=15)
        ),
        leading_width=180,
        actions=[
            ft.IconButton(
                icon=ft.Icons.HOME,
                icon_size=22,
                tooltip="Inicio",
                on_click=lambda _: scroll_to_top(page)
            ),
            *get_role_specific_actions(page, user_role),
            ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                tooltip="Más opciones",
                items=[
                    ft.PopupMenuItem(
                        text="Perfil",
                        icon=ft.Icons.ACCOUNT_CIRCLE,
                        on_click=lambda _: show_profile_info(page, user_name, user_role)
                    ),
                    ft.PopupMenuItem(
                        text="Configuración",
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda _: show_settings_info(page)
                    ),
                    ft.PopupMenuItem(
                        text="Cerrar sesión",
                        icon=ft.Icons.LOGOUT,
                        on_click=lambda _: logout(page)
                    )
                ]
            )
        ]
    )

def get_role_specific_actions(page: ft.Page, user_role: str):
    """Botones específicos con funcionalidad"""
    
    def show_notification(message):
        page.snackbar = modern_snackbar(message, "info", 3000)
        page.open(page.snackbar)
    
    if user_role == "client":
        return [
            ft.IconButton(
                icon=ft.Icons.ADD_TASK,
                icon_size=22,
                tooltip="Nueva Solicitud",
                on_click=lambda _: show_notification("Funcionalidad de nueva solicitud disponible en el catálogo")
            ),
            ft.IconButton(
                icon=ft.Icons.HISTORY,
                icon_size=22,
                tooltip="Historial",
                on_click=lambda _: show_notification("Historial de solicitudes - Próximamente")
            )
        ]
    elif user_role == "engineer":
        return [
            ft.IconButton(
                icon=ft.Icons.ASSIGNMENT,
                icon_size=22,
                tooltip="Mis Tareas",
                on_click=lambda _: show_notification("Panel de tareas del ingeniero")
            ),
            ft.IconButton(
                icon=ft.Icons.TIMELINE,
                icon_size=22,
                tooltip="Progreso",
                on_click=lambda _: show_notification("Seguimiento de progreso de proyectos")
            )
        ]
    elif user_role == "admin":
        return [
            ft.IconButton(
                icon=ft.Icons.DASHBOARD,
                icon_size=22,
                tooltip="Dashboard",
                on_click=lambda _: show_notification("Navegando al dashboard principal")
            ),
            ft.IconButton(
                icon=ft.Icons.NOTIFICATIONS,
                icon_size=22,
                tooltip="Notificaciones",
                on_click=lambda _: show_notification("Sistema de notificaciones - 3 nuevas")
            )
        ]
    return []

# Función para scroll al principio
def scroll_to_top(page: ft.Page):
    page.scroll_to(offset=0, duration=500)
    page.snackbar = modern_snackbar("Volviendo al inicio", "info", 2000)
    page.open(page.snackbar)

# Funciones auxiliares para el menú
def show_profile_info(page: ft.Page, user_name: str, user_role: str):
    page.snackbar = modern_snackbar(
        f"Perfil: {user_name} ({user_role.title()})", 
        "info",
        3000
    )
    page.open(page.snackbar)

def show_settings_info(page: ft.Page):
    page.snackbar = modern_snackbar(
        "Configuración del sistema - Próximamente", 
        "info",
        3000
    )
    page.open(page.snackbar)

# Función para mostrar pantalla de carga
def show_loading_screen(page: ft.Page):
    loading_dialog = ft.AlertDialog(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(width=50, height=50, color=ft.Colors.BLUE_ACCENT),
                    ft.Text("Cerrando sesión...", size=16, text_align=ft.TextAlign.CENTER)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            width=200,
            height=120,
            alignment=ft.alignment.center
        ),
        modal=True
    )
    page.dialog = loading_dialog
    page.open(page.dialog)
    page.update()

# Función de logout con pantalla de carga
def logout(page: ft.Page):
    # Mostrar pantalla de carga
    show_loading_screen(page)
    
    # Función para completar el logout
    def complete_logout():
        # Cerrar diálogo de carga
        if hasattr(page, 'dialog') and page.dialog:
            page.close(page.dialog)
        page.dialog = None
        
        # Limpiar datos de sesión
        page.session_data.clear()
        
        # Limpiar AppBar
        page.appbar = None
        
        # Mostrar mensaje de despedida
        page.snackbar = modern_snackbar(
            "Sesión cerrada correctamente. ¡Hasta pronto!", 
            "success",
            3000
        )
        page.open(page.snackbar)
        
        # Redirigir al login
        page.go("/login")
        page.update()
    
    # Programar cierre después de 1.5 segundos
    import threading
    timer = threading.Timer(1.5, complete_logout)
    timer.start()