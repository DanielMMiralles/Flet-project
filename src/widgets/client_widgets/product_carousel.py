import flet as ft
import os
from models.product import Product
from services.product_service import get_products

def products_carousel_view(page: ft.Page, products=None):
    """Vista de carrusel de productos con diseño moderno en tema oscuro"""
    try:
        # Usar los productos proporcionados o obtenerlos si no se proporcionan
        if products is None:
            products = get_products()
            print(f"Productos obtenidos: {len(products)}")
            for p in products:
                print(f"Producto: ID={p.id}, Nombre={p.name}, Imagen={p.image}")
        
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

        # Función para crear tarjetas de producto
        def product_card(product: Product) -> ft.Container:
            # Determinar la URL de la imagen o usar una imagen por defecto
            image_path = product.image
            
            # Si la ruta es relativa, convertirla en absoluta
            if image_path and image_path.startswith('/'):
                # Quitar el slash inicial para unir correctamente con la ruta base
                relative_path = image_path[1:] if image_path.startswith('/') else image_path
                image_path = os.path.join(base_dir, relative_path)
                # Verificar si el archivo existe
                if not os.path.exists(image_path):
                    print(f"Advertencia: La imagen no existe en: {image_path}")
                    # Intentar otra ubicación
                    image_path = os.path.join(base_dir, "assets", "productos", os.path.basename(relative_path))
                    if not os.path.exists(image_path):
                        # Caso especial para "Plataforma de Recursos Humanos"
                        if "recursos humanos" in product.name.lower():
                            image_path = os.path.join(base_dir, "assets", "productos", "rh.jpg")
                            if not os.path.exists(image_path):
                                image_path = "https://via.placeholder.com/250x180?text=" + product.name.replace(" ", "+")
                        else:
                            print(f"Usando imagen por defecto para: {product.name}")
                            image_path = "https://via.placeholder.com/250x180?text=" + product.name.replace(" ", "+")
            elif not image_path:
                image_path = "https://via.placeholder.com/250x180?text=" + product.name.replace(" ", "+")
            
            # Imprimir información de depuración
            print(f"Creando tarjeta para producto: {product.name if hasattr(product, 'name') else 'Sin nombre'}")
            print(f"  - Imagen: {image_path}")
            print(f"  - Descripción: {product.description if hasattr(product, 'description') else 'Sin descripción'}")
            
            return ft.Container(
                content=ft.Column(
                    controls=[
                        # Imagen del producto
                        ft.Container(
                            content=ft.Image(
                                src=f"{image_path}",
                                height=180,
                                width=280,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.only(top_left=15, top_right=15)
                            ),
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            border_radius=ft.border_radius.only(top_left=15, top_right=15),
                            bgcolor=ft.Colors.BLUE_GREY_100,  # Color de fondo mientras carga la imagen
                            width=280,
                            height=180
                        ),
                        
                        # Contenido de la tarjeta
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        product.name if hasattr(product, 'name') else "Sin nombre",
                                        size=16,
                                        weight="bold",
                                        color=ft.Colors.BLACK,  # Color de texto explícito
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS
                                    ),
                                    ft.Text(
                                        product.description if hasattr(product, 'description') else "Sin descripción",
                                        size=12,
                                        color=ft.Colors.GREY_800,  # Color de texto explícito
                                        max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=14, color=ft.Colors.BLUE_GREY),
                                            ft.Text(
                                                f"{product.engineers if hasattr(product, 'engineers') else 0} ingenieros", 
                                                size=12,
                                                color=ft.Colors.BLUE_GREY
                                            ),
                                            ft.VerticalDivider(width=10),
                                            ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.BLUE_GREY),
                                            ft.Text(
                                                f"{product.days if hasattr(product, 'days') else 0} días", 
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
                            bgcolor=ft.Colors.WHITE,  # Fondo blanco para el contenido
                        )
                    ],
                    spacing=0
                ),
                width=280,
                height=300,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,  # Fondo blanco para la tarjeta
                shadow=ft.BoxShadow(
                    color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                    blur_radius=10,
                    offset=ft.Offset(0, 5)  
                ),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                on_click=lambda e: page.go(f"/client/product/{product.id}" if hasattr(product, 'id') else "/client")
            )
    
        # Crear carrusel horizontal
        try:
            carousel = ft.Row(
                controls=[product_card(p) for p in products],
                scroll=ft.ScrollMode.AUTO,
                spacing=25,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
            
            # Contenedor principal con título
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Nuestros Productos", 
                            size=28, 
                            weight="bold",
                            color=ft.Colors.WHITE,  # Color de texto explícito
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
                                    icon_color=ft.Colors.WHITE,  # Color de icono explícito
                                    on_click=lambda e: carousel.scroll_to(delta=-300, duration=500)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_FORWARD_IOS,
                                    icon_color=ft.Colors.WHITE,  # Color de icono explícito
                                    on_click=lambda e: carousel.scroll_to(delta=300, duration=500)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.symmetric(vertical=40),
                bgcolor=ft.Colors.TRANSPARENT,  # Color de fondo para el contenedor principal
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
            content=ft.Text(f"Error: {str(e)}", color=ft.colors.RED),
            padding=20
        )
