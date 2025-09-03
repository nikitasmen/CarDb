import flet as ft
from app import CarTracker
import asyncio
import threading
from functools import lru_cache

class FletApp:
    def __init__(self):
        self.car_tracker = CarTracker()
        self._cars_cache = None
        self._cache_dirty = True
        self._loading = False
        self._max_cards_initial = 10  # Load only 10 cars initially
        self._cards_loaded = 0
        self._current_cars = []  # Store current cars for pagination

    def main(self, page: ft.Page):
        self.page = page
        page.title = "CarDb"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.padding = 0
        page.spacing = 0
        
        # Simplified app bar for faster rendering
        page.appbar = ft.AppBar(
            title=ft.Text("CarDb", size=18),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            elevation=1  # Reduced elevation for better performance
        )

        # Simplified navigation bar
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Search"),
                ft.NavigationBarDestination(icon=ft.Icons.ADD, label="Add"),
            ],
            on_change=self.nav_change,
            selected_index=0,
            height=60  # Reduced height
        )

        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
        page.go("/")

    @lru_cache(maxsize=1)
    def _get_cars_data_cached(self, cache_key):
        """Cached data retrieval to avoid repeated file reads"""
        try:
            return self.car_tracker.displayData()
        except Exception as e:
            print(f"Error loading cars data: {e}")
            return []

    def _get_cars_data(self, force_refresh=False):
        """Get cars data with optimized caching for better performance"""
        if self._loading:
            return self._cars_cache or []
            
        if self._cache_dirty or force_refresh or self._cars_cache is None:
            # Use a simple timestamp as cache key
            import time
            cache_key = int(time.time()) if force_refresh else 0
            
            if not force_refresh and self._cars_cache is not None:
                return self._cars_cache
                
            try:
                self._cars_cache = self._get_cars_data_cached(cache_key)
                self._cache_dirty = False
            except Exception as e:
                print(f"Error loading cars data: {e}")
                self._cars_cache = []
        return self._cars_cache

    def _invalidate_cache(self):
        """Mark cache as dirty to force refresh on next access"""
        self._cache_dirty = True
        # Clear LRU cache
        self._get_cars_data_cached.cache_clear()

    def _load_data_async(self):
        """Load data in background thread to avoid blocking UI"""
        if self._loading:
            return
            
        def load_data():
            self._loading = True
            try:
                self._invalidate_cache()
                self._get_cars_data(force_refresh=True)
            finally:
                self._loading = False
        
        threading.Thread(target=load_data, daemon=True).start()

    def update_main_view(self):
        """Update main view with error handling and performance optimization"""
        try:
            # Load data asynchronously if needed
            if self._cache_dirty:
                self._load_data_async()
            
            main_view = self.create_main_view()
            self.page.views.clear()
            self.page.views.append(main_view)
            self.page.update()
        except Exception as e:
            self.show_error(f"Error updating view: {e}")

    def show_error(self, message):
        """Show error message to user"""
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            bgcolor=ft.Colors.RED_600
        )
        self.page.snack_bar.open = True
        self.page.update()

    def show_success(self, message):
        """Show success message to user"""
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.page.update()

    def show_delete_dialog(self, model_name):
        def close_dialog(e):
            confirm_dialog.open = False
            self.page.update()

        def delete_confirmed(e):
            try:
                success = self.car_tracker.deleteData(model_name)
                close_dialog(e)
                if success:
                    self.show_success(f"'{model_name}' deleted successfully!")
                    self.update_main_view()
                else:
                    self.show_error(f"Failed to delete '{model_name}'")
            except Exception as ex:
                close_dialog(e)
                self.show_error(f"Error deleting car: {ex}")

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
        try:
            # Use cached data for better performance
            cars_data = self._get_cars_data()
            
            if search_term:
                cars = [car for car in cars_data if search_term.lower() in car.get('model', '').lower()]
            else:
                cars = cars_data
            
            # Store cars for load more functionality
            self._current_cars = cars
            
            # Create lightweight car cards with lazy loading
            car_cards = self._create_car_cards_optimized(cars)
            
            # Simplified header
            header = ft.Container(
                content=ft.Text(f"Cars: {len(cars_data)}", 
                               size=16, 
                               weight=ft.FontWeight.BOLD),
                padding=ft.padding.all(8),
                bgcolor=ft.Colors.BLUE_50,
                border_radius=8,
                margin=ft.margin.all(8)
            )

            # Use ListView with auto_scroll=False to maintain scroll position
            car_list = ft.ListView(
                controls=[header] + car_cards,
                spacing=4,
                padding=ft.padding.all(4),
                expand=True,
                auto_scroll=False  # This prevents auto-scrolling to top
            )

            return ft.View(
                "/",
                [car_list],
                floating_action_button=ft.FloatingActionButton(
                    icon=ft.Icons.ADD, 
                    on_click=lambda _: self.page.go("/add_car"),
                    bgcolor=ft.Colors.BLUE_700,
                    mini=True  # Smaller FAB for mobile
                ),
                appbar=self.page.appbar,
                navigation_bar=self.page.navigation_bar,
                padding=0  # Remove padding for better performance
            )
        except Exception as e:
            print(f"Error creating main view: {e}")
            return self._create_error_view(f"Error loading cars: {e}")

    def _create_car_cards_optimized(self, cars):
        """Create optimized car cards with simplified UI"""
        if not cars:
            return [ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.DIRECTIONS_CAR_OUTLINED, size=48, color=ft.Colors.GREY_400),
                    ft.Text("No cars found", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Tap + to add your first car!", color=ft.Colors.GREY_600)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=ft.padding.all(20),
                alignment=ft.alignment.center
            )]

        cards = []
        # Use the current limit from instance variable
        display_limit = min(len(cars), self._max_cards_initial)
        
        for i, car in enumerate(cars[:display_limit]):
            # Simplified card design for better performance
            card = ft.Card(
                content=ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Text(car.get('model', 'C')[0].upper(), 
                                      color=ft.Colors.WHITE, size=14),
                        bgcolor=ft.Colors.BLUE_700,
                        radius=18
                    ),
                    title=ft.Text(car.get('model', 'Unknown'), 
                                size=14, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{car.get('manufacturer', '')} • {car.get('year', '')}", 
                                   size=12),
                    trailing=ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="Edit",
                                on_click=lambda e, model=car.get('model'): self.page.go(f"/edit_car/{model}")
                            ),
                            ft.PopupMenuItem(
                                text="Delete",
                                on_click=lambda e, model=car.get('model'): self.show_delete_dialog(model)
                            ),
                        ],
                        icon_size=16
                    ),
                    on_click=lambda e, url=car.get('info', ''): self.page.launch_url(url) if url else None
                ),
                elevation=1,  # Reduced elevation
                margin=ft.margin.symmetric(horizontal=8, vertical=2)
            )
            cards.append(card)
        
        # Add "Load More" button if there are more cars
        if len(cars) > display_limit:
            cards.append(
                ft.Container(
                    content=ft.ElevatedButton(
                        f"Load {len(cars) - display_limit} more cars",
                        on_click=lambda e: self._load_more_cars_improved(e),
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_700,
                            padding=ft.padding.symmetric(horizontal=16, vertical=8)
                        ),
                        key="load_more_btn"  # Add key for identification
                    ),
                    alignment=ft.alignment.center,
                    padding=8,
                    key="load_more_container"  # Add key for scroll position
                )
            )
        
        return cards

    def _load_more_cars_improved(self, e):
        """Load more cars without losing scroll position"""
        try:
            # Get current cars and increase display limit
            current_cars = getattr(self, '_current_cars', self._get_cars_data())
            old_limit = self._max_cards_initial
            new_limit = min(len(current_cars), old_limit + 15)
            self._max_cards_initial = new_limit
            
            # Update the ListView in place to maintain scroll position
            if hasattr(self.page, 'views') and self.page.views:
                current_view = self.page.views[-1]
                if current_view.route == "/":
                    # Find the ListView
                    for control in current_view.controls:
                        if isinstance(control, ft.ListView):
                            # Get updated car cards
                            header = control.controls[0]  # Keep the header
                            updated_cards = self._create_car_cards_optimized(current_cars)
                            
                            # Update ListView controls while preserving scroll
                            control.controls = [header] + updated_cards
                            
                            # Update the page
                            self.page.update()
                            
                            # Show feedback to user
                            self.show_success(f"Loaded {new_limit - old_limit} more cars!")
                            return
            
            # Fallback to full update if in-place update fails
            self.update_main_view()
            
        except Exception as ex:
            self.show_error(f"Error loading more cars: {ex}")

    def _load_more_cars(self, all_cars, current_limit):
        """Legacy method - kept for compatibility"""
        self._load_more_cars_improved(None)

    def _create_error_view(self, error_message):
        """Create a simple error view"""
        return ft.View(
            "/",
            [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=ft.Colors.RED_400),
                        ft.Text("Error", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(error_message, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton("Retry", on_click=lambda _: self.update_main_view())
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=ft.padding.all(32),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
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
        # Simplified form fields for faster rendering
        fields = {
            "modelName": ft.TextField(label="Model Name *", hint_text="e.g., Mustang GT"),
            "manufacturer": ft.TextField(label="Manufacturer", hint_text="e.g., Ford"),
            "year": ft.TextField(label="Year", hint_text="e.g., 2023", keyboard_type=ft.KeyboardType.NUMBER),
            "originCountry": ft.TextField(label="Origin Country", hint_text="e.g., USA"),
            "category": ft.TextField(label="Category", hint_text="e.g., Sports Car"),
            "modelManufact": ft.TextField(label="Model Manufacturer", hint_text="e.g., Hot Wheels"),
            "more": ft.TextField(label="More Info (URL)", hint_text="https://...", keyboard_type=ft.KeyboardType.URL)
        }

        def add_car_click(e):
            model_name_field = fields["modelName"]
            if not model_name_field.value or not model_name_field.value.strip():
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
                success = self.car_tracker.addData(**data)
                if success:
                    # Invalidate cache and show success message
                    self._invalidate_cache()
                    self.show_success("Car added successfully!")
                    # Clear the form
                    for field in fields.values():
                        field.value = ""
                        field.error_text = None
                    self.page.go("/")
                else:
                    self.show_error("Failed to save car. Please try again.")
            except Exception as ex:
                self.show_error(f"Error saving car: {str(ex)}")

        # Simplified form layout for better performance
        return ft.View(
            "/add_car",
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Add New Car", size=18, weight=ft.FontWeight.BOLD),
                        *fields.values(),
                        ft.Row([
                            ft.ElevatedButton(
                                "Add Car", 
                                on_click=add_car_click,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
                            ),
                            ft.OutlinedButton("Cancel", on_click=lambda _: self.page.go("/")),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                    ], spacing=8),
                    padding=ft.padding.all(16),
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text("Add Car"), bgcolor=ft.Colors.BLUE_700)
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
    """Run the Flet mobile app with highly optimized settings for fast loading"""
    app = FletApp()
    
    # Pre-load data asynchronously for faster startup
    app._load_data_async()
    
    try:
        ft.app(
            target=app.main, 
            view=ft.AppView.FLET_APP,  # Native app view for better mobile performance
            port=0,  # Let system choose available port
            web_renderer=ft.WebRenderer.HTML,  # HTML renderer for better mobile performance
            route_url_strategy="path",  # Better for mobile navigation
            assets_dir="assets"  # Enable assets for faster resource loading
        )
    except Exception as e:
        print(f"Error starting optimized Flet app: {e}")
        # Fallback with simpler configuration
        try:
            ft.app(
                target=app.main, 
                view=ft.AppView.WEB_BROWSER,
                port=0
            )
        except Exception as fallback_e:
            print(f"Fallback failed: {fallback_e}")
            # Last resort - try with minimal config
            ft.app(target=app.main)
