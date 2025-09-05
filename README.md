# CarDb Mobile

A mobile-first CRUD application for managing your miniature car collection. Track details about model cars, search through your collection, and maintain a comprehensive database of your prized miniatures on any device.

![CarDb Mobile](https://via.placeholder.com/300x600?text=CarDb+Mobile+App)

## Features

- **Mobile-Optimized**: Designed for smartphones and tablets
- Add, view, update, and delete car entries
- Search functionality to find specific cars by model name
- Import data from multiple formats (JSON, CSV, Excel)
- Cross-platform mobile app using Flet framework
- Responsive design that works on all screen sizes
- Touch-friendly interface with intuitive navigation
- CLI mode for command-line operations (desktop only)

## Requirements

- Python 3.7+
- Dependencies:
  - **flet** - Modern mobile app framework
  - **tabulate** - CLI table formatting
  - **pandas** - Data handling
  - **openpyxl** - Excel file support

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

6. (Optional) Build the mobile app:

   ```sh
   flet pack interfaces/flet_app.py
   ```

   The mobile app will be available in the `dist` directory.

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
   - Build a mobile app
   - Create a desktop shortcut (configurable)

## Usage

### Starting the Application

- Start with interface selection:

```sh
python main.py --flet   # Flet UI (mobile/desktop)
python main.py --cli    # CLI
```

### Mobile Interface (Flet)

The mobile interface provides:

- Touch-optimized navigation with bottom navigation bar
- Card-based display of car entries
- Search functionality with mobile keyboard
- Form-based adding and editing of cars
- Swipe-friendly interactions
- Responsive design for all screen sizes

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

```text
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
│   └── flet_app.py      # Mobile Flet interface
├── main.py              # Application entry point
├── requirements.txt     # Project dependencies
├── linux_setup.sh       # Linux/macOS setup script
└── windows_setup.bat    # Windows setup script
```

## Development

### Building for Mobile

To build for Android:

```sh
flet pack interfaces/flet_app.py --android
```

To build for iOS (macOS only):

```sh
flet pack interfaces/flet_app.py --ios
```
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
