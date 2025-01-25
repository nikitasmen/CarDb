from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, 
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QFileDialog
)
import sys
from car_tracker import CarTracker
import webbrowser

class CarTrackerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.car_tracker = CarTracker()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Car Tracker Application")
        self.setGeometry(100, 100, 800, 500)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs = {}
        fields = [
            ("Model Name", "modelName"),
            ("Manufacturer", "manufacturer"),
            ("Year", "year"),
            ("Origin Country", "originCountry"),
            ("Category", "category"),
            ("Model Manufacturer", "modelManufact"),
            ("More Info (URL)", "more"),
        ]

        for label, key in fields:
            entry = QLineEdit(self)
            form_layout.addRow(label, entry)
            self.inputs[key] = entry

        layout.addLayout(form_layout)

        self.add_button = QPushButton("Add Car")
        self.add_button.clicked.connect(self.add_car)
        layout.addWidget(self.add_button)

        self.display_button = QPushButton("Display All Cars")
        self.display_button.clicked.connect(self.display_all)
        layout.addWidget(self.display_button)
        self.search_button = QPushButton("Search Car")
        self.search_button.clicked.connect(self.search_car)
        layout.addWidget(self.search_button)

        self.delete_button = QPushButton("Delete Car")
        self.delete_button.clicked.connect(self.delete_car)
        layout.addWidget(self.delete_button)

        self.import_button = QPushButton("Import Data") 
        self.import_button.clicked.connect(self.import_data)
        layout.addWidget(self.import_button)
        
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Model Name", "Manufacturer", "Year", 
            "Origin Country", "Category", "Model Manufacturer", "More Info"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellDoubleClicked.connect(self.open_url)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_car(self):
        car_details = {key: entry.text() for key, entry in self.inputs.items()}

        if all(car_details.values()):
            self.car_tracker.addData(**car_details)
            QMessageBox.information(self, "Success", "Car added successfully!")
            self.clear_entries()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def display_all(self):
        self.table.setRowCount(0)
        cars = self.car_tracker.displayData()
        
        if cars:
            for row_idx, car in enumerate(cars):
                self.table.insertRow(row_idx)
                for col_idx, key in enumerate(car.values()):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(key)))
        else:
            QMessageBox.information(self, "No Data", "No cars to display.")

    def search_car(self):
        model_name, ok = QInputDialog.getText(self, "Search Car", "Enter the model name:")
        if ok and model_name:
            cars = self.car_tracker.search(model_name)
            if cars:
                car_details = "\n\n".join(
                    f"Model Name: {car['modelName']}\n"
                    f"Manufacturer: {car['manufacturer']}\n"
                    f"Year: {car['year']}\n"
                    f"Origin Country: {car['originCountry']}\n"
                    f"Category: {car['category']}\n"
                    f"Model Manufacturing Details: {car['modelManufact']}\n"
                    f"More Info: {car['more']}"
                    for car in cars
                )
                QMessageBox.information(self, "Car Found", car_details)
            else:
                QMessageBox.warning(self, "Not Found", "Car not found.")

    def delete_car(self):
        model_name, ok = QInputDialog.getText(self, "Delete Car", "Enter the model name:")
        if ok and model_name:
            if self.car_tracker.deleteData(model_name):
                QMessageBox.information(self, "Success", "Car deleted successfully!")
                self.display_all()
            else:
                QMessageBox.warning(self, "Not Found", "Car not found.")

    def open_url(self, row, col):
        url = self.table.item(row, 6).text()
        if url.startswith("http://") or url.startswith("https://"):
            webbrowser.open(url)
        else:
            QMessageBox.critical(self, "Invalid URL", "The selected URL is not valid.")

    def clear_entries(self):
        for entry in self.inputs.values():
            entry.clear()

    def import_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filename, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json);;CSV Files(*.csv);;All Files (*)", options=options)
        if filename:
            if filename.endswith('.json'):
                self.car_tracker.importData(filename)
                QMessageBox.information(self, "Success", "JSON data imported successfully!")
            elif filename.endswith('.csv'):
                self.car_tracker.importDataCSV(filename)
                QMessageBox.information(self, "Success", "CSV data imported successfully!")
            else:
                QMessageBox.warning(self, "Unsupported File", "The selected file type is not supported.")
            self.display_all()