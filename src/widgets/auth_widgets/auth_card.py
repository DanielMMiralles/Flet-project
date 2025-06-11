import flet as ft

def auth_card(page: ft.Page, content: ft.Control, title: str = None):
    """Componente Card reusable para formularios de autenticación"""
    return ft.Card(
        elevation=15,
        content=ft.Container(
            content=ft.Column(
                controls=[
                    # Header con título
                    ft.Container(
                        content=ft.Text(
                            title if title else "Bienvenido",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        padding=ft.padding.symmetric(vertical=20),
                        alignment=ft.alignment.center
                    ) if title else None,
                    
                    # Contenido principal
                    content,
                    
                    # Footer con efecto de onda
                    ft.Container(
                        content=ft.Image(
                            src="wave.svg",  # Puedes usar una onda SVG
                            color=ft.Colors.with_opacity(0.1, ft.Colors.PRIMARY),
                            fit=ft.ImageFit.FILL
                        ),
                        height=30,
                        margin=ft.margin.only(top=30)
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(30),
            width=400 if page.width > 600 else 340,
        ),
        # Estilo adaptable al tema
        color=ft.Colors.with_opacity(
            0.05, ft.Colors.SURFACE_VARIANT
        ) if page.theme_mode == ft.ThemeMode.DARK else None,
        surface_tint_color=ft.Colors.TRANSPARENT,
        shadow_color=ft.Colors.with_opacity(
            0.2, ft.Colors.ON_SURFACE
        ) if page.theme_mode == ft.ThemeMode.DARK else None,
        shape=ft.RoundedRectangleBorder(radius=15),
    )