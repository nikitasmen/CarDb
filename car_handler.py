import os 
import json 
import csv 
import pandas as pd 

class CarFileHandler:
    def __init__(self, target="car.json"):
        self.target = target
        if not os.path.exists(self.target):
            with open(self.target, 'w') as f:
                json.dump([], f)

    def saveTarget(self, data):
        data = self.cleanup(data)
        with open(self.target, 'w') as f:
            json.dump(data, f, indent=4)

    def displayData(self):
        with open(self.target, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def cleanup(self, data):
        allowed_keys = ["modelName", "manufacturer", "year", "originCountry", "category", "modelManufact", "more"]
        for car in data:
            for key in list(car.keys()):
                if key not in allowed_keys:
                    del car[key]
         
        return data
        
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

    