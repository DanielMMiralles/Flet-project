import flet as ft

# Footer para la parte inferior
def page_footer(page: ft.Page):
    # Paleta de colores consistente con la vista del cliente
    primary_color = ft.Colors.BLUE_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    
    return ft.Container(
        content=ft.Column(
            controls=[
                # Línea divisoria elegante
                ft.Container(
                    height=2,
                    bgcolor=ft.Colors.with_opacity(0.1, primary_color),
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Contenido principal del footer
                ft.Row(
                    controls=[
                        # Sección de contacto
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("FLATICOM", size=18, weight="bold", color=secondary_color),
                                    ft.Text("Soluciones Tecnológicas", size=12, color=ft.Colors.GREY_600),
                                    ft.Container(height=8),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.EMAIL, size=16, color=primary_color),
                                            ft.Text("contacto@flaticom.com", size=12, color=ft.Colors.GREY_700)
                                        ],
                                        spacing=8
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.PHONE, size=16, color=primary_color),
                                            ft.Text("+1 (555) 123-4567", size=12, color=ft.Colors.GREY_700)
                                        ],
                                        spacing=8
                                    )
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.START
                            ),
                            expand=True
                        ),
                        
                        # Sección de servicios
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Servicios", size=14, weight="bold", color=secondary_color),
                                    ft.Text("Desarrollo Web", size=12, color=ft.Colors.GREY_700),
                                    ft.Text("Aplicaciones Móviles", size=12, color=ft.Colors.GREY_700),
                                    ft.Text("Consultoría IT", size=12, color=ft.Colors.GREY_700),
                                    ft.Text("Soporte Técnico", size=12, color=ft.Colors.GREY_700)
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.START
                            ),
                            expand=True
                        ),
                        
                        # Sección de redes sociales
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Síguenos", size=14, weight="bold", color=secondary_color),
                                    ft.Container(height=8),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.FACEBOOK, size=20, color=ft.Colors.WHITE),
                                                width=40,
                                                height=40,
                                                border_radius=20,
                                                bgcolor=primary_color,
                                                alignment=ft.alignment.center
                                            ),
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.ALTERNATE_EMAIL, size=20, color=ft.Colors.WHITE),
                                                width=40,
                                                height=40,
                                                border_radius=20,
                                                bgcolor=primary_color,
                                                alignment=ft.alignment.center
                                            ),
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.CAMERA_ALT, size=20, color=ft.Colors.WHITE),
                                                width=40,
                                                height=40,
                                                border_radius=20,
                                                bgcolor=primary_color,
                                                alignment=ft.alignment.center
                                            )
                                        ],
                                        spacing=10
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.START
                            ),
                            expand=True
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=40
                ),
                
                # Línea divisoria y copyright
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.GREY)),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Text("© 2024 FLATICOM. Todos los derechos reservados.", 
                                               size=12, color=ft.Colors.GREY_600),
                                        ft.Row(
                                            controls=[
                                                ft.Text("Política de Privacidad", size=12, color=primary_color),
                                                ft.Text("•", size=12, color=ft.Colors.GREY_400),
                                                ft.Text("Términos de Servicio", size=12, color=primary_color)
                                            ],
                                            spacing=8
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                padding=ft.padding.symmetric(vertical=15)
                            )
                        ]
                    )
                )
            ],
            spacing=0
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.only(top_left=25, top_right=25),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, -8)
        )
    )
