import flet as ft
from widgets.app_bar import app_bar
from widgets.page_footer import page_footer
from widgets.client_widgets.product_carousel import product_carousel
from widgets.client_widgets.client_request_preview import client_request_preview
from services.product_service import get_products
from services.client_service import create_request, get_client_by_user_id

def client_view(page: ft.Page):
    """Vista principal del cliente"""
    
    # Obtener ID del cliente desde la sesión
    user_id = page.session_data.get("user", {}).get("id")
    client = get_client_by_user_id(user_id) if user_id else None
    client_id = client.id if client else 1  # Usar ID 1 como fallback
    
    # Guardar ID del cliente en la sesión
    page.session_data["client_id"] = client_id
    
    # Función para manejar la selección de un producto
    def handle_product_select(product):
        # Mostrar vista previa del producto
        preview = client_request_preview(
            page=page,
            product=product,
            on_submit=handle_request_submit
        )
    
    # Función para manejar el envío de una solicitud
    def handle_request_submit(product, request_data):
        # Crear solicitud en la base de datos
        success = create_request(
            client_id=request_data["client_id"],
            product_id=request_data["product_id"],
            details=request_data["details"],
            desired_date=request_data["desired_date"]
        )
        
        return success
    
    # Obtener productos
    products = get_products()
    
    # Crear carrusel de productos
    carousel = product_carousel(page, products, on_select=handle_product_select)
    
    # Contenido principal
    content = ft.Column(
        controls=[
            # Bienvenida
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Bienvenido a FLATICOM", size=32, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("Seleccione un producto para comenzar", size=16, color=ft.Colors.WHITE)
                    ],
                    spacing=10
                ),
                padding=20,
                margin=ft.margin.only(bottom=20),
                border_radius=10,
                bgcolor=ft.Colors.BLUE,
                width=page.width
            ),
            
            # Carrusel de productos
            carousel,
            
            # Espacio adicional
            ft.Container(height=50)
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Estructura de la página
    return ft.Column(
        controls=[
            app_bar(page),  # Barra superior
            ft.Container(
                content=content,
                padding=20,
                expand=True
            ),
            page_footer(page)  # Pie de página
        ],
        expand=True
    )