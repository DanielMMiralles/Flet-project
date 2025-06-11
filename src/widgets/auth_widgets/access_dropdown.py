import flet as ft

def role_dropdown(page: ft.Page, on_change: callable = None) -> ft.Dropdown:
    """Dropdown moderno para selección de roles con tema oscuro"""
    return ft.Dropdown(
        width=300,
        filled=True,
        border_radius=12,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_ACCENT),
        label="Seleccionar rol",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_100),
        hint_text="Tipo de usuario",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_400),
        options=[
            ft.DropdownOption(text="Admin", leading_icon=ft.Icons.ADMIN_PANEL_SETTINGS),
            ft.DropdownOption(text="Ingeniero", leading_icon=ft.Icons.ENGINEERING),
            ft.DropdownOption(text="Cliente", leading_icon=ft.Icons.PERSON),
        ],
        icon=ft.Icons.ARROW_DROP_DOWN_CIRCLE,
        on_change=on_change,
    )