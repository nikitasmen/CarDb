import flet as ft
from app import CarTracker
import threading
import time
from functools import lru_cache

# UI Constants for better maintainability
class UIConstants:
    # Colors
    PRIMARY_COLOR = ft.Colors.INDIGO_700
    PRIMARY_LIGHT = ft.Colors.INDIGO_600
    PRIMARY_ACCENT = ft.Colors.INDIGO_100
    PRIMARY_SURFACE = ft.Colors.INDIGO_50
    SURFACE_COLOR = ft.Colors.WHITE
    BACKGROUND_COLOR = ft.Colors.GREY_50
    SUCCESS_COLOR = ft.Colors.GREEN_600
    ERROR_COLOR = ft.Colors.RED_600
    TEXT_PRIMARY = ft.Colors.GREY_800
    TEXT_SECONDARY = ft.Colors.GREY_600
    
    # Spacing
    BORDER_RADIUS = 12
    PADDING_STANDARD = 16
    PADDING_LARGE = 20
    SPACING_SMALL = 8
    SPACING_STANDARD = 12
    SPACING_LARGE = 16
    
    # Sizes
    ICON_SIZE_SMALL = 20
    ICON_SIZE_MEDIUM = 24
    ICON_SIZE_LARGE = 32
    FONT_SIZE_SMALL = 12
    FONT_SIZE_MEDIUM = 14
    FONT_SIZE_LARGE = 16
    FONT_SIZE_HEADER = 22

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
        
        # Modern app bar with gradient-like effect
        page.appbar = ft.AppBar(
            title=ft.Row([
                ft.Icon(ft.Icons.DIRECTIONS_CAR, color=UIConstants.SURFACE_COLOR, size=UIConstants.ICON_SIZE_MEDIUM),
                ft.Text("CarDb", size=UIConstants.FONT_SIZE_LARGE + 4, weight=ft.FontWeight.BOLD, color=UIConstants.SURFACE_COLOR)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=UIConstants.SPACING_SMALL),
            center_title=True,
            bgcolor=UIConstants.PRIMARY_COLOR,
            elevation=3,
            color=UIConstants.SURFACE_COLOR
        )

        # Modern navigation bar with better styling
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SEARCH_OUTLINED,
                    selected_icon=ft.Icons.SEARCH,
                    label="Search"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                    selected_icon=ft.Icons.ADD_CIRCLE,
                    label="Add Car"
                ),
            ],
            on_change=self.nav_change,
            selected_index=0,
            height=65,
            bgcolor=UIConstants.SURFACE_COLOR,
            indicator_color=UIConstants.PRIMARY_ACCENT,
            surface_tint_color=UIConstants.PRIMARY_SURFACE
        )

        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
        page.go("/")

    # Helper Methods for DRY Code
    def _create_modern_text_field(self, label, hint_text, icon=None, keyboard_type=None, required=False):
        """Create a standardized text field with modern styling"""
        field = ft.TextField(
            label=f"{label}{' *' if required else ''}",
            hint_text=hint_text,
            prefix_icon=icon,
            border_radius=UIConstants.BORDER_RADIUS,
            filled=True,
            bgcolor=UIConstants.BACKGROUND_COLOR,
            keyboard_type=keyboard_type
        )
        return field

    def _create_modern_button(self, text, icon=None, on_click=None, style_type="primary", expand=False):
        """Create a standardized button with modern styling"""
        colors = {
            "primary": (UIConstants.PRIMARY_COLOR, UIConstants.SURFACE_COLOR),
            "secondary": (UIConstants.SURFACE_COLOR, UIConstants.TEXT_PRIMARY),
            "danger": (UIConstants.ERROR_COLOR, UIConstants.SURFACE_COLOR)
        }
        
        bg_color, text_color = colors.get(style_type, colors["primary"])
        
        content = ft.Row([
            ft.Icon(icon, size=UIConstants.ICON_SIZE_SMALL) if icon else ft.Container(),
            ft.Text(text, size=UIConstants.FONT_SIZE_LARGE, weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=UIConstants.SPACING_SMALL)
        
        button = ft.ElevatedButton(
            content=content,
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor=bg_color,
                color=text_color,
                padding=ft.padding.symmetric(horizontal=24, vertical=UIConstants.PADDING_STANDARD),
                shape=ft.RoundedRectangleBorder(radius=UIConstants.BORDER_RADIUS),
                elevation=2
            )
        )
        
        if expand:
            button.expand = True
            
        return button

    def _create_outlined_button(self, text, icon=None, on_click=None, expand=False):
        """Create a standardized outlined button"""
        content = ft.Row([
            ft.Icon(icon, size=UIConstants.ICON_SIZE_SMALL) if icon else ft.Container(),
            ft.Text(text, size=UIConstants.FONT_SIZE_LARGE)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=UIConstants.SPACING_SMALL)
        
        button = ft.OutlinedButton(
            content=content,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=UIConstants.TEXT_SECONDARY,
                padding=ft.padding.symmetric(horizontal=24, vertical=UIConstants.PADDING_STANDARD),
                shape=ft.RoundedRectangleBorder(radius=UIConstants.BORDER_RADIUS),
                side=ft.BorderSide(width=1, color=ft.Colors.GREY_300)
            )
        )
        
        if expand:
            button.expand = True
            
        return button

    def _create_modern_header(self, title, subtitle, icon):
        """Create a standardized header with icon, title, and subtitle"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=UIConstants.ICON_SIZE_LARGE, color=UIConstants.SURFACE_COLOR),
                    bgcolor=UIConstants.PRIMARY_COLOR,
                    border_radius=UIConstants.PADDING_STANDARD,
                    padding=ft.padding.all(UIConstants.SPACING_SMALL)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=UIConstants.FONT_SIZE_HEADER, weight=ft.FontWeight.BOLD, color=UIConstants.TEXT_PRIMARY),
                        ft.Text(subtitle, size=UIConstants.FONT_SIZE_MEDIUM, color=UIConstants.TEXT_SECONDARY)
                    ], spacing=2),
                    padding=ft.padding.only(left=UIConstants.BORDER_RADIUS),
                    expand=True
                )
            ]),
            padding=ft.padding.all(UIConstants.PADDING_STANDARD),
            margin=ft.margin.only(bottom=UIConstants.PADDING_STANDARD)
        )

    def _show_message(self, message, is_error=False):
        """Unified method for showing success/error messages"""
        color = UIConstants.ERROR_COLOR if is_error else UIConstants.SUCCESS_COLOR
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

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
        if self._loading and not force_refresh and not self._cache_dirty:
            return self._cars_cache or []
            
        if self._cache_dirty or force_refresh or self._cars_cache is None:
            try:
                # Force refresh by clearing cache and getting fresh data
                self._get_cars_data_cached.cache_clear()
                
                # Use timestamp for cache key to ensure fresh data
                cache_key = int(time.time())
                
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

    def _create_modern_button(self, text, icon, on_click, bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE, expand=False):
        """Create a modern styled button with consistent design"""
        return ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(icon, size=20),
                ft.Text(text, size=16, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor=bgcolor,
                color=color,
                padding=ft.padding.symmetric(horizontal=24, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=2
            ),
            expand=expand
        )

    def _create_modern_header(self, title, subtitle, icon, icon_color=ft.Colors.INDIGO_600):
        """Create a modern header with icon and text"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=32, color=ft.Colors.WHITE),
                    bgcolor=icon_color,
                    border_radius=16,
                    padding=ft.padding.all(8)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Text(subtitle, size=14, color=ft.Colors.GREY_600)
                    ], spacing=2),
                    padding=ft.padding.only(left=12),
                    expand=True
                )
            ]),
            padding=ft.padding.all(16),
            margin=ft.margin.only(bottom=16)
        )

    def _create_modern_text_field(self, label, hint_text, icon, keyboard_type=None, required=False):
        """Create a modern styled text field with consistent design"""
        label_text = f"{label} *" if required else label
        return ft.TextField(
            label=label_text,
            hint_text=hint_text,
            prefix_icon=icon,
            keyboard_type=keyboard_type,
            border_radius=12,
            filled=True,
            bgcolor=ft.Colors.GREY_50
        )

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
        """Update main view by navigating to home - DEPRECATED: Use self.page.go('/') directly"""
        self._invalidate_cache()
        self.page.go("/")

    def show_error(self, message):
        """Show error message to user"""
        self._show_message(message, is_error=True)

    def show_success(self, message):
        """Show success message to user"""
        self._show_message(message, is_error=False)

    def show_delete_dialog(self, model_name):
        def close_dialog(e):
            confirm_dialog.open = False
            self.page.update()

        def delete_confirmed(e):
            try:
                success = self.car_tracker.deleteData(model_name)
                close_dialog(e)
                if success:
                    # Invalidate cache to ensure fresh data
                    self._invalidate_cache()
                    self.show_success(f"'{model_name}' deleted successfully!")
                    # Navigate to refresh the main view properly
                    self.page.go("/")
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

    def create_main_view(self, search_term=None, force_refresh=False):
        try:
            # Force cache invalidation if requested
            if force_refresh:
                self._invalidate_cache()
                
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
            
            # Modern header with stats
            header = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.DIRECTIONS_CAR, size=32, color=ft.Colors.INDIGO_700),
                            ft.Text(f"{len(cars_data)}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                            ft.Text("Total Cars", size=12, color=ft.Colors.GREY_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        padding=ft.padding.all(16),
                        bgcolor=ft.Colors.INDIGO_50,
                        border_radius=12,
                        expand=True
                    ),
                    ft.Container(width=8),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.CATEGORY, size=32, color=ft.Colors.GREEN_700),
                            ft.Text(f"{len(set(car.get('category', 'Other') for car in cars_data))}", 
                                   size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                            ft.Text("Categories", size=12, color=ft.Colors.GREY_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        padding=ft.padding.all(16),
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=12,
                        expand=True
                    )
                ], spacing=0),
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8)
            )

            # Use ListView with auto_scroll=False to maintain scroll position
            car_list = ft.ListView(
                controls=[header] + car_cards,
                spacing=6,
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                expand=True,
                auto_scroll=False  # This prevents auto-scrolling to top
            )

            return ft.View(
                "/",
                [car_list],
                floating_action_button=ft.FloatingActionButton(
                    icon=ft.Icons.ADD, 
                    on_click=lambda _: self.page.go("/add_car"),
                    bgcolor=ft.Colors.INDIGO_600,
                    tooltip="Add New Car",
                    shape=ft.CircleBorder(),
                    elevation=4
                ),
                appbar=self.page.appbar,
                navigation_bar=self.page.navigation_bar,
                padding=0,
                bgcolor=ft.Colors.GREY_50  # Light background
            )
        except Exception as e:
            print(f"Error creating main view: {e}")
            return self._create_error_view(f"Error loading cars: {e}")

    def _create_car_cards_optimized(self, cars):
        """Create modern car cards with enhanced UI"""
        if not cars:
            return [ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.DIRECTIONS_CAR_OUTLINED, size=80, color=ft.Colors.GREY_300),
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=40,
                        margin=ft.margin.only(bottom=16)
                    ),
                    ft.Text("No cars in your collection", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                    ft.Text("Start building your dream collection!", color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=16),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=20),
                            ft.Text("Add Your First Car")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda _: self.page.go("/add_car"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.INDIGO_600,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=24, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=25)
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=ft.padding.all(32),
                alignment=ft.alignment.center
            )]

        cards = []
        # Use the current limit from instance variable
        display_limit = min(len(cars), self._max_cards_initial)
        
        for i, car in enumerate(cars[:display_limit]):
            # Get category color
            category_colors = {
                'Sports Car': ft.Colors.RED_400,
                'Racing': ft.Colors.ORANGE_400,
                'SUV': ft.Colors.GREEN_400,
                'Sedan': ft.Colors.BLUE_400,
                'Coupe': ft.Colors.PURPLE_400,
                'Convertible': ft.Colors.PINK_400,
                'Truck': ft.Colors.BROWN_400,
                'Luxury': ft.Colors.AMBER_400,
            }
            category = car.get('category', 'Other')
            category_color = category_colors.get(category, ft.Colors.GREY_400)
            
            # Modern card design
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        # Header with car avatar and category badge
                        ft.Row([
                            ft.Container(
                                content=ft.Text(car.get('model', 'C')[0].upper(), 
                                              color=ft.Colors.WHITE, 
                                              size=16, 
                                              weight=ft.FontWeight.BOLD),
                                bgcolor=ft.Colors.INDIGO_600,
                                border_radius=20,
                                width=40,
                                height=40,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(car.get('model', 'Unknown'), 
                                           size=16, 
                                           weight=ft.FontWeight.BOLD,
                                           color=ft.Colors.GREY_800),
                                    ft.Text(f"{car.get('manufacturer', '')} • {car.get('year', '')}", 
                                           size=13, 
                                           color=ft.Colors.GREY_600)
                                ], spacing=2),
                                expand=True,
                                padding=ft.padding.only(left=12)
                            ),
                            ft.Container(
                                content=ft.Text(category, size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                bgcolor=category_color,
                                border_radius=8,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        # Country and additional info
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.PUBLIC, size=14, color=ft.Colors.GREY_500),
                                ft.Text(car.get('country_of_origin', 'Unknown'), 
                                       size=12, 
                                       color=ft.Colors.GREY_600),
                                ft.Container(expand=True),
                                ft.Icon(ft.Icons.TOYS, size=14, color=ft.Colors.GREY_500),
                                ft.Text(car.get('replica_model', 'N/A'), 
                                       size=12, 
                                       color=ft.Colors.GREY_600)
                            ], spacing=4),
                            margin=ft.margin.only(top=8)
                        ),
                        
                        # Action buttons with modern design
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=ft.Colors.INDIGO_600,
                                    tooltip="Edit Car",
                                    on_click=lambda e, model=car.get('model'): self.page.go(f"/edit_car/{model}"),
                                    style=ft.ButtonStyle(
                                        shape=ft.CircleBorder(),
                                        bgcolor=ft.Colors.INDIGO_50
                                    )
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_600,
                                    tooltip="Delete Car",
                                    on_click=lambda e, model=car.get('model'): self.show_delete_dialog(model),
                                    style=ft.ButtonStyle(
                                        shape=ft.CircleBorder(),
                                        bgcolor=ft.Colors.RED_50
                                    )
                                ),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.OPEN_IN_NEW,
                                    icon_color=ft.Colors.GREEN_600 if car.get('info') else ft.Colors.GREY_400,
                                    tooltip="More Info",
                                    on_click=lambda e, url=car.get('info', ''): self.page.launch_url(url) if url else None,
                                    disabled=not car.get('info'),
                                    style=ft.ButtonStyle(
                                        shape=ft.CircleBorder(),
                                        bgcolor=ft.Colors.GREEN_50 if car.get('info') else ft.Colors.GREY_100
                                    )
                                )
                            ], alignment=ft.MainAxisAlignment.START),
                            margin=ft.margin.only(top=8)
                        )
                    ], spacing=0),
                    padding=ft.padding.all(16),
                    border_radius=12
                ),
                elevation=2,
                margin=ft.margin.symmetric(horizontal=4, vertical=4),
                surface_tint_color=ft.Colors.INDIGO_50
            )
            cards.append(card)
        
        # Modern "Load More" button
        if len(cars) > display_limit:
            cards.append(
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.EXPAND_MORE, size=20),
                            ft.Text(f"Load {min(15, len(cars) - display_limit)} more cars", size=14)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                        on_click=lambda e: self._load_more_cars_improved(e),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.INDIGO_100,
                            color=ft.Colors.INDIGO_700,
                            padding=ft.padding.symmetric(horizontal=24, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=20),
                            elevation=1
                        ),
                        key="load_more_btn"
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(12),
                    key="load_more_container"
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
            try:
                # Create a new dictionary for the updated data
                updated_data = {key: field.value if field.value else "" for key, field in fields.items()}
                # The modelName is disabled, so its value won't be in the dictionary, add it back
                updated_data['modelName'] = model_name

                # Delete the old record and add the new one
                delete_success = self.car_tracker.deleteData(model_name)
                if delete_success:
                    add_success = self.car_tracker.addData(
                        modelName=updated_data["modelName"],
                        manufacturer=updated_data["manufacturer"], 
                        year=updated_data["year"],
                        originCountry=updated_data["originCountry"],
                        category=updated_data["category"],
                        modelManufact=updated_data["modelManufact"],
                        more=updated_data["more"]
                    )
                    if add_success:
                        # Invalidate cache and show success
                        self._invalidate_cache()
                        self.show_success("Car updated successfully!")
                        self.page.go("/")
                    else:
                        self.show_error("Failed to update car. Please try again.")
                else:
                    self.show_error("Failed to update car. Please try again.")
            except Exception as ex:
                self.show_error(f"Error updating car: {str(ex)}")

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
        # Modern form fields using helper method
        fields = {
            "modelName": self._create_modern_text_field("Model Name", "e.g., Mustang GT", ft.Icons.DIRECTIONS_CAR, required=True),
            "manufacturer": self._create_modern_text_field("Manufacturer", "e.g., Ford", ft.Icons.BUSINESS),
            "year": self._create_modern_text_field("Year", "e.g., 2023", ft.Icons.CALENDAR_TODAY, ft.KeyboardType.NUMBER),
            "originCountry": self._create_modern_text_field("Origin Country", "e.g., USA", ft.Icons.PUBLIC),
            "category": self._create_modern_text_field("Category", "e.g., Sports Car", ft.Icons.CATEGORY),
            "modelManufact": self._create_modern_text_field("Model Manufacturer", "e.g., Hot Wheels", ft.Icons.TOYS),
            "more": self._create_modern_text_field("More Info (URL)", "https://...", ft.Icons.LINK, ft.KeyboardType.URL)
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
                # Map the field keys to the exact parameter names expected by addData
                success = self.car_tracker.addData(
                    modelName=data["modelName"],
                    manufacturer=data["manufacturer"], 
                    year=data["year"],
                    originCountry=data["originCountry"],
                    category=data["category"],
                    modelManufact=data["modelManufact"],
                    more=data["more"]
                )
                if success:
                    # Clear the form first
                    for field in fields.values():
                        field.value = ""
                        field.error_text = None
                    
                    # Invalidate cache to ensure fresh data
                    self._invalidate_cache()
                    
                    # Show success message
                    self.show_success("Car added successfully!")
                    
                    # Update page and navigate back to main view
                    self.page.update()
                    self.page.go("/")
                else:
                    self.show_error("Failed to save car. Please try again.")
            except Exception as ex:
                self.show_error(f"Error saving car: {str(ex)}")

        # Modern form layout
        return ft.View(
            "/add_car",
            [
                ft.Container(
                    content=ft.Column([
                        # Header with icon using helper method
                        self._create_modern_header("Add New Car", "Add a new car to your collection", ft.Icons.ADD_CIRCLE),
                        
                        # Form fields with improved spacing
                        *[ft.Container(content=field, margin=ft.margin.only(bottom=16)) 
                          for field in fields.values()],
                        
                        # Action buttons with modern styling using helper method
                        ft.Container(
                            content=ft.Row([
                                self._create_modern_button("Add Car", ft.Icons.ADD, add_car_click, expand=True),
                                ft.Container(width=UIConstants.BORDER_RADIUS),
                                self._create_outlined_button("Cancel", ft.Icons.CANCEL_OUTLINED, lambda _: self.page.go("/"), expand=True)
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                            margin=ft.margin.only(top=UIConstants.PADDING_STANDARD)
                        )
                    ], spacing=0),
                    padding=ft.padding.all(20),
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(
                title=ft.Text("Add Car", color=ft.Colors.WHITE), 
                bgcolor=ft.Colors.INDIGO_700,
                color=ft.Colors.WHITE
            ),
            bgcolor=ft.Colors.GREY_50
        )

    def create_search_view(self):
        search_field = self._create_modern_text_field("Search Cars", "Enter car model to search...", ft.Icons.SEARCH)
        search_field.bgcolor = UIConstants.SURFACE_COLOR
        search_field.on_submit = lambda e: self.perform_search(e.control.value)
        
        search_button = self._create_modern_button("Search", ft.Icons.SEARCH, lambda _: self.perform_search(search_field.value))
        
        return ft.View(
            "/search",
            [
                ft.Container(
                    content=ft.Column([
                        # Header with icon using helper method
                        self._create_modern_header("Search Cars", "Find cars in your collection", ft.Icons.SEARCH),
                        
                        # Search input section
                        ft.Container(
                            content=ft.Column([
                                search_field,
                                ft.Container(height=UIConstants.SPACING_STANDARD),
                                search_button
                            ], spacing=0),
                            padding=ft.padding.all(UIConstants.PADDING_STANDARD),
                            bgcolor=UIConstants.SURFACE_COLOR,
                            border_radius=UIConstants.BORDER_RADIUS,
                            border=ft.border.all(1, ft.Colors.GREY_200),
                            margin=ft.margin.only(bottom=UIConstants.PADDING_STANDARD)
                        ),
                        
                        # Info section
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.INFO_OUTLINE, color=UIConstants.TEXT_SECONDARY, size=UIConstants.ICON_SIZE_SMALL),
                                ft.Text(
                                    "Enter a car model name to search through your collection",
                                    color=UIConstants.TEXT_SECONDARY,
                                    size=UIConstants.FONT_SIZE_MEDIUM
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=UIConstants.SPACING_SMALL),
                            padding=ft.padding.all(UIConstants.PADDING_LARGE),
                            border_radius=UIConstants.BORDER_RADIUS,
                            bgcolor=UIConstants.PRIMARY_SURFACE
                        )
                    ], spacing=0),
                    padding=ft.padding.all(UIConstants.PADDING_LARGE),
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(
                title=ft.Text("Search", color=UIConstants.SURFACE_COLOR), 
                bgcolor=UIConstants.PRIMARY_COLOR,
                color=UIConstants.SURFACE_COLOR
            ),
            bgcolor=UIConstants.BACKGROUND_COLOR,
            navigation_bar=self.page.navigation_bar
        )
    
    def perform_search(self, search_term):
        if search_term and search_term.strip():
            self.page.go(f"/search/{search_term.strip()}")
        else:
            self._show_message("Please enter a search term", is_error=True)

    def route_change(self, route):
        route_path = self.page.route
        self.page.views.clear()

        if route_path == "/":
            self.page.views.append(self.create_main_view(force_refresh=True))
        elif self.page.route == "/add_car":
            self.page.views.append(self.create_add_car_view())
        elif self.page.route.startswith("/edit_car/"):
            model_name = self.page.route.split("/")[-1]
            self.page.views.append(self.create_edit_car_view(model_name))
        elif route_path == "/search":
            self.page.views.append(self.create_search_view())
        elif route_path.startswith("/search/"):
            search_term = route_path.split("/")[-1]
            self.page.views.append(self.create_main_view(search_term=search_term, force_refresh=True))
        else:
            # Default to main view if route is unknown
            self.page.views.append(self.create_main_view(force_refresh=True))
        
        self.page.update()

    def view_pop(self, view):
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        elif len(self.page.views) == 1:
            # If only one view, go to home
            self.page.go("/")
        else:
            # If no views, create home view
            self.page.go("/")

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
