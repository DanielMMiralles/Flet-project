import flet as ft
from services.product_service import get_approved_products
from services.assignment_service import get_project_engineers
from services.progress_service import get_project_progress, get_project_progress_history
from widgets.snackbar_design import modern_snackbar
import sqlite3
from utils.database import get_db_connection

def progress_view(page: ft.Page):
    """Vista de seguimiento de progreso de proyectos con diseño de dos columnas"""
    
    # Paleta de colores
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    card_color = ft.Colors.WHITE
    text_color = ft.Colors.BLUE_GREY_800
    
    # Estado del proyecto seleccionado
    selected_project = None
    
    # Obtener proyectos activos (con equipo asignado)
    def get_active_projects():
        projects = get_approved_products()
        active_projects = []
        
        for project in projects:
            engineers = get_project_engineers(project["id"])
            if engineers and len(engineers) > 0:
                project["assigned_engineers"] = engineers
                project["progress"] = get_project_progress(project["id"])
                active_projects.append(project)
        
        return active_projects
    
    # Obtener avances detallados de un proyecto
    def get_project_advances(project_id):
        """Obtiene los avances registrados por los ingenieros de un proyecto"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si existe la tabla de avances
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Avances'")
            if not cursor.fetchone():
                # Crear tabla de avances si no existe
                cursor.execute("""
                    CREATE TABLE Avances (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_proyecto INTEGER,
                        id_ingeniero INTEGER,
                        descripcion TEXT,
                        porcentaje_avance REAL,
                        fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_proyecto) REFERENCES Producto(id),
                        FOREIGN KEY (id_ingeniero) REFERENCES Engineer(id)
                    )
                """)
                conn.commit()
                conn.close()
                return []
            
            # Obtener avances con información del ingeniero
            cursor.execute("""
                SELECT a.*, e.name as ingeniero_nombre, e.specialty as especialidad
                FROM Avances a
                JOIN Engineer e ON a.id_ingeniero = e.id
                WHERE a.id_proyecto = ?
                ORDER BY a.fecha_registro DESC
            """, (project_id,))
            
            advances = []
            for row in cursor.fetchall():
                advance = {
                    "id": row["id"],
                    "descripcion": row["descripcion"],
                    "porcentaje_avance": row["porcentaje_avance"],
                    "fecha_registro": row["fecha_registro"],
                    "ingeniero_nombre": row["ingeniero_nombre"],
                    "especialidad": row["especialidad"]
                }
                advances.append(advance)
            
            conn.close()
            return advances
            
        except Exception as e:
            print(f"Error obteniendo avances del proyecto: {e}")
            return []
    
    # Estado de la vista
    active_projects = get_active_projects()
    
    # Función para seleccionar proyecto
    def select_project(project):
        try:
            nonlocal selected_project
            selected_project = project
            update_detail_panel()
            page.update()
        except Exception as e:
            print(f"Error seleccionando proyecto: {e}")
            page.snackbar = modern_snackbar("Error al cargar detalles del proyecto", "error", 3000)
            page.open(page.snackbar)
    
    # Función para actualizar el panel de detalles
    def update_detail_panel():
        try:
            if selected_project:
                advances = get_project_advances(selected_project["id"])
                detail_panel.content = create_detail_content(selected_project, advances)
            else:
                detail_panel.content = create_empty_detail_content()
        except Exception as e:
            print(f"Error actualizando panel de detalles: {e}")
            detail_panel.content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.ERROR, size=60, color=ft.Colors.RED),
                        ft.Text("Error cargando detalles", size=18, color=ft.Colors.RED),
                        ft.Text(str(e), size=12, color=ft.Colors.GREY_600)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.center,
                expand=True
            )
    
    # Función para actualizar la vista
    def refresh_view():
        nonlocal active_projects, projects_list
        active_projects = get_active_projects()
        projects_list.controls = [create_project_card(project) for project in active_projects]
        projects_count.value = f"{len(active_projects)} proyectos activos"
        no_projects_message.visible = len(active_projects) == 0
        
        # Actualizar detalles si hay un proyecto seleccionado
        if selected_project:
            # Buscar el proyecto actualizado
            updated_project = None
            for proj in active_projects:
                if proj["id"] == selected_project["id"]:
                    updated_project = proj
                    break
            
            if updated_project:
                select_project(updated_project)
            else:
                selected_project = None
                update_detail_panel()
        
        page.update()
    
    # Función para crear el contenido del panel de detalles
    def create_detail_content(project, advances):
        progress_value = project["progress"] / 100
        progress_color = (ft.Colors.GREEN if progress_value >= 0.7 else 
                         ft.Colors.ORANGE if progress_value >= 0.3 else 
                         ft.Colors.RED)
        
        # Crear lista de avances
        advance_items = []
        if advances:
            for advance in advances:
                advance_item = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.PERSON, color=primary_color, size=16),
                                    ft.Text(f"{advance['ingeniero_nombre']} - {advance['especialidad']}", 
                                           weight="bold", size=14, color=text_color),
                                    ft.Container(expand=True),
                                    ft.Text(f"{advance['porcentaje_avance']}%", 
                                           color=ft.Colors.GREEN, weight="bold")
                                ]
                            ),
                            ft.Text(advance['descripcion'], size=12, color=text_color),
                            ft.Text(f"Registrado: {advance['fecha_registro']}", 
                                   size=10, color=ft.Colors.GREY_600, italic=True)
                        ],
                        spacing=5
                    ),
                    padding=10,
                    margin=ft.margin.only(bottom=10),
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_200)
                )
                advance_items.append(advance_item)
        else:
            advance_items.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=40, color=ft.Colors.GREY_400),
                            ft.Text("No hay avances registrados", size=16, color=text_color)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    alignment=ft.alignment.center,
                    padding=20
                )
            )
        
        return ft.Column(
            controls=[
                # Encabezado del proyecto
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(project['name'], size=24, weight="bold", color=secondary_color),
                            ft.Text(f"Cliente: {project.get('client_name', 'No asignado')}", 
                                   size=14, color=text_color),
                            ft.Divider()
                        ],
                        spacing=5
                    ),
                    padding=ft.padding.only(bottom=10)
                ),
                
                # Información del proyecto
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Información del proyecto", weight="bold", size=16, color=primary_color),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.DESCRIPTION, size=16, color=ft.Colors.BLUE_GREY),
                                    ft.Text(f"Descripción: {project['description']}", size=14, color=text_color)
                                ],
                                spacing=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.MESSAGE, size=16, color=ft.Colors.BLUE_GREY),
                                    ft.Text(f"Solicitud del cliente: {project.get('user_description', 'No especificada')}", 
                                           size=14, color=text_color)
                                ],
                                spacing=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.BLUE_GREY),
                                    ft.Text(f"Duración estimada: {project['days']} días", size=14, color=text_color)
                                ],
                                spacing=10
                            )
                        ],
                        spacing=8
                    ),
                    padding=10,
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_GREY_50
                ),
                
                # Ingenieros asignados
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Equipo asignado", weight="bold", size=16, color=primary_color),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.PERSON, size=16, color=primary_color),
                                                ft.Text(f"{engineer['name']} - {engineer['specialty']}", 
                                                       size=14, color=text_color)
                                            ],
                                            spacing=10
                                        ),
                                        padding=ft.padding.symmetric(vertical=5, horizontal=10),
                                        border_radius=5,
                                        bgcolor=ft.Colors.WHITE,
                                        border=ft.border.all(1, ft.Colors.BLUE_GREY_200)
                                    )
                                    for engineer in project['assigned_engineers']
                                ],
                                spacing=5
                            )
                        ],
                        spacing=10
                    ),
                    padding=10,
                    margin=ft.margin.only(top=10),
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_GREY_50
                ),
                
                # Barra de progreso
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Progreso actual", weight="bold", size=16, color=primary_color),
                            ft.Row(
                                controls=[
                                    ft.ProgressBar(
                                        value=progress_value,
                                        width=300,
                                        color=progress_color,
                                        bgcolor=ft.Colors.GREY_300
                                    ),
                                    ft.Text(f"{int(progress_value * 100)}%", 
                                           size=16, weight="bold", color=progress_color)
                                ],
                                spacing=10
                            )
                        ],
                        spacing=10
                    ),
                    padding=10,
                    margin=ft.margin.only(top=10),
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_GREY_50
                ),
                
                # Lista de avances
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Avances registrados", weight="bold", size=16, color=primary_color),
                            ft.Container(
                                content=ft.Column(
                                    controls=advance_items,
                                    spacing=5,
                                    scroll=ft.ScrollMode.AUTO
                                ),
                                height=300,
                                border=ft.border.all(1, ft.Colors.GREY_300),
                                border_radius=5,
                                padding=10
                            )
                        ],
                        spacing=10
                    ),
                    margin=ft.margin.only(top=10)
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
    
    # Función para crear contenido vacío del panel de detalles
    def create_empty_detail_content():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.TIMELINE, size=80, color=ft.Colors.GREY_300),
                    ft.Text("Selecciona un proyecto", size=20, color=ft.Colors.GREY_400, weight="bold"),
                    ft.Text("Haz clic en cualquier proyecto de la lista para ver sus detalles y avances", 
                           size=14, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            alignment=ft.alignment.center,
            expand=True
        )
    
    # Función para crear tarjeta de proyecto (versión compacta para lista)
    def create_project_card(project):
        progress_value = project["progress"] / 100
        progress_color = (ft.Colors.GREEN if progress_value >= 0.7 else 
                         ft.Colors.ORANGE if progress_value >= 0.3 else 
                         ft.Colors.RED)
        
        is_selected = selected_project and selected_project["id"] == project["id"]
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Encabezado
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ENGINEERING, color=primary_color, size=20),
                            ft.Column(
                                controls=[
                                    ft.Text(project['name'], weight="bold", size=14, color=secondary_color),
                                    ft.Text(f"Cliente: {project.get('client_name', 'No asignado')}", 
                                           size=12, color=ft.Colors.GREY_600)
                                ],
                                spacing=2,
                                expand=True
                            )
                        ],
                        spacing=10
                    ),
                    
                    # Barra de progreso compacta
                    ft.Row(
                        controls=[
                            ft.ProgressBar(
                                value=progress_value,
                                width=200,
                                color=progress_color,
                                bgcolor=ft.Colors.GREY_300,
                                height=6
                            ),
                            ft.Text(f"{int(progress_value * 100)}%", 
                                   size=12, weight="bold", color=progress_color)
                        ],
                        spacing=10
                    )
                ],
                spacing=8
            ),
            padding=15,
            margin=ft.margin.only(bottom=8),
            border_radius=8,
            bgcolor=primary_color if is_selected else ft.Colors.WHITE,
            border=ft.border.all(2, primary_color if is_selected else ft.Colors.GREY_300),
            ink=True,
            on_click=lambda e: select_project(project),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )
    
    # Contador de proyectos
    projects_count = ft.Text(
        f"{len(active_projects)} proyectos activos",
        size=16,
        color=text_color
    )
    
    # Lista de proyectos
    projects_list = ft.Column(
        controls=[create_project_card(project) for project in active_projects],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Mensaje si no hay proyectos
    no_projects_message = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.TIMELINE, size=60, color=ft.Colors.GREY_400),
                ft.Text("No hay proyectos activos", size=20, color=ft.Colors.GREY_400),
                ft.Text("Los proyectos aparecerán aquí cuando tengan equipos asignados", 
                       size=14, color=ft.Colors.GREY_400)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True,
        visible=len(active_projects) == 0
    )
    
    # Panel de detalles
    detail_panel = ft.Container(
        content=create_empty_detail_content(),
        expand=True,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREY_300)
    )
    
    # Vista principal con diseño de dos columnas
    return ft.Container(
        content=ft.Column(
            controls=[
                # Encabezado
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Seguimiento de Progreso", size=32, weight="bold", color=secondary_color),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                tooltip="Actualizar",
                                icon_color=primary_color,
                                on_click=lambda _: refresh_view()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.only(bottom=20)
                ),
                
                # Contenido principal con dos columnas
                ft.Container(
                    content=ft.Row(
                        controls=[
                            # Columna izquierda - Lista de proyectos
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        # Título de la sección
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.LIST, color=primary_color, size=20),
                                                ft.Text("Proyectos activos", size=18, weight="bold", color=secondary_color),
                                                ft.Container(expand=True),
                                                projects_count
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        
                                        # Lista de proyectos
                                        ft.Container(
                                            content=ft.Stack(
                                                controls=[
                                                    projects_list,
                                                    no_projects_message
                                                ]
                                            ),
                                            height=500,
                                            border_radius=10,
                                            padding=10,
                                            margin=ft.margin.only(top=10),
                                            bgcolor=ft.Colors.WHITE,
                                            border=ft.border.all(1, ft.Colors.GREY_300)
                                        )
                                    ],
                                    spacing=10
                                ),
                                width=350,
                                padding=ft.padding.only(right=10)
                            ),
                            
                            # Columna derecha - Panel de detalles
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        # Título del panel de detalles
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.TIMELINE, color=primary_color, size=20),
                                                ft.Text("Detalles del proyecto", size=18, weight="bold", color=secondary_color)
                                            ],
                                            spacing=10
                                        ),
                                        
                                        # Panel de detalles
                                        ft.Container(
                                            content=detail_panel,
                                            height=500,
                                            margin=ft.margin.only(top=10),
                                            expand=True
                                        )
                                    ],
                                    spacing=10
                                ),
                                expand=True,
                                padding=ft.padding.only(left=10)
                            )
                        ],
                        spacing=0,
                        expand=True
                    ),
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