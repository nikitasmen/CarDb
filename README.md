# CarDb

Simple CRUD application for miniature car collection.

## Requirements

1. Python 3
    - PyQt5
    - tabulate
    - pandas
    - openpyxl
    - PyInstaller (Optional)

## Installation

1. Install Python 3

### -Manual Setup

1. Download zip/clone the repo
2. Extract files
3. Navigate to the project directory:

    ```sh
    cd /path/to/the/project
    ```

4. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

5. Activate the virtual environment:

    ```sh
    source venv/bin/activate
    ```

6. Install required packages:

    ```sh
    pip install pyqt5 pyinstaller tabulate pandas openpyxl
    ```

7. (Optional) Build the executable:

    ```sh
    pyinstaller --onefile --windowed main.py
    ```

    - Create a shortcut for `./dist/main`

**Notice:**
After installation, don't change the path of the project.

### -Automatic Setup:

1. Install Python 3

2. Run the setup script:

    ```sh
    ./linux_setup.sh
    ```
    ```sh
    ./windows_setup.bat
    ```

## Usage

To start the application, run:

```sh
python main.py
```

You will be prompted to choose between GUI and CLI mode.

- For GUI mode, type `Gui` or press Enter.
- For CLI mode, type `Cli`.
<!-- 
## Running Tests

To run tests, use:

```sh
pytest
```

## Linting

To check for linting errors, use:

```sh
flake8 .
``` -->
<!-- 
## GitHub Actions

This project uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/python-app.yml`.

## Contributing

Feel free to open issues or submit pull requests for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
 -->
