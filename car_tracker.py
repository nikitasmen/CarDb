import os
import json
import csv

class CarTracker:
    def __init__(self):
        self.target = "car.json"
        if not os.path.exists(self.target):
            with open(self.target, 'w') as f:
                json.dump([], f)

    def addData(self, modelName, manufacturer, year, originCountry, category, modelManufact, more):
        carDetails = {
            "modelName": modelName,
            "manufacturer": manufacturer,
            "year": year,
            "originCountry": originCountry,
            "category": category,
            "modelManufact": modelManufact,
            "more": more
        }

        try:
            with open(self.target, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(carDetails)
        self.saveTarget(data)

    def saveTarget(self, data):
        with open(self.target, 'w') as f:
            json.dump(data, f, indent=4)

    def displayData(self):
        with open(self.target, 'r') as f:
            return json.load(f)

    def search(self, modelName):
        results = []
        with open(self.target, 'r') as f:
            for data in json.load(f):
                if modelName.lower() in data["modelName"].lower():
                    results.append(data)
        return results if results else None

    def deleteData(self, modelName):
        with open(self.target, 'r') as f:
            data = json.load(f)

        for car in data:
            if car["modelName"].lower() == modelName.lower():
                data.remove(car)
                self.saveTarget(data)
                return True
        return False

    def importData(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found.")
            return False
        
        try:
            with open(self.target, 'r') as f:
                current_data = json.load(f)
        except FileNotFoundError:
            current_data = []

        current_data.extend(data)

        with open(self.target, 'w') as f:
            json.dump(current_data, f, indent=4)

        
    def importDataCSV(self, filename):
        try:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        except FileNotFoundError:
            print("File not found.")
            return False

        try:
            with open(self.target, 'r') as f:
                current_data = json.load(f)
        except FileNotFoundError:
            current_data = []

        current_data.extend(data)

        with open(self.target, 'w') as f:
            json.dump(current_data, f, indent=4)
