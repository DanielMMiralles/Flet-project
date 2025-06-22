import flet as ft
import os
from widgets.app_bar import app_bar
from widgets.page_footer import page_footer
from widgets.client_widgets.product_carousel import products_carousel_view
from widgets.client_widgets.client_request_preview import client_request_preview
from widgets.client_widgets.project_tracking import project_tracking_view
from services.product_service import get_products
from services.client_service import create_request, get_client_by_user_id
from utils.database import get_db_connection


def client_view(page: ft.Page):
    """Vista principal del cliente con diseño moderno y elegante"""
    
    # Paleta de colores consistente con la aplicación
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    
    # Obtener nombre de usuario y rol desde la sesión
    username = page.session_data.get("user", "Usuario")
    role = page.session_data.get("role", "cliente").lower()
    
    # Asignar el AppBar a la página
    page.appbar = app_bar(page, role, username)
    
    # Función para mostrar seguimiento de proyectos
    def show_project_tracking(e):
        # Obtener client_id real
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id FROM Clientes c
                INNER JOIN Usuarios u ON c.id_usuario = u.id
                WHERE u.usuario = ?
            """, (username,))
            result = cursor.fetchone()
            conn.close()
            real_client_id = result["id"] if result else 1
        except:
            real_client_id = 1
            
        page.clean()
        page.add(project_tracking_view(page, real_client_id))
        page.update()
    
    # Guardar ID de cliente en la sesión (valor por defecto = 1)
    page.session_data["client_id"] = 1
    
    # Mostrar snackbar de bienvenida
    def show_welcome_snackbar():
        from widgets.snackbar_design import modern_snackbar
        page.snackbar = modern_snackbar(
            f"¡Bienvenido {username}! Explora nuestro catálogo de soluciones",
            "success",
            4000
        )
        page.open(page.snackbar)
    
    # Programar snackbar después de cargar la vista
    import threading
    timer = threading.Timer(0.5, show_welcome_snackbar)
    timer.start()
    
    # Contenido principal
    content = ft.Column(
        controls=[
            # Hero Section - Diseño moderno de pantalla completa
            ft.Container(
                content=ft.Row(
                    controls=[
                        # Lado izquierdo - Contenido principal
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "FLATICOM",
                                        size=48,
                                        weight="bold",
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        "Soluciones Tecnológicas",
                                        size=24,
                                        weight="w500",
                                        color=ft.Colors.WHITE70,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Transformamos ideas en realidad digital. Desarrollamos soluciones innovadoras que impulsan el crecimiento de tu empresa hacia el futuro.",
                                            size=16,
                                            color=ft.Colors.WHITE60,
                                            text_align=ft.TextAlign.LEFT
                                        ),
                                        margin=ft.margin.only(top=20, bottom=30),
                                        width=500
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Row(
                                                    controls=[
                                                        ft.Icon(ft.Icons.ROCKET_LAUNCH, color=ft.Colors.WHITE, size=20),
                                                        ft.Text("Innovación", color=ft.Colors.WHITE, size=14, weight="bold")
                                                    ],
                                                    spacing=8
                                                ),
                                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                                border_radius=20,
                                                bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
                                            ),
                                            ft.Container(
                                                content=ft.Row(
                                                    controls=[
                                                        ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.WHITE, size=20),
                                                        ft.Text("Crecimiento", color=ft.Colors.WHITE, size=14, weight="bold")
                                                    ],
                                                    spacing=8
                                                ),
                                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                                border_radius=20,
                                                bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
                                            )
                                        ],
                                        spacing=15
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=12
                            ),
                            expand=True,
                            padding=ft.padding.only(left=50, right=30)
                        ),
                        
                        # Lado derecho - Elemento visual
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Icon(
                                            ft.Icons.COMPUTER,
                                            size=120,
                                            color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
                                        ),
                                        width=200,
                                        height=200,
                                        border_radius=100,
                                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                                        alignment=ft.alignment.center
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            width=300,
                            padding=ft.padding.only(right=50)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True
                ),
                height=350,
                margin=ft.margin.only(bottom=40),
                border_radius=25,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[
                        primary_color,
                        secondary_color,
                        ft.Colors.INDIGO_900
                    ]
                ),
                shadow=ft.BoxShadow(
                    spread_radius=3,
                    blur_radius=25,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    offset=ft.Offset(0, 10)
                )
            ),
            
            # Sección de estadísticas y características
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Estadísticas superiores
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("150+", size=32, weight="bold", color=primary_color),
                                            ft.Text("Proyectos Completados", size=14, color=secondary_color, text_align=ft.TextAlign.CENTER)
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    padding=25,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=15,
                                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 6)
                                    ),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("98%", size=32, weight="bold", color=primary_color),
                                            ft.Text("Satisfacción del Cliente", size=14, color=secondary_color, text_align=ft.TextAlign.CENTER)
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    padding=25,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=15,
                                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 6)
                                    ),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("24/7", size=32, weight="bold", color=primary_color),
                                            ft.Text("Soporte Técnico", size=14, color=secondary_color, text_align=ft.TextAlign.CENTER)
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    padding=25,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=15,
                                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 6)
                                    ),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("5★", size=32, weight="bold", color=primary_color),
                                            ft.Text("Calificación Promedio", size=14, color=secondary_color, text_align=ft.TextAlign.CENTER)
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    padding=25,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=15,
                                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                        offset=ft.Offset(0, 6)
                                    ),
                                    expand=True
                                )
                            ],
                            spacing=25
                        ),
                        
                        # Características principales
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    content=ft.Icon(ft.Icons.SPEED, size=50, color=ft.Colors.WHITE),
                                                    width=80,
                                                    height=80,
                                                    border_radius=40,
                                                    bgcolor=primary_color,
                                                    alignment=ft.alignment.center
                                                ),
                                                ft.Text("Desarrollo Ágil", size=18, weight="bold", color=secondary_color),
                                                ft.Text("Metodologías modernas para entregas rápidas y eficientes", 
                                                       size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER)
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=15
                                        ),
                                        padding=30,
                                        border_radius=20,
                                        bgcolor=ft.Colors.WHITE,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=15,
                                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                            offset=ft.Offset(0, 6)
                                        ),
                                        expand=True
                                    ),
                                    
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    content=ft.Icon(ft.Icons.SECURITY, size=50, color=ft.Colors.WHITE),
                                                    width=80,
                                                    height=80,
                                                    border_radius=40,
                                                    bgcolor=primary_color,
                                                    alignment=ft.alignment.center
                                                ),
                                                ft.Text("Máxima Seguridad", size=18, weight="bold", color=secondary_color),
                                                ft.Text("Protección avanzada de datos con estándares internacionales", 
                                                       size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER)
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=15
                                        ),
                                        padding=30,
                                        border_radius=20,
                                        bgcolor=ft.Colors.WHITE,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=15,
                                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                            offset=ft.Offset(0, 6)
                                        ),
                                        expand=True
                                    ),
                                    
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    content=ft.Icon(ft.Icons.SUPPORT_AGENT, size=50, color=ft.Colors.WHITE),
                                                    width=80,
                                                    height=80,
                                                    border_radius=40,
                                                    bgcolor=primary_color,
                                                    alignment=ft.alignment.center
                                                ),
                                                ft.Text("Soporte Continuo", size=18, weight="bold", color=secondary_color),
                                                ft.Text("Asistencia técnica especializada disponible siempre", 
                                                       size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER)
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=15
                                        ),
                                        padding=30,
                                        border_radius=20,
                                        bgcolor=ft.Colors.WHITE,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=15,
                                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                            offset=ft.Offset(0, 6)
                                        ),
                                        expand=True
                                    )
                                ],
                                spacing=25
                            ),
                            margin=ft.margin.only(top=30)
                        )
                    ]
                ),
                margin=ft.margin.only(bottom=50)
            ),
            
            # Sección de productos con diseño moderno
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Header de la sección con diseño atractivo
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    # Lado izquierdo - Texto
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Catálogo de Productos",
                                                    size=36,
                                                    weight="bold",
                                                    color=ft.Colors.WHITE
                                                ),
                                                ft.Text(
                                                    "Descubre nuestras soluciones tecnológicas diseñadas para impulsar tu negocio",
                                                    size=16,
                                                    color=ft.Colors.WHITE70
                                                ),
                                                ft.Container(
                                                    content=ft.Row(
                                                        controls=[
                                                            ft.ElevatedButton(
                                                                "Ver Mis Proyectos",
                                                                icon=ft.Icons.TIMELINE,
                                                                style=ft.ButtonStyle(
                                                                    color=ft.Colors.WHITE,
                                                                    bgcolor=ft.Colors.AMBER_ACCENT,
                                                                    elevation=3
                                                                ),
                                                                on_click=show_project_tracking
                                                            ),
                                                            ft.Container(width=20),
                                                            ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.WHITE60, size=20),
                                                            ft.Text("Explora y selecciona", color=ft.Colors.WHITE60, size=14)
                                                        ],
                                                        spacing=8
                                                    ),
                                                    margin=ft.margin.only(top=15)
                                                )
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                            spacing=8
                                        ),
                                        expand=True,
                                        padding=ft.padding.only(left=40, top=30, bottom=30)
                                    ),
                                    
                                    # Lado derecho - Elemento decorativo
                                    ft.Container(
                                        content=ft.Icon(
                                            ft.Icons.SHOPPING_BAG_OUTLINED,
                                            size=80,
                                            color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
                                        ),
                                        width=150,
                                        alignment=ft.alignment.center
                                    )
                                ]
                            ),
                            margin=ft.margin.only(bottom=40),
                            border_radius=20,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.center_left,
                                end=ft.alignment.center_right,
                                colors=[
                                    secondary_color,
                                    primary_color
                                ]
                            ),
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                offset=ft.Offset(0, 8)
                            )
                        ),
                        
                        # Carrusel con fondo mejorado
                        ft.Container(
                            content=products_carousel_view(page),
                            padding=ft.padding.all(30),
                            border_radius=25,
                            bgcolor=ft.Colors.WHITE,
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                offset=ft.Offset(0, 8)
                            )
                        )
                    ]
                )
            ),
            
            # Espacio adicional
            ft.Container(height=40)
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Contenido principal con scroll y footer al final
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=content,
                padding=ft.padding.symmetric(horizontal=40, vertical=20)
            ),
            ft.Container(height=80),  # Espacio reducido para acercar el footer
            ft.Container(
                content=page_footer(page),
                margin=ft.margin.only(top=50)
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    # Estructura de la página con fondo elegante
    return ft.Container(
        content=main_content,
        bgcolor=background_color,
        expand=True
    )