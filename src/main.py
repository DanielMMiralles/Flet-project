import flet as ft
from app.routes import setup_routes

def main(page: ft.Page):
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

    # Verificar la versión de Flet para determinar la propiedad correcta para AppBar
    try:
        # Intentar acceder a la propiedad app_bar
        test_appbar = page.app_bar
        print("Esta versión de Flet usa page.app_bar")
    except:
        try:
            # Intentar acceder a la propiedad appbar
            test_appbar = page.appbar
            print("Esta versión de Flet usa page.appbar")
        except:
            print("No se pudo determinar la propiedad correcta para AppBar")

    setup_routes(page)
    page.go("/login")

ft.app(main)