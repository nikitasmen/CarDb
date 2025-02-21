# Project details
$PROJECT_DIR = "CarDb"
$REPO_URL = "https://github.com/nikitasmen/CarDb.git"

# Detect platform and get desktop path
$DESKTOP_PATH = [Environment]::GetFolderPath("Desktop")

# Ask user for the shortcut location (default to desktop)
$SHORTCUT_DIR = Read-Host "Enter the desired shortcut location (leave blank for Desktop)"
if ([string]::IsNullOrEmpty($SHORTCUT_DIR)) {
    $SHORTCUT_DIR = $DESKTOP_PATH
}

# Ensure the shortcut directory exists
if (-Not (Test-Path -Path $SHORTCUT_DIR)) {
    Write-Host "The directory '$SHORTCUT_DIR' does not exist. Please enter a valid location."
    exit 1
}

# Remove existing project if it exists
if (Test-Path -Path $PROJECT_DIR) {
    Write-Host "Project directory $PROJECT_DIR already exists. Deleting it..."
    Remove-Item -Recurse -Force $PROJECT_DIR
}

# Check and install Python3 if not available
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python3 is not installed. Please install it manually."
    exit 1
} else {
    Write-Host "Python3 is already installed."
}

# Clone the repository
git clone $REPO_URL $PROJECT_DIR

# Navigate to the project directory
Set-Location $PROJECT_DIR

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
& .\venv\Scripts\Activate

# Install required packages
pip install -r requirements.txt

Write-Host "Setup completed successfully."