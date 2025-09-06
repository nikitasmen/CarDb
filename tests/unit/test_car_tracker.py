"""
Unit tests for CarTracker functionality
"""
import pytest
from unittest.mock import patch, Mock
from app.car_tracker import CarTracker


class TestCarTrackerInitialization:
    """Test cases for CarTracker initialization"""
    
    @pytest.mark.unit
    def test_init_success(self):
        """Test successful initialization"""
        with patch('app.car_tracker.CarFileHandler') as mock_handler:
            mock_handler.return_value = Mock()
            tracker = CarTracker()
            
            assert tracker.fileHandler is not None
            mock_handler.assert_called_once()
    
    @pytest.mark.unit
    def test_init_failure(self):
        """Test initialization failure handling"""
        with patch('app.car_tracker.CarFileHandler', side_effect=Exception("Init error")):
            tracker = CarTracker()
            
            assert tracker.fileHandler is None
    
    @pytest.mark.unit
    def test_ensure_handler_success(self, empty_car_tracker):
        """Test successful handler reinitialization"""
        empty_car_tracker.fileHandler = None
        
        with patch('app.car_tracker.CarFileHandler') as mock_handler:
            mock_handler.return_value = Mock()
            result = empty_car_tracker._ensure_handler()
            
            assert result is True
            assert empty_car_tracker.fileHandler is not None
    
    @pytest.mark.unit
    def test_ensure_handler_failure(self, empty_car_tracker):
        """Test handler reinitialization failure"""
        empty_car_tracker.fileHandler = None
        
        with patch('app.car_tracker.CarFileHandler', side_effect=Exception("Handler error")):
            result = empty_car_tracker._ensure_handler()
            
            assert result is False
            assert empty_car_tracker.fileHandler is None


class TestCarTrackerDataOperations:
    """Test cases for data operations"""
    
    @pytest.mark.unit
    def test_add_data_success(self, empty_car_tracker):
        """Test successfully adding car data"""
        result = empty_car_tracker.addData(
            modelName="Test Car",
            manufacturer="Test Manufacturer",
            year="2020",
            originCountry="Test Country",
            category="Test Category",
            modelManufact="Test Replica",
            more="https://test.com"
        )
        
        assert result is True
        
        # Verify data was added
        cars = empty_car_tracker.displayData()
        assert len(cars) == 1
        assert cars[0]["model"] == "Test Car"
    
    @pytest.mark.unit
    def test_add_data_duplicate_model(self, car_tracker_with_data):
        """Test adding car with duplicate model name"""
        # Try to add car with existing model name
        result = car_tracker_with_data.addData(
            modelName="Toyota Corolla",  # Already exists
            manufacturer="Different Manufacturer",
            year="2021",
            originCountry="Different Country",
            category="Different Category",
            modelManufact="Different Replica",
            more="https://different.com"
        )
        
        assert result is False
        
        # Verify no duplicate was added
        cars = car_tracker_with_data.displayData()
        assert len(cars) == 3  # Original 3 cars
    
    @pytest.mark.unit
    def test_add_data_case_insensitive_duplicate(self, car_tracker_with_data):
        """Test adding car with case-insensitive duplicate model name"""
        result = car_tracker_with_data.addData(
            modelName="toyota corolla",  # Different case
            manufacturer="Different Manufacturer",
            year="2021",
            originCountry="Different Country",
            category="Different Category",
            modelManufact="Different Replica",
            more="https://different.com"
        )
        
        assert result is False
    
    @pytest.mark.unit
    def test_add_data_invalid_data(self, empty_car_tracker):
        """Test adding car with invalid data"""
        result = empty_car_tracker.addData(
            modelName="",  # Empty model (invalid)
            manufacturer="Test Manufacturer",
            year="1800",  # Invalid year
            originCountry="Test Country",
            category="Test Category",
            modelManufact="Test Replica",
            more="not-a-url"  # Invalid URL
        )
        
        assert result is False
    
    @pytest.mark.unit
    def test_add_data_handler_failure(self, empty_car_tracker):
        """Test adding data when handler fails"""
        empty_car_tracker.fileHandler = None
        
        result = empty_car_tracker.addData(
            modelName="Test Car",
            manufacturer="Test Manufacturer",
            year="2020",
            originCountry="Test Country",
            category="Test Category",
            modelManufact="Test Replica",
            more="https://test.com"
        )
        
        assert result is False
    
    @pytest.mark.unit
    def test_add_data_exception_handling(self, empty_car_tracker):
        """Test exception handling during add operation"""
        with patch.object(empty_car_tracker, '_load_cars', side_effect=Exception("Load error")):
            result = empty_car_tracker.addData(
                modelName="Test Car",
                manufacturer="Test Manufacturer",
                year="2020",
                originCountry="Test Country",
                category="Test Category",
                modelManufact="Test Replica",
                more="https://test.com"
            )
            
            assert result is False


class TestCarTrackerSearchOperations:
    """Test cases for search operations"""
    
    @pytest.mark.unit
    def test_search_exact_match(self, car_tracker_with_data):
        """Test searching for exact model match"""
        results = car_tracker_with_data.search("Toyota Corolla")
        
        assert len(results) == 1
        assert results[0]["model"] == "Toyota Corolla"
    
    @pytest.mark.unit
    def test_search_partial_match(self, car_tracker_with_data):
        """Test searching for partial model match"""
        results = car_tracker_with_data.search("Toyota")
        
        assert len(results) == 1
        assert "Toyota" in results[0]["model"]
    
    @pytest.mark.unit
    def test_search_case_insensitive(self, car_tracker_with_data):
        """Test case-insensitive search"""
        results = car_tracker_with_data.search("toyota corolla")
        
        assert len(results) == 1
        assert results[0]["model"] == "Toyota Corolla"
    
    @pytest.mark.unit
    def test_search_no_match(self, car_tracker_with_data):
        """Test searching for non-existent model"""
        results = car_tracker_with_data.search("Non-existent Car")
        
        assert len(results) == 0
    
    @pytest.mark.unit
    def test_search_empty_string(self, car_tracker_with_data):
        """Test searching with empty string"""
        results = car_tracker_with_data.search("")
        
        assert len(results) == 3  # Should match all cars
    
    @pytest.mark.unit
    def test_search_whitespace(self, car_tracker_with_data):
        """Test searching with whitespace"""
        results = car_tracker_with_data.search("  Toyota  ")
        
        assert len(results) == 1
        assert results[0]["model"] == "Toyota Corolla"
    
    @pytest.mark.unit
    def test_search_handler_failure(self, empty_car_tracker):
        """Test search when handler fails"""
        empty_car_tracker.fileHandler = None
        
        results = empty_car_tracker.search("Test")
        
        assert results == []
    
    @pytest.mark.unit
    def test_search_exception_handling(self, car_tracker_with_data):
        """Test exception handling during search"""
        with patch.object(car_tracker_with_data, '_load_cars', side_effect=Exception("Load error")):
            results = car_tracker_with_data.search("Test")
            
            assert results == []


class TestCarTrackerDeleteOperations:
    """Test cases for delete operations"""
    
    @pytest.mark.unit
    def test_delete_data_existing_car(self, car_tracker_with_data):
        """Test deleting existing car"""
        result = car_tracker_with_data.deleteData("Toyota Corolla")
        
        assert result is True
        
        # Verify car was deleted
        cars = car_tracker_with_data.displayData()
        assert len(cars) == 2
        assert not any(car["model"] == "Toyota Corolla" for car in cars)
    
    @pytest.mark.unit
    def test_delete_data_case_insensitive(self, car_tracker_with_data):
        """Test case-insensitive delete"""
        result = car_tracker_with_data.deleteData("toyota corolla")
        
        assert result is True
        
        cars = car_tracker_with_data.displayData()
        assert len(cars) == 2
        assert not any(car["model"] == "Toyota Corolla" for car in cars)
    
    @pytest.mark.unit
    def test_delete_data_non_existent_car(self, car_tracker_with_data):
        """Test deleting non-existent car"""
        result = car_tracker_with_data.deleteData("Non-existent Car")
        
        assert result is False
        
        # Verify no cars were deleted
        cars = car_tracker_with_data.displayData()
        assert len(cars) == 3
    
    @pytest.mark.unit
    def test_delete_data_empty_string(self, car_tracker_with_data):
        """Test deleting with empty string"""
        result = car_tracker_with_data.deleteData("")
        
        assert result is False
        
        cars = car_tracker_with_data.displayData()
        assert len(cars) == 3
    
    @pytest.mark.unit
    def test_delete_data_handler_failure(self, empty_car_tracker):
        """Test delete when handler fails"""
        empty_car_tracker.fileHandler = None
        
        result = empty_car_tracker.deleteData("Test Car")
        
        assert result is False
    
    @pytest.mark.unit
    def test_delete_data_exception_handling(self, car_tracker_with_data):
        """Test exception handling during delete"""
        with patch.object(car_tracker_with_data, '_load_cars', side_effect=Exception("Load error")):
            result = car_tracker_with_data.deleteData("Toyota Corolla")
            
            assert result is False


class TestCarTrackerDisplayOperations:
    """Test cases for display operations"""
    
    @pytest.mark.unit
    def test_display_data_success(self, car_tracker_with_data):
        """Test successfully displaying data"""
        cars = car_tracker_with_data.displayData()
        
        assert len(cars) == 3
        assert all("id" not in car for car in cars)  # IDs should be hidden
        assert cars[0]["model"] == "Toyota Corolla"
    
    @pytest.mark.unit
    def test_display_data_empty(self, empty_car_tracker):
        """Test displaying empty data"""
        cars = empty_car_tracker.displayData()
        
        assert cars == []
    
    @pytest.mark.unit
    def test_display_data_handler_failure(self, empty_car_tracker):
        """Test display when handler fails"""
        empty_car_tracker.fileHandler = None
        
        cars = empty_car_tracker.displayData()
        
        assert cars == []
    
    @pytest.mark.unit
    def test_display_data_exception_handling(self, car_tracker_with_data):
        """Test exception handling during display"""
        with patch.object(car_tracker_with_data, '_load_cars', side_effect=Exception("Load error")):
            cars = car_tracker_with_data.displayData()
            
            assert cars == []


class TestCarTrackerImportOperations:
    """Test cases for import operations"""
    
    @pytest.mark.unit
    def test_import_data_json(self, empty_car_tracker, temp_data_dir):
        """Test importing JSON data"""
        import os
        json_file = os.path.join(temp_data_dir, "import.json")
        
        with patch.object(empty_car_tracker.fileHandler, 'importDataJSON', return_value=True):
            result = empty_car_tracker.importData(json_file)
            
            assert result is True
    
    @pytest.mark.unit
    def test_import_data_csv(self, empty_car_tracker, temp_data_dir):
        """Test importing CSV data"""
        import os
        csv_file = os.path.join(temp_data_dir, "import.csv")
        
        with patch.object(empty_car_tracker.fileHandler, 'importDataCSV', return_value=True):
            result = empty_car_tracker.importData(csv_file)
            
            assert result is True
    
    @pytest.mark.unit
    def test_import_data_excel(self, empty_car_tracker, temp_data_dir):
        """Test importing Excel data"""
        import os
        excel_file = os.path.join(temp_data_dir, "import.xlsx")
        
        with patch.object(empty_car_tracker.fileHandler, 'importDataExcel', return_value=True):
            result = empty_car_tracker.importData(excel_file)
            
            assert result is True
    
    @pytest.mark.unit
    def test_import_data_unsupported_format(self, empty_car_tracker):
        """Test importing unsupported file format"""
        result = empty_car_tracker.importData("file.txt")
        
        assert result is False
    
    @pytest.mark.unit
    def test_import_data_handler_failure(self, empty_car_tracker):
        """Test import when handler fails"""
        empty_car_tracker.fileHandler = None
        
        result = empty_car_tracker.importData("file.json")
        
        assert result is False
    
    @pytest.mark.unit
    def test_import_data_exception_handling(self, empty_car_tracker):
        """Test exception handling during import"""
        with patch.object(empty_car_tracker.fileHandler, 'importDataJSON', side_effect=Exception("Import error")):
            result = empty_car_tracker.importData("file.json")
            
            assert result is False

