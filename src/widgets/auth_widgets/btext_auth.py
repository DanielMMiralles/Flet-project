import flet as ft

def btext_auth(page: ft.Page, normal: str, link: str, route: str):
    # Crear un texto normal con Row para simular el comportamiento de RichText
    normal_text = ft.Text(normal, color=ft.Colors.WHITE70)
    link_text = ft.Text(
        link,
        color=ft.Colors.BLUE_700,
        weight="bold",
        size=14,
    )
    
    # Contenedor para el texto de registro
    text_row = ft.Row(
        [normal_text, link_text],
        spacing=2,
    )
    
    # Usamos un Stack para poder aplicar efectos de elevación
    container = ft.Container(
        content=text_row,
        on_click=lambda e: page.go(route),
        width=300,
        padding=ft.padding.only(top=50),
        alignment=ft.alignment.center_right,
        # Usamos margin para simular la elevación
        margin=ft.margin.only(top=0),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
    )
    
    # Función para manejar el hover dentro del componente
    def handle_hover(e):
        if e.data == "true":  # Mouse entra
            link_text.color = ft.Colors.BLUE_ACCENT_400
            link_text.size = 16  # Hacemos el texto más grande
            container.margin = ft.margin.only(top=-5)  # Simulamos elevación con margen negativo
        else:  # Mouse sale
            link_text.color = ft.Colors.BLUE_700
            link_text.size = 14  # Volvemos al tamaño original
            container.margin = ft.margin.only(top=0)  # Volvemos a la posición original
        
        page.update()
    
    # Asignamos el manejador de hover
    container.on_hover = handle_hover
    
    return container