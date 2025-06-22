import flet as ft
from utils.database import get_db_connection

def project_tracking_view(page: ft.Page, client_id: int):
    """Vista de seguimiento de proyectos para el cliente"""
    
    # Paleta de colores
    primary_color = ft.Colors.AMBER_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.AMBER_50
    card_color = ft.Colors.WHITE
    
    def get_client_projects():
        """Obtiene los proyectos aprobados del cliente con su progreso"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            print(f"\n=== DEBUG SEGUIMIENTO CLIENTE ===")
            print(f"Client ID: {client_id}")
            
            # Verificar solicitudes del cliente
            cursor.execute("""
                SELECT * FROM Solicitudes WHERE id_cliente = ?
            """, (client_id,))
            
            all_requests = cursor.fetchall()
            print(f"Todas las solicitudes del cliente {client_id}: {len(all_requests)}")
            for req in all_requests:
                print(f"  - Solicitud {req['id']}: Producto {req['id_producto']}, Estado: {req['estado']}")
            
            cursor.execute("""
                SELECT DISTINCT p.*, s.fecha_solicitud, s.detalles,
                       COALESCE(pr.porcentaje, 0) as progreso
                FROM Producto p
                INNER JOIN Solicitudes s ON p.id = s.id_producto
                LEFT JOIN Progreso pr ON p.id = pr.id_producto
                WHERE s.id_cliente = ? AND s.estado = 'aprobada'
                ORDER BY s.fecha_solicitud DESC
            """, (client_id,))
            
            projects = []
            for row in cursor.fetchall():
                # Obtener equipo asignado
                cursor.execute("""
                    SELECT i.nombre, i.especialidad
                    FROM Ingenieros i
                    INNER JOIN Asignaciones a ON i.id = a.id_ingeniero
                    WHERE a.id_producto = ?
                """, (row["id"],))
                
                team = cursor.fetchall()
                
                # Obtener últimos avances
                cursor.execute("""
                    SELECT a.fecha, a.descripcion, a.porcentaje, i.nombre as ingeniero
                    FROM Avances a
                    INNER JOIN Ingenieros i ON a.id_ingeniero = i.id
                    WHERE a.id_producto = ?
                    ORDER BY a.fecha DESC
                    LIMIT 3
                """, (row["id"],))
                
                recent_advances = cursor.fetchall()
                
                project = {
                    "id": row["id"],
                    "name": row["nombre"],
                    "description": row["descripcion"],
                    "days": row["dias"],
                    "request_date": row["fecha_solicitud"],
                    "request_details": row["detalles"],
                    "progress": min(100, row["progreso"]),
                    "team": [{"name": t["nombre"], "specialty": t["especialidad"]} for t in team],
                    "recent_advances": [{"date": a["fecha"], "description": a["descripcion"], 
                                       "percentage": a["porcentaje"], "engineer": a["ingeniero"]} for a in recent_advances]
                }
                projects.append(project)
            
            conn.close()
            print(f"Proyectos encontrados: {len(projects)}")
            for proj in projects:
                print(f"  - {proj['name']}: {proj['progress']}%")
            print(f"================================\n")
            return projects
            
        except Exception as e:
            print(f"Error obteniendo proyectos del cliente: {e}")
            return []
    
    def create_project_card(project):
        """Crea una tarjeta de proyecto con su progreso"""
        progress_value = project["progress"] / 100
        progress_color = (ft.Colors.GREEN if progress_value >= 0.7 else 
                         ft.Colors.ORANGE if progress_value >= 0.3 else 
                         ft.Colors.RED)
        
        # Estado del proyecto
        if progress_value >= 1.0:
            status = "Completado"
            status_color = ft.Colors.GREEN
            status_icon = ft.Icons.CHECK_CIRCLE
        elif progress_value >= 0.5:
            status = "En Desarrollo"
            status_color = ft.Colors.ORANGE
            status_icon = ft.Icons.BUILD_CIRCLE
        else:
            status = "Iniciando"
            status_color = ft.Colors.BLUE
            status_icon = ft.Icons.PLAY_CIRCLE
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header del proyecto
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.WORK, color=ft.Colors.WHITE, size=24),
                                width=50,
                                height=50,
                                border_radius=25,
                                bgcolor=primary_color,
                                alignment=ft.alignment.center
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(project["name"], size=18, weight="bold", color=secondary_color),
                                    ft.Text(f"Solicitado: {project['request_date']}", size=12, color=ft.Colors.GREY_600)
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(status_icon, color=status_color, size=16),
                                        ft.Text(status, color=status_color, weight="bold", size=14)
                                    ],
                                    spacing=5
                                ),
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=15,
                                bgcolor=ft.Colors.with_opacity(0.1, status_color)
                            )
                        ],
                        spacing=15
                    ),
                    
                    # Descripción del proyecto
                    ft.Container(
                        content=ft.Text(project["description"], size=14, color=ft.Colors.GREY_700),
                        padding=ft.padding.symmetric(vertical=10)
                    ),
                    
                    # Barra de progreso
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("Progreso", size=14, weight="bold", color=secondary_color),
                                        ft.Container(expand=True),
                                        ft.Text(f"{project['progress']}%", size=14, weight="bold", color=progress_color)
                                    ]
                                ),
                                ft.ProgressBar(
                                    value=progress_value,
                                    color=progress_color,
                                    bgcolor=ft.Colors.GREY_300,
                                    height=8
                                )
                            ],
                            spacing=8
                        ),
                        margin=ft.margin.only(bottom=15)
                    ),
                    
                    # Información del equipo
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Equipo Asignado", size=14, weight="bold", color=secondary_color),
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.PERSON, size=16, color=primary_color),
                                                    ft.Text(f"{member['name']} - {member['specialty']}", 
                                                           size=12, color=ft.Colors.GREY_700)
                                                ],
                                                spacing=8
                                            ),
                                            padding=ft.padding.symmetric(vertical=2)
                                        ) for member in project["team"]
                                    ] if project["team"] else [
                                        ft.Text("Equipo por asignar", size=12, color=ft.Colors.GREY_500, italic=True)
                                    ],
                                    spacing=2
                                )
                            ],
                            spacing=8
                        ),
                        margin=ft.margin.only(bottom=15)
                    ),
                    
                    # Últimos avances
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Últimos Avances", size=14, weight="bold", color=secondary_color),
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text(f"{advance['engineer']}", size=12, weight="bold", color=secondary_color),
                                                            ft.Container(expand=True),
                                                            ft.Text(f"+{advance['percentage']}%", size=12, color=ft.Colors.GREEN, weight="bold"),
                                                            ft.Text(advance['date'], size=10, color=ft.Colors.GREY_500)
                                                        ]
                                                    ),
                                                    ft.Text(advance['description'], size=11, color=ft.Colors.GREY_700)
                                                ],
                                                spacing=3
                                            ),
                                            padding=8,
                                            margin=ft.margin.only(bottom=5),
                                            border_radius=5,
                                            bgcolor=ft.Colors.BLUE_GREY_50,
                                            border=ft.border.all(1, ft.Colors.BLUE_GREY_100)
                                        ) for advance in project["recent_advances"]
                                    ] if project["recent_advances"] else [
                                        ft.Text("No hay avances registrados", size=12, color=ft.Colors.GREY_500, italic=True)
                                    ],
                                    spacing=0
                                )
                            ],
                            spacing=8
                        )
                    )
                ],
                spacing=10
            ),
            padding=20,
            border_radius=15,
            bgcolor=card_color,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            ),
            margin=ft.margin.only(bottom=20)
        )
    
    # Obtener proyectos del cliente
    client_projects = get_client_projects()
    
    # Contenido principal
    return ft.Container(
        content=ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.TIMELINE, size=32, color=primary_color),
                            ft.Text("Seguimiento de Proyectos", size=28, weight="bold", color=secondary_color),
                            ft.Container(expand=True),
                            ft.Text(f"{len(client_projects)} proyectos", size=16, color=ft.Colors.GREY_600)
                        ]
                    ),
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Lista de proyectos o mensaje vacío
                ft.Column(
                    controls=[create_project_card(project) for project in client_projects] if client_projects else [
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(ft.Icons.WORK_OFF, size=80, color=ft.Colors.GREY_300),
                                    ft.Text("No tienes proyectos en desarrollo", size=20, color=ft.Colors.GREY_400, weight="bold"),
                                    ft.Text("Los proyectos aparecerán aquí una vez que sean aprobados", 
                                           size=14, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            ),
                            alignment=ft.alignment.center,
                            height=300,
                            border_radius=15,
                            bgcolor=card_color,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=10,
                                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)
                            )
                        )
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO
                )
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=30,
        bgcolor=background_color,
        expand=True
    )