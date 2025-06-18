import flet as ft
from app.routes import setup_routes
from utils.init_app import initialize_application

def main(page: ft.Page):
    # Inicializar la aplicación (configurar base de datos, etc.)
    initialize_application()
    
    page.title = "Flet App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Configurar tema
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 800

    # Initialize session dictionary to store user data
    page.session_data = {
        "user": None,
        "password": None,
        "role": None
    }

    page.assets_dir = "assets"

    setup_routes(page)
    page.go("/login")

ft.app(main)