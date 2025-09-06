"""
Unit tests for data models and validation
"""
import pytest
from app.models import Car, normalize_car_record, validate_car_record, to_car_list, to_dict_list


class TestCarModel:
    """Test cases for Car model"""
    
    @pytest.mark.unit
    def test_car_creation_with_all_fields(self):
        """Test creating a car with all fields populated"""
        car = Car(
            id="test-id",
            model="Toyota Corolla",
            manufacturer="Toyota",
            year="2020",
            country_of_origin="Japan",
            category="Sedan",
            replica_model="Hot Wheels",
            info="https://www.toyota.com/corolla"
        )
        
        assert car.id == "test-id"
        assert car.model == "Toyota Corolla"
        assert car.manufacturer == "Toyota"
        assert car.year == "2020"
        assert car.country_of_origin == "Japan"
        assert car.category == "Sedan"
        assert car.replica_model == "Hot Wheels"
        assert car.info == "https://www.toyota.com/corolla"
    
    @pytest.mark.unit
    def test_car_creation_with_minimal_fields(self):
        """Test creating a car with only required fields"""
        car = Car(id="test-id", model="Test Model")
        
        assert car.id == "test-id"
        assert car.model == "Test Model"
        assert car.manufacturer == ""
        assert car.year == ""
        assert car.country_of_origin == ""
        assert car.category == ""
        assert car.replica_model == ""
        assert car.info == ""
    
    @pytest.mark.unit
    def test_car_to_dict(self):
        """Test converting car to dictionary"""
        car = Car(
            id="test-id",
            model="Test Model",
            manufacturer="Test Manufacturer",
            year="2020"
        )
        
        car_dict = car.to_dict()
        
        assert isinstance(car_dict, dict)
        assert car_dict["id"] == "test-id"
        assert car_dict["model"] == "Test Model"
        assert car_dict["manufacturer"] == "Test Manufacturer"
        assert car_dict["year"] == "2020"
    
    @pytest.mark.unit
    def test_car_from_dict(self):
        """Test creating car from dictionary"""
        car_dict = {
            "id": "test-id",
            "model": "Test Model",
            "manufacturer": "Test Manufacturer",
            "year": "2020",
            "country_of_origin": "Test Country",
            "category": "Test Category",
            "replica_model": "Test Replica",
            "info": "https://test.com"
        }
        
        car = Car.from_dict(car_dict)
        
        assert car.id == "test-id"
        assert car.model == "Test Model"
        assert car.manufacturer == "Test Manufacturer"
        assert car.year == "2020"
        assert car.country_of_origin == "Test Country"
        assert car.category == "Test Category"
        assert car.replica_model == "Test Replica"
        assert car.info == "https://test.com"


class TestDataNormalization:
    """Test cases for data normalization"""
    
    @pytest.mark.unit
    def test_normalize_car_record_valid_data(self):
        """Test normalizing valid car record"""
        raw_data = {
            "Model Name": "Toyota Corolla",  # Test key normalization
            "MANUFACTURER": "Toyota",  # Test case normalization
            "Year": 2020,  # Test type conversion
            "Country Of Origin": "Japan",  # Test space replacement
            "Category": "Sedan",
            "Replica Model": "Hot Wheels",
            "Info": "https://www.toyota.com/corolla"
        }
        
        normalized = normalize_car_record(raw_data)
        
        assert normalized["model"] == "Toyota Corolla"
        assert normalized["manufacturer"] == "Toyota"
        assert normalized["year"] == "2020"
        assert normalized["country_of_origin"] == "Japan"
        assert normalized["category"] == "Sedan"
        assert normalized["replica_model"] == "Hot Wheels"
        assert normalized["info"] == "https://www.toyota.com/corolla"
        assert "id" in normalized  # Should have generated ID
    
    @pytest.mark.unit
    def test_normalize_car_record_with_none_values(self):
        """Test normalizing car record with None values"""
        raw_data = {
            "model": "Test Model",
            "manufacturer": None,
            "year": None,
            "country_of_origin": None,
            "category": None,
            "replica_model": None,
            "info": None
        }
        
        normalized = normalize_car_record(raw_data)
        
        assert normalized["model"] == "Test Model"
        assert normalized["manufacturer"] == ""
        assert normalized["year"] == ""
        assert normalized["country_of_origin"] == ""
        assert normalized["category"] == ""
        assert normalized["replica_model"] == ""
        assert normalized["info"] == ""
    
    @pytest.mark.unit
    def test_normalize_car_record_with_empty_strings(self):
        """Test normalizing car record with empty strings"""
        raw_data = {
            "model": "   ",  # Whitespace only
            "manufacturer": "",
            "year": "",
            "country_of_origin": "",
            "category": "",
            "replica_model": "",
            "info": ""
        }
        
        normalized = normalize_car_record(raw_data)
        
        assert normalized["model"] == ""
        assert normalized["manufacturer"] == ""
        assert normalized["year"] == ""
        assert normalized["country_of_origin"] == ""
        assert normalized["category"] == ""
        assert normalized["replica_model"] == ""
        assert normalized["info"] == ""
    
    @pytest.mark.unit
    def test_normalize_car_record_year_coercion(self):
        """Test year field coercion and validation"""
        test_cases = [
            (2020, "2020"),  # Integer
            ("2020", "2020"),  # String number
            ("  2020  ", "2020"),  # String with whitespace
            (1885, "1885"),  # Minimum valid year
            (2100, "2100"),  # Maximum valid year
            (1800, ""),  # Too old
            (2200, ""),  # Too new
            ("invalid", "invalid"),  # Non-numeric
            (None, ""),  # None value
            ("", "")  # Empty string
        ]
        
        for input_year, expected in test_cases:
            raw_data = {"model": "Test Model", "year": input_year}
            normalized = normalize_car_record(raw_data)
            assert normalized["year"] == expected, f"Failed for input: {input_year}"
    
    @pytest.mark.unit
    def test_normalize_car_record_preserves_existing_id(self):
        """Test that existing ID is preserved during normalization"""
        raw_data = {
            "id": "existing-id",
            "model": "Test Model"
        }
        
        normalized = normalize_car_record(raw_data)
        
        assert normalized["id"] == "existing-id"
    
    @pytest.mark.unit
    def test_normalize_car_record_generates_id_when_missing(self):
        """Test that ID is generated when missing"""
        raw_data = {
            "model": "Test Model"
        }
        
        normalized = normalize_car_record(raw_data)
        
        assert "id" in normalized
        assert normalized["id"] != ""
        assert len(normalized["id"]) > 0


class TestDataValidation:
    """Test cases for data validation"""
    
    @pytest.mark.unit
    def test_validate_car_record_valid_data(self):
        """Test validating valid car record"""
        valid_data = {
            "id": "test-id",
            "model": "Toyota Corolla",
            "year": "2020",
            "info": "https://www.toyota.com/corolla"
        }
        
        is_valid, errors = validate_car_record(valid_data)
        
        assert is_valid is True
        assert len(errors) == 0
    
    @pytest.mark.unit
    def test_validate_car_record_missing_required_fields(self):
        """Test validating car record with missing required fields"""
        invalid_data = {
            "year": "2020"
            # Missing id and model
        }
        
        is_valid, errors = validate_car_record(invalid_data)
        
        assert is_valid is False
        assert "id is required" in errors
        assert "model is required" in errors
    
    @pytest.mark.unit
    def test_validate_car_record_invalid_year_range(self):
        """Test validating car record with invalid year range"""
        test_cases = [
            ("1800", "year out of valid range (1885-2100)"),
            ("2200", "year out of valid range (1885-2100)"),
            ("2020", None),  # Valid year
            ("", None),  # Empty year (valid)
            ("invalid", None)  # Non-numeric year (valid)
        ]
        
        for year, expected_error in test_cases:
            data = {
                "id": "test-id",
                "model": "Test Model",
                "year": year
            }
            
            is_valid, errors = validate_car_record(data)
            
            if expected_error:
                assert is_valid is False
                assert expected_error in errors
            else:
                assert is_valid is True
                assert len(errors) == 0
    
    @pytest.mark.unit
    def test_validate_car_record_invalid_url(self):
        """Test validating car record with invalid URL"""
        data = {
            "id": "test-id",
            "model": "Test Model",
            "info": "not-a-valid-url"
        }
        
        is_valid, errors = validate_car_record(data)
        
        # URL validation is currently non-fatal, so should still be valid
        assert is_valid is True
        assert len(errors) == 0


class TestDataConversion:
    """Test cases for data conversion utilities"""
    
    @pytest.mark.unit
    def test_to_car_list_valid_records(self):
        """Test converting valid records to car list"""
        records = [
            {
                "id": "id1",
                "model": "Car 1",
                "manufacturer": "Manufacturer 1"
            },
            {
                "id": "id2",
                "model": "Car 2",
                "manufacturer": "Manufacturer 2"
            }
        ]
        
        cars = to_car_list(records)
        
        assert len(cars) == 2
        assert isinstance(cars[0], Car)
        assert cars[0].model == "Car 1"
        assert cars[1].model == "Car 2"
    
    @pytest.mark.unit
    def test_to_car_list_invalid_records(self):
        """Test converting records with invalid data"""
        records = [
            {
                "id": "id1",
                "model": "Valid Car"
            },
            {
                "invalid": "data"  # Missing required fields
            },
            {
                "id": "id3",
                "model": "Another Valid Car"
            }
        ]
        
        cars = to_car_list(records)
        
        # Should only include valid records
        assert len(cars) == 2
        assert cars[0].model == "Valid Car"
        assert cars[1].model == "Another Valid Car"
    
    @pytest.mark.unit
    def test_to_car_list_empty_list(self):
        """Test converting empty record list"""
        cars = to_car_list([])
        assert len(cars) == 0
    
    @pytest.mark.unit
    def test_to_car_list_none_input(self):
        """Test converting None input"""
        cars = to_car_list(None)
        assert len(cars) == 0
    
    @pytest.mark.unit
    def test_to_dict_list(self):
        """Test converting car list to dictionary list"""
        cars = [
            Car(id="id1", model="Car 1"),
            Car(id="id2", model="Car 2")
        ]
        
        dict_list = to_dict_list(cars)
        
        assert len(dict_list) == 2
        assert isinstance(dict_list[0], dict)
        assert dict_list[0]["model"] == "Car 1"
        assert dict_list[1]["model"] == "Car 2"
    
    @pytest.mark.unit
    def test_to_dict_list_empty_list(self):
        """Test converting empty car list"""
        dict_list = to_dict_list([])
        assert len(dict_list) == 0
    
    @pytest.mark.unit
    def test_to_dict_list_none_input(self):
        """Test converting None input"""
        dict_list = to_dict_list(None)
        assert len(dict_list) == 0
