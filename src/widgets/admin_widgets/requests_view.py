import flet as ft
from services.request_service import get_pending_requests, update_request_status, get_request_details
from services.product_service import get_product_by_id
import datetime
from widgets.snackbar_design import modern_snackbar

def requests_view(page: ft.Page):
    """Vista de solicitudes pendientes para el administrador"""
    
    # Paleta de colores de la aplicación
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    card_color = ft.Colors.WHITE
    text_color = ft.Colors.BLUE_GREY_800
    
    # Obtener solicitudes pendientes
    pending_requests = get_pending_requests()
    
    # Función para actualizar la lista de solicitudes
    def refresh_requests():
        nonlocal pending_requests
        pending_requests = get_pending_requests()
        requests_list.controls = [create_request_card(request) for request in pending_requests]
        page.update()
    
    # Función para ver detalles de una solicitud
    def view_request_details(e, request_id):
        # Obtener detalles de la solicitud
        request_details = get_request_details(request_id)
        if not request_details:
            # Mostrar mensaje de error
            page.snackbar = modern_snackbar(
                "Error al obtener detalles de la solicitud",
                "error",
                3000
            )
            page.open(page.snackbar)
            page.update()
            return
        
        # Obtener detalles del producto
        product = get_product_by_id(request_details["product_id"])
        if not product:
            # Mostrar mensaje de error
            page.snackbar = modern_snackbar(
                "Error al obtener detalles del producto",
                "error",
                3000
            )
            page.open(page.snackbar)
            page.update()
            return
        
        # Crear diálogo con detalles
        dialog = ft.AlertDialog(
            title=ft.Text(f"Solicitud #{request_id} - {product.name}"),
            content=ft.Column(
                controls=[
                    # Información del cliente
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del cliente", weight="bold", size=16),
                                ft.Text(f"Cliente: {request_details['client_name']}"),
                                ft.Text(f"Email: {request_details['client_email'] if 'client_email' in request_details else 'No disponible'}"),
                                ft.Text(f"Teléfono: {request_details['client_phone'] if 'client_phone' in request_details else 'No disponible'}")
                            ],
                            spacing=5
                        ),
                        padding=10,
                        border_radius=5,
                        bgcolor=ft.Colors.BLUE_GREY_50
                    ),
                    
                    # Información del producto
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del producto", weight="bold", size=16),
                                ft.Text(f"Producto: {product.name}"),
                                ft.Text(f"Descripción: {product.description}"),
                                ft.Text(f"Duración estimada: {product.days} días"),
                                ft.Text(f"Ingenieros requeridos: {product.engineers}", color=ft.Colors.RED)
                            ],
                            spacing=5
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10),
                        border_radius=5,
                        bgcolor=ft.Colors.BLUE_GREY_50
                    ),
                    
                    # Detalles de la solicitud
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Detalles de la solicitud", weight="bold", size=16),
                                ft.Text(f"Fecha de solicitud: {request_details['request_date']}"),
                                ft.Text(f"Detalles adicionales: {request_details['details'] if request_details['details'] else 'No se proporcionaron detalles adicionales'}")
                            ],
                            spacing=5
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10),
                        border_radius=5,
                        bgcolor=ft.Colors.BLUE_GREY_50
                    ),
                    
                    # Nota importante
                    ft.Container(
                        content=ft.Text(
                            "Nota: La asignación de ingenieros se realizará en el apartado de Gestión de Equipos una vez aprobada la solicitud.",
                            color=ft.Colors.RED,
                            italic=True,
                            size=12
                        ),
                        margin=ft.margin.only(top=15)
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                width=500,
                height=400
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog()),
                ft.TextButton("Rechazar", on_click=lambda e: reject_request_from_dialog(request_id)),
                ft.TextButton("Aprobar", on_click=lambda e: approve_request_from_dialog(request_id, product.id))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        # Función para cerrar el diálogo
        def close_dialog():
            page.dialog = None
            page.update()
        
        # Función para rechazar la solicitud desde el diálogo
        def reject_request_from_dialog(request_id):
            close_dialog()
            reject_request(None, request_id)
        
        # Función para aprobar la solicitud desde el diálogo
        def approve_request_from_dialog(request_id, product_id):
            close_dialog()
            approve_request(None, request_id, product_id)
        
        # Mostrar diálogo
        page.dialog = dialog
        page.update()
    
    # Función para aprobar una solicitud
    def approve_request(e, request_id, product_id):
        # Actualizar estado de la solicitud
        success = update_request_status(request_id, "aprobada")
        
        if success:
            # Mostrar mensaje de éxito
            page.snackbar = modern_snackbar(
                " Solicitud aprobada",
                "success",
                3000
            )
            page.open(page.snackbar)
            
            # Actualizar lista de solicitudes
            refresh_requests()
        else:
            # Mostrar mensaje de error
            page.snackbar = modern_snackbar(
                "Error al aprobar la solicitud",
                "error",
                3000
            )
            page.open(page.snackbar)
        
        page.update()
    
    # Función para rechazar una solicitud
    def reject_request(e, request_id):
        # Actualizar estado de la solicitud
        success = update_request_status(request_id, "rechazada")
        
        if success:
            # Mostrar mensaje de éxito
            page.snackbar = modern_snackbar(
                "Solicitud rechazada correctamente",
                "info",
                3000
            )
            page.open(page.snackbar)
            
            # Actualizar lista de solicitudes
            refresh_requests()
        else:
            # Mostrar mensaje de error
            page.snackbar = modern_snackbar(
                "Error al rechazar la solicitud",
                "error",
                3000
            )
            page.open(page.snackbar)
        
        page.update()
    
    # Función para crear una tarjeta de solicitud
    def create_request_card(request):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Encabezado de la tarjeta
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.REQUEST_PAGE, color=primary_color, size=30),
                            title=ft.Text(f"Solicitud #{request['id']} - {request['product_name']}", weight="bold"),
                            subtitle=ft.Text(f"Cliente: {request['client_name']} - Fecha: {request['request_date']}")
                        ),
                        
                        # Botones de acción
                        ft.Row(
                            controls=[
                                ft.OutlinedButton(
                                    "Ver detalles",
                                    icon=ft.Icons.VISIBILITY,
                                    on_click=lambda e: view_request_details(e, request['id']),
                                    style=ft.ButtonStyle(
                                        color=primary_color
                                    )
                                ),
                                ft.OutlinedButton(
                                    "Rechazar",
                                    icon=ft.Icons.CANCEL,
                                    on_click=lambda e: reject_request(e, request['id']),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.RED
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Aprobar",
                                    icon=ft.Icons.CHECK_CIRCLE,
                                    on_click=lambda e: approve_request(e, request['id'], request['product_id']),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.GREEN
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10
                        )
                    ],
                    spacing=15
                ),
                padding=15,
                width=800
            ),
            elevation=3,
            margin=ft.margin.only(bottom=15)
        )
    
    # Lista de solicitudes pendientes
    requests_list = ft.Column(
        controls=[create_request_card(request) for request in pending_requests],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    # Mensaje si no hay solicitudes
    no_requests_message = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.INBOX, size=60, color=ft.Colors.GREY_400),
                ft.Text("No hay solicitudes pendientes", size=20, color=ft.Colors.GREY_400)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True,
        visible=len(pending_requests) == 0
    )
    
    # Vista principal
    return ft.Container(
        content=ft.Column(
            controls=[
                # Encabezado
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Solicitudes Pendientes", size=32, weight="bold", color=secondary_color),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                tooltip="Actualizar",
                                icon_color=primary_color,
                                on_click=lambda _: refresh_requests()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.padding.only(bottom=20)
                ),
                
                # Contador de solicitudes
                ft.Container(
                    content=ft.Text(
                        f"{len(pending_requests)} solicitudes pendientes",
                        size=16,
                        color=text_color
                    ),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Lista de solicitudes o mensaje de no hay solicitudes
                ft.Stack(
                    controls=[
                        requests_list,
                        no_requests_message
                    ],
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