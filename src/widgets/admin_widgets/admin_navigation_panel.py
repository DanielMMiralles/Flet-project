import flet as ft

def admin_navigation_panel(page: ft.Page, current_view: str = "dashboard", on_view_change=None):
    """
    Panel de navegación lateral para la vista de administrador en aplicación de escritorio.
    
    Args:
        page: Página de Flet
        current_view: Vista actual para resaltar la opción seleccionada
        on_view_change: Función a llamar cuando se cambia de vista
    """
    
    # Función para crear un elemento de navegación
    def nav_item(icon, label, view_name, badge_count=None):
        is_selected = current_view == view_name
        
        # Contenido del elemento
        controls = [
            ft.Icon(
                icon,
                size=24,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400
            ),
            ft.Container(
                content=ft.Text(
                    label,
                    color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400,
                    size=16,
                    weight="bold" if is_selected else "normal"
                ),
                expand=True
            )
        ]
        
        # Añadir badge si es necesario
        if badge_count is not None and badge_count > 0:
            controls.append(ft.Container(
                content=ft.Text(str(badge_count), size=14, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_500,
                width=28,
                height=28,
                border_radius=14,
                alignment=ft.alignment.center
            ))
        
        # Función para manejar el clic
        def handle_click(e):
            if on_view_change:
                on_view_change(view_name)
        
        return ft.Container(
            content=ft.Row(
                controls=controls,
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=320,
            height=56,
            border_radius=8,
            bgcolor=ft.Colors.BLUE_GREY_800 if is_selected else ft.Colors.TRANSPARENT,
            padding=ft.padding.symmetric(horizontal=20),
            ink=True,
            on_click=handle_click,
            animate=ft.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)
        )

    # Encabezado fijo (siempre visible)
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=40, color=ft.Colors.BLUE_ACCENT),
                ft.Column(
                    controls=[
                        ft.Text("FLATICOM", size=22, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("Panel de Administración", size=14, color=ft.Colors.GREY_400)
                    ],
                    spacing=0
                )
            ],
            spacing=15
        ),
        padding=ft.padding.only(left=20, top=30, bottom=20, right=20),
        width=350
    )
    
    # Perfil de usuario fijo (siempre visible en la parte inferior)
    profile = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("A", size=20, color=ft.Colors.WHITE),
                    width=48,
                    height=48,
                    bgcolor=ft.Colors.BLUE_ACCENT,
                    border_radius=24,
                    alignment=ft.alignment.center
                ),
                ft.Column(
                    controls=[
                        ft.Text("Administrador", size=16, color=ft.Colors.WHITE),
                        ft.Text("admin@flaticom.com", size=14, color=ft.Colors.GREY_400)
                    ],
                    spacing=2
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.GREY_400,
                    tooltip="Cerrar sesión"
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(20),
        margin=ft.margin.only(bottom=10, left=10, right=10, top=10),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        width=330
    )
    
    # Contenido desplazable
    scrollable_content = ft.Column(
        controls=[
            # Sección principal de navegación
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("PRINCIPAL", size=12, color=ft.Colors.GREY_500, weight="bold"),
                        nav_item(ft.Icons.DASHBOARD_ROUNDED, "Visión Global", "dashboard", None),
                        nav_item(ft.Icons.PENDING_ACTIONS, "Solicitudes Pendientes", "requests", 5),
                        nav_item(ft.Icons.GROUPS, "Gestión de Equipos", "teams", None),
                        nav_item(ft.Icons.TRENDING_UP, "Progreso y Avances", "progress", None),
                    ],
                    spacing=8
                ),
                padding=ft.padding.only(left=20, right=20, bottom=30)
            ),

            ft.Divider(height=1, color=ft.Colors.GREY_800),

            # Sección de herramientas
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("HERRAMIENTAS", size=12, color=ft.Colors.GREY_500, weight="bold"),
                        nav_item(ft.Icons.SETTINGS, "Configuración", "settings", None),
                        nav_item(ft.Icons.HELP_OUTLINE, "Ayuda", "help", None),
                        nav_item(ft.Icons.ANALYTICS, "Estadísticas", "stats", None),
                        nav_item(ft.Icons.PEOPLE, "Usuarios", "users", None),
                        nav_item(ft.Icons.FOLDER, "Archivos", "files", None),
                        nav_item(ft.Icons.EMAIL, "Mensajes", "messages", 3),
                    ],
                    spacing=8
                ),
                padding=ft.padding.only(left=20, right=20, top=20, bottom=20)
            ),

            # Información del sistema
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("SISTEMA", size=12, color=ft.Colors.GREY_500, weight="bold"),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.CIRCLE, size=10, color=ft.Colors.GREEN),
                                    ft.Text("Sistema en línea", size=14, color=ft.Colors.GREY_400)
                                ],
                                spacing=10
                            ),
                            padding=ft.padding.symmetric(vertical=10, horizontal=20)
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_400),
                                    ft.Text("Versión 1.2.5", size=14, color=ft.Colors.GREY_400)
                                ],
                                spacing=10
                            ),
                            padding=ft.padding.symmetric(vertical=10, horizontal=20)
                        )
                    ],
                    spacing=5
                ),
                padding=ft.padding.only(left=20, right=20, top=10, bottom=20)
            )
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO  # Habilitar scroll
    )

    # Crear el panel de navegación con estructura de tres partes
    return ft.Container(
        content=ft.Column(
            controls=[
                header,  # Encabezado fijo
                ft.Container(  # Contenido desplazable
                    content=scrollable_content,
                    expand=True
                ),
                profile  # Perfil fijo
            ],
            spacing=0
        ),
        width=350,
        height=page.height,
        bgcolor=ft.Colors.BLUE_GREY_900,
        border_radius=ft.border_radius.only(top_right=15, bottom_right=15),
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            blur_radius=10,
            spread_radius=1,
            offset=ft.Offset(5, 0)
        )
    )