import flet as ft
from widgets.auth_widgets.auth_card import auth_card
from widgets.auth_widgets.auth_buttom import minimal_button
from widgets.auth_widgets.access_dropdown import role_dropdown
from widgets.auth_widgets.btext_auth import btext_auth

def login_view(page: ft.Page):
    def login(e):
        page.session_data["user"] = user_input.value
        page.session_data["password"] = password_input.value
        page.session_data["role"] = role_input.value
        

    user_input = ft.TextField(label="Username", autofocus=True)
    password_input = ft.TextField(label="Password", password=True)
    role_input = role_dropdown(page)
    login_button = minimal_button(
        "Login",
        login
    )
    bttext_auth = btext_auth(page,  "¿No tienes cuenta?", "Regístrate aquí")

    return auth_card(
        page,
        content=ft.Column(
            controls=[
                user_input,
                password_input,
                role_input,
                login_button,
                bttext_auth          
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        title="Iniciar sesión"
    )
