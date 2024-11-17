from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)
TARGET_FILE = "car.json"

# Ensure the car.json file exists
if not os.path.exists(TARGET_FILE):
    with open(TARGET_FILE, 'w') as f:
        json.dump([], f)

class CarTracker:
    def __init__(self):
        self.target = TARGET_FILE

    def add_data(self, modelName, manufacturer, year, originCountry, category, modelManufact, more):
        car_details = {
            "modelName": modelName,
            "manufacturer": manufacturer,
            "year": year,
            "originCountry": originCountry,
            "category": category,
            "modelManufact": modelManufact,
            "more": more
        }
        with open(self.target, 'r') as f:
            data = json.load(f)
        data.append(car_details)
        self.save_data(data)

    def save_data(self, data):
        with open(self.target, 'w') as f:
            json.dump(data, f, indent=4)

    def get_all_cars(self):
        with open(self.target, 'r') as f:
            return json.load(f)

    def search_car(self, modelName):
        with open(self.target, 'r') as f:
            cars = json.load(f)
            for car in cars:
                if car["modelName"].lower() == modelName.lower():
                    return car
        return None

    def delete_car(self, modelName):
        with open(self.target, 'r') as f:
            data = json.load(f)

        for car in data:
            if car["modelName"].lower() == modelName.lower():
                data.remove(car)
                self.save_data(data)
                return True
        return False

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/add_car', methods=['POST'])
def add_car():
    car_details = request.form.to_dict()
    car_tracker = CarTracker()
    car_tracker.add_data(**car_details)
    return redirect(url_for('index'))

@app.route('/display_cars')
def display_cars():
    car_tracker = CarTracker()
    cars = car_tracker.get_all_cars()
    return jsonify(cars)

@app.route('/search_car', methods=['POST'])
def search_car():
    model_name = request.form.get('modelName')
    car_tracker = CarTracker()
    car = car_tracker.search_car(model_name)
    if car:
        return jsonify(car)
    else:
        return jsonify({"message": "Car not found"}), 404

@app.route('/delete_car', methods=['POST'])
def delete_car():
    model_name = request.form.get('modelName')
    car_tracker = CarTracker()
    success = car_tracker.delete_car(model_name)
    if success:
        return jsonify({"message": "Car deleted successfully!"})
    else:
        return jsonify({"message": "Car not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
