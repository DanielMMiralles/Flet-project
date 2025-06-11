#Where to define the routes for the application
from views.auth.login_view import login_view


def setup_routes(page):
    # Initialize routes dictionary
    routes = {
        "/login": login_view(page)
    }

    def route_change(route):
        # Clear current view
        page.controls.clear()
        # Add the new view based on route
        page.add(routes.get(route.route, login_view(page)))
        page.update()

    page.on_route_change = route_change