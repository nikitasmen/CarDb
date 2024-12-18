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

# 5. python -m venv venv
python3 -m venv venv

# 6. (bash) venv\Scripts\activate
source venv/bin/activate

# 7. pip install tkinter pyinstaller
pip install tkinter 
pip install pyinstaller

# 8. pyinstaller --onefile --windowed main.py
pyinstaller --onefile --windowed main.py

# Create a shortcut for ./dist/main
# This part is platform-specific. On Linux, you can create a symbolic link:
ln -s $PROJECT_DIR/dist/main /home/makis/Desktop/carDb

echo "Setup complete. The executable is available on your Desktop."