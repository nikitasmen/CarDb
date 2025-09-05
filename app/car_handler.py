import os
import json
import csv
import pandas as pd
import sys
from .data import FileIO
from .models import (
    ALLOWED_KEYS,
    Car,
    to_car_list,
    to_dict_list,
)

class CarFileHandler:
    def __init__(self, target=None):
        if target is None:
            # Mobile-friendly path resolution
            if getattr(sys, 'frozen', False):
                # For packaged apps
                base_dir = sys._MEIPASS
            else:
                # For development
                base_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Ensure data directory exists
            data_dir = os.path.join(base_dir, 'data')
            os.makedirs(data_dir, exist_ok=True)
            target = os.path.join(data_dir, 'car.json')
            
        self.target = target
        # Initialize file if it doesn't exist
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the target file exists and is valid JSON"""
        try:
            if not os.path.exists(self.target):
                os.makedirs(os.path.dirname(self.target), exist_ok=True)
                with open(self.target, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            else:
                # Validate existing file
                with open(self.target, 'r', encoding='utf-8') as f:
                    json.load(f)
        except (json.JSONDecodeError, IOError):
            # Reset corrupted file
            with open(self.target, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def saveTarget(self, data):
        # Convert incoming records to Car objects (normalizes internally)
        cars = to_car_list(data or [])
        return FileIO.write_json(self.target, to_dict_list(cars))

    def displayData(self):
        return FileIO.read_json(self.target)

    def cleanup(self, data):
        cleaned_data = []
        for car in data:
            car = {key: car[key] for key in car if key in ALLOWED_KEYS}
            if car:
                cleaned_data.append(car)
        return cleaned_data
        
    def importDataJSON(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Invalid or missing JSON file.")
            return False

        if isinstance(data, dict):
            data = [data]

        current_data = self.displayData()
        current_data.extend(data)
        if self.saveTarget(current_data): 
            print("Data imported successfully from JSON!")
            return True
        return False

    def importDataCSV(self, filename):
        try:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        except FileNotFoundError:
            print("File not found.")
            return False
        except csv.Error:
            print("Error: Invalid CSV file.")
            return False

        current_data = self.displayData()
        current_data.extend(data)
        if self.saveTarget(current_data): 
            print("Data imported successfully from CSV!")
            return True
        return False

    def importDataExcel(self, filename):
        try:
            df = pd.read_excel(filename, engine='openpyxl')  
            df.dropna(how='all', inplace=True)
            
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            if df.columns[0].startswith("Unnamed"):
                df.columns = [f"Column_{i}" for i in range(len(df.columns))]  # Generic column names

            data = df.to_dict(orient='records')
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return False

        current_data = self.displayData()
        current_data.extend(data)
        if self.saveTarget(current_data):
            print("Data imported successfully from Excel!")
            return True
        return False
