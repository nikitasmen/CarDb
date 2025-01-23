import os
import json

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
        with open(self.target, 'r') as f:
            for data in json.load(f):
                if data["modelName"].lower() == modelName.lower():
                    return data
        return None

    def deleteData(self, modelName):
        with open(self.target, 'r') as f:
            data = json.load(f)

        for car in data:
            if car["modelName"].lower() == modelName.lower():
                data.remove(car)
                self.saveTarget(data)
                return True
        return False
