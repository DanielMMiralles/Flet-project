import flet as ft

def modern_snackbar(
    message: str, 
    message_type: str = "info",  # "success", "error", "warning", "info"
    duration: int = 3000  # milisegundos
) -> ft.SnackBar:
    """SnackBar moderno con estilado para tema oscuro"""
    
    # Configuración por tipo de mensaje
    type_config = {
        "success": {
            "bgcolor": ft.Colors.GREEN_900,
            "border": ft.Colors.GREEN_700,
            "icon": ft.Icons.CHECK_CIRCLE_OUTLINE,
            "icon_color": ft.Colors.GREEN_300
        },
        "error": {
            "bgcolor": ft.Colors.RED_900,
            "border": ft.Colors.RED_700,
            "icon": ft.Icons.ERROR_OUTLINE,
            "icon_color": ft.Colors.RED_300
        },
        "warning": {
            "bgcolor": ft.Colors.AMBER_900,
            "border": ft.Colors.AMBER_700,
            "icon": ft.Icons.WARNING_AMBER_ROUNDED,
            "icon_color": ft.Colors.AMBER_300
        },
        "info": {
            "bgcolor": ft.Colors.BLUE_900,
            "border": ft.Colors.BLUE_700,
            "icon": ft.Icons.INFO_OUTLINE,
            "icon_color": ft.Colors.BLUE_300
        }
    }
    
    config = type_config.get(message_type, type_config["info"])
    
    return ft.SnackBar(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(config["icon"], color=config["icon_color"], size=24),
                    ft.Text(
                        message,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_300,
                        size=14
                    ),
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.symmetric(vertical=18, horizontal=20),
            border_radius=12,
            border=ft.border.all(1, config["border"]),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.with_opacity(0.3, config["bgcolor"]),
                    config["bgcolor"]
                ]
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 3)
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        ),
        bgcolor=ft.Colors.TRANSPARENT,
        elevation=0,
        behavior=ft.SnackBarBehavior.FLOATING,
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.all(0),
        margin=ft.margin.only(bottom=20, left=20, right=20),
        duration=duration
    )