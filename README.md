# CarDb

Simple CRUD application for miniature car collection.

## Requirements

1. Python 3
    - PyQt5
    - PyInstaller (Optional)
2. Git account

## Installation

1. Install Python 3

    ### 2a. Manual Setup

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

    #### 2b: Automatic Setup:

    1. Install Python 3

    3. Run the setup script:

        ```sh
        ./linux_setup.sh
        ```
        ```sh
        ./windows_setup.bat
        ```
        
