#!/bin/bash

# 1. Install python3
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

# 2. Download zip/clone the repo
# Replace the URL with the actual repository URL
REPO_URL="https://github.com/nikitasmen/CarDb.git"
git clone $REPO_URL

# 3. Extract files (if downloaded as a zip)
# Uncomment the following lines if you downloaded a zip file
# ZIP_FILE="your-repo.zip"
# unzip $ZIP_FILE

# 4. cd /path/to/the/project
PROJECT_DIR="./CarDb"  # Replace with the actual directory name
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
ln -s $(pwd)/dist/main ~/Desktop/carDb

echo "Setup complete. The executable is available on your Desktop."