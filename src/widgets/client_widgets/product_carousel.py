import flet as ft
import os
from models.product import Product
from services.product_service import get_products
from widgets.snackbar_design import modern_snackbar
from widgets.client_widgets.client_request_preview import client_request_preview

def products_carousel_view(page: ft.Page, products=None):
    """Vista de carrusel de productos con diseño moderno en tema oscuro"""
    try:
        # Variable para almacenar el producto seleccionado
        selected_product_id = None
        selected_product = None
        
        
        # Usar los productos proporcionados o obtenerlos si no se proporcionan
        if products is None:
            products = get_products()
            print(f"Productos obtenidos: {len(products)}")

        
        if not products:
            # Si no hay productos, mostrar mensaje
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("No hay productos disponibles", size=20),
                        ft.ElevatedButton("Actualizar", on_click=lambda _: page.update())
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=40,
                alignment=ft.alignment.center
            )

        # Obtener la ruta base del proyecto para las imágenes
        from pathlib import Path
        base_dir = Path(__file__).parent.parent.parent
        assets_dir = os.path.join(base_dir, "assets")
        
        # Función para manejar la selección de tarjetas
        def select_product(e, product_id):
            nonlocal selected_product_id
            # Actualizar el producto seleccionado
            selected_product_id = product_id
            selected_product = next((p for p in products if p.id == product_id), None)

            # Actualizar todas las tarjetas para reflejar la selección
            for card in carousel.controls:
                card_id = getattr(card, "data", None)
                if card_id == selected_product_id:
                    # Tarjeta seleccionada
                    card.border = ft.border.all(3, ft.Colors.BLUE_ACCENT)
                    card.shadow = ft.BoxShadow(
                        color=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_ACCENT),
                        blur_radius=15,
                        spread_radius=2,
                        offset=ft.Offset(0, 0)
                    )
                else:
                    # Tarjeta no seleccionada
                    card.border = None
                    card.shadow = ft.BoxShadow(
                        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                        blur_radius=10,
                        offset=ft.Offset(0, 5)
                    )
            
            # Mostrar el botón de enviar solicitud
            send_request_btn.visible = True
            send_request_btn.text = f"Enviar solicitud para {next((p.name for p in products if p.id == selected_product_id), 'producto')}"
            
            send_request_btn.on_click = lambda e: show_request_preview(e, selected_product)
            page.update()

        # Función para mostrar la vista previa de solicitud
        def show_request_preview(e, product):
            if product:
                client_request_preview(
                    page, 
                    product,
                    on_close=lambda: print(f"Vista previa cerrada para {product.name}"),
                    on_submit=lambda p: modern_snackbar(
                        f"Solicitud enviada para {p.name}",
                        "info",
                        3000
                    )
                )
            else:
                page.snackbar = modern_snackbar(
                    "Error: No se ha seleccionado ningún producto",
                    "warning",
                    3000
                )

        # Crear el botón de enviar solicitud
        send_request_btn = ft.ElevatedButton(
            text="Enviar solicitud",
            icon=ft.Icons.SEND,
            visible=False,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE,
                elevation=5,
                padding=15
            )
        )    

        # Función para crear tarjetas de producto
        def product_card(product: Product, index: int) -> ft.Container:
            # Determinar la URL de la imagen o usar una imagen por defecto
            image_path = product.image
            
            # Si la ruta es relativa, convertirla en absoluta
            if image_path and image_path.startswith('/'):
                # Quitar el slash inicial para unir correctamente con la ruta base
                relative_path = image_path[1:] if image_path.startswith('/') else image_path
                image_path = os.path.join(base_dir, relative_path)
                # Verificar si el archivo existe
                if not os.path.exists(image_path):
                    # Intentar otra ubicación
                    image_path = os.path.join(base_dir, "assets", "productos", os.path.basename(relative_path))
                    if not os.path.exists(image_path):
                        # Caso especial para "Plataforma de Recursos Humanos"
                        if "recursos humanos" in product.name.lower():
                            image_path = os.path.join(base_dir, "assets", "productos", "rh.jpg")
                            if not os.path.exists(image_path):
                                image_path = "https://via.placeholder.com/250x180?text=" + product.name.replace(" ", "+")
                        else:
                            image_path = "https://via.placeholder.com/250x180?text=" + product.name.replace(" ", "+")
            elif not image_path:
                image_path = "https://via.placeholder.com/250x180?text=" + product.name.replace(" ", "+")

            # Calcular la elevación basada en la posición (para efecto 3D)
            # Las tarjetas centrales tendrán más elevación
            center_position = len(products)/2
            distance_from_center = abs(index - center_position)
            max_distance = center_position
            normalized_distance = distance_from_center / max_distance if max_distance > 0 else 1
            elevation_factor = 1 - normalized_distance  # 1 para el centro, 0 para los extremos

            # Aplicar una escala no lineal para hacer el efecto más pronunciado
            elevation_factor = elevation_factor ** 2.5  # Potencia más alta para un efecto más dramático

            
            # Crear la tarjeta
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        # Imagen del producto
                        ft.Container(
                            content=ft.Image(
                                src=image_path,
                                height=180,
                                width=280,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.only(top_left=15, top_right=15)
                            ),
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            border_radius=ft.border_radius.only(top_left=15, top_right=15),
                            bgcolor=ft.Colors.BLUE_GREY_100,
                            width=280,
                            height=180
                        ),
                        
                        # Contenido de la tarjeta
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        product.name,
                                        size=16,
                                        weight="bold",
                                        color=ft.Colors.BLACK,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS
                                    ),
                                    ft.Text(
                                        product.description,
                                        size=12,
                                        color=ft.Colors.GREY_800,
                                        max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=14, color=ft.Colors.BLUE_GREY),
                                            ft.Text(
                                                f"{product.engineers} ingenieros", 
                                                size=12,
                                                color=ft.Colors.BLUE_GREY
                                            ),
                                            ft.VerticalDivider(width=10),
                                            ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.BLUE_GREY),
                                            ft.Text(
                                                f"{product.days} días", 
                                                size=12,
                                                color=ft.Colors.BLUE_GREY
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=5
                                    )
                                ],
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            padding=15,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.WHITE,
                        )
                    ],
                    spacing=0
                ),
                width=280,
                height=300,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                on_click=lambda e: select_product(e, product.id),
                data=product.id,  # Almacenar el ID del producto para referencia
                shadow=ft.BoxShadow(
                    color=ft.Colors.with_opacity(0.2 + (0.6 * elevation_factor), ft.Colors.WHITE54),  # Mucho más contraste
                    blur_radius=5 + (25 * elevation_factor),  # Diferencia mucho mayor en el blur
                    spread_radius=elevation_factor * 8,  # Spread mucho más pronunciado
                    offset=ft.Offset(0, 2 - (elevation_factor * 4))  # Offset más pronunciado
                ),
            )
            
            return card
    
        # Crear carrusel horizontal
        try:
            # Crear el carrusel con tarjetas de productos
            carousel = ft.Row(
                controls=[product_card(p, i) for i, p in enumerate(products)],
                scroll=ft.ScrollMode.AUTO,
                spacing=25,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
            # Snackbar para confirmar envío
            page.snackbar = ft.SnackBar(
                content=ft.Text("Solicitud enviada correctamente"),
                action="OK"
            )
            
            # Contenedor principal con título
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Nuestros Productos", 
                            size=28, 
                            weight="bold",
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Container(
                            content=carousel,
                            padding=ft.padding.symmetric(horizontal=20),
                            height=350
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: carousel.scroll_to(delta=-300, duration=500)
                                ),
                                send_request_btn,
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_FORWARD_IOS,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda e: carousel.scroll_to(delta=300, duration=500)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=0
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.symmetric(vertical=20),
                bgcolor=ft.Colors.TRANSPARENT
            )
        except Exception as e:
            print(f"Error al crear el carrusel: {e}")
            import traceback
            traceback.print_exc()
            
            # Devolver un mensaje de error
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Error al cargar los productos", size=20, color=ft.Colors.RED),
                        ft.Text(str(e), size=14, color=ft.Colors.WHITE),
                        ft.ElevatedButton("Reintentar", on_click=lambda _: page.update())
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=40,
                alignment=ft.alignment.center
            )
    except Exception as e:
        print(f"Error general en products_carousel_view: {e}")
        import traceback
        traceback.print_exc()
        
        # Devolver un mensaje de error
        return ft.Container(
            content=ft.Text(f"Error: {str(e)}", color=ft.Colors.RED),
            padding=20
        )
