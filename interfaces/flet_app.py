import flet as ft
from app import CarTracker

class FletApp:
    def __init__(self):
        self.car_tracker = CarTracker()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "CarDb Mobile"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.padding = 0
        page.spacing = 0
        
        # Mobile-optimized app bar
        page.appbar = ft.AppBar(
            title=ft.Text("CarDb", size=20, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            elevation=4
        )

        # Mobile-optimized navigation
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
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADD,
                    selected_icon=ft.Icons.ADD,
                    label="Add Car"
                ),
            ],
            on_change=self.nav_change,
            selected_index=0,
            height=80
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
        
        # Mobile-optimized scrollable list
        car_list = ft.ListView(expand=1, spacing=8, padding=ft.padding.all(16))
        cars_data = self.car_tracker.displayData()
        total_cars = len(cars_data)
        
        # Header with car count
        header = ft.Container(
            content=ft.Column([
                ft.Text(f"Total Cars: {total_cars}", 
                       size=18, 
                       weight=ft.FontWeight.BOLD, 
                       color=ft.Colors.BLUE_700),
                ft.Divider(height=1)
            ]),
            padding=ft.padding.symmetric(horizontal=16, vertical=8)
        )

        if cars:
            for car in cars:
                # Mobile-optimized car card
                car_card = ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(12),
                        content=ft.Column([
                            # Main car info
                            ft.Row([
                                ft.Icon(ft.Icons.DIRECTIONS_CAR, 
                                       color=ft.Colors.BLUE_700, 
                                       size=24),
                                ft.Expanded(
                                    child=ft.Column([
                                        ft.Text(f"{car.get('model', '')}", 
                                               weight=ft.FontWeight.BOLD, 
                                               size=16),
                                        ft.Text(f"{car.get('manufacturer', '')} • {car.get('year', '')}", 
                                               size=14, 
                                               color=ft.Colors.GREY_700)
                                    ], spacing=2)
                                )
                            ], spacing=8),
                            
                            # Additional details
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.CATEGORY, size=16, color=ft.Colors.GREY_600),
                                        ft.Text(f"{car.get('category', 'N/A')}", size=12)
                                    ], spacing=4),
                                    ft.Row([
                                        ft.Icon(ft.Icons.PUBLIC, size=16, color=ft.Colors.GREY_600),
                                        ft.Text(f"{car.get('country_of_origin', 'N/A')}", size=12)
                                    ], spacing=4)
                                ], spacing=4),
                                padding=ft.padding.only(top=8)
                            ),
                            
                            # Action buttons
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE_600,
                                    tooltip="Edit",
                                    on_click=lambda e, car=car: self.page.go(f"/edit_car/{car.get('model')}")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED_600,
                                    tooltip="Delete",
                                    on_click=lambda e, car=car: self.show_delete_dialog(car.get('model'))
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.OPEN_IN_NEW,
                                    icon_color=ft.Colors.GREEN_600,
                                    tooltip="More Info",
                                    on_click=lambda e, url=car.get('info', ''): self.page.launch_url(url) if url else None,
                                    disabled=not car.get('info')
                                )
                            ], alignment=ft.MainAxisAlignment.END)
                        ], spacing=8)
                    ),
                    elevation=2,
                    margin=ft.margin.only(bottom=4)
                )
                car_list.controls.append(car_card)
        else:
            car_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.DIRECTIONS_CAR_OUTLINED, size=64, color=ft.Colors.GREY_400),
                        ft.Text("No cars found", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Tap the + button to add your first car!", 
                               color=ft.Colors.GREY_600)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=ft.padding.all(32),
                    alignment=ft.alignment.center
                )
            )

        return ft.View(
            "/",
            [
                header,
                car_list
            ],
            floating_action_button=ft.FloatingActionButton(
                icon=ft.Icons.ADD, 
                on_click=lambda _: self.page.go("/add_car"),
                bgcolor=ft.Colors.BLUE_700,
                tooltip="Add New Car"
            ),
            appbar=self.page.appbar,
            navigation_bar=self.page.navigation_bar
        )

    def create_edit_car_view(self, model_name):
        car_to_edit = next((car for car in self.car_tracker.displayData() if car.get('model') == model_name), None)

        if not car_to_edit:
            return ft.View(f"/edit_car/{model_name}", [ft.AppBar(title=ft.Text("Edit Car"), bgcolor="#333333"), ft.Text("Car not found.")])

        fields = {
            "modelName": ft.TextField(label="Model Name", value=car_to_edit.get("model", ""), disabled=True),
            "manufacturer": ft.TextField(label="Manufacturer", value=car_to_edit.get("manufacturer", "")),
            "year": ft.TextField(label="Year", value=str(car_to_edit.get("year", ""))),
            "originCountry": ft.TextField(label="Origin Country", value=car_to_edit.get("country_of_origin", "")),
            "category": ft.TextField(label="Category", value=car_to_edit.get("category", "")),
            "modelManufact": ft.TextField(label="Replica Model", value=car_to_edit.get("replica_model", "")),
            "more": ft.TextField(label="More Info (URL)", value=car_to_edit.get("info", ""))
        }

        def update_car_click(e):
            # Create a new dictionary for the updated data
            updated_data = {key: field.value if field.value else "" for key, field in fields.items()}
            # The modelName is disabled, so its value won't be in the dictionary, add it back
            updated_data['modelName'] = model_name

            # Delete the old record and add the new one
            self.car_tracker.deleteData(model_name)
            self.car_tracker.addData(**updated_data)
            self.page.go("/")

        return ft.View(
            f"/edit_car/{model_name}",
            [
                ft.AppBar(title=ft.Text("Edit Car"), bgcolor="#333333"),
                *fields.values(),
                ft.Row(
                    [
                        ft.ElevatedButton("Update Car", on_click=update_car_click),
                        ft.ElevatedButton("Cancel", on_click=lambda _: self.page.go("/")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )

    def create_add_car_view(self):
        # Mobile-optimized form fields
        fields = {
            "modelName": ft.TextField(
                label="Model Name *", 
                hint_text="e.g., Mustang GT",
                border_radius=8,
                filled=True
            ),
            "manufacturer": ft.TextField(
                label="Manufacturer", 
                hint_text="e.g., Ford",
                border_radius=8,
                filled=True
            ),
            "year": ft.TextField(
                label="Year", 
                hint_text="e.g., 2023",
                keyboard_type=ft.KeyboardType.NUMBER,
                border_radius=8,
                filled=True
            ),
            "originCountry": ft.TextField(
                label="Origin Country", 
                hint_text="e.g., USA",
                border_radius=8,
                filled=True
            ),
            "category": ft.TextField(
                label="Category", 
                hint_text="e.g., Sports Car",
                border_radius=8,
                filled=True
            ),
            "modelManufact": ft.TextField(
                label="Model Manufacturer", 
                hint_text="e.g., Hot Wheels",
                border_radius=8,
                filled=True
            ),
            "more": ft.TextField(
                label="More Info (URL)", 
                hint_text="https://...",
                keyboard_type=ft.KeyboardType.URL,
                border_radius=8,
                filled=True
            )
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
                key: field.value.strip() if field.value else "" 
                for key, field in fields.items()
            }
            
            try:
                self.car_tracker.addData(**data)
                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Car added successfully!"),
                    bgcolor=ft.Colors.GREEN_600
                )
                self.page.snack_bar.open = True
                # Clear the form
                for field in fields.values():
                    field.value = ""
                    field.error_text = None
                self.page.go("/")
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error saving car: {str(ex)}"),
                    bgcolor=ft.Colors.RED_600
                )
                self.page.snack_bar.open = True
                self.page.update()

        # Mobile-optimized form layout
        form_content = ft.Column([
            ft.Container(
                content=ft.Text("Add New Car", size=20, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(bottom=16)
            ),
            *[ft.Container(content=field, padding=ft.padding.only(bottom=8)) 
              for field in fields.values()],
            ft.Container(
                content=ft.Row(
                    [
                        ft.ElevatedButton(
                            "Add Car", 
                            on_click=add_car_click,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.all(16)
                            ),
                            expand=True
                        ),
                        ft.OutlinedButton(
                            "Cancel", 
                            on_click=lambda _: self.page.go("/"),
                            style=ft.ButtonStyle(
                                padding=ft.padding.all(16)
                            ),
                            expand=True
                        ),
                    ],
                    spacing=8
                ),
                padding=ft.padding.only(top=16)
            )
        ], spacing=0)

        return ft.View(
            "/add_car",
            [
                ft.Container(
                    content=form_content,
                    padding=ft.padding.all(16),
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(
                title=ft.Text("Add Car"), 
                bgcolor=ft.Colors.BLUE_700,
                automatically_imply_leading=True
            )
        )

    def create_search_view(self):
        search_field = ft.TextField(
            label="Search by model name", 
            hint_text="Enter car model to search...",
            border_radius=8,
            filled=True,
            prefix_icon=ft.Icons.SEARCH,
            on_submit=lambda e: self.perform_search(e.control.value)
        )
        
        search_button = ft.ElevatedButton(
            "Search",
            icon=ft.Icons.SEARCH,
            on_click=lambda _: self.perform_search(search_field.value),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                padding=ft.padding.all(16)
            )
        )
        
        return ft.View(
            "/search",
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Search Cars", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(height=16),
                        search_field,
                        ft.Container(height=16),
                        search_button
                    ]),
                    padding=ft.padding.all(16)
                )
            ],
            appbar=self.page.appbar,
            navigation_bar=self.page.navigation_bar
        )
    
    def perform_search(self, search_term):
        if search_term and search_term.strip():
            self.page.go(f"/search/{search_term.strip()}")
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Please enter a search term"),
                bgcolor=ft.Colors.ORANGE_600
            )
            self.page.snack_bar.open = True
            self.page.update()

    def route_change(self, route):
        route_path = self.page.route
        self.page.views.clear()

        if route_path == "/":
            self.page.views.append(self.create_main_view())
        if self.page.route == "/add_car":
            self.page.views.append(self.create_add_car_view())
        elif self.page.route.startswith("/edit_car/"):
            model_name = self.page.route.split("/")[-1]
            self.page.views.append(self.create_edit_car_view(model_name))
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
        destinations = ["/", "/search", "/add_car"]
        self.page.go(destinations[e.control.selected_index])

def run_flet_app():
    app = FletApp()
    ft.app(target=app.main, view=ft.AppView.FLET_APP_WEB)
