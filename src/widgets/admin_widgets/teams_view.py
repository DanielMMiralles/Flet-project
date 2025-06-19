import flet as ft
from services.product_service import get_approved_products, get_product_by_id
from services.engineer_service import get_available_engineers, get_engineer_by_id
from services.assignment_service import assign_engineers_to_project, get_project_engineers, remove_engineer_from_project
from services.progress_service import get_project_progress
from widgets.snackbar_design import modern_snackbar

def teams_view(page: ft.Page):
    """Vista de gestión de equipos para proyectos"""
    
    # Paleta de colores de la aplicación
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    card_color = ft.Colors.WHITE
    text_color = ft.Colors.BLUE_GREY_800
    
    # Obtener proyectos aprobados
    projects = get_approved_products()
    
    # Separar proyectos con y sin ingenieros asignados
    projects_with_engineers = []
    projects_without_engineers = []
    
    for project in projects:
        engineers = get_project_engineers(project["id"])
        if engineers and len(engineers) > 0:
            project["assigned_engineers"] = engineers
            project["progress"] = get_project_progress(project["id"])
            projects_with_engineers.append(project)
        else:
            project["assigned_engineers"] = []
            projects_without_engineers.append(project)
    
    # Estado para rastrear qué proyectos están expandidos
    expanded_projects = {}
    
    # Estado para el proyecto seleccionado para asignación
    selected_project = None
    selected_engineers = []
    
    # Función para actualizar la vista
    def refresh_view():
        nonlocal projects, projects_with_engineers, projects_without_engineers
        
        # Obtener proyectos actualizados
        projects = get_approved_products()
        
        # Separar proyectos con y sin ingenieros asignados
        projects_with_engineers = []
        projects_without_engineers = []
        
        for project in projects:
            engineers = get_project_engineers(project["id"])
            if engineers and len(engineers) > 0:
                project["assigned_engineers"] = engineers
                project["progress"] = get_project_progress(project["id"])
                projects_with_engineers.append(project)
            else:
                project["assigned_engineers"] = []
                projects_without_engineers.append(project)
        
        # Actualizar las listas de proyectos
        projects_without_engineers_list.controls = [
            create_project_card(project, False) for project in projects_without_engineers
        ]
        
        projects_with_engineers_list.controls = [
            create_project_card(project, True) for project in projects_with_engineers
        ]
        
        # Actualizar mensajes de no hay proyectos
        no_unassigned_projects_message.visible = len(projects_without_engineers) == 0
        no_assigned_projects_message.visible = len(projects_with_engineers) == 0
        
        # Actualizar contadores
        unassigned_count.value = f"{len(projects_without_engineers)} proyectos sin asignar"
        assigned_count.value = f"{len(projects_with_engineers)} proyectos con equipo asignado"
        
        page.update()
    
    # Función para alternar la expansión de un proyecto
    def toggle_project_expansion(e, project_id):
        expanded_projects[project_id] = not expanded_projects.get(project_id, False)
        refresh_view()
    
    # Función para mostrar el diálogo de asignación de ingenieros (ORIGINAL)
    def show_assignment_dialog(e, project):
        print("EJECUTANDO show_assignment_dialog ORIGINAL")
        nonlocal selected_project, selected_engineers
        selected_project = project
        selected_engineers = []
        
        # FORZAR cierre completo de cualquier diálogo existente
        if hasattr(page, 'dialog') and page.dialog:
            page.close(page.dialog)
        page.dialog = None
        page.update()
        import time
        time.sleep(0.1)
        
        # Obtener datos completamente frescos de la base de datos
        assigned_engineers = get_project_engineers(project["id"])
        engineers_needed = project['engineers'] - len(assigned_engineers)
        
        # Si ya están todos asignados, no mostrar el diálogo
        if engineers_needed <= 0:
            page.snackbar = modern_snackbar(
                "Este proyecto ya tiene todos los ingenieros asignados",
                "info",
                3000
            )
            page.open(page.snackbar)
            return
        
        # Obtener ingenieros disponibles y filtrar los ya asignados
        available_engineers = get_available_engineers()
        assigned_engineer_ids = [eng["id"] for eng in assigned_engineers]
        available_engineers = [eng for eng in available_engineers if eng["id"] not in assigned_engineer_ids]
        
        # Crear lista de ingenieros con checkboxes
        engineer_checkboxes = []
        for engineer in available_engineers:
            checkbox = ft.Checkbox(
                label=f"{engineer['name']} - {engineer['specialty']}",
                value=False,
                on_change=lambda e, eng_id=engineer['id']: toggle_engineer_selection(e, eng_id)
            )
            engineer_checkboxes.append(checkbox)
        
        # Función para manejar la selección de ingenieros
        def toggle_engineer_selection(e, engineer_id):
            if e.control.value:
                if engineer_id not in selected_engineers:
                    selected_engineers.append(engineer_id)
            else:
                if engineer_id in selected_engineers:
                    selected_engineers.remove(engineer_id)
            
            # Actualizar contador y botón de asignar
            engineers_count_text.value = f"Ingenieros seleccionados: {len(selected_engineers)}/{engineers_needed}"
            assign_button.disabled = len(selected_engineers) != engineers_needed
            
            page.update()
        
        # Texto para mostrar el número de ingenieros seleccionados
        engineers_count_text = ft.Text(
            f"Ingenieros seleccionados: 0/{engineers_needed}",
            color=primary_color,
            weight="bold"
        )
        
        # Botón para asignar ingenieros
        assign_button = ft.ElevatedButton(
            "Asignar ingenieros",
            icon=ft.Icons.ASSIGNMENT_TURNED_IN,
            disabled=True,
            on_click=lambda e: assign_engineers(project['id'])
        )
        
        # Función para asignar ingenieros al proyecto
        def assign_engineers(project_id):
            success = assign_engineers_to_project(project_id, selected_engineers)
            
            if success:
                # FORZAR cierre completo del diálogo (solución que funciona)
                if hasattr(page, 'dialog') and page.dialog:
                    page.close(page.dialog)
                page.dialog = None
                page.update()
                
                page.snackbar = modern_snackbar(
                    "Ingenieros asignados correctamente",
                    "success",
                    3000
                )
                page.open(page.snackbar)
                refresh_view()
                
                # Esperar un momento para que se actualice la base de datos
                import time
                time.sleep(0.1)
                
                # Obtener el proyecto completamente actualizado
                updated_projects = get_approved_products()
                updated_project = None
                for p in updated_projects:
                    if p["id"] == project["id"]:
                        updated_project = p
                        break
                
                # Verificar si aún faltan ingenieros por asignar
                if updated_project:
                    # Obtener datos completamente frescos de la base de datos
                    fresh_assigned = get_project_engineers(updated_project["id"])
                    engineers_still_needed = updated_project["engineers"] - len(fresh_assigned)
                    
                    if engineers_still_needed > 0:
                        # Cerrar el diálogo actual completamente
                        page.close(page.dialog)
                        page.update()
                        
                        # Esperar un momento para asegurar el cierre
                        import time
                        time.sleep(0.2)
                        
                        # Crear y abrir un nuevo diálogo completamente fresco
                        show_assignment_dialog(None, updated_project)
                    else:
                        # Proyecto completo
                        page.snackbar = modern_snackbar(
                            "Proyecto completamente asignado",
                            "success",
                            2000
                        )
                        page.open(page.snackbar)
            else:
                page.snackbar = modern_snackbar(
                    "Error al asignar ingenieros",
                    "error",
                    3000
                )
                page.open(page.snackbar)
            
            page.update()
        
        # Función para cerrar el diálogo
        def close_dialog(e=None):
            if page.dialog:
                page.close(page.dialog)
            page.dialog = None
            page.update()
        
        # Crear el diálogo
        dialog = ft.AlertDialog(
            title=ft.Text(f"Asignar ingenieros a {project['name']}"),
            content=ft.Column(
                controls=[
                    # Información del proyecto
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del proyecto", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.INVENTORY_2, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Proyecto: {project['name']}", size=14, color=text_color)
                                    ],
                                    spacing=10
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
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Duración estimada: {project['days']} días", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PEOPLE, size=16, color=ft.Colors.RED),
                                        ft.Text(f"Ingenieros requeridos: {project['engineers']}", size=14, color=ft.Colors.RED)
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
                    
                    ft.Divider(),
                    
                    # Título de la sección de ingenieros
                    ft.Text("Seleccione ingenieros disponibles", weight="bold", size=16),
                    
                    # Lista de ingenieros disponibles
                    ft.Container(
                        content=ft.Column(
                            controls=engineer_checkboxes,
                            spacing=5,
                            scroll=ft.ScrollMode.AUTO
                        ),
                        height=200,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5,
                        padding=10
                    ),
                    
                    # Contador de ingenieros seleccionados
                    engineers_count_text,
                    
                    # Nota importante
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.INFO, size=16, color=ft.Colors.RED),
                                ft.Text(
                                    f"Debe seleccionar exactamente {engineers_needed} ingenieros adicionales para este proyecto.",
                                    color=ft.Colors.RED,
                                    italic=True,
                                    size=12
                                )
                            ],
                            spacing=10
                        ),
                        margin=ft.margin.only(top=10)
                    )
                ],
                spacing=15,
                width=500,
                height=500,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                assign_button
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        # Asegurar que no hay diálogo previo y crear uno completamente nuevo
        page.dialog = None
        page.update()
        
        # Crear y mostrar el nuevo diálogo
        page.dialog = dialog
        page.open(page.dialog)
    
    # Función para mostrar el diálogo de autenticación para editar un proyecto
    def show_auth_dialog(e, project):
        # Campo de contraseña
        password_field = ft.TextField(
            label="Contraseña de administrador",
            password=True,
            border_color=primary_color,
            width=300
        )
        
        # Función para verificar la contraseña
        def verify_password(e):
            # En un caso real, verificaríamos la contraseña contra la base de datos
            # Por ahora, usamos una contraseña fija para demostración
            if password_field.value == "admin123":
                close_dialog()
                show_edit_dialog(project)
            else:
                password_field.error_text = "Contraseña incorrecta"
                page.update()
        
        # Función para cerrar el diálogo
        def close_dialog(e=None):
            if hasattr(page, 'dialog') and page.dialog:
                page.close(page.dialog)
            page.dialog = None
            page.update()
        
        # Crear el diálogo
        dialog = ft.AlertDialog(
            title=ft.Text("Autenticación requerida"),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Para editar un proyecto con ingenieros asignados, debe ingresar la contraseña de administrador.",
                        size=14
                    ),
                    password_field
                ],
                spacing=20,
                width=400
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.ElevatedButton("Verificar", on_click=verify_password)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        # Mostrar el diálogo usando page.open
        page.dialog = dialog
        page.open(page.dialog)
    
    # Función para mostrar el diálogo de edición de un proyecto
    def show_edit_dialog(project):
        # Obtener ingenieros asignados al proyecto (datos actualizados)
        assigned_engineers = get_project_engineers(project["id"])
        
        # Crear lista de ingenieros asignados
        engineer_items = []
        for engineer in assigned_engineers:
            engineer_items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PERSON, color=primary_color),
                            ft.Text(f"{engineer['name']} - {engineer['specialty']}", size=14, color=ft.Colors.BLACK87),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Eliminar ingeniero",
                                on_click=lambda e, eng_id=engineer['id'], proj_id=project['id']: remove_engineer(eng_id, proj_id)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=10,
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_GREY_50
                )
            )
        
        # Función para eliminar un ingeniero del proyecto
        def remove_engineer(engineer_id, project_id):
            success = remove_engineer_from_project(project_id, engineer_id)
            
            if success:
                page.snackbar = modern_snackbar(
                    "Ingeniero eliminado correctamente",
                    "success",
                    3000
                )
                page.open(page.snackbar)
                close_dialog()
                refresh_view()
                # Obtener el proyecto actualizado con los datos más recientes
                updated_projects = get_approved_products()
                updated_project = None
                for p in updated_projects:
                    if p["id"] == project["id"]:
                        p["assigned_engineers"] = get_project_engineers(p["id"])
                        updated_project = p
                        break
                
                # Volver a mostrar el diálogo de edición con la lista actualizada
                if updated_project:
                    show_edit_dialog(updated_project)
            else:
                page.snackbar = modern_snackbar(
                    "Error al eliminar ingeniero",
                    "error",
                    3000
                )
                page.open(page.snackbar)
            
            page.update()
        
        # Función para cerrar el diálogo
        def close_dialog(e=None):
            if hasattr(page, 'dialog') and page.dialog:
                page.close(page.dialog)
            page.dialog = None
            page.update()
        
        # Crear el diálogo
        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar equipo de {project['name']}"),
            content=ft.Column(
                controls=[
                    # Información del proyecto
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del proyecto", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.INVENTORY_2, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Proyecto: {project['name']}", size=14, color=text_color)
                                    ],
                                    spacing=10
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
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Duración estimada: {project['days']} días", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PEOPLE, size=16, color=ft.Colors.RED),
                                        ft.Text(f"Ingenieros requeridos: {project['engineers']}", size=14, color=ft.Colors.RED)
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
                    
                    ft.Divider(),
                    
                    # Título de la sección de ingenieros
                    ft.Text("Ingenieros asignados", weight="bold", size=16),
                    
                    # Lista de ingenieros asignados
                    ft.Container(
                        content=ft.Column(
                            controls=engineer_items,
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO
                        ),
                        height=200,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5,
                        padding=10
                    ),
                    
                    # Nota importante
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.WARNING, size=16, color=ft.Colors.RED),
                                ft.Text(
                                    "Al eliminar ingenieros, deberá asignar nuevos ingenieros para mantener el número requerido.",
                                    color=ft.Colors.RED,
                                    italic=True,
                                    size=12
                                )
                            ],
                            spacing=10
                        ),
                        margin=ft.margin.only(top=10)
                    )
                ],
                spacing=15,
                width=500,
                height=500,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog),
                ft.ElevatedButton(
                    "Asignar nuevos ingenieros",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=lambda e: (close_dialog(), print("LLAMANDO A show_additional_assignment_dialog"), show_additional_assignment_dialog(project))
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        # Mostrar el diálogo usando page.open
        page.dialog = dialog
        page.open(page.dialog)
    
    # Función para crear una tarjeta de proyecto
    def create_project_card(project, has_engineers):
        project_id = project["id"]
        is_expanded = expanded_projects.get(project_id, False)
        
        # Crear los controles para la tarjeta
        card_controls = [
            # Encabezado de la tarjeta
            ft.ListTile(
                leading=ft.Icon(
                    ft.Icons.ENGINEERING if has_engineers else ft.Icons.ASSIGNMENT_LATE,
                    color=primary_color if has_engineers else ft.Colors.ORANGE,
                    size=30
                ),
                title=ft.Text(f"{project['name']}", weight="bold"),
                subtitle=ft.Text(f"Cliente: {project.get('client_name', 'No asignado')} - Duración: {project['days']} días")
            )
        ]
        
        # Si está expandido, añadir los detalles
        if is_expanded:
            # Añadir un divisor
            card_controls.append(ft.Divider(height=1, color=ft.Colors.GREY_300))
            
            # Información del proyecto
            card_controls.append(
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
                                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.BLUE_GREY),
                                    ft.Text(f"Duración estimada: {project['days']} días", size=14, color=text_color)
                                ],
                                spacing=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.PEOPLE, size=16, color=ft.Colors.BLUE_GREY),
                                    ft.Text(f"Ingenieros requeridos: {project['engineers']}", size=14, color=text_color)
                                ],
                                spacing=10
                            )
                        ],
                        spacing=8
                    ),
                    padding=10,
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_GREY_50
                )
            )
            
            # Si tiene ingenieros asignados, mostrar información adicional
            if has_engineers:
                # Progreso del proyecto
                progress_value = project.get("progress", 0) / 100
                
                card_controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Progreso del proyecto", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.ProgressBar(
                                            value=progress_value,
                                            width=300,
                                            color=ft.Colors.GREEN if progress_value >= 0.7 else 
                                                  ft.Colors.ORANGE if progress_value >= 0.3 else 
                                                  ft.Colors.RED
                                        ),
                                        ft.Text(f"{int(progress_value * 100)}%", size=14, color=text_color)
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
                    )
                )
                
                # Ingenieros asignados
                engineers_list = []
                for engineer in project["assigned_engineers"]:
                    engineers_list.append(
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.BLUE_GREY),
                                ft.Text(f"{engineer['name']} - {engineer['specialty']}", size=14, color=text_color)
                            ],
                            spacing=10
                        )
                    )
                
                card_controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Ingenieros asignados", weight="bold", size=16, color=primary_color),
                                *engineers_list
                            ],
                            spacing=8
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10),
                        border_radius=5,
                        bgcolor=ft.Colors.BLUE_GREY_50
                    )
                )
        
        # Añadir los botones de acción
        action_buttons = []
        
        # Botón para ver detalles
        action_buttons.append(
            ft.OutlinedButton(
                "Ocultar detalles" if is_expanded else "Ver detalles",
                icon=ft.Icons.VISIBILITY_OFF if is_expanded else ft.Icons.VISIBILITY,
                on_click=lambda e, pid=project_id: toggle_project_expansion(e, pid),
                style=ft.ButtonStyle(
                    color=ft.Colors.BLUE_GREY if is_expanded else primary_color
                )
            )
        )
        
        # Botones específicos según si tiene ingenieros o no
        if has_engineers:
            action_buttons.append(
                ft.ElevatedButton(
                    "Editar equipo",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e, proj=project: show_auth_dialog(e, proj),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.ORANGE
                    )
                )
            )
        else:
            action_buttons.append(
                ft.ElevatedButton(
                    "Asignar ingenieros",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=lambda e, proj=project: show_assignment_dialog(e, proj),
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREEN
                    )
                )
            )
        
        card_controls.append(
            ft.Row(
                controls=action_buttons,
                alignment=ft.MainAxisAlignment.END,
                spacing=10
            )
        )
        
        # Crear la tarjeta con todos los controles
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=card_controls,
                    spacing=15
                ),
                padding=15,
                width=800
            ),
            elevation=8 if is_expanded else 3,  # Mayor elevación cuando está expandido
            margin=ft.margin.only(bottom=15)
        )
        
        return card
    
    # Contador de proyectos sin asignar
    unassigned_count = ft.Text(
        f"{len(projects_without_engineers)} proyectos sin asignar",
        size=16,
        color=text_color
    )
    
    # Lista de proyectos sin ingenieros asignados
    projects_without_engineers_list = ft.Column(
        controls=[create_project_card(project, False) for project in projects_without_engineers],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Mensaje si no hay proyectos sin asignar
    no_unassigned_projects_message = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=60, color=ft.Colors.GREEN),
                ft.Text("No hay proyectos pendientes de asignación", size=20, color=ft.Colors.GREY_400)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True,
        visible=len(projects_without_engineers) == 0
    )
    
    # Contador de proyectos con equipo asignado
    assigned_count = ft.Text(
        f"{len(projects_with_engineers)} proyectos con equipo asignado",
        size=16,
        color=text_color
    )
    
    # Lista de proyectos con ingenieros asignados
    projects_with_engineers_list = ft.Column(
        controls=[create_project_card(project, True) for project in projects_with_engineers],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Mensaje si no hay proyectos con equipo asignado
    no_assigned_projects_message = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.ENGINEERING, size=60, color=ft.Colors.GREY_400),
                ft.Text("No hay proyectos con equipo asignado", size=20, color=ft.Colors.GREY_400)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True,
        visible=len(projects_with_engineers) == 0
    )
    
    # Función específica para asignar ingenieros adicionales - VERSIÓN COMPLETA Y BONITA
    def show_additional_assignment_dialog(project):
        # Obtener datos frescos
        assigned_engineers = get_project_engineers(project["id"])
        engineers_needed = project['engineers'] - len(assigned_engineers)
        
        if engineers_needed <= 0:
            return
        
        # FORZAR cierre completo
        if hasattr(page, 'dialog') and page.dialog:
            page.close(page.dialog)
        page.dialog = None
        page.update()
        import time
        time.sleep(0.1)
        
        # Obtener ingenieros disponibles y filtrar correctamente
        available_engineers = get_available_engineers()
        assigned_ids = [eng["id"] for eng in assigned_engineers]
        filtered_engineers = [eng for eng in available_engineers if eng["id"] not in assigned_ids]
        
        selected_ids = []
        
        def toggle_selection(eng_id, checkbox_value):
            if checkbox_value:
                if eng_id not in selected_ids:
                    selected_ids.append(eng_id)
            else:
                if eng_id in selected_ids:
                    selected_ids.remove(eng_id)
            
            engineers_count_text.value = f"Ingenieros seleccionados: {len(selected_ids)}/{engineers_needed}"
            assign_button.disabled = len(selected_ids) != engineers_needed
            page.update()
        
        def assign_engineers():
            success = assign_engineers_to_project(project['id'], selected_ids)
            
            if success:
                # Verificar cuántos ingenieros faltan después de la asignación
                after_assigned = get_project_engineers(project["id"])
                engineers_still_needed = project['engineers'] - len(after_assigned)
                
                # FORZAR cierre completo del diálogo (solución que funciona)
                if hasattr(page, 'dialog') and page.dialog:
                    page.close(page.dialog)
                page.dialog = None
                page.update()
                
                page.snackbar = modern_snackbar("Ingenieros asignados correctamente", "success", 2000)
                page.open(page.snackbar)
                refresh_view()
                
                # Si aún faltan ingenieros, mostrar diálogo nuevamente
                if engineers_still_needed > 0:
                    import time
                    time.sleep(0.3)
                    show_additional_assignment_dialog(project)
            else:
                page.snackbar = modern_snackbar("Error al asignar", "error", 2000)
                page.open(page.snackbar)
        
        # Crear checkboxes con ingenieros filtrados
        engineer_checkboxes = []
        for engineer in filtered_engineers:
            active_projects = engineer.get("active_projects", 0)
            checkbox = ft.Checkbox(
                label=f"{engineer['name']} - {engineer['specialty']} (Proyectos: {active_projects}/5)",
                value=False,
                on_change=lambda e, eng_id=engineer['id']: toggle_selection(eng_id, e.control.value)
            )
            engineer_checkboxes.append(checkbox)
        
        # Texto para mostrar el número de ingenieros seleccionados
        engineers_count_text = ft.Text(
            f"Ingenieros seleccionados: 0/{engineers_needed}",
            color=primary_color,
            weight="bold"
        )
        
        # Botón para asignar ingenieros
        assign_button = ft.ElevatedButton(
            "Asignar ingenieros",
            icon=ft.Icons.ASSIGNMENT_TURNED_IN,
            disabled=True,
            on_click=lambda e: assign_engineers()
        )
        
        # Función para cerrar el diálogo con cierre forzado
        def close_dialog(e=None):
            if hasattr(page, 'dialog') and page.dialog:
                page.close(page.dialog)
            page.dialog = None
            page.update()
        
        # Crear el diálogo completo y bonito
        dialog = ft.AlertDialog(
            title=ft.Text(f"Asignar ingenieros adicionales a {project['name']}"),
            content=ft.Column(
                controls=[
                    # Información del proyecto
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del proyecto", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.INVENTORY_2, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Proyecto: {project['name']}", size=14, color=text_color)
                                    ],
                                    spacing=10
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
                                        ft.Icon(ft.Icons.PEOPLE, size=16, color=ft.Colors.RED),
                                        ft.Text(f"Ingenieros requeridos: {project['engineers']}", size=14, color=ft.Colors.RED)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PERSON_ADD, size=16, color=ft.Colors.ORANGE),
                                        ft.Text(f"Ingenieros adicionales necesarios: {engineers_needed}", size=14, color=ft.Colors.ORANGE)
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
                    
                    ft.Divider(),
                    
                    # Título de la sección de ingenieros
                    ft.Text("Seleccione ingenieros disponibles", weight="bold", size=16),
                    
                    # Lista de ingenieros disponibles
                    ft.Container(
                        content=ft.Column(
                            controls=engineer_checkboxes,
                            spacing=5,
                            scroll=ft.ScrollMode.AUTO
                        ),
                        height=200,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5,
                        padding=10
                    ),
                    
                    # Contador de ingenieros seleccionados
                    engineers_count_text,
                    
                    # Nota importante
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.INFO, size=16, color=ft.Colors.RED),
                                ft.Text(
                                    f"Debe seleccionar exactamente {engineers_needed} ingenieros adicionales para completar este proyecto.",
                                    color=ft.Colors.RED,
                                    italic=True,
                                    size=12
                                )
                            ],
                            spacing=10
                        ),
                        margin=ft.margin.only(top=10)
                    )
                ],
                spacing=15,
                width=500,
                height=500,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog()),
                assign_button
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialog
        page.open(page.dialog)
    
    # Vista principal
    return ft.Container(
        content=ft.Column(
            controls=[
                # Encabezado
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Gestión de Equipos", size=32, weight="bold", color=secondary_color),
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
                
                # Sección de proyectos sin asignar
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Título de la sección
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ASSIGNMENT_LATE, color=ft.Colors.ORANGE, size=24),
                                    ft.Text("Proyectos pendientes de asignación", size=20, weight="bold", color=secondary_color),
                                    ft.Container(expand=True),
                                    unassigned_count
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            
                            # Lista de proyectos o mensaje de no hay proyectos
                            ft.Container(
                                content=ft.Stack(
                                    controls=[
                                        projects_without_engineers_list,
                                        no_unassigned_projects_message
                                    ]
                                ),
                                height=300,
                                border_radius=10,
                                padding=10,
                                margin=ft.margin.only(top=10),
                                bgcolor=ft.Colors.WHITE
                            )
                        ],
                        spacing=10
                    ),
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Sección de proyectos con equipo asignado
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Título de la sección
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ENGINEERING, color=primary_color, size=24),
                                    ft.Text("Proyectos con equipo asignado", size=20, weight="bold", color=secondary_color),
                                    ft.Container(expand=True),
                                    assigned_count
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            
                            # Lista de proyectos o mensaje de no hay proyectos
                            ft.Container(
                                content=ft.Stack(
                                    controls=[
                                        projects_with_engineers_list,
                                        no_assigned_projects_message
                                    ]
                                ),
                                height=300,
                                border_radius=10,
                                padding=10,
                                margin=ft.margin.only(top=10),
                                bgcolor=ft.Colors.WHITE
                            )
                        ],
                        spacing=10
                    )
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=30,
        expand=True,
        bgcolor=background_color
    )