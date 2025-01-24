import click
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
        else:
            print("Invalid command. Type '--help' to see the available commands.")


    def add_car(self, modelname, manufacturer, year, origincountry, category, modelmanufact, more):
        """Add a new car to the database"""
        self.tracker.addData(modelname, manufacturer, year, origincountry, category, modelmanufact, more)
        click.echo(f"Car '{modelname}' added successfully!")

    def display_all_cars(self):
        """Display all cars in the database"""
        cars = self.tracker.displayData()
        if cars:
            print(tabulate(cars, headers="keys", tablefmt="grid"))
        else:
            click.echo("No cars found.")

    def search_car(self, modelname):
        """Search for a car in the database"""
        car = self.tracker.search(modelname)
        if car:
            print(tabulate([car], headers="keys", tablefmt="grid"))
        else:
            click.echo("Car not found.")

    def delete_car(self, modelname):
        """Delete a car from the database"""
        self.tracker.deleteData(modelname)
        click.echo(f"Car '{modelname}' deleted successfully!")


@click.group()
def cli():
    """Car Tracker CLI Application"""
    pass

@click.command()
@click.option('--modelName', prompt="Model Name", help="The model of the car")
@click.option('--manufacturer', prompt="Manufacturer", help="The car's manufacturer")
@click.option('--year', prompt="Year", help="Year of manufacture")
@click.option('--originCountry', prompt="Origin Country", help="Country of origin")
@click.option('--category', prompt="Category", help="Car category")
@click.option('--modelManufact', prompt="Model Manufacturer", help="Model manufacturing details")
@click.option('--more', prompt="More Info (URL)", help="Additional info link")
def add(modelname, manufacturer, year, origincountry, category, modelmanufact, more):
    """Add a new car"""
    cli_instance.add_car(modelname, manufacturer, year, origincountry, category, modelmanufact, more)

@click.command()
def display():
    """Display all cars"""
    cli_instance.display_all_cars()

@click.command()
@click.option('--modelName', prompt="Enter Model Name", help="Model to search")
def search(modelname):
    """Search for a car"""
    cli_instance.search_car(modelname)

@click.command()
@click.option('--modelName', prompt="Enter Model Name", help="Model to delete")
def delete(modelname):
    """Delete a car"""
    cli_instance.delete_car(modelname)

# Create an instance of the Cli class
cli_instance = Cli()

# Add commands to the CLI group
cli.add_command(add)
cli.add_command(display)
cli.add_command(search)
cli.add_command(delete)

