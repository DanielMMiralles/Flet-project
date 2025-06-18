import flet as ft
import os
from widgets.app_bar import app_bar
from widgets.page_footer import page_footer
from widgets.client_widgets.product_carousel import products_carousel_view
from widgets.client_widgets.client_request_preview import client_request_preview
from services.product_service import get_products
from services.client_service import create_request, get_client_by_user_id
from utils.database import get_db_connection


def client_view(page: ft.Page):
    """Vista principal del cliente"""
    
    # Obtener nombre de usuario y rol desde la sesión
    username = page.session_data.get("user", "Usuario")
    role = page.session_data.get("role", "cliente").lower()
    
    # Asignar el AppBar a la página
    page.appbar = app_bar(page, role, username)
    
    # Guardar ID de cliente en la sesión (valor por defecto = 1)
    page.session_data["client_id"] = 1
    
    # Contenido principal
    content = ft.Column(
        controls=[
            # Encabezado elegante
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.DASHBOARD_CUSTOMIZE_ROUNDED,
                                    size=36,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    "Catálogo de Soluciones",
                                    size=28,
                                    weight="bold",
                                    color=ft.Colors.WHITE
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Seleccione un producto para ver detalles y enviar una solicitud",
                                size=14,
                                color=ft.Colors.WHITE70,
                                text_align=ft.TextAlign.CENTER
                            ),
                            margin=ft.margin.only(top=5)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                padding=ft.padding.symmetric(vertical=25, horizontal=20),
                margin=ft.margin.only(bottom=20),
                border_radius=15,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[
                        ft.Colors.BLUE_700,
                        ft.Colors.INDIGO_900
                    ]
                ),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    offset=ft.Offset(0, 5)
                )
            ),
            
            # Carrusel de productos
            products_carousel_view(page),
            
            # Espacio adicional
            ft.Container(height=50)
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Estructura de la página
    return ft.Column(
        controls=[
            ft.Container(
                content=content,
                padding=20,
                expand=True
            ),
            page_footer(page)  # Pie de página
        ],
        expand=True
    )