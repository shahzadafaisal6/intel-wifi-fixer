#!/bin/bash

# Intel WiFi Fixer - Launcher Script
# This script launches the Intel WiFi Fixer application with the necessary privileges
# Developed by: Shahzada Faisal Abbas (Hamn-Tec)

# Function to display colored text
function echo_color() {
    local color=$1
    local text=$2
    
    case $color in
        "red")    echo -e "\033[0;31m$text\033[0m" ;;
        "green")  echo -e "\033[0;32m$text\033[0m" ;;
        "yellow") echo -e "\033[0;33m$text\033[0m" ;;
        "blue")   echo -e "\033[0;34m$text\033[0m" ;;
        "cyan")   echo -e "\033[0;36m$text\033[0m" ;;
        *)        echo "$text" ;;
    esac
}

# Function to display a header
function display_header() {
    local text=$1
    local width=70
    
    echo
    echo_color "blue" "$(printf '═%.0s' $(seq 1 $width))"
    echo_color "blue" "$(printf '%-'$width's' "  $text")"
    echo_color "blue" "$(printf '═%.0s' $(seq 1 $width))"
    echo
}

# Display banner
function display_banner() {
    echo_color "cyan" "
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                  Intel WiFi Fixer Tool v1.0.0                    ║
    ║                                                                  ║
    ║          Diagnose and fix Intel Centrino Advanced-N             ║
    ║                 6205 wireless adapter issues                     ║
    ║                                                                  ║
    ║  Developed by: Shahzada Faisal Abbas (Hamn-Tec)                 ║
    ║  GitHub: https://github.com/shahzadafaisal6/intel-wifi-fixer    ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    "
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    display_banner
    echo_color "red" "Error: This application requires administrative privileges."
    echo_color "yellow" "Please run with sudo or as root."
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Display banner
display_banner
display_header "Initializing Intel WiFi Fixer"

# Check if Python 3 is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo_color "red" "Error: Python 3 is required but not installed."
    echo_color "yellow" "Please install Python 3 and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PYTHON_VERSION"

# Check if venv module is available
echo "Checking Python venv module..."
if ! python3 -m venv --help &> /dev/null; then
    echo_color "red" "Error: Python venv module is required but not installed."
    echo_color "yellow" "Please install python3-venv package and try again."
    echo_color "yellow" "On Debian/Ubuntu/Kali: sudo apt install python3-venv"
    echo_color "yellow" "On Fedora: sudo dnf install python3-venv"
    echo_color "yellow" "On Arch Linux: sudo pacman -S python-virtualenv"
    exit 1
fi

# Create virtual environment if it doesn't exist
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo_color "red" "Error: Failed to create virtual environment."
        exit 1
    fi
    echo_color "green" "Virtual environment created successfully."
else
    echo "Using existing virtual environment."
fi

# Check if the required dependencies are installed
if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo_color "red" "Error: requirements.txt not found."
    exit 1
fi

# Activate virtual environment and install dependencies
echo "Setting up environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Failed to activate virtual environment."
    exit 1
fi

echo "Upgrading pip..."
pip install --upgrade pip > /dev/null
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Failed to upgrade pip."
    deactivate
    exit 1
fi

echo "Installing dependencies..."
pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Failed to install dependencies."
    deactivate
    exit 1
fi

echo_color "green" "Environment setup complete."

# Run the application
echo "Starting Intel WiFi Fixer..."
cd "$SCRIPT_DIR"
python -m src.main
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

if [ $EXIT_CODE -ne 0 ]; then
    echo_color "red" "Application exited with error code: $EXIT_CODE"
    exit $EXIT_CODE
fi

exit 0