@echo off
setlocal

:: Project details
set PROJECT_DIR=CarDb

:: Function to get Desktop path based on the OS
set "SHORTCUT_DIR=%USERPROFILE%\Desktop"

:: Ask user for the shortcut location (default to Desktop)
set /p SHORTCUT_DIR_USER=Enter the desired shortcut location (leave blank for Desktop): 
if not "%SHORTCUT_DIR_USER%"=="" (
    set SHORTCUT_DIR=%SHORTCUT_DIR_USER%
)

:: Ensure the shortcut directory exists
if not exist "%SHORTCUT_DIR%" (
    echo The directory "%SHORTCUT_DIR%" does not exist. Please enter a valid location.
    exit /b 1
)

:: Remove existing project if it exists
if exist "%PROJECT_DIR%" (
    echo Project directory %PROJECT_DIR% already exists. Deleting it...
    rmdir /s /q "%PROJECT_DIR%"
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python3 is not installed. Installing Python3...
    :: Install Python using Chocolatey (if installed)
    choco install python3 -y
)

:: Check for pip and install dependencies
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

:: Ensure the virtual environment is created
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Install required packages
echo Installing required packages...
python -m pip install pyinstaller
python -m pip install -r requirements.txt --no-warn-script-location

:: Check if main.py exists
if not exist "main.py" (
    echo main.py not found. Exiting...
    exit /b 1
)

:: Clean previous builds if they exist
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

:: Build the project using PyInstaller without windowed mode
echo Building project with PyInstaller...
pyinstaller --onefile --add-data "data\car.json;data" main.py

:: Wait for the build to complete
timeout /t 2 /nobreak >nul

:: Create the shortcut in the specified directory
echo Creating shortcut...
if exist "dist\main.exe" (
    del /f /q "%SHORTCUT_DIR%\carDb.exe" 2>nul
    copy "dist\main.exe" "%SHORTCUT_DIR%\carDb.exe"
) else (
    echo Build failed. Executable not found.
    exit /b 1
)

:: Confirmation message
if exist "%SHORTCUT_DIR%\carDb.exe" (
    echo Setup complete. The executable is available at: "%SHORTCUT_DIR%\carDb.exe"
) else (
    echo Failed to create the shortcut. Please check permissions and try again.
)

endlocal