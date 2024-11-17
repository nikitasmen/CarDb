@echo off
REM Windows setup script for CarDb

REM 1. Ensure Python3 is installed
echo Ensure Python3 is installed and added to PATH before running this script.

REM 2. Clone the repository
REM Replace the URL with the actual repository URL
set REPO_URL=https://github.com/nikitasmen/CarDb.git
echo Cloning repository from %REPO_URL%...
git clone %REPO_URL%

REM 3. Navigate to the project directory
set PROJECT_DIR=CarDb REM Replace with the actual directory name
cd %PROJECT_DIR%

REM 4. Create a virtual environment
echo Creating virtual environment...
python -m venv venv

REM 5. Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM 6. Install required Python packages
echo Installing required packages...
pip install tkinter
pip install pyinstaller

REM 7. Create the executable
echo Building executable using PyInstaller...
pyinstaller --onefile --windowed main.py

REM 8. Create a shortcut on the Desktop
set EXE_PATH=%CD%\dist\main.exe
set SHORTCUT_PATH=%USERPROFILE%\Desktop\CarDb.lnk

REM Use PowerShell to create a shortcut
echo Creating shortcut on Desktop...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%EXE_PATH%'; $s.Save()"

echo Setup complete. The executable is available on your Desktop.
pause
