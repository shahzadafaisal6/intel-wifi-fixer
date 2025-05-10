#!/bin/bash

# Intel WiFi Fixer - Launcher Script
# This script launches the Intel WiFi Fixer application with the necessary privileges

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "This application requires administrative privileges."
    echo "Please run with sudo or as root."
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if venv module is available
if ! python3 -m venv --help &> /dev/null; then
    echo "Python venv module is required but not installed."
    echo "Please install python3-venv package and try again."
    echo "On Debian/Ubuntu/Kali: sudo apt install python3-venv"
    exit 1
fi

# Create virtual environment if it doesn't exist
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Check if the required dependencies are installed
if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "Error: requirements.txt not found."
    exit 1
fi

# Activate virtual environment and install dependencies
echo "Setting up environment..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip > /dev/null
pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null

# Run the application
cd "$SCRIPT_DIR"
python -m src.main

# Deactivate virtual environment
deactivate

exit 0