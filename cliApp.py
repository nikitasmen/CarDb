import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import flask as fl 

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


class CarTrackerApp:
    def __init__(self, root):
        self.car_tracker = CarTracker()

        # Main window setup
        self.root = root
        self.root.title("Car Tracker Application")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Create UI components
        self._create_widgets()

    def _create_widgets(self):
        # Input fields
        fields = [
            ("Model Name", "modelName"),
            ("Manufacturer", "manufacturer"),
            ("Year", "year"),
            ("Origin Country", "originCountry"),
            ("Category", "category"),
            ("Model Manufacturer", "modelManufact"),
            ("More Info (URL)", "more"),
        ]
        self.entries = {}

        for idx, (label_text, field_name) in enumerate(fields):
            label = tk.Label(self.root, text=label_text, font=("Arial", 10))
            label.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)

            entry = tk.Entry(self.root, width=50)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[field_name] = entry

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        add_button = tk.Button(button_frame, text="Add Car", width=15, command=self.add_car)
        add_button.pack(side=tk.LEFT, padx=5)

        display_button = tk.Button(button_frame, text="Display All Cars", width=15, command=self.display_all)
        display_button.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(button_frame, text="Search Car", width=15, command=self.search_car)
        search_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Car", width=15, command=self.delete_car)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Table for displaying data
        self.tree = ttk.Treeview(self.root, columns=("model", "manufacturer", "year", "origin", "category", "manufact", "more"), show="headings", height=10)
        self.tree.grid(row=len(fields) + 1, column=0, columnspan=2, padx=10, pady=10)

        # Define table headings
        self.tree.heading("model", text="Model Name")
        self.tree.heading("manufacturer", text="Manufacturer")
        self.tree.heading("year", text="Year")
        self.tree.heading("origin", text="Origin Country")
        self.tree.heading("category", text="Category")
        self.tree.heading("manufact", text="Model Manufacturer")
        self.tree.heading("more", text="More Info (URL)")

        # Adjust column width
        for col in ("model", "manufacturer", "year", "origin", "category", "manufact", "more"):
            self.tree.column(col, width=120, anchor=tk.CENTER)

        # Bind double-click to open URL
        self.tree.bind("<Double-1>", self.on_double_click)

    def add_car(self):
        car_details = {field: entry.get() for field, entry in self.entries.items()}

        if all(car_details.values()):
            self.car_tracker.addData(**car_details)
            messagebox.showinfo("Success", "Car added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def display_all(self):
        # Clear the table first
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch data and populate the table
        cars = self.car_tracker.displayData()
        if cars:
            for car in cars:
                self.tree.insert("", tk.END, values=(
                    car["modelName"],
                    car["manufacturer"],
                    car["year"],
                    car["originCountry"],
                    car["category"],
                    car["modelManufact"],
                    car["more"]
                ))
        else:
            messagebox.showinfo("No Data", "No cars to display.")

    def on_double_click(self, event):
        """Handle double-click event to open the URL in the browser."""
        item = self.tree.identify('item', event.x, event.y)
        if item:
            selected_values = self.tree.item(item, "values")
            url = selected_values[-1]  # The "more" column contains the URL
            if url.startswith("http://") or url.startswith("https://"):
                webbrowser.open(url)
            else:
                messagebox.showerror("Invalid URL", "The selected 'More Info' value is not a valid URL.")

    def search_car(self):
        modelName = simpledialog.askstring("Search Car", "Enter the model name:")
        if modelName:
            car = self.car_tracker.search(modelName)
            if car:
                messagebox.showinfo("Car Found", json.dumps(car, indent=4))
            else:
                messagebox.showinfo("Not Found", "Car not found.")

    def delete_car(self):
        modelName = simpledialog.askstring("Delete Car", "Enter the model name to delete:")
        if modelName:
            if self.car_tracker.deleteData(modelName):
                messagebox.showinfo("Success", "Car deleted successfully!")
                self.display_all()  # Refresh the table
            else:
                messagebox.showinfo("Not Found", "Car not found.")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarTrackerApp(root)
    root.mainloop()
