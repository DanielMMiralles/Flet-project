#Where to define the routes for the application
from views.auth.login_view import login_view
from views.auth.register_view import register_view
from views.client.client_view import client_view
from widgets.snackbar_design import modern_snackbar
from views.admin.admin_view import admin_view

def setup_routes(page):
    # Inicializar session_data si no existe
    if not hasattr(page, "session_data"):
        page.session_data = {}

    def route_change(route):
        # Clear current view
        page.controls.clear()
        
        # Limpiar AppBar anterior si existe
        page.appbar = None
        
        # Imprimir información de depuración
        print(f"Cambiando a ruta: {route.route}")
        print(f"Session data: {page.session_data}")
        
        # Verificar rutas protegidas
        if route.route == "/cliente" and not page.session_data.get("user"):
            # Redirigir a login si intenta acceder a client sin iniciar sesión
            print("Redirigiendo a login: usuario no autenticado")
            page.go("/login")
            page.snackbar = modern_snackbar(
                "Debes iniciar sesión para acceder a esta página",
                "warning",
                3000
            )
            page.open(page.snackbar)
            page.update()
            return
            
        # Cargar la vista correspondiente
        try:
            if route.route == "/login":
                page.add(login_view(page))
            elif route.route == "/register":
                page.add(register_view(page))
            elif route.route == "/cliente":
                print("Cargando vista de cliente")
                view = client_view(page)
                print(f"Vista de cliente generada: {type(view)}")
                page.add(view)
            elif route.route == "/admin":
                # Aquí puedes cargar la vista de administrador
                page.add(admin_view(page))
            else:
                # Ruta por defecto
                page.add(login_view(page))
        except Exception as e:
            print(f"Error al cargar la vista: {e}")
            import traceback
            traceback.print_exc()
            
        page.update()

    page.on_route_change = route_change