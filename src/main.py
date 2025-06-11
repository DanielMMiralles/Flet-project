import flet as ft
from app.routes import setup_routes

def main(page: ft.Page):
    page.title = "Flet App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Initialize session dictionary to store user data
    page.session_data = {
        "user": None,
        "password": None,
        "role": None
    }

    setup_routes(page)
    page.go("/login")
ft.app(main)
