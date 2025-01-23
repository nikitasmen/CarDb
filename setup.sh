#!/bin/bash

PROJECT_DIR="./CarDb"
REPO_URL="https://github.com/nikitasmen/CarDb.git"

if [ -d "$PROJECT_DIR" ]; then
    echo "Project directory $PROJECT_DIR already exists. Deleting it..."
    sudo rm -rf "$PROJECT_DIR"
fi

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip
else
    echo "Python3 is already installed."
fi
if [ -d "/home/makis/Desktop/carDb" ]; then
    sudo rm -f "/home/makis/Desktop/carDb"
fi

# 2. clone the repo
git clone $REPO_URL

# 3. Extract files (if downloaded as a zip)
# Uncomment the following lines if you downloaded a zip file
# ZIP_FILE="your-repo.zip"
# unzip $ZIP_FILE

# 4. cd /path/to/the/project
cd $PROJECT_DIR

git checkout cliApp

# 5. python -m venv venv
python3 -m venv venv

# 6. (bash) venv\Scripts\activate
source venv/bin/activate

# 7. pip install pyqt5 pyinstaller
pip install pyqt5 
pip install pyinstaller

#check if main.py exists
if [ ! -f "main.py" ]; then
    echo "main.py not found. Exiting..."
    exit 1
fi

# 8. pyinstaller --onefile --windowed main.py
pyinstaller --onefile --windowed main.py

# Create a shortcut for ./dist/main
# This part is platform-specific. On Linux, you can create a symbolic link:
ln -s $PROJECT_DIR/dist/main /home/makis/Desktop/carDb

echo "Setup complete. The executable is available on your Desktop."