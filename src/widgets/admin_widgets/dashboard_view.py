import flet as ft
from services.dashboard_service import get_dashboard_data

def refresh_dashboard(page: ft.Page):
    """Función para refrescar el dashboard"""
    page.go("/admin")
    page.update()

def dashboard_view(page: ft.Page):
    """Vista de dashboard con visión global de proyectos"""
    
    # Obtener datos reales del dashboard (siempre frescos)
    dashboard_data = get_dashboard_data()
    print(f"Dashboard data: {dashboard_data}")  # Debug
    
    # Paleta de colores de la aplicación
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    card_color = ft.Colors.WHITE
    text_color = ft.Colors.BLUE_GREY_800

    return ft.Container(
        content=ft.Column(
            controls=[
                # Encabezado
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Visión Global", size=32, weight="bold", color=secondary_color),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                tooltip="Actualizar",
                                icon_color=primary_color,
                                on_click=lambda _: refresh_dashboard(page)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.FILTER_LIST,
                                tooltip="Filtrar",
                                icon_color=primary_color
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.only(bottom=20)
                ),
                
                # Tarjetas de resumen
                ft.Row(
                    controls=[
                        # Proyectos activos
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Proyectos Activos", size=16, color=text_color),
                                    ft.Text(str(dashboard_data["active_projects"]), size=40, weight="bold", color=primary_color),
                                    ft.Text("En desarrollo", size=12, color=ft.Colors.GREEN)
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=200,
                            height=120,
                            bgcolor=card_color,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                blur_radius=10,
                                offset=ft.Offset(0, 5)
                            )
                        ),
                        
                        # Solicitudes pendientes
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Solicitudes Pendientes", size=16, color=text_color),
                                    ft.Text(str(dashboard_data["pending_requests"]), size=40, weight="bold", color=ft.Colors.ORANGE),
                                    ft.Text("Requieren atención" if dashboard_data["pending_requests"] > 0 else "No hay solicitudes pendientes", 
                                           size=12, 
                                           color=ft.Colors.RED if dashboard_data["pending_requests"] > 0 else ft.Colors.GREEN)
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=200,
                            height=120,
                            bgcolor=card_color,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                blur_radius=10,
                                offset=ft.Offset(0, 5)
                            )
                        ),
                        
                        # Ingenieros asignados
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Ingenieros Asignados", size=16, color=text_color),
                                    ft.Text(str(dashboard_data["assigned_engineers"]), size=40, weight="bold", color=primary_color),
                                    ft.Text("Trabajando en proyectos", size=12, color=text_color)
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=200,
                            height=120,
                            bgcolor=card_color,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                blur_radius=10,
                                offset=ft.Offset(0, 5)
                            )
                        ),
                        
                        # Proyectos completados
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Proyectos Completados", size=16, color=text_color),
                                    ft.Text(str(dashboard_data["completed_projects"]), size=40, weight="bold", color=ft.Colors.GREEN),
                                    ft.Text("Finalizados con éxito", size=12, color=text_color)
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            width=200,
                            height=120,
                            bgcolor=card_color,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                blur_radius=10,
                                offset=ft.Offset(0, 5)
                            )
                        )
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True  # Permite que las tarjetas se ajusten en pantallas pequeñas
                ),
                
                # Tabla de proyectos recientes
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Proyectos Recientes", size=20, weight="bold", color=secondary_color),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Proyecto", color=text_color)),
                                    ft.DataColumn(ft.Text("Cliente", color=text_color)),
                                    ft.DataColumn(ft.Text("Ingenieros", color=text_color)),
                                    ft.DataColumn(ft.Text("Progreso", color=text_color)),
                                    ft.DataColumn(ft.Text("Estado", color=text_color)),
                                    ft.DataColumn(ft.Text("Acciones", color=text_color))
                                ],
                                rows=get_project_rows(dashboard_data["recent_projects"], primary_color),
                                heading_text_style=ft.TextStyle(color=text_color),
                            )
                        ],
                        spacing=20
                    ),
                    margin=ft.margin.only(top=30),
                    padding=20,
                    bgcolor=card_color,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                        blur_radius=10,
                        offset=ft.Offset(0, 5)
                    )
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=30,
        expand=True,
        bgcolor=background_color
    )

def get_project_rows(projects, primary_color):
    """Genera las filas de la tabla de proyectos"""
    rows = []
    
    # Si no hay proyectos, mostrar mensaje
    if not projects:
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("No hay proyectos recientes")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(""))
                ]
            )
        ]
    
    # Generar filas para cada proyecto
    for project in projects:
        # Determinar color según estado
        status_color = ft.Colors.BLUE
        text_color = ft.Colors.BLUE_GREY_800
        if project["status"] == "completado":
            status_color = ft.Colors.GREEN
            text_color = ft.Colors.GREEN_800
        elif project["status"] == "pendiente":
            status_color = ft.Colors.ORANGE
            text_color = ft.Colors.ORANGE_800
        elif project["status"] == "activo":
            status_color = ft.Colors.BLUE
            text_color = ft.Colors.BLUE_GREY_800
        
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(project["name"], color=text_color)),
                    ft.DataCell(ft.Text(project["client"], color=text_color)),
                    ft.DataCell(ft.Text(project["team"], color=text_color)),  # Ahora muestra los ingenieros asignados
                    ft.DataCell(
                        ft.Container(
                            content=ft.ProgressBar(
                                value=project["progress"],
                                bgcolor=ft.Colors.BLUE_100,
                                color=primary_color
                            ),
                            width=100
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(project["status"].capitalize(), color=ft.Colors.WHITE),
                            bgcolor=status_color,
                            border_radius=15,
                            padding=5,
                            alignment=ft.alignment.center
                        )
                    ),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(icon=ft.Icons.VISIBILITY, icon_color=primary_color),
                                ft.IconButton(icon=ft.Icons.EDIT, icon_color=primary_color)
                            ],
                            spacing=0
                        )
                    )
                ]
            )
        )
    
    return rows