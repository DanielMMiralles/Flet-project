import flet as ft 

def minimal_button(text: str, on_click: ft.ControlEventType) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.TRANSPARENT,
            shadow_color=ft.Colors.TRANSPARENT,
            side=ft.BorderSide(1.5, ft.Colors.PRIMARY),
            padding=20,
            overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.PRIMARY)
        ),
        height=45
    )