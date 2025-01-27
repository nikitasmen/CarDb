import os
import json
import csv
import pandas as pd
import sys
from data import FileIO

class CarFileHandler:
    def __init__(self, target=None):
        if target is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Adjust the path to work in both development and packaged environments
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            target = os.path.join(base_dir, 'data/car.json')
        self.target = target
        if not os.path.exists(self.target):
            with open(self.target, 'w') as f:
                json.dump([], f)

    def saveTarget(self, data):
        data = self.cleanup(data)
        FileIO.write_json(self.target, data)

    def displayData(self):
        return FileIO.read_json(self.target)

    def cleanup(self, data):
        allowed_keys = ["model", "manufacturer", "year", "country_of_origin", "category", "replica_model", "info"]
        cleaned_data = []
        for car in data:
            car = {key: car[key] for key in car if key in allowed_keys}
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

        current_data = self.displayData()
        current_data.extend(data)
        self.saveTarget(current_data)
        print("Data imported successfully from JSON!")
        
        return True

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
        self.saveTarget(current_data)
        print("Data imported successfully from CSV!")
        return True


    def importDataExcel(self, filename):
        try:
            df = pd.read_excel(filename, engine='openpyxl')  
            df.dropna(how='all', inplace=True)
            
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            if df.columns[0].startswith("Unnamed"):
                df.columns = [f"Column_{i}" for i in range(len(df.columns))]  # Generic column names

            print(df.head())  # Check the cleaned dataframe
            data = df.to_dict(orient='records')
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return False

        current_data = self.displayData()
        current_data.extend(data)
        self.saveTarget(current_data)
        print("Data imported successfully from Excel!")
        return True
