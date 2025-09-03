from app import CarFileHandler

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

    def addData(self, modelName, manufacturer, year, originCountry, category, modelManufact, more):
        if not self._ensure_handler():
            return False
            
        try:
            carDetails = {
                "model": str(modelName).strip(),
                "manufacturer": str(manufacturer).strip(),
                "year": str(year).strip(),
                "country_of_origin": str(originCountry).strip(),
                "category": str(category).strip(),
                "replica_model": str(modelManufact).strip(),
                "info": str(more).strip()
            }

            data = self.fileHandler.displayData()
            if data is None:
                data = []
            
            # Check for duplicate model names
            for existing_car in data:
                if existing_car.get("model", "").lower() == carDetails["model"].lower():
                    print(f"Car with model '{carDetails['model']}' already exists")
                    return False
            
            data.append(carDetails)
            return self.fileHandler.saveTarget(data)
        except Exception as e:
            print(f"Error adding car data: {e}")
            return False
    
    def search(self, modelName):
        if not self._ensure_handler():
            return []
            
        try:
            results = []
            data = self.fileHandler.displayData()
            if data is None:
                return []
                
            search_term = str(modelName).lower().strip()
            for car_data in data:
                if search_term in car_data.get("model", "").lower():
                    results.append(car_data)
            return results
        except Exception as e:
            print(f"Error searching cars: {e}")
            return []

    def deleteData(self, modelName):
        if not self._ensure_handler():
            return False
            
        try:
            data = self.fileHandler.displayData()
            if data is None:
                return False
                
            model_to_delete = str(modelName).lower().strip()
            filtered_data = [car for car in data if car.get("model", "").lower() != model_to_delete]

            if len(filtered_data) == len(data):
                return False  # No car found to delete

            return self.fileHandler.saveTarget(filtered_data)
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
            data = self.fileHandler.displayData()
            return data if data is not None else []
        except Exception as e:
            print(f"Error displaying data: {e}")
            return []
    