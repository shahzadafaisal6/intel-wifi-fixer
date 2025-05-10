# File: /intel-wifi-fixer/intel-wifi-fixer/src/diagnostics.py

import subprocess
import re
import os
import time
from src.utils.command_runner import run_command, execute_with_sudo
from src.utils.ui_helpers import display_progress, display_message, display_warning
from src.config.adapter_configs import IntelCentrino6205Config

def check_adapter_status():
    """Check the status of the Intel Centrino Advanced-N 6205 adapter."""
    try:
        output = run_command(["nmcli", "device", "status"])
        for line in output.splitlines():
            if "wlan0" in line:
                return "Connected" if "connected" in line else "Disconnected"
    except Exception as e:
        display_warning(f"Error checking adapter status: {str(e)}")
    return "Unknown"

def check_rfkill():
    """Check if the WiFi is blocked by rfkill."""
    try:
        output = run_command(["rfkill", "list", "wifi"])
        if "Soft blocked: yes" in output:
            return "Soft blocked"
        if "Hard blocked: yes" in output:
            return "Hard blocked"
    except Exception as e:
        display_warning(f"Error checking rfkill status: {str(e)}")
    return "Not blocked"

def check_driver_status():
    """Check if the driver for the Intel Centrino Advanced-N 6205 is loaded."""
    try:
        output = run_command(["lsmod"])
        if "iwlwifi" in output:
            return "Driver loaded"
    except Exception as e:
        display_warning(f"Error checking driver status: {str(e)}")
    return "Driver not loaded"

def check_firmware_version():
    """Check the firmware version of the Intel Centrino Advanced-N 6205 adapter."""
    try:
        # Using dmesg with subprocess directly to handle the pipe correctly
        dmesg_output = subprocess.check_output("dmesg | grep -i 'iwlwifi.*firmware'", 
                                              shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        if dmesg_output:
            match = re.search(r"loaded firmware version ([0-9.]+)", dmesg_output)
            if match:
                return match.group(1)
            
            # Try alternative pattern that might be used in some distributions
            match = re.search(r"firmware: ([0-9.]+)", dmesg_output)
            if match:
                return match.group(1)
                
        # If dmesg doesn't work, try checking the firmware file directly
        firmware_path = "/lib/firmware/iwlwifi-6000g2a-6.ucode"
        if os.path.exists(firmware_path):
            # Get file info to determine version
            file_info = run_command(["ls", "-la", firmware_path])
            if file_info:
                return f"File exists: {os.path.basename(firmware_path)}"
    except Exception as e:
        display_warning(f"Error checking firmware version: {str(e)}")
    return "Unknown"

def check_signal_strength():
    """Check the signal strength of the connected WiFi network."""
    try:
        output = run_command(["nmcli", "-f", "SIGNAL", "device", "wifi", "list"])
        if output:
            lines = output.strip().split('\n')
            if len(lines) > 1:  # Skip header
                signal_values = [int(s) for s in re.findall(r'\d+', lines[1])]
                if signal_values:
                    return f"{signal_values[0]}%"
    except Exception as e:
        display_warning(f"Error checking signal strength: {str(e)}")
    return "Unknown"

def check_network_manager_status():
    """Check if NetworkManager is running."""
    try:
        output = run_command(["systemctl", "status", "NetworkManager"])
        if "active (running)" in output:
            return "Running"
        else:
            return "Not running"
    except Exception as e:
        display_warning(f"Error checking NetworkManager status: {str(e)}")
    return "Unknown"

def check_wpa_supplicant_status():
    """Check if wpa_supplicant service is running."""
    try:
        output = run_command(["systemctl", "status", "wpa_supplicant.service"])
        if "active (running)" in output:
            return "Running"
        else:
            return "Not running"
    except Exception as e:
        display_warning(f"Error checking wpa_supplicant status: {str(e)}")
    return "Unknown"

def check_interface_status():
    """Check if the wlan0 interface is up."""
    try:
        output = run_command(["ip", "link", "show", "wlan0"])
        if "UP" in output:
            return "Up"
        else:
            return "Down"
    except Exception as e:
        display_warning(f"Error checking interface status: {str(e)}")
    return "Unknown"

def check_driver_parameters():
    """Check the current driver parameters for iwlwifi."""
    try:
        if os.path.exists("/etc/modprobe.d/iwlwifi.conf"):
            output = run_command(["cat", "/etc/modprobe.d/iwlwifi.conf"])
            return output
        else:
            return "No custom parameters set"
    except Exception as e:
        display_warning(f"Error checking driver parameters: {str(e)}")
    return "Unknown"

def check_regulatory_domain():
    """Check the current regulatory domain."""
    try:
        output = run_command(["iw", "reg", "get"])
        match = re.search(r"country ([A-Z]{2}):", output)
        if match:
            return match.group(1)
    except Exception as e:
        display_warning(f"Error checking regulatory domain: {str(e)}")
    return "Unknown"

def gather_diagnostics():
    """Gather all diagnostics for the Intel Centrino Advanced-N 6205 adapter."""
    display_message("Running diagnostics...", color='blue')
    
    steps = 9
    
    display_progress("Checking adapter status", steps, 1)
    time.sleep(0.5)
    adapter_status = check_adapter_status()
    
    display_progress("Checking RFKill status", steps, 2)
    time.sleep(0.5)
    rfkill_status = check_rfkill()
    
    display_progress("Checking driver status", steps, 3)
    time.sleep(0.5)
    driver_status = check_driver_status()
    
    display_progress("Checking firmware version", steps, 4)
    time.sleep(0.5)
    firmware_version = check_firmware_version()
    
    display_progress("Checking signal strength", steps, 5)
    time.sleep(0.5)
    signal_strength = check_signal_strength()
    
    display_progress("Checking NetworkManager status", steps, 6)
    time.sleep(0.5)
    nm_status = check_network_manager_status()
    
    display_progress("Checking wpa_supplicant status", steps, 7)
    time.sleep(0.5)
    wpa_status = check_wpa_supplicant_status()
    
    display_progress("Checking interface status", steps, 8)
    time.sleep(0.5)
    interface_status = check_interface_status()
    
    display_progress("Checking driver parameters", steps, 9)
    time.sleep(0.5)
    driver_params = check_driver_parameters()
    
    diagnostics = {
        "Adapter Status": adapter_status,
        "RFKill Status": rfkill_status,
        "Driver Status": driver_status,
        "Firmware Version": firmware_version,
        "Signal Strength": signal_strength,
        "NetworkManager Status": nm_status,
        "WPA Supplicant Status": wpa_status,
        "Interface Status": interface_status,
        "Driver Parameters": driver_params
    }
    
    return diagnostics

def display_diagnostics(diagnostics):
    """Display the gathered diagnostics in a user-friendly format."""
    # This function is now handled by the run_diagnostics_menu function
    # in main.py using the display_table function for a more professional look
    pass

def identify_issues(diagnostics):
    """Identify issues based on the diagnostic results."""
    issues = []
    
    if diagnostics["Adapter Status"] == "Disconnected":
        issues.append("WiFi adapter is disconnected")
    
    if diagnostics["RFKill Status"] != "Not blocked":
        issues.append("WiFi is blocked by rfkill")
    
    if diagnostics["Driver Status"] != "Driver loaded":
        issues.append("WiFi driver is not loaded")
    
    if diagnostics["NetworkManager Status"] != "Running":
        issues.append("NetworkManager is not running")
        
    if diagnostics["WPA Supplicant Status"] != "Running":
        issues.append("wpa_supplicant is not running")
    
    if diagnostics["Interface Status"] != "Up":
        issues.append("WiFi interface is down")
    
    if diagnostics["Firmware Version"] == "Unknown":
        issues.append("Unable to determine firmware version")
    
    if "11n_disable=1" not in diagnostics["Driver Parameters"]:
        issues.append("11n mode is enabled, which may cause issues with this adapter")
    
    if "power_save=0" not in diagnostics["Driver Parameters"]:
        issues.append("Power save mode is enabled, which may cause connectivity issues")
    
    return issues

def run_diagnostics(adapter_info):
    """Run diagnostics and identify issues."""
    diagnostics = gather_diagnostics()
    issues = identify_issues(diagnostics)
    return issues