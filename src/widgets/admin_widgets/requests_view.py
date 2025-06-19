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
    
    # Diccionario para rastrear qué tarjetas están expandidas
    expanded_cards = {}
    
    # Función para actualizar la lista de solicitudes
    def refresh_requests():
        nonlocal pending_requests, expanded_cards
        pending_requests = get_pending_requests()
        
        # Mantener el estado de expansión solo para las solicitudes que aún existen
        new_expanded_cards = {}
        for request in pending_requests:
            request_id = request['id']
            if request_id in expanded_cards:
                new_expanded_cards[request_id] = expanded_cards[request_id]
        
        expanded_cards = new_expanded_cards
        requests_list.controls = [create_request_card(request) for request in pending_requests]
        
        # Actualizar el mensaje de no hay solicitudes
        no_requests_message.visible = len(pending_requests) == 0
        
        page.update()
    
    # Función para alternar la expansión de una tarjeta
    def toggle_card_expansion(e, request_id):
        # Invertir el estado de expansión
        expanded_cards[request_id] = not expanded_cards.get(request_id, False)
        
        # Actualizar la lista de solicitudes para reflejar el cambio
        requests_list.controls = [create_request_card(request) for request in pending_requests]
        page.update()
    
    # Función para aprobar una solicitud
    def approve_request(e, request_id, product_id):
        # Actualizar estado de la solicitud
        success = update_request_status(request_id, "aprobada")
        
        if success:
            # Mostrar mensaje de éxito
            page.snackbar = modern_snackbar(
                "Solicitud aprobada correctamente",
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
        request_id = request['id']
        is_expanded = expanded_cards.get(request_id, False)
        
        # Crear los controles para la tarjeta
        card_controls = [
            # Encabezado de la tarjeta
            ft.ListTile(
                leading=ft.Icon(ft.Icons.REQUEST_PAGE, color=primary_color, size=30),
                title=ft.Text(f"Solicitud #{request['id']} - {request['product_name']}", weight="bold"),
                subtitle=ft.Text(f"Cliente: {request['client_name']} - Fecha: {request['request_date']}")
            )
        ]
        
        # Si está expandido, añadir los detalles
        if is_expanded:
            # Obtener detalles completos de la solicitud
            request_details = get_request_details(request_id)
            product = get_product_by_id(request_details["product_id"]) if request_details else None
            
            if request_details and product:
                # Añadir un divisor
                card_controls.append(ft.Divider(height=1, color=ft.Colors.GREY_300))
                
                # Información del cliente
                card_controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del cliente", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Cliente: {request_details['client_name']}", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.EMAIL, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Email: {request_details.get('client_email', 'No disponible')}", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PHONE, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Teléfono: {request_details.get('client_phone', 'No disponible')}", size=14, color=text_color)
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
                
                # Información del producto
                card_controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Información del producto", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.INVENTORY_2, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Producto: {product.name}", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DESCRIPTION, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Descripción: {product.description}", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Duración estimada: {product.days} días", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.PEOPLE, size=16, color=ft.Colors.RED),
                                        ft.Text(f"Ingenieros requeridos: {product.engineers}", size=14, color=ft.Colors.RED)
                                    ],
                                    spacing=10
                                )
                            ],
                            spacing=8
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10),
                        border_radius=5,
                        bgcolor=ft.Colors.BLUE_GREY_50
                    )
                )
                
                # Detalles de la solicitud
                card_controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Detalles de la solicitud", weight="bold", size=16, color=primary_color),
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.EVENT, size=16, color=ft.Colors.BLUE_GREY),
                                        ft.Text(f"Fecha de solicitud: {request_details['request_date']}", size=14, color=text_color)
                                    ],
                                    spacing=10
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("Detalles adicionales:", size=14, weight="bold", color=text_color),
                                            ft.Text(
                                                request_details['details'] if request_details['details'] else "No se proporcionaron detalles adicionales",
                                                size=14,
                                                color=text_color,
                                                italic=True if not request_details['details'] else False
                                            )
                                        ],
                                        spacing=5
                                    ),
                                    padding=10,
                                    border_radius=5,
                                    bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_GREY_50)
                                )
                            ],
                            spacing=8
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10),
                        border_radius=5,
                        bgcolor=ft.Colors.BLUE_GREY_50
                    )
                )
                
                # Nota importante
                card_controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.INFO, size=16, color=ft.Colors.RED),
                                ft.Text(
                                    "La asignación de ingenieros se realizará en el apartado de Gestión de Equipos una vez aprobada la solicitud.",
                                    color=ft.Colors.RED,
                                    italic=True,
                                    size=12
                                )
                            ],
                            spacing=10
                        ),
                        margin=ft.margin.only(top=15)
                    )
                )
        
        # Añadir los botones de acción
        card_controls.append(
            ft.Row(
                controls=[
                    ft.OutlinedButton(
                        "Ocultar detalles" if is_expanded else "Ver detalles",
                        icon=ft.Icons.VISIBILITY_OFF if is_expanded else ft.Icons.VISIBILITY,
                        on_click=lambda e, rid=request_id: toggle_card_expansion(e, rid),
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_GREY if is_expanded else primary_color
                        )
                    ),
                    ft.OutlinedButton(
                        "Rechazar",
                        icon=ft.Icons.CANCEL,
                        on_click=lambda e, rid=request_id: reject_request(e, rid),
                        style=ft.ButtonStyle(
                            color=ft.Colors.RED
                        )
                    ),
                    ft.ElevatedButton(
                        "Aprobar",
                        icon=ft.Icons.CHECK_CIRCLE,
                        on_click=lambda e, rid=request_id, pid=request['product_id']: approve_request(e, rid, pid),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREEN
                        )
                    )
                ],
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