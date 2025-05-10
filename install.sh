#!/bin/bash

# Intel WiFi Fixer - Installation Script
# This script installs the Intel WiFi Fixer application
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

# Function to detect the Linux distribution
function detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        DISTRO_VERSION=$VERSION_ID
        echo "Detected distribution: $DISTRO $DISTRO_VERSION"
    else
        DISTRO="unknown"
        echo_color "yellow" "Warning: Could not detect Linux distribution."
    fi
}

# Function to install packages based on the distribution
function install_package() {
    local package=$1
    
    case $DISTRO in
        "debian"|"ubuntu"|"kali"|"parrot")
            apt-get install -y $package
            ;;
        "fedora")
            dnf install -y $package
            ;;
        "centos"|"rhel")
            yum install -y $package
            ;;
        "arch"|"manjaro")
            pacman -S --noconfirm $package
            ;;
        "opensuse"*)
            zypper install -y $package
            ;;
        *)
            echo_color "yellow" "Warning: Unsupported distribution for automatic package installation."
            echo_color "yellow" "Please install $package manually."
            return 1
            ;;
    esac
    
    return $?
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    display_banner
    echo_color "red" "Error: This installation requires administrative privileges."
    echo_color "yellow" "Please run with sudo or as root."
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Display banner
display_banner
display_header "Installing Intel WiFi Fixer"

# Detect the Linux distribution
detect_distro

# Update package lists if on Debian-based systems
if [[ "$DISTRO" == "debian" || "$DISTRO" == "ubuntu" || "$DISTRO" == "kali" || "$DISTRO" == "parrot" ]]; then
    echo "Updating package lists..."
    apt-get update
fi

# Check if Python 3 is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo_color "yellow" "Python 3 is required but not installed."
    echo "Installing Python 3..."
    install_package "python3"
    if [ $? -ne 0 ]; then
        echo_color "red" "Error: Failed to install Python 3."
        exit 1
    fi
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PYTHON_VERSION"

# Check if pip is installed
echo "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo_color "yellow" "pip3 is required but not installed."
    echo "Installing pip3..."
    install_package "python3-pip"
    if [ $? -ne 0 ]; then
        echo_color "red" "Error: Failed to install pip3."
        exit 1
    fi
fi

# Check if venv module is available
echo "Checking Python venv module..."
if ! python3 -m venv --help &> /dev/null; then
    echo_color "yellow" "Python venv module is required but not installed."
    echo "Installing Python venv module..."
    
    case $DISTRO in
        "debian"|"ubuntu"|"kali"|"parrot")
            install_package "python3-venv"
            ;;
        "fedora")
            install_package "python3-virtualenv"
            ;;
        "centos"|"rhel")
            install_package "python3-virtualenv"
            ;;
        "arch"|"manjaro")
            install_package "python-virtualenv"
            ;;
        "opensuse"*)
            install_package "python3-virtualenv"
            ;;
        *)
            echo_color "red" "Error: Unsupported distribution for automatic venv installation."
            echo_color "yellow" "Please install Python venv module manually and try again."
            exit 1
            ;;
    esac
    
    if [ $? -ne 0 ]; then
        echo_color "red" "Error: Failed to install Python venv module."
        exit 1
    fi
fi

# Install required system packages
echo "Installing required system packages..."
REQUIRED_PACKAGES=("network-manager" "wireless-tools" "rfkill" "ethtool" "iw")

for package in "${REQUIRED_PACKAGES[@]}"; do
    echo "Installing $package..."
    install_package "$package"
    if [ $? -ne 0 ]; then
        echo_color "yellow" "Warning: Failed to install $package. The application may not function correctly."
    fi
done

# Create virtual environment
echo "Setting up virtual environment..."
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

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
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

echo "Installing requirements..."
pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Failed to install requirements."
    deactivate
    exit 1
fi

# Install the package in development mode
echo "Installing Intel WiFi Fixer package..."
pip install -e "$SCRIPT_DIR" > /dev/null
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Failed to install the package."
    deactivate
    exit 1
fi

deactivate

# Create a symlink to the launcher script
echo "Creating launcher script..."
chmod +x "$SCRIPT_DIR/intel-wifi-fixer.sh"
ln -sf "$SCRIPT_DIR/intel-wifi-fixer.sh" /usr/local/bin/intel-wifi-fixer
if [ $? -ne 0 ]; then
    echo_color "red" "Error: Failed to create launcher script symlink."
    exit 1
fi

echo_color "green" "Installation complete!"
echo_color "green" "You can now run the Intel WiFi Fixer by typing 'sudo intel-wifi-fixer' in the terminal."

exit 0