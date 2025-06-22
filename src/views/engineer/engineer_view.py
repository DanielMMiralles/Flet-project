import flet as ft
from widgets.app_bar import app_bar
from services.engineer_dashboard_service import get_engineer_dashboard_data, register_progress, get_engineer_projects_for_dropdown
from widgets.snackbar_design import modern_snackbar

def engineer_view(page: ft.Page):
    """Vista principal del ingeniero con diseño moderno"""
    
    # Paleta de colores consistente
    primary_color = ft.Colors.TEAL_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    card_color = ft.Colors.WHITE
    
    # Obtener datos de sesión
    username = page.session_data.get("user", "Ingeniero")
    role = "engineer"  # Forzar rol de ingeniero
    
    # Asignar AppBar
    page.appbar = app_bar(page, role, username)
    
    # Obtener ID del ingeniero (por ahora usaré ID 1 como ejemplo)
    engineer_id = 1
    
    # Obtener datos reales del dashboard
    dashboard_data = get_engineer_dashboard_data(engineer_id)
    
    # Obtener proyectos para el dropdown
    engineer_projects = get_engineer_projects_for_dropdown(engineer_id)
    
    # Referencias para el formulario de registro
    project_dropdown = ft.Ref[ft.Dropdown]()
    progress_field = ft.Ref[ft.TextField]()
    description_field = ft.Ref[ft.TextField]()
    
    # Función para manejar el registro de progreso
    def handle_register_progress():
        if not project_dropdown.current.value or not progress_field.current.value or not description_field.current.value:
            page.snackbar = modern_snackbar("Complete todos los campos", "error", 3000)
            page.open(page.snackbar)
            return
            
        try:
            percentage = int(progress_field.current.value)
            if percentage <= 0:
                page.snackbar = modern_snackbar("El progreso debe ser mayor a 0", "error", 3000)
                page.open(page.snackbar)
                return
            if percentage > 100:
                page.snackbar = modern_snackbar("El progreso no puede ser mayor a 100", "error", 3000)
                page.open(page.snackbar)
                return
        except ValueError:
            page.snackbar = modern_snackbar("El progreso debe ser un número", "error", 3000)
            page.open(page.snackbar)
            return
            
        # Registrar el progreso
        success, message = register_progress(
            engineer_id,
            int(project_dropdown.current.value),
            percentage,
            description_field.current.value
        )
        
        if success:
            page.snackbar = modern_snackbar(message, "success", 3000)
            # Limpiar campos
            project_dropdown.current.value = None
            progress_field.current.value = ""
            description_field.current.value = ""
            # Recargar vista
            page.go("/engineer")
        else:
            page.snackbar = modern_snackbar(message, "error", 3000)
            
        page.open(page.snackbar)
        page.update()
    
    # Dashboard Personal - Métricas
    metrics_section = ft.Row(
        controls=[
            # Mis Proyectos
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.WORK, size=40, color=primary_color),
                        ft.Text(str(dashboard_data["projects_count"]), size=36, weight="bold", color=secondary_color, text_align=ft.TextAlign.CENTER),
                        ft.Text("Mis Proyectos", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=3
                ),
                width=180,
                height=140,
                padding=20,
                border_radius=20,
                bgcolor=card_color,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 6)
                )
            ),
            
            # Tareas Pendientes
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.ASSIGNMENT, size=40, color=ft.Colors.ORANGE),
                        ft.Text(str(dashboard_data["pending_tasks"]), size=36, weight="bold", color=secondary_color, text_align=ft.TextAlign.CENTER),
                        ft.Text("Tareas Pendientes", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=3
                ),
                width=180,
                height=140,
                padding=20,
                border_radius=20,
                bgcolor=card_color,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 6)
                )
            ),
            
            # Progreso Total
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.TRENDING_UP, size=40, color=ft.Colors.GREEN),
                        ft.Text(f"{dashboard_data['avg_progress']}%", size=36, weight="bold", color=secondary_color, text_align=ft.TextAlign.CENTER),
                        ft.Text("Progreso Promedio", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=3
                ),
                width=180,
                height=140,
                padding=20,
                border_radius=20,
                bgcolor=card_color,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 6)
                )
            )
        ],
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    # Función para crear elementos del historial
    def create_advance_item(advance):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=16),
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=primary_color,
                        alignment=ft.alignment.center
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(advance["engineer"], size=14, weight="bold", color=secondary_color),
                                    ft.Container(expand=True),
                                    ft.Text(f"{advance['progress']}%", size=12, color=ft.Colors.GREEN, weight="bold"),
                                    ft.Text(advance["date"], size=12, color=ft.Colors.GREY_500)
                                ]
                            ),
                            ft.Text(advance["description"], size=12, color=ft.Colors.GREY_700, max_lines=2)
                        ],
                        spacing=4,
                        expand=True
                    )
                ],
                spacing=12
            ),
            padding=12,
            margin=ft.margin.only(bottom=8),
            border_radius=10,
            bgcolor=ft.Colors.BLUE_GREY_50,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100)
        )
    
    # Función para crear tarjetas de proyecto expandidas
    def create_project_card(project):
        progress_color = (ft.Colors.GREEN if project["progress"] >= 70 else 
                         ft.Colors.ORANGE if project["progress"] >= 40 else 
                         ft.Colors.RED)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header del proyecto
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.WORK, color=ft.Colors.WHITE, size=28),
                                width=60,
                                height=60,
                                border_radius=30,
                                bgcolor=primary_color,
                                alignment=ft.alignment.center
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(project["name"], size=20, weight="bold", color=secondary_color),
                                    ft.Text(f"Cliente: {project['client']}", size=14, color=ft.Colors.GREY_600),
                                    ft.Text(f"Inicio: {project['start_date']}", size=12, color=ft.Colors.GREY_500)
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Text(f"{project['progress']}%", color=ft.Colors.WHITE, size=16, weight="bold"),
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                border_radius=20,
                                bgcolor=progress_color
                            )
                        ],
                        spacing=15
                    ),
                    
                    # Información del equipo y progreso
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PEOPLE, size=18, color=ft.Colors.GREY_500),
                                        ft.Text(f"{project['team_size']} ingenieros", size=14, color=ft.Colors.GREY_600)
                                    ],
                                    spacing=8
                                ),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "Registrar Avance",
                                    icon=ft.Icons.ADD_TASK,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=primary_color,
                                        elevation=2
                                    ),
                                    height=38
                                )
                            ]
                        ),
                        margin=ft.margin.symmetric(vertical=15)
                    ),
                    
                    # Barra de progreso
                    ft.Container(
                        content=ft.ProgressBar(
                            value=project["progress"] / 100,
                            bgcolor=ft.Colors.GREY_200,
                            color=progress_color,
                            height=10
                        ),
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Historial de avances
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.HISTORY, size=20, color=primary_color),
                                        ft.Text("Historial de Avances", size=16, weight="bold", color=secondary_color),
                                        ft.Container(expand=True),
                                        ft.Text(f"{len(project['advances'])} registros", size=12, color=ft.Colors.GREY_500)
                                    ],
                                    spacing=8
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[create_advance_item(advance) for advance in project["advances"]],
                                        spacing=0,
                                        scroll=ft.ScrollMode.AUTO
                                    ),
                                    height=200,
                                    margin=ft.margin.only(top=12)
                                ),
                                ft.TextButton(
                                    "Ver todos los avances",
                                    icon=ft.Icons.EXPAND_MORE,
                                    style=ft.ButtonStyle(color=primary_color)
                                ) if len(project["advances"]) > 3 else ft.Container()
                            ],
                            spacing=8
                        ),
                        padding=20,
                        border_radius=15,
                        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_50),
                        border=ft.border.all(1, ft.Colors.BLUE_GREY_100)
                    )
                ],
                spacing=15
            ),
            padding=30,
            border_radius=25,
            bgcolor=card_color,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 8)
            ),
            margin=ft.margin.only(bottom=30)
        )
    
    # Lista de proyectos
    projects_section = ft.Container(
        content=ft.Column(
            controls=[
                # Header de la sección
                ft.Row(
                    controls=[
                        ft.Text("Mis Proyectos Asignados", size=24, weight="bold", color=secondary_color),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Actualizar",
                            icon_color=primary_color
                        )
                    ]
                ),
                
                # Lista de proyectos
                ft.Column(
                    controls=[create_project_card(project) for project in dashboard_data["projects"]] if dashboard_data["projects"] else [
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(ft.Icons.WORK_OFF, size=60, color=ft.Colors.GREY_400),
                                    ft.Text("No tienes proyectos asignados", size=18, color=ft.Colors.GREY_500),
                                    ft.Text("Contacta con tu administrador", size=14, color=ft.Colors.GREY_400)
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            alignment=ft.alignment.center,
                            height=200,
                            width=800,
                            border_radius=20,
                            bgcolor=card_color,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)
                            )
                        )
                    ],
                    spacing=0
                )
            ],
            spacing=20
        ),
        margin=ft.margin.only(top=40)
    )
    
    # Sección de registro rápido de avance
    quick_progress_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SPEED, size=28, color=primary_color),
                        ft.Text("Registro Rápido de Avance", size=20, weight="bold", color=secondary_color)
                    ],
                    spacing=10
                ),
                
                ft.Row(
                    controls=[
                        # Selector de proyecto
                        ft.Container(
                            content=ft.Dropdown(
                                ref=project_dropdown,
                                hint_text="Seleccionar proyecto" if engineer_projects else "No hay proyectos asignados",
                                options=[
                                    ft.dropdown.Option(str(p["id"]), p["name"]) for p in engineer_projects
                                ],
                                width=250,
                                disabled=len(engineer_projects) == 0,
                                color=ft.Colors.BLUE_GREY_800
                            ),
                            expand=True
                        ),
                        
                        # Campo de progreso
                        ft.Container(
                            content=ft.TextField(
                                ref=progress_field,
                                hint_text="% Progreso",
                                width=120,
                                suffix_text="%",
                                disabled=len(engineer_projects) == 0,
                                color=ft.Colors.BLUE_GREY_800
                            )
                        ),
                        
                        # Botón de registro
                        ft.ElevatedButton(
                            "Registrar",
                            icon=ft.Icons.SAVE,
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.GREEN if engineer_projects else ft.Colors.GREY,
                                elevation=3
                            ),
                            height=40,
                            disabled=len(engineer_projects) == 0,
                            on_click=lambda _: handle_register_progress()
                        )
                    ],
                    spacing=15
                ),
                
                # Campo de descripción
                ft.TextField(
                    ref=description_field,
                    hint_text="Descripción del avance realizado...",
                    multiline=True,
                    min_lines=2,
                    max_lines=3,
                    border_radius=10,
                    disabled=len(engineer_projects) == 0,
                    color=ft.Colors.BLUE_GREY_800
                )
            ],
            spacing=15
        ),
        padding=25,
        border_radius=20,
        bgcolor=card_color,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 6)
        ),
        margin=ft.margin.only(top=30)
    )
    
    # Contenido principal
    main_content = ft.Column(
        controls=[
            # Hero section con saludo
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"¡Hola, {username}!", size=32, weight="bold", color=ft.Colors.WHITE),
                                ft.Text("Gestiona tus proyectos y registra tu progreso", size=16, color=ft.Colors.WHITE70)
                            ],
                            spacing=5
                        ),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.ENGINEERING, size=60, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE))
                    ]
                ),
                padding=30,
                border_radius=20,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[primary_color, secondary_color]
                ),
                margin=ft.margin.only(bottom=30)
            ),
            
            # Métricas
            metrics_section,
            
            # Proyectos
            projects_section,
            
            # Registro rápido
            quick_progress_section,
            
            # Espacio adicional
            ft.Container(height=50)
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0
    )
    
    # Estructura principal sin footer
    return ft.Container(
        content=ft.Container(
            content=main_content,
            padding=30,
            expand=True
        ),
        bgcolor=background_color,
        expand=True
    )