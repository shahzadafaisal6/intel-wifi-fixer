# Intel WiFi Fixer

**Developed by: Shahzada Faisal Abbas (Hamn-Tec)**  
**GitHub: [https://github.com/shahzadafaisal6/intel-wifi-fixer](https://github.com/shahzadafaisal6/intel-wifi-fixer)**

## Overview
The Intel WiFi Fixer is a comprehensive Python-based application designed to diagnose and resolve issues specifically related to the Intel Centrino Advanced-N 6205 wireless adapter. This tool automates the process of identifying common problems and applying appropriate fixes, ensuring a smoother wireless experience for users across various Linux distributions.

## Features

### Diagnostics
- **Adapter Status Check**: Verifies if the adapter is recognized and functioning.
- **Driver Status**: Checks if the correct driver is loaded and functioning properly.
- **Firmware Version**: Identifies the current firmware version and suggests updates if needed.
- **RFKill Status**: Detects if the wireless adapter is blocked by hardware or software switches.
- **Network Manager Status**: Ensures the network management service is running correctly.
- **Signal Strength Analysis**: Measures and reports on WiFi signal quality.
- **Driver Parameter Check**: Verifies optimal driver configuration for the Intel 6205 adapter.

### Automated Fixes
- **Driver Configuration**: Applies optimal driver parameters for the Intel 6205 adapter.
- **Firmware Updates**: Assists with updating the adapter firmware to the latest version.
- **RFKill Unblocking**: Automatically unblocks the adapter if it's blocked.
- **Interface Reset**: Resets the wireless interface to resolve connectivity issues.
- **Network Manager Restart**: Restarts the network management service when needed.
- **WPA Supplicant Management**: Restarts the wpa_supplicant service to resolve authentication issues.

### Network Management
- **WiFi Scanning**: Scans and displays available wireless networks with detailed information.
- **Connection Management**: Helps establish and manage wireless connections.
- **Signal Quality Monitoring**: Monitors and reports on signal strength and quality.

### User Interface
- **Professional UI**: Clean, modern interface with color-coded status indicators.
- **Tabular Data Display**: Information presented in well-formatted tables.
- **Progress Indicators**: Visual feedback during operations.
- **Developer Information**: Integrated developer and project details.

### Advanced Features

#### 1. Enterprise WiFi Configuration
- EAP-TLS, PEAP, TTLS support
- Certificate management
- 802.1X authentication

#### 2. Multi-Connection Management
- Load balancing multiple connections
- Failover configuration
- Traffic routing rules

#### 3. Regulatory Domain Handling
- Region-specific channel restrictions
- Transmit power compliance
- Dynamic regulatory domain handling

#### 4. Captive Portal Detection and Handling
- Portal detection without online services
- Authentication helpers
- Session management

#### 5. Advanced Troubleshooting
- Packet capture and analysis
- Connection timing diagnostics
- Interference detection
- WPA Supplicant service management
- System logs analysis
- Driver debug information

## Installation

### Prerequisites
- Linux operating system
- Python 3.6 or higher
- NetworkManager
- Administrative (sudo) privileges
- Python venv module (for virtual environment installation)

### Method 1: Quick Start with Installation Script (Recommended)
This method automatically sets up a virtual environment and installs all dependencies:

1. Clone the repository:
   ```bash
   git clone https://github.com/shahzadafaisal6/intel-wifi-fixer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd intel-wifi-fixer
   ```
3. Make the installation script executable:
   ```bash
   chmod +x install.sh
   ```
4. Run the installation script:
   ```bash
   sudo ./install.sh
   ```

### Method 2: Using Virtual Environment (Manual Setup)
This method allows you to run the tool in an isolated Python environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/shahzadafaisal6/intel-wifi-fixer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd intel-wifi-fixer
   ```
3. Install the Python venv package if not already installed:
   ```bash
   # For Debian/Ubuntu/Kali Linux
   sudo apt install python3-venv
   
   # For Fedora
   sudo dnf install python3-venv
   
   # For Arch Linux
   sudo pacman -S python-virtualenv
   ```
4. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
5. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
6. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
7. Run the application (still requires sudo):
   ```bash
   sudo -E .venv/bin/python -m src.main
   ```

### Method 3: System-Wide Installation
This method installs the tool globally on your system:

1. Clone the repository:
   ```bash
   git clone https://github.com/shahzadafaisal6/intel-wifi-fixer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd intel-wifi-fixer
   ```
3. Install the package:
   ```bash
   sudo pip3 install -e .
   ```

### Method 4: Install from PyPI (Coming Soon)
Once the package is published to PyPI, you'll be able to install it directly:
```bash
sudo pip3 install intel-wifi-fixer
```

### Method 5: Install from GitHub
Install directly from the GitHub repository:
```bash
sudo pip3 install git+https://github.com/shahzadafaisal6/intel-wifi-fixer.git
```

## Usage

### Running the Application

#### If installed using the installation script (Method 1):
```bash
sudo intel-wifi-fixer
```

#### If using virtual environment (Method 2):
```bash
# With virtual environment already activated
sudo -E python -m src.main

# Or without activating the virtual environment
sudo -E /path/to/intel-wifi-fixer/.venv/bin/python -m src.main
```

#### If installed system-wide (Methods 3, 4, or 5):
```bash
sudo intel-wifi-fixer
```

#### Direct execution from source:
```bash
cd /path/to/intel-wifi-fixer
sudo python3 -m src.main
```

### Main Menu Options
1. **Run Diagnostics**: Analyze your Intel Centrino Advanced-N 6205 adapter for issues.
2. **Fix Common Issues**: Apply automated fixes for detected problems.
3. **Advanced Options**: Access advanced configuration and troubleshooting tools.
4. **Scan for Networks**: Scan and display available wireless networks.
5. **About**: View developer and project information.

### Fix Common Issues Menu
1. **Fix All Issues**: Automatically apply all necessary fixes.
2. **Update Firmware**: Update the adapter firmware.
3. **Configure Driver Parameters**: Set optimal driver parameters.
4. **Restart wpa_supplicant Service**: Restart the authentication service.
5. **Scan for Networks**: Scan and connect to WiFi networks.

### Example Workflow
1. Run the application with `sudo intel-wifi-fixer`
2. Select "Run Diagnostics" to identify any issues
3. If issues are found, select "Fix Common Issues" to apply automated fixes
4. Use "Scan for Networks" to find and connect to available networks

## Cross-Distribution Support Matrix

| Distribution | Package Manager | Init System | Network Service | Config Location |
|--------------|----------------|-------------|-----------------|-----------------|
| Debian/Ubuntu| apt            | systemd     | NetworkManager  | /etc/NetworkManager |
| Fedora/RHEL  | dnf/yum        | systemd     | NetworkManager  | /etc/NetworkManager |
| Arch Linux   | pacman         | systemd     | NetworkManager  | /etc/NetworkManager |
| OpenSUSE     | zypper         | systemd     | NetworkManager  | /etc/NetworkManager |
| Gentoo       | portage        | OpenRC      | NetworkManager  | /etc/NetworkManager |
| Alpine       | apk            | OpenRC      | networkmanager  | /etc/NetworkManager |
| Void Linux   | xbps           | runit       | NetworkManager  | /etc/NetworkManager |
| Slackware    | slackpkg       | sysvinit    | wicd/NetworkManager| /etc/NetworkManager |
| Kali Linux   | apt            | systemd     | NetworkManager  | /etc/NetworkManager |
| Parrot OS    | apt            | systemd     | NetworkManager  | /etc/NetworkManager |

## Troubleshooting
If you encounter issues:
1. Ensure you're running the application with sudo privileges
2. Check that NetworkManager is installed and running
3. Verify that your system has the required wireless tools installed
4. For persistent issues, try rebooting after applying fixes

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
- The Linux wireless community for documentation and insights
- Contributors to the NetworkManager project
- Intel for hardware specifications

## Conclusion

This comprehensive Intel WiFi Fixer tool ensures that you can resolve any networking issue with the Intel Centrino Advanced-N 6205 wireless adapter across any Linux distribution, even without internet connectivity, making it a truly universal solution for Linux networking challenges with this specific hardware.