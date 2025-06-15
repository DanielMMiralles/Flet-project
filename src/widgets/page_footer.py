import flet as ft

# Footer para la parte inferior
def page_footer(page: ft.Page):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Divider(height=1, color=ft.Colors.GREY_100),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Soporte técnico", size=14, weight="bold", color=ft.Colors.WHITE),
                                    ft.Text("Lun-Vie: 9:00 - 18:00", size=12, color=ft.Colors.GREY_300),
                                    ft.Text("soporte@empresa.com", size=12, color=ft.Colors.BLUE)
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START
                            ),
                            ft.VerticalDivider(width=30, thickness=1, color=ft.Colors.GREY_100),
                            ft.Column(
                                controls=[
                                    ft.Text("Síguenos", size=14, weight="bold", color=ft.Colors.WHITE),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(icon=ft.Icons.FACEBOOK, icon_color=ft.Colors.BLUE),
                                            ft.IconButton(icon=ft.Icons.ALTERNATE_EMAIL, icon_color=ft.Colors.BLUE),
                                            ft.IconButton(icon=ft.Icons.PHOTO_CAMERA_BACK_ROUNDED, icon_color=ft.Colors.BLUE)
                                        ],
                                        spacing=0
                                    )
                                ],
                                spacing=2
                            ),
                            ft.Container(expand=True),  # Espacio flexible
                            ft.Column(
                                controls=[
                                    ft.Text("© 2023 FLATICOM", size=12, color=ft.Colors.GREY_300),
                                    ft.Text("Todos los derechos reservados", size=10, color=ft.Colors.GREY_100)
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=2
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                )
            ]
        ),
        bgcolor=ft.Colors.BLACK12,
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            blur_radius=5,
            offset=ft.Offset(0, -2)
        ),
        height=80,
    )
