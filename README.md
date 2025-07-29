# CarDb

A CRUD application for managing your miniature car collection. Track details about model cars, search through your collection, and maintain a comprehensive database of your prized miniatures.

![CarDb Logo](https://via.placeholder.com/150)

## Features

- Add, view, update, and delete car entries
- Search functionality to find specific cars by model name
- Import data from multiple formats (JSON, CSV, Excel)
- Multiple interface options:
  - PyQt5 GUI mode with form-based input and table display
  - Flet GUI mode for a modern, web-based experience
  - CLI mode for command-line operations
- URL support for additional car information
- Cross-platform compatibility (Windows, macOS, Linux)

## Requirements

- Python 3.6+
- Dependencies:
  - PyQt5 - GUI framework
  - flet - Flet GUI framework
  - tabulate - CLI table formatting
  - pandas - Data handling
  - openpyxl - Excel file support
  - PyInstaller (optional) - For creating standalone executables

## Installation

### Method 1: Manual Setup

1. Download zip or clone the repository:
   ```sh
   git clone https://github.com/yourusername/CarDb.git
   ```

2. Navigate to the project directory:
   ```sh
   cd CarDb
   ```

3. Create a virtual environment:
   ```sh
   # On Windows
   python -m venv venv
   
   # On macOS/Linux
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   ```sh
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

5. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```
   
   Or install packages individually:
   ```sh
   pip install pyqt5 flet tabulate pandas openpyxl pyinstaller
   ```

6. (Optional) Build the executable:
   ```sh
   pyinstaller --onefile --windowed main.py
   ```

   The executable will be available in the `dist` directory.

**Important:** After installation, maintain the project directory structure for proper operation.

### Method 2: Automatic Setup

1. Install Python 3

2. Run the appropriate setup script for your operating system:

   **For Linux/macOS:**
   ```sh
   chmod +x ./linux_setup.sh
   ./linux_setup.sh
   ```

   **For Windows:**
   ```sh
   .\windows_setup.bat
   ```
   
   The script will:
   - Create a virtual environment
   - Install dependencies
   - Build an executable
   - Create a desktop shortcut (configurable)

## Usage

### Starting the Application

Run the application using Python:
```sh
python main.py
```

When prompted, select your preferred interface:
- For PyQt5 GUI mode: Type `Gui` or simply press Enter (default)
- For Flet GUI mode: Type `Flet`
- For CLI mode: Type `Cli`

### PyQt5 GUI Interface

The graphical interface provides:
- Input form for adding new car entries
- Table display of all car entries
- Search functionality by model name
- Import support for external data files
- URL opening for additional information (double-click More Info cell)

### Flet Interface

The Flet interface provides a modern, web-based GUI with similar functionality to the PyQt5 GUI, including adding, viewing, and searching for car entries.

### CLI Interface

The command-line interface supports the following commands:
- `add` - Add a new car entry
- `display` - Show all car entries in a formatted table
- `search` - Find cars by model name
- `delete` - Remove a car entry
- `import` - Import car data from external files
- `--help` - Show available commands
- `exit` - Quit the application

## Data Structure

Each car entry contains the following fields:
- Model Name
- Manufacturer
- Year
- Origin Country
- Category
- Model Manufacturer (replica brand)
- More Info (URL link)

## Project Structure

```
CarDb/
├── app/                 # Core application code
│   ├── data/            # Data storage and handling
│   │   ├── car.json     # Car database file
│   │   └── file_io.py   # File operations
│   ├── car_handler.py   # File handling logic
│   ├── car_tracker.py   # Business logic
│   └── utils.py         # Utility functions
├── interfaces/          # User interface implementations
│   ├── cli.py           # Command-line interface
│   ├── gui.py           # PyQt5 graphical user interface
│   └── flet_app.py      # Flet graphical user interface
├── main.py              # Application entry point
├── requirements.txt     # Project dependencies
├── linux_setup.sh       # Linux/macOS setup script
└── windows_setup.bat    # Windows setup script
```

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Running Tests

```sh
pytest
```

### Linting

```sh
flake8 .
```

## License

This project is licensed under the MIT License.
