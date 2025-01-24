#!/bin/bash

# Project details
PROJECT_DIR="./CarDb"
REPO_URL="https://github.com/nikitasmen/CarDb.git"

# Detect platform and get desktop path
get_desktop_path() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "$HOME/Desktop"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "$HOME/Desktop"
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "$USERPROFILE/Desktop"
    else
        echo "Unsupported OS detected."
        exit 1
    fi
}

# Ask user for the shortcut location (default to desktop)
read -p "Enter the desired shortcut location (leave blank for Desktop): " SHORTCUT_DIR

# Use the default desktop path if the user leaves it blank
if [[ -z "$SHORTCUT_DIR" ]]; then
    SHORTCUT_DIR=$(get_desktop_path)
fi

# Ensure the shortcut directory exists
if [[ ! -d "$SHORTCUT_DIR" ]]; then
    echo "The directory '$SHORTCUT_DIR' does not exist. Please enter a valid location."
    exit 1
fi

# Remove existing project if it exists
if [ -d "$PROJECT_DIR" ]; then
    echo "Project directory $PROJECT_DIR already exists. Deleting it..."
    sudo rm -rf "$PROJECT_DIR"
fi

# Check and install Python3 if not available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip
else
    echo "Python3 is already installed."
fi

# Remove any existing shortcut in the specified location
if [ -f "$SHORTCUT_DIR/carDb" ]; then
    sudo rm -f "$SHORTCUT_DIR/carDb"
fi

# Remove existing project if it exists
if [ -d "$PROJECT_DIR" ]; then
    echo "Project directory $PROJECT_DIR already exists. Deleting it..."
    sudo rm -rf "$PROJECT_DIR"
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing Git..."
    sudo apt-get update
    sudo apt-get install -y git    
else
    echo "Git is already installed."
fi

#check git credentials 
if ! git config --get user.email; then
    echo "Please configure your git credentials before proceeding."
    read -p "Enter your Git username: " username
    git config --global user.name "$username"
    read -p "Enter your Git email: " email
    git config --global user.email "$email"
fi

# Clone the repository using git
git clone https://github.com/nikitasmen/CarDb.git "$PROJECT_DIR"

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Failed to enter directory $PROJECT_DIR"; exit 1; }

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install pyqt5 
pip install tabulate 
pip install pyinstaller

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "main.py not found. Exiting..."
    exit 1
fi

# Build the project using PyInstaller
pyinstaller --onefile --windowed main.py

# Create the shortcut in the specified directory
ln -sfn "$(pwd)/dist/main" "$SHORTCUT_DIR/carDb"

# Confirmation message
if [[ -L "$SHORTCUT_DIR/carDb" ]]; then
    echo "Setup complete. The executable is available at: $SHORTCUT_DIR/carDb"
else
    echo "Failed to create the shortcut. Please check permissions and try again."
fi
