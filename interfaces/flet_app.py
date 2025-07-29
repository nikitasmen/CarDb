import flet as ft
from app import CarTracker

class FletApp:
    def __init__(self):
        self.car_tracker = CarTracker()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "CarDb"
        page.theme_mode = ft.ThemeMode.DARK

        page.appbar = ft.AppBar(
            title=ft.Text("CarDb"),
            center_title=True,
            bgcolor="#333333"
        )

        # Create navigation bar with destinations
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SEARCH,
                    selected_icon=ft.Icons.SEARCH,
                    label="Search"
                ),
            ],
            on_change=self.nav_change,
            selected_index=0
        )

        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
        page.go("/")

    def update_main_view(self):
        main_view = self.create_main_view()
        self.page.views.clear()
        self.page.views.append(main_view)
        self.page.update()

    def show_delete_dialog(self, model_name):
        def close_dialog(e):
            confirm_dialog.open = False
            self.page.update()

        def delete_confirmed(e):
            self.car_tracker.deleteData(model_name)
            close_dialog(e)
            self.update_main_view()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete '{model_name}'?"),
            actions=[
                ft.TextButton("Delete", on_click=delete_confirmed, style=ft.ButtonStyle(color=ft.Colors.RED)),
                ft.TextButton("Cancel", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()

    def create_main_view(self, search_term=None):
        cars = self.car_tracker.displayData() if not search_term else self.car_tracker.search(search_term)
        
        car_list = ft.ListView(expand=1, spacing=10, padding=20)
        if cars:
            for car in cars:
                car_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.DIRECTIONS_CAR),
                                    title=ft.Text(f"{car.get('model', '')}", weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"{car.get('manufacturer', '')} - {car.get('year', '')}"),
                                    on_click=lambda e, url=car.get('info', ''): self.page.launch_url(url) if url else None,
                                    trailing=ft.Icon(ft.Icons.OPEN_IN_NEW) if car.get('info') else None
                                ),
                                ft.Row([ft.Text(f"Category: {car.get('category', '')}")], alignment=ft.MainAxisAlignment.START),
                                ft.Row([ft.Text(f"Origin: {car.get('country_of_origin', '')}")], alignment=ft.MainAxisAlignment.START),
                            ])
                        )
                    )
                )
        else:
            car_list.controls.append(ft.Text("No cars found.", text_align=ft.TextAlign.CENTER))

        return ft.View(
            "/",
            [car_list],
            floating_action_button=ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda _: self.page.go("/add_car")),
            appbar=self.page.appbar,
            navigation_bar=self.page.navigation_bar
        )

    def create_add_car_view(self):
        fields = {
            "modelName": ft.TextField(label="Model Name"),
            "manufacturer": ft.TextField(label="Manufacturer"),
            "year": ft.TextField(label="Year", keyboard_type=ft.KeyboardType.NUMBER),
            "originCountry": ft.TextField(label="Origin Country"),
            "category": ft.TextField(label="Category"),
            "modelManufact": ft.TextField(label="Model Manufacturer"),
            "more": ft.TextField(label="More Info (URL)")
        }

        def add_car_click(e):
            model_name_field = fields["modelName"]
            if not model_name_field.value:
                model_name_field.error_text = "Model Name is required"
                self.page.update()
                return
            else:
                model_name_field.error_text = None
                
            # Prepare data with empty strings for missing optional fields
            data = {
                key: field.value if field.value else "" 
                for key, field in fields.items()
            }
            
            try:
                self.car_tracker.addData(**data)
                # Clear the form
                for field in fields.values():
                    field.value = ""
                self.page.go("/")
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error saving car: {str(ex)}"))
                self.page.snack_bar.open = True
                self.page.update()

        return ft.View(
            "/add_car",
            [
                ft.AppBar(title=ft.Text("Add Car"), bgcolor="#333333"),
                *fields.values(),
                ft.ElevatedButton("Add Car", on_click=add_car_click)
            ],
            scroll=ft.ScrollMode.AUTO
        )

    def create_search_view(self):
        search_field = ft.TextField(label="Enter model name to search", on_submit=lambda e: self.page.go(f"/search/{e.control.value}"))
        return ft.View(
            "/search",
            [search_field],
            appbar=self.page.appbar,
            navigation_bar=self.page.navigation_bar
        )

    def route_change(self, route):
        route_path = self.page.route
        self.page.views.clear()

        if route_path == "/":
            self.page.views.append(self.create_main_view())
        elif route_path == "/add_car":
            self.page.views.append(self.create_add_car_view())
        elif route_path == "/search":
            self.page.views.append(self.create_search_view())
        elif route_path.startswith("/search/"):
            search_term = route_path.split("/")[-1]
            self.page.views.append(self.create_main_view(search_term=search_term))
        
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def nav_change(self, e):
        destinations = ["/", "/search"]
        self.page.go(destinations[e.control.selected_index])

def run_flet_app():
    app = FletApp()
    ft.app(target=app.main)
