import flet as ft
from widgets.auth_widgets.auth_card import auth_card
from widgets.auth_widgets.auth_buttom import minimal_button
from widgets.auth_widgets.access_dropdown import role_dropdown
from widgets.auth_widgets.btext_auth import btext_auth
from widgets.snackbar_design import modern_snackbar
from utils.database import register_user


def register_view(page: ft.Page):
    def register(e):
        user = user_input.value
        password = password_input.value
        password2 = password_input2.value
        role = role_input.value

        if validate_registration(user, password, password2, role):
            page.snackbar = modern_snackbar(
                message="Registro exitoso. Ahora puedes iniciar sesión.",
                message_type="success",
                open=True
            )
            page.open(page.snackbar)
            page.session_data["user"] = user
            page.session_data["password"] = password
            page.session_data["role"] = role
            page.update()
            page.go("/login")
        
    def validate_registration(user, password, password2, role):
        if password != password2:
            page.snackbar = modern_snackbar(
                message="Las contraseñas no coinciden. Inténtalo de nuevo.",
                message_type="error"
            )
            page.open(page.snackbar)
            page.update()
            return False
        if not user or not password or not role:
            page.snackbar = modern_snackbar(
                message="Por favor, completa todos los campos.",
                message_type="error"
            )
            page.open(page.snackbar)
            page.update()
            return False
        if role not in ["Cliente"]:
            page.snackbar = modern_snackbar(
                message="Por favor, selecciona un rol válido. No posees los permisos necesarios.",
                message_type="error"
            )
            page.open(page.snackbar)
            page.update()
            return False
        if not register_user(user, password, role):
            page.snackbar = modern_snackbar(
                message="El usuario ya existe o hubo un error al registrar usuario. Inténtalo de nuevo.",
                message_type="error"
            )
            page.open(page.snackbar)
            page.update()
            return False
        
        
        return True

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