import flet as ft
from widgets.snackbar_design import modern_snackbar
from widgets.app_bar import app_bar
from widgets.client_widgets.product_carousel import products_carousel_view

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
        
        # Crear componentes de la interfaz
        title = ft.Text("Panel de Cliente", size=30, weight="bold")
        welcome = ft.Text(f"Bienvenido, {username}", size=20)
        user_info = ft.Text(f"Has iniciado sesión como Cliente", size=16)
        
        # Botón de cerrar sesión
        logout_btn = ft.ElevatedButton(
            "Cerrar sesión", 
            icon=ft.Icons.LOGOUT,
            on_click=lambda _: page.go("/login")
        )
        
        products_carousel = products_carousel_view(page)
        if products_carousel is None:
            print("Error: products_carousel_view devolvió None")
            products_carousel = ft.Text("No se pudieron cargar los productos", size=16, color=ft.Colors.RED)

        # Crear contenido principal
        content = ft.Column(
            controls=[
                products_carousel,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                title,
                welcome,
                user_info,
                logout_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
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

  


    