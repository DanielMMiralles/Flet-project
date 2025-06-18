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
                tooltip="Dashboard",
                on_click=lambda _: page.go(f"/{user_role}/dashboard")
            ),
            *get_role_specific_actions(page, user_role),
            ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                tooltip="Más opciones",
                items=[
                    ft.PopupMenuItem(
                        text="Perfil",
                        icon=ft.Icons.ACCOUNT_CIRCLE,
                        on_click=lambda _: page.go(f"/{user_role}")
                    ),
                    ft.PopupMenuItem(
                        text="Configuración",
                        icon=ft.Icons.SETTINGS
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
    """Botones específicos simplificados"""
    if user_role == "client":
        return [
            ft.IconButton(
                icon=ft.Icons.ADD_TASK,
                icon_size=22,
                tooltip="Nueva Solicitud",
                on_click=lambda _: page.go("/client/new-request")
            )
        ]
    elif user_role == "engineer":
        return [
            ft.IconButton(
                icon=ft.Icons.ASSIGNMENT,
                icon_size=22,
                tooltip="Mis Tareas",
                on_click=lambda _: page.go("/engineer/tasks")
            )
        ]
    elif user_role == "admin":
        return [
            ft.IconButton(
                icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                icon_size=22,
                tooltip="Administración",
                on_click=lambda _: page.go("/admin/dashboard")
            ),
            ft.IconButton(
                icon=ft.Icons.ASSIGNMENT_IND,
                icon_size=22,
                tooltip="Asignar Tareas",
                on_click=lambda _: page.go("/admin/assignments")
            )
        ]
    return []

# Función de logout común
def logout(page: ft.Page):
    page.session_data.clear()
    page.snackbar = modern_snackbar(
        "Sesión cerrada correctamente", 
        "success",
        3000
    )
    page.open(page.snackbar)
    page.go("/login")
    page.update()