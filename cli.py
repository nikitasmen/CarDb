from car_tracker import CarTracker
from tabulate import tabulate

class Cli: 
    def __init__(self):
        self.tracker = CarTracker()     
    
    def run(self): 
        while True:
            command = input("Enter command: ")
            if command == "exit":
                break
            self.process_command(command)

    def process_command(self, command): 
        command = command.strip().lower()
        if command == "--help":
            self.print_help()
        elif command == "add":
            self.add_car()
        elif command == "display":
            self.display_all_cars()
        elif command == "search":
            self.search_car()
        elif command == "delete":
            self.delete_car()
        elif command == "import": 
            self.import_data()
        else:
            print("Invalid command. Type '--help' to see the available commands.")

    def add_car(self):
        modelname = input("Enter model name: ")
        manufacturer = input("Enter manufacturer: ")
        year = input("Enter year: ")
        origincountry = input("Enter origin country: ")
        category = input("Enter category: ")
        modelmanufact = input("Enter model manufacturing details: ")
        more = input("Enter more info link: ")
        self.tracker.addData(modelname, manufacturer, year, origincountry, category, modelmanufact, more)
        print(f"Car '{modelname}' added successfully!")

    def import_data(self):
        filename = input("Enter filename to import data: ")
        filetype = input("Enter file type (json/csv): ").lower()
        if filetype == "json":
            self.tracker.importData(filename)
        elif filetype == "csv":
            self.tracker.importDataCSV(filename)
        else:
            print("Unsupported file type.")
        print("Data imported successfully!")
   
    def display_all_cars(self):
        cars = self.tracker.displayData()
        print("All cars:", len(cars), "found.", cars)
        if cars:
            print(tabulate(cars, headers="keys", tablefmt="grid"))
        else:
            print("No cars found.")

    def search_car(self):
        modelname = input("Enter model name to search: ")
        car = self.tracker.search(modelname)
        if car:
            print(tabulate(car, headers="keys", tablefmt="grid"))
        else:
            print("Car not found.")

    def delete_car(self):
        modelname = input("Enter model name to delete: ")
        self.tracker.deleteData(modelname)
        print(f"Car '{modelname}' deleted successfully!")

    def print_help(self):
        print("Available commands:")
        print("  add     - Add a new car")
        print("  display - Display all cars")
        print("  search  - Search for a car")
        print("  delete  - Delete a car")
        print("  exit    - Exit the program")
