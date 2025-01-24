
:: Project details
set "PROJECT_DIR=CarDb"
set "REPO_URL=https://github.com/nikitasmen/CarDb.git"

:: Detect platform and get desktop path
for /f "tokens=*" %%D in ('powershell "$env:USERPROFILE\Desktop"') do set "DESKTOP_PATH=%%D"

:: Ask user for the shortcut location (default to desktop)
set /p SHORTCUT_DIR="Enter the desired shortcut location (leave blank for Desktop): "
if "%SHORTCUT_DIR%"=="" set "SHORTCUT_DIR=%DESKTOP_PATH%"

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

:: Check and install Python3 if not available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python3 is not installed. Please install it manually.
    exit /b 1
) else (
    echo Python3 is already installed.
)

:: Remove any existing shortcut in the specified location
if exist "%SHORTCUT_DIR%\carDb.lnk" (
    del "%SHORTCUT_DIR%\carDb.lnk"
)

:: Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git manually.
    exit /b 1
) else (
    echo Git is already installed.
)

:: Clone the repository using git
git clone %REPO_URL% "%PROJECT_DIR%"

:: Navigate to the project directory
cd "%PROJECT_DIR%" || exit /b 1

git checkout cliApp

:: Create a Python virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Install dependencies
pip install pyqt5
pip install pyinstaller

:: Check if main.py exists
if not exist "main.py" (
    echo main.py not found. Exiting...
    exit /b 1
)

:: Build the project using PyInstaller
pyinstaller --onefile --windowed main.py

:: Create the shortcut in the specified directory
set "TARGET=%CD%\dist\main.exe"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_DIR%\carDb.lnk');$s.TargetPath='%TARGET%';$s.Save()"

:: Confirmation message
if exist "%SHORTCUT_DIR%\carDb.lnk" (
    echo Setup complete. The executable is available at: %SHORTCUT_DIR%\carDb.lnk
) else (
    echo Failed to create the shortcut. Please check permissions and try again.
)
