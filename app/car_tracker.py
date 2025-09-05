from app import CarFileHandler
from .models import (
    normalize_car_record,
    validate_car_record,
    to_car_list,
    to_dict_list,
    Car,
)

class CarTracker:
    def __init__(self):
        try:
            self.fileHandler = CarFileHandler()
        except Exception as e:
            print(f"Error initializing CarTracker: {e}")
            # Try to reinitialize with a fallback path
            self.fileHandler = None

    def _ensure_handler(self):
        """Ensure file handler is available, reinitialize if needed"""
        if self.fileHandler is None:
            try:
                self.fileHandler = CarFileHandler()
            except Exception as e:
                print(f"Failed to reinitialize file handler: {e}")
                return False
        return True

    def _load_cars(self) -> list[Car]:
        data = self.fileHandler.displayData()
        return to_car_list(data)

    def _save_cars(self, cars: list[Car]) -> bool:
        return self.fileHandler.saveTarget(to_dict_list(cars))

    def addData(self, modelName, manufacturer, year, originCountry, category, modelManufact, more):
        if not self._ensure_handler():
            return False
            
        try:
            raw = {
                "model": modelName,
                "manufacturer": manufacturer,
                "year": year,
                "country_of_origin": originCountry,
                "category": category,
                "replica_model": modelManufact,
                "info": more,
            }
            carDetails = normalize_car_record(raw)
            ok, _ = validate_car_record(carDetails)
            if not ok:
                return False

            cars = self._load_cars()
            
            # Check for duplicate model names (case-insensitive)
            for existing_car in cars:
                if existing_car.model.lower() == carDetails["model"].lower():
                    print(f"Car with model '{carDetails['model']}' already exists")
                    return False
            
            # Append as object to keep internal consistency
            cars.append(Car.from_dict(carDetails))
            return self._save_cars(cars)
        except Exception as e:
            print(f"Error adding car data: {e}")
            return False
    
    def search(self, modelName):
        if not self._ensure_handler():
            return []
            
        try:
            results = []
            cars = self._load_cars()
            search_term = str(modelName).lower().strip()
            for car in cars:
                if search_term in car.model.lower():
                    d = car.to_dict()
                    if 'id' in d:
                        d.pop('id')
                    results.append(d)
            return results
        except Exception as e:
            print(f"Error searching cars: {e}")
            return []

    def deleteData(self, modelName):
        if not self._ensure_handler():
            return False
            
        try:
            cars = self._load_cars()
            model_to_delete = str(modelName).lower().strip()
            filtered_cars = [car for car in cars if car.model.lower() != model_to_delete]

            if len(filtered_cars) == len(cars):
                return False  # No car found to delete

            return self._save_cars(filtered_cars)
        except Exception as e:
            print(f"Error deleting car data: {e}")
            return False

    def importData(self, filename):
        if not self._ensure_handler():
            return False
            
        try:
            if filename.endswith('.json'):
                return self.fileHandler.importDataJSON(filename)
            elif filename.endswith('.csv'):
                return self.fileHandler.importDataCSV(filename)
            elif filename.endswith('.xlsx'):
                return self.fileHandler.importDataExcel(filename)
            else:
                print("Unsupported file type.")
                return False
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def displayData(self):
        if not self._ensure_handler():
            return []
            
        try:
            # Return dicts for UI compatibility but hide internal id
            public = []
            for c in self._load_cars():
                d = c.to_dict()
                if 'id' in d:
                    d.pop('id')
                public.append(d)
            return public
        except Exception as e:
            print(f"Error displaying data: {e}")
            return []
    