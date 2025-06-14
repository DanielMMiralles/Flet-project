import flet as ft
from widgets.auth_widgets.auth_card import auth_card
from widgets.auth_widgets.auth_buttom import minimal_button
from widgets.auth_widgets.access_dropdown import role_dropdown
from widgets.auth_widgets.btext_auth import btext_auth

def register_view(page: ft.Page):
    def register(e):
        page.session_data["user"] = user_input.value
        page.session_data["password"] = password_input.value
        page.session_data["role"] = role_input.value
        # Aquí podrías agregar lógica para registrar al usuario

    user_input = ft.TextField(label="Username", autofocus=True)
    password_input = ft.TextField(label="Password", password=True)
    password_input2 = ft.TextField(label="Confirm Password", password=True)
    role_input = role_dropdown(page)
    register_button = minimal_button(
        "Registrar",
        register,
    )
    bttext_auth = btext_auth(page, "¿Ya tienes cuenta?", "Inicia sesión aquí", "/login")

    return auth_card(
        page,
        content=ft.Column(
            controls=[
                user_input,
                password_input,
                password_input2,
                role_input,
                register_button,
                bttext_auth          
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        title="Registrarse"
    )