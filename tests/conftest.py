"""
Pytest configuration and fixtures for CarDb Mobile App tests
"""
import pytest
import tempfile
import os
import json
import shutil
from unittest.mock import Mock, patch
from app.models import Car, normalize_car_record, validate_car_record
from app.car_tracker import CarTracker
from app.car_handler import CarFileHandler


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_car_data():
    """Sample car data for testing"""
    return [
        {
            "model": "Toyota Corolla",
            "manufacturer": "Toyota",
            "year": "2020",
            "country_of_origin": "Japan",
            "category": "Sedan",
            "replica_model": "Hot Wheels",
            "info": "https://www.toyota.com/corolla"
        },
        {
            "model": "Ford Mustang",
            "manufacturer": "Ford",
            "year": "2021",
            "country_of_origin": "USA",
            "category": "Sports Car",
            "replica_model": "Matchbox",
            "info": "https://www.ford.com/mustang"
        },
        {
            "model": "BMW X5",
            "manufacturer": "BMW",
            "year": "2022",
            "country_of_origin": "Germany",
            "category": "SUV",
            "replica_model": "Majorette",
            "info": "https://www.bmw.com/x5"
        }
    ]


@pytest.fixture
def invalid_car_data():
    """Invalid car data for testing error handling"""
    return [
        {
            "model": "",  # Empty model (invalid)
            "manufacturer": "Toyota",
            "year": "1800",  # Invalid year
            "country_of_origin": "Japan",
            "category": "Sedan",
            "replica_model": "Hot Wheels",
            "info": "not-a-url"  # Invalid URL
        },
        {
            "model": "Test Car",
            "manufacturer": "Test Manufacturer",
            "year": "invalid-year",  # Non-numeric year
            "country_of_origin": "Test Country",
            "category": "Test Category",
            "replica_model": "Test Replica",
            "info": "https://valid-url.com"
        }
    ]


@pytest.fixture
def car_file_handler(temp_data_dir):
    """Create a CarFileHandler with temporary data directory"""
    test_file = os.path.join(temp_data_dir, "test_cars.json")
    return CarFileHandler(target=test_file)


@pytest.fixture
def car_tracker_with_data(car_file_handler, sample_car_data):
    """Create a CarTracker with sample data loaded"""
    # Save sample data to the test file
    car_file_handler.saveTarget(sample_car_data)
    return CarTracker()


@pytest.fixture
def empty_car_tracker(car_file_handler):
    """Create an empty CarTracker"""
    return CarTracker()


@pytest.fixture
def mock_page():
    """Mock Flet page for UI testing"""
    page = Mock()
    page.title = "Test App"
    page.route = "/"
    page.views = []
    page.appbar = None
    page.navigation_bar = None
    page.snack_bar = None
    page.overlay = []
    
    def mock_go(route):
        page.route = route
        
    def mock_update():
        pass
        
    page.go = mock_go
    page.update = mock_update
    page.launch_url = Mock()
    
    return page


@pytest.fixture
def flet_app_instance(empty_car_tracker):
    """Create a FletApp instance for testing"""
    from interfaces.flet_app import FletApp
    app = FletApp()
    app.car_tracker = empty_car_tracker
    return app


@pytest.fixture
def large_dataset():
    """Generate a large dataset for performance testing"""
    cars = []
    manufacturers = ["Toyota", "Ford", "BMW", "Mercedes", "Audi", "Honda", "Nissan", "Chevrolet"]
    categories = ["Sedan", "SUV", "Sports Car", "Coupe", "Convertible", "Truck", "Luxury"]
    countries = ["Japan", "USA", "Germany", "Italy", "UK", "France", "South Korea"]
    
    for i in range(1000):
        car = {
            "model": f"Test Model {i}",
            "manufacturer": manufacturers[i % len(manufacturers)],
            "year": str(2000 + (i % 24)),
            "country_of_origin": countries[i % len(countries)],
            "category": categories[i % len(categories)],
            "replica_model": f"Replica {i}",
            "info": f"https://example.com/car{i}"
        }
        cars.append(car)
    
    return cars


@pytest.fixture
def mock_flet_components():
    """Mock Flet components for testing"""
    with patch('flet.Container'), \
         patch('flet.Text'), \
         patch('flet.TextField'), \
         patch('flet.ElevatedButton'), \
         patch('flet.Row'), \
         patch('flet.Column'), \
         patch('flet.Card'), \
         patch('flet.Icon'), \
         patch('flet.ListView'), \
         patch('flet.View'), \
         patch('flet.AppBar'), \
         patch('flet.NavigationBar'), \
         patch('flet.SnackBar'), \
         patch('flet.AlertDialog') as mock_dialog:
        yield {
            'dialog': mock_dialog
        }


# Test data cleanup
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically clean up test files after each test"""
    yield
    # Cleanup is handled by tempfile fixtures
    pass


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as a UI test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "mobile: mark test as a mobile-specific test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

