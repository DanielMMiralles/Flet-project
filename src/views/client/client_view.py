import flet as ft
from widgets.snackbar_design import modern_snackbar
from widgets.app_bar import app_bar
from widgets.client_widgets.product_carousel import products_carousel_view
from widgets.page_footer import page_footer

def client_view(page: ft.Page):
    """Vista para el panel de cliente"""
            # Mostrar mensaje de bienvenida
    username = page.session_data["user"]

    page.snackbar = modern_snackbar(
            message=f"Bienvenido al panel del cliente Sr(a) {username}",
            message_type="success",
            duration=3000
        )
    
    try:
        print("Iniciando client_view")
        
        # Verificar si session_data existe
        if not hasattr(page, "session_data") or not page.session_data:
            print("Error: session_data no existe o está vacío")
            page.session_data = {}
            username = "Invitado"
        else:
            # Obtener el nombre de usuario
            username = page.session_data.get("user", "Invitado")
            print(f"Usuario conectado: {username}")
            page.open(page.snackbar)

        page.appbar = app_bar(page, "client", username)
        
        page.title = "Cliente"
        
        products_carousel = products_carousel_view(page)
        if products_carousel is None:
            print("Error: products_carousel_view devolvió None")
            products_carousel = ft.Text("No se pudieron cargar los productos", size=16, color=ft.Colors.RED)

        # Crear pie de página
        footer = page_footer(page)

        # Crear contenido principal
        content = ft.Stack(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            products_carousel,
                            ft.Container(height=60)  # Espacio para el pie de página
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
                ft.Container(
                    content=footer,
                    bottom=0,
                    left=0,
                    right=0,
                    alignment=ft.Alignment(0, 1),  # Alineación al centro inferior,
                ),
            ],
            expand=True
        )
        
        
        # Crear y devolver el contenedor principal
        print("Devolviendo contenido de client_view")
        return content
        
    except Exception as e:
        print(f"Error en client_view: {e}")
        import traceback
        traceback.print_exc()
        
        # Devolver un contenido de error para que al menos se muestre algo
        return ft.Text(
            f"Error al cargar la vista de cliente: {str(e)}",
            size=20, 
            color=ft.Colors.RED
        )

  


    