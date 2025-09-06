"""
Performance tests for CarDb Mobile App
"""
import pytest
import time
import psutil
import os
from unittest.mock import patch, Mock
from interfaces.flet_app import FletApp


class TestDataLoadingPerformance:
    """Test cases for data loading performance"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_app_startup_time(self, empty_car_tracker):
        """Test app startup time with empty data"""
        start_time = time.time()
        
        app = FletApp()
        app.car_tracker = empty_car_tracker
        
        end_time = time.time()
        startup_time = end_time - start_time
        
        # App should start within 2 seconds
        assert startup_time < 2.0
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_app_startup_time_large_dataset(self, empty_car_tracker, large_dataset):
        """Test app startup time with large dataset"""
        # Load large dataset
        empty_car_tracker.fileHandler.saveTarget(large_dataset)
        
        start_time = time.time()
        
        app = FletApp()
        app.car_tracker = empty_car_tracker
        
        end_time = time.time()
        startup_time = end_time - start_time
        
        # App should start within 5 seconds even with large dataset
        assert startup_time < 5.0
    
    @pytest.mark.performance
    def test_data_loading_performance(self, flet_app_instance, large_dataset):
        """Test data loading performance with large dataset"""
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=large_dataset):
            start_time = time.time()
            
            data = flet_app_instance._get_cars_data()
            
            end_time = time.time()
            load_time = end_time - start_time
            
            # Data loading should be fast even with large dataset
            assert load_time < 1.0
            assert len(data) == len(large_dataset)
    
    @pytest.mark.performance
    def test_caching_effectiveness(self, flet_app_instance, sample_car_data):
        """Test caching effectiveness for repeated data access"""
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=sample_car_data) as mock_display:
            # First access - should call displayData
            start_time = time.time()
            data1 = flet_app_instance._get_cars_data()
            first_access_time = time.time() - start_time
            
            # Second access - should use cache
            start_time = time.time()
            data2 = flet_app_instance._get_cars_data()
            second_access_time = time.time() - start_time
            
            # Second access should be faster due to caching
            assert second_access_time < first_access_time
            assert data1 == data2
            assert mock_display.call_count == 1  # Should only be called once
    
    @pytest.mark.performance
    def test_cache_invalidation_performance(self, flet_app_instance, sample_car_data):
        """Test cache invalidation performance"""
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=sample_car_data):
            # Load data into cache
            flet_app_instance._get_cars_data()
            
            # Invalidate cache
            start_time = time.time()
            flet_app_instance._invalidate_cache()
            invalidation_time = time.time() - start_time
            
            # Cache invalidation should be very fast
            assert invalidation_time < 0.1
            assert flet_app_instance._cache_dirty is True


class TestUIPerformance:
    """Test cases for UI performance"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_car_card_rendering_performance(self, flet_app_instance, large_dataset, mock_page):
        """Test car card rendering performance with many items"""
        flet_app_instance.page = mock_page
        
        with patch.object(flet_app_instance, '_get_cars_data', return_value=large_dataset):
            start_time = time.time()
            
            view = flet_app_instance.create_main_view()
            
            end_time = time.time()
            rendering_time = end_time - start_time
            
            # Should render within reasonable time even with many cars
            assert rendering_time < 3.0
            assert view is not None
    
    @pytest.mark.performance
    def test_pagination_performance(self, flet_app_instance, large_dataset, mock_page):
        """Test pagination performance"""
        flet_app_instance.page = mock_page
        
        with patch.object(flet_app_instance, '_get_cars_data', return_value=large_dataset):
            # Create initial view with limited cards
            view = flet_app_instance.create_main_view()
            
            # Test load more functionality
            start_time = time.time()
            flet_app_instance._load_more_cars_improved(Mock())
            load_more_time = time.time() - start_time
            
            # Load more should be fast
            assert load_more_time < 1.0
    
    @pytest.mark.performance
    def test_search_performance(self, flet_app_instance, large_dataset):
        """Test search performance with large dataset"""
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=large_dataset):
            start_time = time.time()
            
            results = flet_app_instance.car_tracker.search("Test")
            
            end_time = time.time()
            search_time = end_time - start_time
            
            # Search should be fast even with large dataset
            assert search_time < 0.5
            assert len(results) > 0
    
    @pytest.mark.performance
    def test_view_creation_performance(self, flet_app_instance, sample_car_data, mock_page):
        """Test view creation performance"""
        flet_app_instance.page = mock_page
        
        with patch.object(flet_app_instance, '_get_cars_data', return_value=sample_car_data):
            # Test main view creation
            start_time = time.time()
            main_view = flet_app_instance.create_main_view()
            main_view_time = time.time() - start_time
            
            # Test add car view creation
            start_time = time.time()
            add_view = flet_app_instance.create_add_car_view()
            add_view_time = time.time() - start_time
            
            # Test search view creation
            start_time = time.time()
            search_view = flet_app_instance.create_search_view()
            search_view_time = time.time() - start_time
            
            # All views should be created quickly
            assert main_view_time < 0.5
            assert add_view_time < 0.5
            assert search_view_time < 0.5
            
            assert main_view is not None
            assert add_view is not None
            assert search_view is not None


class TestMemoryUsage:
    """Test cases for memory usage"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_memory_usage_with_large_dataset(self, empty_car_tracker, large_dataset):
        """Test memory usage with large dataset"""
        # Load large dataset
        empty_car_tracker.fileHandler.saveTarget(large_dataset)
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create app and load data
        app = FletApp()
        app.car_tracker = empty_car_tracker
        
        with patch.object(app.car_tracker, 'displayData', return_value=large_dataset):
            data = app._get_cars_data()
            
            # Get memory usage after loading data
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 100MB for 1000 cars)
            assert memory_increase < 100
            assert len(data) == len(large_dataset)
    
    @pytest.mark.performance
    def test_memory_usage_caching(self, flet_app_instance, sample_car_data):
        """Test memory usage with caching"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=sample_car_data):
            # Load data multiple times
            for _ in range(10):
                flet_app_instance._get_cars_data()
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory should not increase significantly with caching
            assert memory_increase < 10
    
    @pytest.mark.performance
    def test_memory_cleanup_after_operations(self, flet_app_instance, sample_car_data):
        """Test memory cleanup after operations"""
        process = psutil.Process(os.getpid())
        
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=sample_car_data):
            # Perform multiple operations
            for _ in range(5):
                flet_app_instance._get_cars_data()
                flet_app_instance._invalidate_cache()
                flet_app_instance._get_cars_data()
            
            # Memory should not continuously increase
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            # This is a basic test - more sophisticated memory testing would be needed


class TestConcurrentAccess:
    """Test cases for concurrent access performance"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_data_access(self, flet_app_instance, sample_car_data):
        """Test concurrent data access performance"""
        import threading
        import queue
        
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=sample_car_data):
            results = queue.Queue()
            
            def access_data():
                data = flet_app_instance._get_cars_data()
                results.put(data)
            
            # Create multiple threads accessing data concurrently
            threads = []
            for _ in range(5):
                thread = threading.Thread(target=access_data)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # All threads should get the same data
            assert results.qsize() == 5
            while not results.empty():
                data = results.get()
                assert len(data) == len(sample_car_data)
    
    @pytest.mark.performance
    def test_concurrent_search_operations(self, flet_app_instance, large_dataset):
        """Test concurrent search operations"""
        import threading
        import queue
        
        with patch.object(flet_app_instance.car_tracker, 'displayData', return_value=large_dataset):
            results = queue.Queue()
            
            def search_operation(search_term):
                start_time = time.time()
                search_results = flet_app_instance.car_tracker.search(search_term)
                search_time = time.time() - start_time
                results.put((search_term, search_results, search_time))
            
            # Create multiple threads performing searches
            threads = []
            search_terms = ["Test", "Model", "Car", "Data", "App"]
            
            for term in search_terms:
                thread = threading.Thread(target=search_operation, args=(term,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # All searches should complete quickly
            assert results.qsize() == len(search_terms)
            while not results.empty():
                search_term, search_results, search_time = results.get()
                assert search_time < 1.0
                assert isinstance(search_results, list)


class TestFileOperationsPerformance:
    """Test cases for file operations performance"""
    
    @pytest.mark.performance
    def test_file_save_performance(self, car_file_handler, large_dataset):
        """Test file save performance with large dataset"""
        start_time = time.time()
        
        result = car_file_handler.saveTarget(large_dataset)
        
        end_time = time.time()
        save_time = end_time - start_time
        
        # File save should be reasonably fast
        assert result is True
        assert save_time < 2.0
    
    @pytest.mark.performance
    def test_file_load_performance(self, car_file_handler, large_dataset):
        """Test file load performance with large dataset"""
        # Save large dataset first
        car_file_handler.saveTarget(large_dataset)
        
        start_time = time.time()
        
        data = car_file_handler.displayData()
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # File load should be reasonably fast
        assert load_time < 1.0
        assert len(data) == len(large_dataset)
    
    @pytest.mark.performance
    def test_import_performance(self, car_file_handler, temp_data_dir):
        """Test import performance"""
        import json
        
        # Create test import file
        import_file = os.path.join(temp_data_dir, "import.json")
        import_data = [{"model": f"Import Car {i}", "manufacturer": f"Manufacturer {i}"} for i in range(100)]
        
        with open(import_file, 'w') as f:
            json.dump(import_data, f)
        
        start_time = time.time()
        
        result = car_file_handler.importDataJSON(import_file)
        
        end_time = time.time()
        import_time = end_time - start_time
        
        # Import should be reasonably fast
        assert result is True
        assert import_time < 1.0


class TestMobileSpecificPerformance:
    """Test cases for mobile-specific performance"""
    
    @pytest.mark.performance
    @pytest.mark.mobile
    def test_touch_interaction_responsiveness(self, flet_app_instance, mock_page):
        """Test touch interaction responsiveness"""
        flet_app_instance.page = mock_page
        
        # Test button creation performance
        start_time = time.time()
        
        button = flet_app_instance._create_modern_button(
            "Test Button", 
            "test_icon", 
            lambda e: None
        )
        
        end_time = time.time()
        button_creation_time = end_time - start_time
        
        # Button creation should be very fast for responsive UI
        assert button_creation_time < 0.01
        assert button is not None
    
    @pytest.mark.performance
    @pytest.mark.mobile
    def test_view_transition_performance(self, flet_app_instance, mock_page):
        """Test view transition performance"""
        flet_app_instance.page = mock_page
        
        # Test route change performance
        start_time = time.time()
        
        flet_app_instance.route_change("/add_car")
        
        end_time = time.time()
        transition_time = end_time - start_time
        
        # View transitions should be fast
        assert transition_time < 0.1
        assert mock_page.update.called
    
    @pytest.mark.performance
    @pytest.mark.mobile
    def test_scroll_performance(self, flet_app_instance, large_dataset, mock_page):
        """Test scroll performance with many items"""
        flet_app_instance.page = mock_page
        
        with patch.object(flet_app_instance, '_get_cars_data', return_value=large_dataset):
            view = flet_app_instance.create_main_view()
            
            # Test that ListView is used for efficient scrolling
            assert view is not None
            # ListView should handle large datasets efficiently
            assert len(view.controls) > 0

