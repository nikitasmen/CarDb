"""
Unit tests for file handler operations
"""
import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from app.car_handler import CarFileHandler


class TestCarFileHandler:
    """Test cases for CarFileHandler class"""
    
    @pytest.mark.unit
    def test_init_with_custom_target(self, temp_data_dir):
        """Test initializing with custom target file"""
        target_file = os.path.join(temp_data_dir, "custom_cars.json")
        handler = CarFileHandler(target=target_file)
        
        assert handler.target == target_file
        assert os.path.exists(target_file)
    
    @pytest.mark.unit
    def test_init_with_default_target(self):
        """Test initializing with default target file"""
        with patch('app.car_handler.os.path.dirname') as mock_dirname, \
             patch('app.car_handler.os.makedirs') as mock_makedirs, \
             patch('builtins.open', mock_open()) as mock_file:
            
            mock_dirname.return_value = "/test/path"
            handler = CarFileHandler()
            
            assert handler.target.endswith("car.json")
            mock_makedirs.assert_called_once()
    
    @pytest.mark.unit
    def test_ensure_file_exists_creates_new_file(self, temp_data_dir):
        """Test creating new file when it doesn't exist"""
        target_file = os.path.join(temp_data_dir, "new_file.json")
        handler = CarFileHandler(target=target_file)
        
        assert os.path.exists(target_file)
        
        with open(target_file, 'r') as f:
            data = json.load(f)
        assert data == []
    
    @pytest.mark.unit
    def test_ensure_file_exists_validates_existing_file(self, temp_data_dir):
        """Test validating existing valid JSON file"""
        target_file = os.path.join(temp_data_dir, "existing_file.json")
        
        # Create a valid JSON file
        with open(target_file, 'w') as f:
            json.dump([{"test": "data"}], f)
        
        handler = CarFileHandler(target=target_file)
        
        assert os.path.exists(target_file)
        with open(target_file, 'r') as f:
            data = json.load(f)
        assert data == [{"test": "data"}]
    
    @pytest.mark.unit
    def test_ensure_file_exists_recovers_corrupted_file(self, temp_data_dir):
        """Test recovering from corrupted JSON file"""
        target_file = os.path.join(temp_data_dir, "corrupted_file.json")
        
        # Create a corrupted JSON file
        with open(target_file, 'w') as f:
            f.write("invalid json content")
        
        handler = CarFileHandler(target=target_file)
        
        assert os.path.exists(target_file)
        with open(target_file, 'r') as f:
            data = json.load(f)
        assert data == []
    
    @pytest.mark.unit
    def test_save_target_valid_data(self, car_file_handler, sample_car_data):
        """Test saving valid car data"""
        result = car_file_handler.saveTarget(sample_car_data)
        
        assert result is True
        
        # Verify data was saved
        saved_data = car_file_handler.displayData()
        assert len(saved_data) == len(sample_car_data)
        assert saved_data[0]["model"] == sample_car_data[0]["model"]
    
    @pytest.mark.unit
    def test_save_target_empty_data(self, car_file_handler):
        """Test saving empty data"""
        result = car_file_handler.saveTarget([])
        
        assert result is True
        
        saved_data = car_file_handler.displayData()
        assert saved_data == []
    
    @pytest.mark.unit
    def test_save_target_none_data(self, car_file_handler):
        """Test saving None data"""
        result = car_file_handler.saveTarget(None)
        
        assert result is True
        
        saved_data = car_file_handler.displayData()
        assert saved_data == []
    
    @pytest.mark.unit
    def test_display_data_returns_saved_data(self, car_file_handler, sample_car_data):
        """Test displaying saved data"""
        car_file_handler.saveTarget(sample_car_data)
        displayed_data = car_file_handler.displayData()
        
        assert displayed_data == sample_car_data
    
    @pytest.mark.unit
    def test_display_data_empty_file(self, car_file_handler):
        """Test displaying data from empty file"""
        displayed_data = car_file_handler.displayData()
        
        assert displayed_data == []
    
    @pytest.mark.unit
    def test_cleanup_removes_invalid_keys(self, car_file_handler):
        """Test cleanup removes invalid keys"""
        dirty_data = [
            {
                "model": "Test Car",
                "manufacturer": "Test Manufacturer",
                "invalid_key": "should be removed",
                "another_invalid": "also removed"
            },
            {
                "model": "Another Car",
                "valid_key": "should be kept"
            }
        ]
        
        cleaned_data = car_file_handler.cleanup(dirty_data)
        
        assert len(cleaned_data) == 2
        assert "invalid_key" not in cleaned_data[0]
        assert "another_invalid" not in cleaned_data[0]
        assert "model" in cleaned_data[0]
        assert "manufacturer" in cleaned_data[0]
        assert "valid_key" not in cleaned_data[1]  # Not in ALLOWED_KEYS


class TestImportOperations:
    """Test cases for import operations"""
    
    @pytest.mark.unit
    def test_import_data_json_valid_file(self, car_file_handler, temp_data_dir):
        """Test importing valid JSON file"""
        json_file = os.path.join(temp_data_dir, "import.json")
        import_data = [{"model": "Imported Car", "manufacturer": "Imported Manufacturer"}]
        
        with open(json_file, 'w') as f:
            json.dump(import_data, f)
        
        result = car_file_handler.importDataJSON(json_file)
        
        assert result is True
        
        # Verify data was imported
        all_data = car_file_handler.displayData()
        assert len(all_data) == 1
        assert all_data[0]["model"] == "Imported Car"
    
    @pytest.mark.unit
    def test_import_data_json_single_object(self, car_file_handler, temp_data_dir):
        """Test importing JSON file with single object"""
        json_file = os.path.join(temp_data_dir, "single.json")
        import_data = {"model": "Single Car", "manufacturer": "Single Manufacturer"}
        
        with open(json_file, 'w') as f:
            json.dump(import_data, f)
        
        result = car_file_handler.importDataJSON(json_file)
        
        assert result is True
        
        all_data = car_file_handler.displayData()
        assert len(all_data) == 1
        assert all_data[0]["model"] == "Single Car"
    
    @pytest.mark.unit
    def test_import_data_json_invalid_file(self, car_file_handler, temp_data_dir):
        """Test importing invalid JSON file"""
        json_file = os.path.join(temp_data_dir, "invalid.json")
        
        with open(json_file, 'w') as f:
            f.write("invalid json content")
        
        result = car_file_handler.importDataJSON(json_file)
        
        assert result is False
    
    @pytest.mark.unit
    def test_import_data_json_missing_file(self, car_file_handler):
        """Test importing non-existent JSON file"""
        result = car_file_handler.importDataJSON("nonexistent.json")
        
        assert result is False
    
    @pytest.mark.unit
    def test_import_data_csv_valid_file(self, car_file_handler, temp_data_dir):
        """Test importing valid CSV file"""
        csv_file = os.path.join(temp_data_dir, "import.csv")
        csv_content = "model,manufacturer,year\nTest Car,Test Manufacturer,2020\nAnother Car,Another Manufacturer,2021"
        
        with open(csv_file, 'w') as f:
            f.write(csv_content)
        
        result = car_file_handler.importDataCSV(csv_file)
        
        assert result is True
        
        all_data = car_file_handler.displayData()
        assert len(all_data) == 2
        assert all_data[0]["model"] == "Test Car"
        assert all_data[1]["model"] == "Another Car"
    
    @pytest.mark.unit
    def test_import_data_csv_missing_file(self, car_file_handler):
        """Test importing non-existent CSV file"""
        result = car_file_handler.importDataCSV("nonexistent.csv")
        
        assert result is False
    
    @pytest.mark.unit
    def test_import_data_csv_invalid_file(self, car_file_handler, temp_data_dir):
        """Test importing invalid CSV file"""
        csv_file = os.path.join(temp_data_dir, "invalid.csv")
        
        with open(csv_file, 'w') as f:
            f.write("invalid,csv,content\nwith,malformed,structure")
        
        result = car_file_handler.importDataCSV(csv_file)
        
        assert result is False
    
    @pytest.mark.unit
    @patch('app.car_handler.pd.read_excel')
    def test_import_data_excel_valid_file(self, mock_read_excel, car_file_handler, temp_data_dir):
        """Test importing valid Excel file"""
        excel_file = os.path.join(temp_data_dir, "import.xlsx")
        
        # Mock pandas DataFrame
        mock_df = mock_read_excel.return_value
        mock_df.columns = ['model', 'manufacturer', 'year']
        mock_df.to_dict.return_value = [
            {'model': 'Excel Car', 'manufacturer': 'Excel Manufacturer', 'year': 2020}
        ]
        mock_df.dropna.return_value = mock_df
        
        result = car_file_handler.importDataExcel(excel_file)
        
        assert result is True
        mock_read_excel.assert_called_once_with(excel_file, engine='openpyxl')
    
    @pytest.mark.unit
    @patch('app.car_handler.pd.read_excel')
    def test_import_data_excel_missing_file(self, mock_read_excel, car_file_handler):
        """Test importing non-existent Excel file"""
        mock_read_excel.side_effect = FileNotFoundError()
        
        result = car_file_handler.importDataExcel("nonexistent.xlsx")
        
        assert result is False
    
    @pytest.mark.unit
    @patch('app.car_handler.pd.read_excel')
    def test_import_data_excel_invalid_file(self, mock_read_excel, car_file_handler, temp_data_dir):
        """Test importing invalid Excel file"""
        excel_file = os.path.join(temp_data_dir, "invalid.xlsx")
        mock_read_excel.side_effect = Exception("Invalid Excel file")
        
        result = car_file_handler.importDataExcel(excel_file)
        
        assert result is False


class TestFileHandlerErrorHandling:
    """Test cases for error handling in file operations"""
    
    @pytest.mark.unit
    def test_save_target_file_write_error(self, car_file_handler, sample_car_data):
        """Test handling file write errors"""
        with patch('builtins.open', side_effect=IOError("Write error")):
            result = car_file_handler.saveTarget(sample_car_data)
            assert result is False
    
    @pytest.mark.unit
    def test_display_data_file_read_error(self, car_file_handler):
        """Test handling file read errors"""
        with patch('builtins.open', side_effect=IOError("Read error")):
            result = car_file_handler.displayData()
            assert result == []
    
    @pytest.mark.unit
    def test_ensure_file_exists_io_error(self, temp_data_dir):
        """Test handling IO errors during file creation"""
        with patch('builtins.open', side_effect=IOError("IO error")):
            target_file = os.path.join(temp_data_dir, "error_file.json")
            handler = CarFileHandler(target=target_file)
            
            # Should not raise exception, should handle gracefully
            assert handler.target == target_file
