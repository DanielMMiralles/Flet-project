import flet as ft
from widgets.auth_widgets.auth_card import auth_card
from widgets.auth_widgets.auth_buttom import minimal_button
from widgets.auth_widgets.access_dropdown import role_dropdown
from widgets.auth_widgets.btext_auth import btext_auth
from widgets.snackbar_design import modern_snackbar 
from utils.database import authenticate_user



def login_view(page: ft.Page):
    def login(e):
        user = user_input.value
        password = password_input.value
        role = role_input.value
        validate_login(user, password, role)

    def validate_login(user, password, role):
        if not user or not password or not role:
            page.snackbar = modern_snackbar(
                "Por favor, completa todos los campos.",
                "error",
                3000
            )
            page.open(page.snackbar)
            page.update()
            return

        if authenticate_user(user, password, role):
            # Guardar datos de sesión
            page.session_data['user'] = user
            page.session_data['password'] = password
            page.session_data['role'] = role
            
            print(f"Login exitoso. Datos de sesión: {page.session_data}")
            
            # Redirigir según el rol (asegurarse de que sea minúscula)
            target_route = f"/{role.lower()}"
            print(f"Redirigiendo a: {target_route}")
            page.go(target_route)
        else:
            page.snackbar = modern_snackbar(
                "Credenciales incorrectas. Inténtalo de nuevo.",
                "error",
                3000
            )
            page.open(page.snackbar)
            page.update()

    user_input = ft.TextField(label="Username", autofocus=True)
    password_input = ft.TextField(label="Password", password=True)
    role_input = role_dropdown(page)
    login_button = minimal_button(
        "Login",
        login
    )
    bttext_auth = btext_auth(page,  "¿No tienes cuenta?", "Regístrate aquí", "/register")

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