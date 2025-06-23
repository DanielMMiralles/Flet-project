import flet as ft
import datetime
from widgets.snackbar_design import modern_snackbar

# Variable global para eventos temporales que no se pudieron guardar en BD
_temp_events = {}

def calendar_view(page: ft.Page):
    """Vista de calendario para el ingeniero"""
    
    # Paleta de colores
    primary_color = ft.Colors.TEAL_ACCENT
    secondary_color = ft.Colors.BLUE_GREY_900
    background_color = ft.Colors.BLUE_GREY_50
    card_color = ft.Colors.WHITE
    
    # Fecha actual
    today = datetime.date.today()
    current_month = ft.Ref[int]()
    current_year = ft.Ref[int]()
    current_month.current = today.month
    current_year.current = today.year
    
    # Estado del día seleccionado
    selected_date_str = ft.Ref[str]()
    selected_date_str.current = None
    
    # Nombres de meses
    month_names = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    # Cargar eventos desde la base de datos
    def load_events_from_db():
        try:
            from utils.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT fecha_evento, titulo, tipo_evento
                FROM CalendarioEventos
                WHERE id_ingeniero = ?
                ORDER BY fecha_evento
            """, (1,))  # ID del ingeniero
            
            db_events = {}
            for row in cursor.fetchall():
                date_str = row["fecha_evento"]
                event = {
                    "type": row["tipo_evento"],
                    "title": row["titulo"],
                    "project": "Personal"
                }
                
                if date_str not in db_events:
                    db_events[date_str] = []
                db_events[date_str].append(event)
            
            conn.close()
            return db_events
            
        except Exception as e:
            print(f"Error cargando eventos de BD: {e}")
            return {}
    
    # Combinar eventos de BD con eventos por defecto
    today_str = today.strftime("%Y-%m-%d")
    
    default_events = {
        "2024-12-15": [{"type": "deadline", "title": "Entrega Sistema Inventario", "project": "Sistema de Inventario"}],
        "2024-12-20": [{"type": "meeting", "title": "Reunión de equipo", "project": "App E-commerce"}],
        "2024-12-25": [{"type": "deadline", "title": "Entrega CRM", "project": "Plataforma CRM"}],
        "2024-12-28": [{"type": "personal", "title": "Revisión de código", "project": "Personal"}],
        "2025-01-05": [{"type": "meeting", "title": "Planificación Sprint", "project": "Desarrollo"}],
        "2025-01-15": [{"type": "deadline", "title": "Entrega Módulo Pagos", "project": "E-commerce"}],
        "2025-02-10": [{"type": "personal", "title": "Capacitación", "project": "Personal"}]
    }
    
    # Cargar eventos de BD y combinar
    db_events = load_events_from_db()
    mock_events = default_events.copy()
    
    # Combinar eventos de BD
    for date_str, events in db_events.items():
        if date_str in mock_events:
            mock_events[date_str].extend(events)
        else:
            mock_events[date_str] = events
    
    # Usar variable global para eventos temporales
    global _temp_events
    
    print(f"Eventos disponibles: {list(mock_events.keys())}")
    print(f"Fecha actual: {today_str}")
    
    # Estado del calendario
    calendar_container = ft.Ref[ft.Column]()
    events_list = ft.Ref[ft.Column]()
    
    def get_days_in_month(year, month):
        """Obtiene los días del mes"""
        import calendar
        return calendar.monthrange(year, month)[1]
    
    def get_first_weekday(year, month):
        """Obtiene el primer día de la semana del mes"""
        import calendar
        return calendar.monthrange(year, month)[0]
    
    def create_day_cell(day, has_events=False, is_today=False, is_past=False):
        """Crea una celda del día"""
        def on_day_click(e):
            if is_past:
                page.snackbar = modern_snackbar("No se pueden seleccionar fechas pasadas", "error", 2000)
                page.open(page.snackbar)
                return
                
            # Actualizar fecha seleccionada
            date_str = f"{current_year.current}-{current_month.current:02d}-{day:02d}"
            selected_date_str.current = date_str
            update_events_list(date_str)
            
            # Autocompletar campo de fecha
            event_date.value = date_str
            
            # Actualizar el calendario para mostrar la selección
            update_calendar_display()
            page.update()
        
        # Determinar colores
        if is_past:
            cell_color = ft.Colors.GREY_100
            text_color = ft.Colors.GREY_400
            border_color = ft.Colors.GREY_200
        elif selected_date_str.current == f"{current_year.current}-{current_month.current:02d}-{day:02d}":
            cell_color = ft.Colors.BLUE_100
            text_color = ft.Colors.BLUE_900
            border_color = ft.Colors.BLUE
        elif is_today:
            cell_color = ft.Colors.TEAL_100
            text_color = ft.Colors.TEAL_900
            border_color = ft.Colors.TEAL
        elif has_events:
            cell_color = ft.Colors.ORANGE_100
            text_color = ft.Colors.ORANGE_900
            border_color = ft.Colors.ORANGE_300
        else:
            cell_color = ft.Colors.WHITE
            text_color = ft.Colors.GREY_800
            border_color = ft.Colors.GREY_300
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(str(day), size=16, weight="bold", color=text_color),
                    ft.Container(
                        width=8,
                        height=8,
                        border_radius=4,
                        bgcolor=ft.Colors.ORANGE if has_events else ft.Colors.TRANSPARENT
                    ) if not is_past else ft.Container(width=8, height=8)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            ),
            width=50,
            height=50,
            border_radius=8,
            bgcolor=cell_color,
            border=ft.border.all(2 if selected_date_str.current == f"{current_year.current}-{current_month.current:02d}-{day:02d}" else 1, border_color),
            alignment=ft.alignment.center,
            on_click=on_day_click if not is_past else None
        )
    
    def update_events_list(date_str):
        """Actualiza la lista de eventos para la fecha seleccionada"""
        events = mock_events.get(date_str, [])
        
        print(f"Buscando eventos para fecha: {date_str}")
        print(f"Eventos encontrados: {events}")
        print(f"Mock_events actual: {list(mock_events.keys())}")
        if date_str in mock_events:
            print(f"Eventos para {date_str}: {mock_events[date_str]}")
        
        if not events:
            events_list.current.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.EVENT_AVAILABLE, size=40, color=ft.Colors.GREY_400),
                            ft.Text("No hay eventos para esta fecha", size=14, color=ft.Colors.GREY_500),
                            ft.Text(f"Fecha: {date_str}", size=12, color=ft.Colors.GREY_400)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    alignment=ft.alignment.center,
                    height=120
                )
            ]
        else:
            events_list.current.controls = [create_event_item(event) for event in events]
        
        page.update()
    
    def create_event_item(event):
        """Crea un elemento de evento"""
        icon_map = {
            "deadline": ft.Icons.SCHEDULE,
            "meeting": ft.Icons.PEOPLE,
            "personal": ft.Icons.PERSON
        }
        
        color_map = {
            "deadline": ft.Colors.RED,
            "meeting": ft.Colors.BLUE,
            "personal": ft.Colors.GREEN
        }
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon_map.get(event["type"], ft.Icons.EVENT), 
                                      color=ft.Colors.WHITE, size=20),
                        width=40,
                        height=40,
                        border_radius=20,
                        bgcolor=color_map.get(event["type"], ft.Colors.GREY),
                        alignment=ft.alignment.center
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(event["title"], size=14, weight="bold", color=secondary_color),
                            ft.Text(event["project"], size=12, color=ft.Colors.GREY_600)
                        ],
                        spacing=2,
                        expand=True
                    )
                ],
                spacing=12
            ),
            padding=12,
            margin=ft.margin.only(bottom=8),
            border_radius=10,
            bgcolor=ft.Colors.BLUE_GREY_50,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100)
        )
    
    # Funciones de navegación
    def previous_month():
        if current_month.current == 1:
            current_month.current = 12
            current_year.current -= 1
        else:
            current_month.current -= 1
        
        # No permitir navegar a meses anteriores al actual
        if (current_year.current < today.year or 
            (current_year.current == today.year and current_month.current < today.month)):
            current_month.current = today.month
            current_year.current = today.year
            page.snackbar = modern_snackbar("No se puede navegar a meses anteriores", "error", 2000)
            page.open(page.snackbar)
        
        update_calendar_display()
        page.update()
    
    def next_month():
        if current_month.current == 12:
            current_month.current = 1
            current_year.current += 1
        else:
            current_month.current += 1
        update_calendar_display()
        page.update()
    
    def update_calendar_display():
        calendar_container.current.controls[0] = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: previous_month(),
                    icon_color=primary_color
                ),
                ft.Text(
                    f"{month_names[current_month.current-1]} {current_year.current}", 
                    size=20, 
                    weight="bold", 
                    color=secondary_color,
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    on_click=lambda _: next_month(),
                    icon_color=primary_color
                )
            ]
        )
        calendar_container.current.controls[1] = create_calendar()
    
    def reload_events_from_db():
        """Recarga eventos desde la base de datos sin perder los existentes"""
        try:
            from utils.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT fecha_evento, titulo, tipo_evento
                FROM CalendarioEventos
                WHERE id_ingeniero = ?
                ORDER BY fecha_evento
            """, (1,))
            
            # Limpiar eventos de BD anteriores y recargar
            db_events = {}
            for row in cursor.fetchall():
                date_str = row["fecha_evento"]
                event = {
                    "type": row["tipo_evento"],
                    "title": row["titulo"],
                    "project": "Personal"
                }
                
                if date_str not in db_events:
                    db_events[date_str] = []
                db_events[date_str].append(event)
            
            # Actualizar mock_events con eventos de BD sin perder los existentes
            nonlocal mock_events
            global _temp_events
            
            # Reinicializar con eventos por defecto
            mock_events = default_events.copy()
            
            # Agregar eventos de BD
            for date_str, events in db_events.items():
                if date_str in mock_events:
                    mock_events[date_str].extend(events)
                else:
                    mock_events[date_str] = events
            
            # Agregar eventos temporales (que no se pudieron guardar en BD)
            for date_str, events in _temp_events.items():
                if date_str in mock_events:
                    # Evitar duplicados
                    existing_titles = [e['title'] for e in mock_events[date_str]]
                    for event in events:
                        if event['title'] not in existing_titles:
                            mock_events[date_str].append(event)
                else:
                    mock_events[date_str] = events
            
            conn.close()
            
        except Exception as e:
            print(f"Error recargando eventos: {e}")
    
    # Crear calendario
    def create_calendar():
        days_in_month = get_days_in_month(current_year.current, current_month.current)
        first_weekday = get_first_weekday(current_year.current, current_month.current)
        
        # Días de la semana
        weekdays = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        weekday_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(day, size=12, weight="bold", color=ft.Colors.GREY_600),
                    width=50,
                    alignment=ft.alignment.center
                ) for day in weekdays
            ],
            spacing=5
        )
        
        # Crear filas de días
        calendar_rows = [weekday_row]
        current_row = []
        
        # Espacios vacíos al inicio
        for _ in range(first_weekday):
            current_row.append(ft.Container(width=50, height=50))
        
        # Recargar eventos antes de crear el calendario
        reload_events_from_db()
        
        # Días del mes
        for day in range(1, days_in_month + 1):
            date_str = f"{current_year.current}-{current_month.current:02d}-{day:02d}"
            has_events = date_str in mock_events
            is_today = (day == today.day and current_month.current == today.month and current_year.current == today.year)
            
            # Debug para verificar eventos
            if has_events:
                print(f"Día {day} tiene eventos: {date_str}")
            
            # Verificar si es fecha pasada
            current_date = datetime.date(current_year.current, current_month.current, day)
            is_past = current_date < today
            
            current_row.append(create_day_cell(day, has_events, is_today, is_past))
            
            if len(current_row) == 7:
                calendar_rows.append(ft.Row(controls=current_row, spacing=5))
                current_row = []
        
        # Completar última fila si es necesario
        if current_row:
            while len(current_row) < 7:
                current_row.append(ft.Container(width=50, height=50))
            calendar_rows.append(ft.Row(controls=current_row, spacing=5))
        
        return ft.Column(controls=calendar_rows, spacing=5)
    
    # Formulario para agregar evento
    event_title = ft.TextField(
        hint_text="Título del evento", 
        width=300,
        color=ft.Colors.BLUE_GREY_800
    )
    event_date = ft.TextField(
        hint_text="Fecha seleccionada", 
        width=150,
        color=ft.Colors.BLUE_GREY_800,
        read_only=True,
        bgcolor=ft.Colors.GREY_100
    )
    event_type = ft.Dropdown(
        hint_text="Tipo",
        options=[
            ft.dropdown.Option("deadline", "Fecha límite"),
            ft.dropdown.Option("meeting", "Reunión"),
            ft.dropdown.Option("personal", "Personal")
        ],
        width=150,
        color=ft.Colors.BLUE_GREY_800
    )
    
    def add_event(e):
        if not event_title.value or not event_date.value or not event_type.value:
            page.snackbar = modern_snackbar("Complete todos los campos", "error", 3000)
            page.open(page.snackbar)
            return
            
        # Validar fecha
        try:
            event_date_obj = datetime.datetime.strptime(event_date.value, "%Y-%m-%d").date()
            if event_date_obj < today:
                page.snackbar = modern_snackbar("No se pueden agregar eventos en fechas pasadas", "error", 3000)
                page.open(page.snackbar)
                return
        except ValueError:
            page.snackbar = modern_snackbar("Formato de fecha inválido. Use YYYY-MM-DD", "error", 3000)
            page.open(page.snackbar)
            return
            
        # Guardar evento en la base de datos
        try:
            from utils.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO CalendarioEventos (id_ingeniero, titulo, descripcion, fecha_evento, tipo_evento)
                VALUES (?, ?, ?, ?, ?)
            """, (1, event_title.value, event_title.value, event_date.value, event_type.value))
            
            print(f"Insertando evento: {event_title.value} para fecha {event_date.value}")
            
            conn.commit()
            
            # Verificar que se insertó correctamente
            cursor.execute("""
                SELECT COUNT(*) as count FROM CalendarioEventos 
                WHERE fecha_evento = ? AND titulo = ?
            """, (event_date.value, event_title.value))
            
            result = cursor.fetchone()
            print(f"Eventos insertados para {event_date.value}: {result['count']}")
            
            conn.close()
            
            # También agregar a mock_events para mostrar inmediatamente
            new_event = {
                "type": event_type.value,
                "title": event_title.value,
                "project": "Personal"
            }
            
            if event_date.value not in mock_events:
                mock_events[event_date.value] = []
            mock_events[event_date.value].append(new_event)
            
        except Exception as e:
            print(f"Error guardando evento en BD: {e}")
            # Guardar en temp_events para persistir entre recargas
            new_event = {
                "type": event_type.value,
                "title": event_title.value,
                "project": "Personal"
            }
            
            if event_date.value not in _temp_events:
                _temp_events[event_date.value] = []
            _temp_events[event_date.value].append(new_event)
            
            if event_date.value not in mock_events:
                mock_events[event_date.value] = []
            mock_events[event_date.value].append(new_event)
        
        print(f"Evento agregado: {event_date.value} -> {new_event}")
        print(f"Eventos actualizados: {mock_events}")
        
        # Recargar eventos desde BD inmediatamente
        reload_events_from_db()
        
        # Actualizar calendario para mostrar la nueva marca
        update_calendar_display()
        
        # Si la fecha agregada está seleccionada, actualizar la lista
        if selected_date_str.current == event_date.value:
            update_events_list(event_date.value)
        
        page.snackbar = modern_snackbar("Evento agregado correctamente", "success", 3000)
        page.open(page.snackbar)
        
        # Limpiar campos
        event_title.value = ""
        event_date.value = ""
        event_type.value = None
        page.update()
    
    # Contenido principal
    return ft.Container(
        content=ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=32, color=primary_color),
                            ft.Text("Calendario de Actividades", size=28, weight="bold", color=secondary_color),
                            ft.Container(expand=True),
                            ft.Text(f"{current_month.current}/{current_year.current}", size=20, color=ft.Colors.GREY_600)
                        ]
                    ),
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Contenido principal
                ft.Row(
                    controls=[
                        # Calendario
                        ft.Container(
                            content=ft.Column(
                                ref=calendar_container,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.Icons.CHEVRON_LEFT,
                                                on_click=lambda _: previous_month(),
                                                icon_color=primary_color
                                            ),
                                            ft.Text(
                                                f"{month_names[current_month.current-1]} {current_year.current}", 
                                                size=20, 
                                                weight="bold", 
                                                color=secondary_color,
                                                expand=True,
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.CHEVRON_RIGHT,
                                                on_click=lambda _: next_month(),
                                                icon_color=primary_color
                                            )
                                        ]
                                    ),
                                    create_calendar()
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            ),
                            padding=25,
                            border_radius=20,
                            bgcolor=card_color,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=15,
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                offset=ft.Offset(0, 6)
                            ),
                            width=400
                        ),
                        
                        # Panel lateral
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # Eventos del día
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("Eventos del Día", size=18, weight="bold", color=secondary_color),
                                                ft.Container(height=10),
                                                ft.Column(ref=events_list, controls=[
                                                    ft.Container(
                                                        content=ft.Text("Selecciona una fecha (desde hoy en adelante)", size=14, color=ft.Colors.GREY_500),
                                                        alignment=ft.alignment.center,
                                                        height=100
                                                    )
                                                ])
                                            ]
                                        ),
                                        padding=20,
                                        border_radius=15,
                                        bgcolor=card_color,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=10,
                                            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                                            offset=ft.Offset(0, 4)
                                        ),
                                        margin=ft.margin.only(bottom=20)
                                    ),
                                    
                                    # Agregar evento
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("Agregar Evento", size=18, weight="bold", color=secondary_color),
                                                ft.Container(height=10),
                                                event_title,
                                                ft.Row(
                                                    controls=[event_date, event_type],
                                                    spacing=10
                                                ),
                                                ft.ElevatedButton(
                                                    "Agregar",
                                                    icon=ft.Icons.ADD,
                                                    style=ft.ButtonStyle(
                                                        color=ft.Colors.WHITE,
                                                        bgcolor=primary_color
                                                    ),
                                                    on_click=add_event
                                                )
                                            ],
                                            spacing=10
                                        ),
                                        padding=20,
                                        border_radius=15,
                                        bgcolor=card_color,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=10,
                                            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                                            offset=ft.Offset(0, 4)
                                        )
                                    )
                                ]
                            ),
                            width=350,
                            expand=True
                        )
                    ],
                    spacing=30,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ],
            scroll=ft.ScrollMode.AUTO
        ),
        padding=30,
        bgcolor=background_color,
        expand=True
    )