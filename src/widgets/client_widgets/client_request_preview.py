import flet as ft
import time
from models.product import Product
from widgets.snackbar_design import modern_snackbar

def client_request_preview(page: ft.Page, product: Product, on_close=None, on_submit=None):
    """
    Componente de vista previa de solicitud que se desliza desde el lado derecho.
    
    Args:
        page: Página de Flet
        product: Producto seleccionado
        on_close: Función a llamar cuando se cierra la vista previa
        on_submit: Función a llamar cuando se envía la solicitud
    """
    # Función para cerrar el panel con animación
    def close_preview():
        # Animar el panel para que salga de la pantalla
        side_panel.animate_position = ft.Animation(500, ft.AnimationCurve.EASE_OUT)
        side_panel.right = page.width
        overlay.visible = False
        page.update()

        # Llamar a la función de cierre si se proporcionó
        if on_close:
            on_close()

    # Overlay para oscurecer y desenfocar el fondo
    overlay = ft.Container(
        width=page.width,
        height=page.height,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        visible=False,
        on_click=lambda _: close_preview()
    )
    
    # Crear campos con referencias como objetos Control.ref, no como strings
    details_field_ref = ft.Ref[ft.TextField]()
    day_dropdown_ref = ft.Ref[ft.Dropdown]()
    month_dropdown_ref = ft.Ref[ft.Dropdown]()
    year_dropdown_ref = ft.Ref[ft.Dropdown]()
    error_message_ref = ft.Ref[ft.Container]()
    
    # Mapeo de meses a números
    month_mapping = {
        "Enero": "01",
        "Febrero": "02",
        "Marzo": "03",
        "Abril": "04",
        "Mayo": "05",
        "Junio": "06",
        "Julio": "07",
        "Agosto": "08",
        "Septiembre": "09",
        "Octubre": "10",
        "Noviembre": "11",
        "Diciembre": "12"
    }
    
    # Crear el contenido del panel con scroll
    content_column = ft.Column(
        controls=[
            # Encabezado con botón de cierre
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ARROW_BACK_IOS,
                            size=16,
                            color=ft.Colors.BLUE
                        ),
                        ft.Text(
                            "Volver al catálogo",
                            size=14,
                            color=ft.Colors.BLUE,
                            weight="w500"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                border=ft.border.all(1, ft.Colors.BLUE_200),
                border_radius=25,
                margin=ft.margin.only(top=10, bottom=20),
                ink=True,
                animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_TO_LINEAR),
                on_click=lambda _: close_preview()
            ),
            # Información del producto - Color de texto cambiado a negro
            ft.Text(product.name, size=24, weight="bold", color=ft.Colors.BLACK),
            
            ft.Container(
                content=ft.Text(product.description, size=14, color=ft.Colors.BLACK),
                margin=ft.margin.only(top=10, bottom=20)
            ),
            
            # Detalles técnicos - Color de texto cambiado a negro
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.BLUE),
                                ft.Text(f"Duración estimada: {product.days} días", size=14, color=ft.Colors.BLACK)
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=16, color=ft.Colors.BLUE),
                                ft.Text(f"Equipo: {product.engineers} ingenieros", size=14, color=ft.Colors.BLACK)
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.ATTACH_MONEY, size=16, color=ft.Colors.BLUE),
                                ft.Text(f"Presupuesto estimado: ${product.days * product.engineers * 100}", size=14, color=ft.Colors.BLACK)
                            ],
                            spacing=10
                        )
                    ],
                    spacing=15
                ),
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_50
            ),
            
            # Más información del producto - Color de texto cambiado a negro
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Características del producto", size=16, weight="bold", color=ft.Colors.BLACK),
                        ft.Text("• Desarrollo personalizado según sus necesidades", size=14, color=ft.Colors.BLACK),
                        ft.Text("• Soporte técnico incluido por 6 meses", size=14, color=ft.Colors.BLACK),
                        ft.Text("• Actualizaciones gratuitas durante el primer año", size=14, color=ft.Colors.BLACK),
                        ft.Text("• Capacitación para su equipo incluida", size=14, color=ft.Colors.BLACK),
                        ft.Text("• Documentación completa del proyecto", size=14, color=ft.Colors.BLACK),
                    ],
                ),
                margin=ft.margin.only(top=20, bottom=20),
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.GREY_50
            ),
            
            # Formulario de solicitud - Color de texto cambiado a negro
            ft.Text("Detalles adicionales", size=16, weight="bold", color=ft.Colors.BLACK),
            ft.TextField(
                ref=details_field_ref,
                hint_text="Describe tus necesidades específicas...",
                multiline=True,
                min_lines=3,
                max_lines=5,
                border_color=ft.Colors.GREY_400,
                focused_border_color=ft.Colors.BLUE,
                color=ft.Colors.BLACK
            ),
            
            # Fecha de entrega deseada - Color de texto cambiado a negro
            ft.Container(
                content=ft.Text("Fecha de entrega deseada", size=16, weight="bold", color=ft.Colors.BLACK),
                margin=ft.margin.only(top=10, bottom=5)
            ),
            ft.Row(
                controls=[
                    ft.Dropdown(
                        ref=day_dropdown_ref,
                        width=100,
                        label="Día",
                        options=[ft.dropdown.Option(str(i)) for i in range(1, 32)],
                        color=ft.Colors.BLACK,
                        menu_height= 200,
                        enable_filter= True
                    ),
                    ft.Dropdown(
                        ref=month_dropdown_ref,
                        width=120,
                        label="Mes",
                        options=[ft.dropdown.Option(mes) for mes in month_mapping.keys()],
                        color=ft.Colors.BLACK,
                        menu_height= 200,
                        enable_filter= True
                    ),
                    ft.Dropdown(
                        ref=year_dropdown_ref,
                        width=100,
                        label="Año",
                        options=[ft.dropdown.Option(str(i)) for i in range(2023, 2031)],
                        color=ft.Colors.BLACK,
                        menu_height= 200,
                        enable_filter= True
                    )
                ],
                spacing=10
            ),
            
            # Mensaje de error (inicialmente oculto)
            ft.Container(
                ref=error_message_ref,
                content=ft.Text("Por favor complete todos los campos", color=ft.Colors.RED),
                visible=False,
                margin=ft.margin.only(top=10)
            ),
            
            # Botón adicional para solicitar ahora
            ft.Container(
                content=ft.ElevatedButton(
                    "Solicitar ahora",
                    icon=ft.Icons.SHOPPING_CART,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREEN,
                        elevation=5,
                        padding=15
                    ),
                    width=200,
                    on_click=lambda e: validate_and_submit()
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=20, bottom=10)
            ),
            
            # Espacio antes de los botones
            ft.Container(height=20)
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO  # Habilitar scroll
    )
    
    # Panel lateral con la información del producto
    side_panel = ft.Container(
        width=400,
        height=page.height,
        right=page.width,  # Inicialmente fuera de la pantalla
        top=0,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.only(top_left=15, bottom_left=15),
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            blur_radius=15,
            spread_radius=1,
            offset=ft.Offset(-5, 0)
        ),
        padding=ft.padding.only(left=20, right=20, top=20),
        animate_position=ft.Animation(500, ft.AnimationCurve.EASE_IN_TO_LINEAR),
        content=ft.Column(
            controls=[
                # Contenido con scroll
                ft.Container(
                    content=content_column,
                    expand=True
                ),
                
                # Barra de botones fija en la parte inferior
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.OutlinedButton(
                                "Cancelar",
                                icon=ft.Icons.CANCEL,
                                on_click=lambda _: close_preview()
                            ),
                            ft.ElevatedButton(
                                "Enviar solicitud",
                                icon=ft.Icons.SEND,
                                bgcolor=ft.Colors.BLUE,
                                color=ft.Colors.WHITE,
                                on_click=lambda _: validate_and_submit()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10
                    ),
                    padding=ft.padding.only(top=10, bottom=10),
                    bgcolor=ft.Colors.WHITE
                )
            ],
            spacing=0
        )
    )
    
    # Función para validar y enviar la solicitud
    def validate_and_submit():
        # Obtener referencias a los campos
        details_field = details_field_ref.current
        day_dropdown = day_dropdown_ref.current
        month_dropdown = month_dropdown_ref.current
        year_dropdown = year_dropdown_ref.current
        error_message = error_message_ref.current
        
        # Validar que todos los campos estén completos
        if not details_field.value or not day_dropdown.value or not month_dropdown.value or not year_dropdown.value:
            error_message.visible = True
            page.update()
            return
        
        # Ocultar mensaje de error si todo está bien
        error_message.visible = False
        
        # Formatear fecha - Usar el mapeo para obtener el número del mes
        month_number = month_mapping.get(month_dropdown.value, "01")
        desired_date = f"{year_dropdown.value}-{month_number}-{day_dropdown.value.zfill(2)}"
        
        # Crear datos de la solicitud
        request_data = {
            "product_id": product.id,
            "client_id": page.session_data.get("client_id", 1),  # Usar ID del cliente de la sesión o valor por defecto
            "details": details_field.value,
            "desired_date": desired_date
        }
        
        # Mostrar indicador de carga
        page.snackbar = modern_snackbar(
            "Enviando solicitud...",
            "info",
            3000
        )
        page.open(page.snackbar)
        page.update()
        
        # Llamar a la función de envío si se proporcionó
        if on_submit:
            success = on_submit(product, request_data)
            
            # Mostrar mensaje de éxito o error
            if success:
                page.snackbar = modern_snackbar(
                    "Solicitud enviada correctamente",
                    "success",
                    3000
                )
            else:
                page.snackbar = modern_snackbar(
                    "Error al enviar la solicitud",
                    "error",
                    3000
                )
            page.open(page.snackbar)
            page.update()
        else:
            page.snackbar = modern_snackbar(
                "Error al enviar la solicitud",
                "error",
                3000
            )
            page.open(page.snackbar)
            page.update()
        
        # Cerrar la vista previa
        close_preview()
    
    # Función para mostrar la vista previa
    def show_preview():
        # Añadir los componentes a la página si aún no están
        if overlay not in page.overlay:
            page.overlay.append(overlay)
        if side_panel not in page.overlay:
            page.overlay.append(side_panel)

        # Mostrar el overlay
        overlay.visible = True

        # Animar el panel para que entre en la pantalla
        side_panel.animate_position = ft.Animation(500, ft.AnimationCurve.EASE_IN_TO_LINEAR)
        side_panel.right = 0

        # Actualizar la página
        page.update()
    
    # Mostrar la vista previa inmediatamente
    show_preview()
    
    # Devolver funciones para controlar la vista previa
    return {
        "show": show_preview,
        "close": close_preview,
        "submit": validate_and_submit
    }