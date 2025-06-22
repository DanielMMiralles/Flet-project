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
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Obtener proyectos que tienen equipo asignado
            cursor.execute("""
                SELECT DISTINCT p.*, c.nombre as client_name
                FROM Producto p
                INNER JOIN Asignaciones a ON p.id = a.id_producto
                LEFT JOIN Clientes c ON p.client_id = c.id
                ORDER BY p.nombre
            """)
            
            projects_rows = cursor.fetchall()
            active_projects = []
            
            for row in projects_rows:
                # Obtener ingenieros asignados
                cursor.execute("""
                    SELECT i.nombre as name, i.especialidad as specialty
                    FROM Ingenieros i
                    INNER JOIN Asignaciones a ON i.id = a.id_ingeniero
                    WHERE a.id_producto = ?
                """, (row["id"],))
                
                engineers = []
                for eng_row in cursor.fetchall():
                    engineers.append({
                        "name": eng_row["name"],
                        "specialty": eng_row["specialty"]
                    })
                
                # Obtener progreso total
                cursor.execute("""
                    SELECT COALESCE(SUM(porcentaje), 0) as total_progress
                    FROM Avances
                    WHERE id_producto = ?
                """, (row["id"],))
                
                progress_row = cursor.fetchone()
                progress = min(100, progress_row["total_progress"]) if progress_row else 0
                
                # Verificar qué columnas existen
                try:
                    dias = row["dias"] if "dias" in row.keys() else 30
                except (KeyError, IndexError):
                    dias = 30
                
                try:
                    user_desc = row["user_description"] if "user_description" in row.keys() else "No especificada"
                except (KeyError, IndexError):
                    user_desc = "No especificada"
                
                project = {
                    "id": row["id"],
                    "name": row["nombre"],
                    "description": row["descripcion"] or "Sin descripción",
                    "client_name": row["client_name"] or "No asignado",
                    "days": dias,
                    "user_description": user_desc,
                    "assigned_engineers": engineers,
                    "progress": progress
                }
                active_projects.append(project)
            
            conn.close()
            return active_projects
            
        except Exception as e:
            print(f"Error obteniendo proyectos activos: {e}")
            return []
    
    # Obtener avances detallados de un proyecto
    def get_project_advances(project_id):
        """Obtiene los avances registrados por los ingenieros de un proyecto"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Obtener avances con información del ingeniero
            cursor.execute("""
                SELECT a.*, i.nombre as ingeniero_nombre, i.especialidad as especialidad
                FROM Avances a
                JOIN Ingenieros i ON a.id_ingeniero = i.id
                WHERE a.id_producto = ?
                ORDER BY a.fecha DESC
            """, (project_id,))
            
            advances = []
            for row in cursor.fetchall():
                advance = {
                    "id": row["id"],
                    "descripcion": row["descripcion"],
                    "porcentaje": row["porcentaje"],
                    "fecha": row["fecha"],
                    "ingeniero_nombre": row["ingeniero_nombre"],
                    "especialidad": row["especialidad"]
                }
                advances.append(advance)
            
            conn.close()
            return advances
            
        except Exception as e:
            print(f"Error obteniendo avances del proyecto: {e}")
            return []
    
    # Función para eliminar avance
    def delete_advance(advance_id, project_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Avances WHERE id = ?", (advance_id,))
            
            # Recalcular progreso
            cursor.execute("""
                SELECT COALESCE(SUM(porcentaje), 0) as total_progress
                FROM Avances
                WHERE id_producto = ?
            """, (project_id,))
            
            progress_row = cursor.fetchone()
            total_progress = progress_row["total_progress"] if progress_row else 0
            
            # Actualizar tabla Progreso
            cursor.execute("""
                INSERT OR REPLACE INTO Progreso (id_producto, porcentaje, fecha_actualizacion)
                VALUES (?, ?, datetime('now'))
            """, (project_id, total_progress))
            
            conn.commit()
            conn.close()
            return True, "Avance eliminado correctamente"
            
        except Exception as e:
            print(f"Error eliminando avance: {e}")
            return False, f"Error: {str(e)}"
    
    # Función para editar avance
    def edit_advance(advance_id, project_id, new_percentage, new_description):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Avances 
                SET porcentaje = ?, descripcion = ?
                WHERE id = ?
            """, (new_percentage, new_description, advance_id))
            
            # Recalcular progreso
            cursor.execute("""
                SELECT COALESCE(SUM(porcentaje), 0) as total_progress
                FROM Avances
                WHERE id_producto = ?
            """, (project_id,))
            
            progress_row = cursor.fetchone()
            total_progress = progress_row["total_progress"] if progress_row else 0
            
            # Actualizar tabla Progreso
            cursor.execute("""
                INSERT OR REPLACE INTO Progreso (id_producto, porcentaje, fecha_actualizacion)
                VALUES (?, ?, datetime('now'))
            """, (project_id, total_progress))
            
            conn.commit()
            conn.close()
            return True, "Avance actualizado correctamente"
            
        except Exception as e:
            print(f"Error editando avance: {e}")
            return False, f"Error: {str(e)}"
    
    # Función para verificar contraseña de administrador
    def verify_admin_password(password):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar en la tabla Usuarios con rol admin
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM Usuarios
                WHERE password = ? AND rol = 'admin'
            """, (password,))
            
            result = cursor.fetchone()
            conn.close()
            return result["count"] > 0
            
        except Exception as e:
            print(f"Error verificando contraseña: {e}")
            return False
    
    # Función para eliminar proyecto
    def delete_project(project_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Eliminar en orden para respetar foreign keys
            cursor.execute("DELETE FROM Avances WHERE id_producto = ?", (project_id,))
            cursor.execute("DELETE FROM Progreso WHERE id_producto = ?", (project_id,))
            cursor.execute("DELETE FROM Asignaciones WHERE id_producto = ?", (project_id,))
            cursor.execute("DELETE FROM Producto WHERE id = ?", (project_id,))
            
            conn.commit()
            conn.close()
            return True, "Proyecto eliminado correctamente"
            
        except Exception as e:
            print(f"Error eliminando proyecto: {e}")
            return False, f"Error: {str(e)}"
    
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
        nonlocal active_projects, projects_list, selected_project
        current_selected_id = selected_project["id"] if selected_project else None
        
        active_projects = get_active_projects()
        projects_list.controls = [create_project_card(project) for project in active_projects]
        projects_count.value = f"{len(active_projects)} proyectos activos"
        no_projects_message.visible = len(active_projects) == 0
        
        # Actualizar detalles si hay un proyecto seleccionado
        if current_selected_id:
            # Buscar el proyecto actualizado
            updated_project = None
            for proj in active_projects:
                if proj["id"] == current_selected_id:
                    updated_project = proj
                    break
            
            if updated_project:
                select_project(updated_project)
            else:
                selected_project = None
                update_detail_panel()
        
        page.update()
    
    # Función para mostrar diálogo de eliminar proyecto
    def show_delete_project_dialog(project):
        password_field = ft.TextField(
            label="Contraseña de Administrador",
            password=True,
            width=300
        )
        
        def confirm_delete(e):
            if not password_field.value:
                page.snackbar = modern_snackbar("Ingrese la contraseña", "error", 3000)
                page.open(page.snackbar)
                return
            
            if not verify_admin_password(password_field.value):
                page.snackbar = modern_snackbar("Contraseña incorrecta", "error", 3000)
                page.open(page.snackbar)
                return
            
            success, message = delete_project(project["id"])
            page.close(delete_dialog)
            
            if success:
                page.snackbar = modern_snackbar(message, "success", 3000)
                refresh_view()
            else:
                page.snackbar = modern_snackbar(message, "error", 3000)
            
            page.open(page.snackbar)
        
        delete_dialog = ft.AlertDialog(
            title=ft.Text("¿Eliminar proyecto?"),
            content=ft.Column(
                controls=[
                    ft.Text(f"Se eliminará permanentemente el proyecto '{project['name']}' y todos sus datos asociados."),
                    ft.Text("Esta acción no se puede deshacer.", color=ft.Colors.RED, weight="bold"),
                    password_field
                ],
                spacing=10,
                tight=True
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: page.close(delete_dialog)),
                ft.ElevatedButton(
                    "Eliminar", 
                    on_click=confirm_delete,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE
                )
            ]
        )
        page.dialog = delete_dialog
        page.open(delete_dialog)
    
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
                def create_edit_dialog(adv):
                    edit_percentage = ft.TextField(
                        label="Porcentaje",
                        value=str(adv['porcentaje']),
                        width=100,
                        suffix_text="%"
                    )
                    edit_description = ft.TextField(
                        label="Descripción",
                        value=adv['descripcion'],
                        multiline=True,
                        width=300
                    )
                    
                    def save_edit(e):
                        try:
                            new_percentage = int(edit_percentage.value)
                            if new_percentage < 0 or new_percentage > 100:
                                page.snackbar = modern_snackbar("El porcentaje debe estar entre 0 y 100", "error", 3000)
                                page.open(page.snackbar)
                                return
                        except ValueError:
                            page.snackbar = modern_snackbar("El porcentaje debe ser un número", "error", 3000)
                            page.open(page.snackbar)
                            return
                        
                        success, message = edit_advance(adv['id'], project['id'], new_percentage, edit_description.value)
                        page.close(edit_dialog)
                        
                        if success:
                            page.snackbar = modern_snackbar(message, "success", 3000)
                            refresh_view()
                        else:
                            page.snackbar = modern_snackbar(message, "error", 3000)
                        
                        page.open(page.snackbar)
                    
                    edit_dialog = ft.AlertDialog(
                        title=ft.Text("Editar Avance"),
                        content=ft.Column(
                            controls=[edit_percentage, edit_description],
                            spacing=10,
                            tight=True
                        ),
                        actions=[
                            ft.TextButton("Cancelar", on_click=lambda _: page.close(edit_dialog)),
                            ft.ElevatedButton("Guardar", on_click=save_edit)
                        ]
                    )
                    return edit_dialog
                
                def show_edit_dialog(adv):
                    dialog = create_edit_dialog(adv)
                    page.dialog = dialog
                    page.open(dialog)
                
                def confirm_delete(adv):
                    def delete_confirmed(e):
                        success, message = delete_advance(adv['id'], project['id'])
                        page.close(confirm_dialog)
                        
                        if success:
                            page.snackbar = modern_snackbar(message, "success", 3000)
                            refresh_view()
                        else:
                            page.snackbar = modern_snackbar(message, "error", 3000)
                        
                        page.open(page.snackbar)
                    
                    confirm_dialog = ft.AlertDialog(
                        title=ft.Text("¿Eliminar avance?"),
                        content=ft.Text(f"Se eliminará el avance de {adv['porcentaje']}% registrado por {adv['ingeniero_nombre']}"),
                        actions=[
                            ft.TextButton("Cancelar", on_click=lambda _: page.close(confirm_dialog)),
                            ft.ElevatedButton("Eliminar", on_click=delete_confirmed, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
                        ]
                    )
                    page.dialog = confirm_dialog
                    page.open(confirm_dialog)
                
                advance_item = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.PERSON, color=primary_color, size=16),
                                    ft.Text(f"{advance['ingeniero_nombre']} - {advance['especialidad']}", 
                                           weight="bold", size=14, color=text_color),
                                    ft.Container(expand=True),
                                    ft.Text(f"{advance['porcentaje']}%", 
                                           color=ft.Colors.GREEN, weight="bold"),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_size=16,
                                        tooltip="Editar",
                                        on_click=lambda _, adv=advance: show_edit_dialog(adv)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_size=16,
                                        icon_color=ft.Colors.RED,
                                        tooltip="Eliminar",
                                        on_click=lambda _, adv=advance: confirm_delete(adv)
                                    )
                                ]
                            ),
                            ft.Text(advance['descripcion'], size=12, color=text_color),
                            ft.Text(f"Registrado: {advance['fecha']}", 
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
                            ft.Row(
                                controls=[
                                    ft.Text("Información del proyecto", weight="bold", size=16, color=primary_color),
                                    ft.Container(expand=True),
                                    ft.ElevatedButton(
                                        "Eliminar Proyecto",
                                        icon=ft.Icons.DELETE_FOREVER,
                                        bgcolor=ft.Colors.RED,
                                        color=ft.Colors.WHITE,
                                        on_click=lambda _: show_delete_project_dialog(project)
                                    )
                                ]
                            ),
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