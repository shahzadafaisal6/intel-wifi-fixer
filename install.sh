#!/bin/bash

# Intel WiFi Fixer - Installation Script
# This script installs the Intel WiFi Fixer application

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "This installation requires administrative privileges."
    echo "Please run with sudo or as root."
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Installing Intel WiFi Fixer..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    echo "Installing Python 3..."
    apt-get update
    apt-get install -y python3 python3-pip
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed."
    echo "Installing pip3..."
    apt-get install -y python3-pip
fi

# Install required system packages
echo "Installing required system packages..."
apt-get install -y network-manager wireless-tools rfkill ethtool iw

# Install the package
echo "Installing Intel WiFi Fixer package..."
cd "$SCRIPT_DIR"
pip3 install -e .

# Create a symlink to the launcher script
echo "Creating launcher script..."
ln -sf "$SCRIPT_DIR/intel-wifi-fixer.sh" /usr/local/bin/intel-wifi-fixer
chmod +x /usr/local/bin/intel-wifi-fixer

echo "Installation complete!"
echo "You can now run the Intel WiFi Fixer by typing 'sudo intel-wifi-fixer' in the terminal."

exit 0