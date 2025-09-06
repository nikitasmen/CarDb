import pytest
from PyQt5.QtWidgets import QApplication
from car_db import CarSearchWindow

@pytest.mark.qt
def test_search_car_ui(qtbot):
    app = QApplication([])  # Initialize the QApplication
    window = CarSearchWindow()
    qtbot.addWidget(window)  # Add the window to the qtbot for testing

    # Test the UI components
    assert len(window.search_results()) == 0  # Initial search results should be empty

    # Search for a specific car model
    window.search_field().setText("Toyota Corolla")
    qtbot.mouseClick(window.search_button(), Qt.LeftButton)

    # Verify the search results
    results = window.search_results()
    assert len(results) > 0
    assert "Toyota Corolla" in [result.text() for result in results]

    # Test the UI's ability to handle invalid input
    window.search_field().setText("Invalid search term")
    qtbot.mouseClick(window.search_button(), Qt.LeftButton)

    # Verify that an error message is displayed
    error_message = window.error_label().text()
    assert "Invalid search term" in error_message

    app.quit()
