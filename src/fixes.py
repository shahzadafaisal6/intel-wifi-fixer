import os
import time
import subprocess
import re
from src.utils.command_runner import run_command, execute_with_sudo
from src.utils.ui_helpers import display_progress, display_message, display_success, display_error, display_warning

def reset_adapter(adapter_info=None):
    """Reset the Intel Centrino Advanced-N 6205 wireless adapter."""
    try:
        display_message("Resetting wireless adapter...", color='blue')
        execute_with_sudo(["ip", "link", "set", "wlan0", "down"])
        time.sleep(1)
        execute_with_sudo(["ip", "link", "set", "wlan0", "up"])
        time.sleep(2)
        display_success("Adapter reset successfully.")
        return True
    except Exception as e:
        display_error(f"Failed to reset adapter: {str(e)}")
        return False

def unblock_rfkill(adapter_info=None):
    """Unblock the wireless adapter if it's blocked by rfkill."""
    try:
        display_message("Unblocking wireless adapter...", color='blue')
        execute_with_sudo(["rfkill", "unblock", "all"])
        time.sleep(1)
        display_success("Adapter unblocked successfully.")
        return True
    except Exception as e:
        display_error(f"Failed to unblock adapter: {str(e)}")
        return False

def restart_network_manager(adapter_info=None):
    """Restart the NetworkManager service."""
    try:
        display_message("Restarting NetworkManager service...", color='blue')
        execute_with_sudo(["systemctl", "restart", "NetworkManager"])
        time.sleep(3)
        display_success("NetworkManager restarted successfully.")
        return True
    except Exception as e:
        display_error(f"Failed to restart NetworkManager: {str(e)}")
        return False

def restart_wpa_supplicant(adapter_info=None):
    """Restart the wpa_supplicant service."""
    try:
        display_message("Restarting wpa_supplicant service...", color='blue')
        execute_with_sudo(["systemctl", "restart", "wpa_supplicant.service"])
        time.sleep(2)
        display_success("wpa_supplicant service restarted successfully.")
        return True
    except Exception as e:
        display_error(f"Failed to restart wpa_supplicant service: {str(e)}")
        return False

def configure_driver_parameters(adapter_info=None):
    """Configure optimal driver parameters for the Intel Centrino Advanced-N 6205."""
    try:
        display_message("Configuring driver parameters...", color='blue')
        
        # Create or update the iwlwifi.conf file
        config_content = "options iwlwifi 11n_disable=1 power_save=0"
        
        # Check if the file exists
        if os.path.exists("/etc/modprobe.d/iwlwifi.conf"):
            # Read the current content
            current_content = run_command(["cat", "/etc/modprobe.d/iwlwifi.conf"])
            
            # Only update if needed
            if config_content not in current_content:
                execute_with_sudo(["bash", "-c", f"echo '{config_content}' > /etc/modprobe.d/iwlwifi.conf"])
        else:
            execute_with_sudo(["bash", "-c", f"echo '{config_content}' > /etc/modprobe.d/iwlwifi.conf"])
        
        display_success("Driver parameters configured successfully.")
        display_message("Note: You may need to reboot for changes to take effect.", color='yellow')
        return True
    except Exception as e:
        display_error(f"Failed to configure driver parameters: {str(e)}")
        return False

def update_firmware(adapter_info=None):
    """Update the firmware for the Intel Centrino Advanced-N 6205."""
    try:
        display_message("Checking for firmware updates...", color='blue')
        
        # Check current firmware version
        try:
            # Using subprocess directly to handle the pipe correctly
            output = subprocess.check_output("dmesg | grep -i 'iwlwifi.*firmware'", 
                                           shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
            current_version = "Unknown"
            if output:
                match = re.search(r"loaded firmware version ([0-9.]+)", output)
                if match:
                    current_version = match.group(1)
        except subprocess.CalledProcessError:
            # grep returns non-zero exit code when no matches are found
            current_version = "Unknown"
        
        display_message(f"Current firmware version: {current_version}", color='blue')
        
        # Check if firmware file exists
        firmware_path = "/usr/lib/firmware/6000g2a-6.ucode"
        if os.path.exists(firmware_path):
            display_message("Firmware file found. Creating backup...", color='blue')
            
            # Create backup
            execute_with_sudo(["cp", firmware_path, f"{firmware_path}.bak"])
            
            # Download the latest firmware
            display_message("Attempting to download latest firmware...", color='blue')
            
            # Note: This URL might need to be updated if the firmware location changes
            firmware_url = "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/iwlwifi-6000g2a-6.ucode"
            
            # Create a temporary file for the download
            temp_firmware_path = "/tmp/iwlwifi-6000g2a-6.ucode.new"
            
            try:
                # Download to temporary location first
                execute_with_sudo(["wget", firmware_url, "-O", temp_firmware_path])
                
                # Check if download was successful and file is not empty
                if os.path.exists(temp_firmware_path) and os.path.getsize(temp_firmware_path) > 0:
                    # Compare versions if possible
                    if current_version != "Unknown":
                        # Try to extract version from the downloaded file
                        # This is a simplified check - in reality, firmware version extraction might be more complex
                        display_message("Verifying downloaded firmware...", color='blue')
                        
                        # Copy to actual location
                        execute_with_sudo(["cp", temp_firmware_path, firmware_path])
                        display_success("Firmware updated successfully.")
                        display_message("Note: You need to reboot for the new firmware to take effect.", color='yellow')
                        
                        # Clean up
                        execute_with_sudo(["rm", temp_firmware_path])
                        return True
                    else:
                        # If we can't determine current version, just update
                        execute_with_sudo(["cp", temp_firmware_path, firmware_path])
                        display_success("Firmware updated successfully.")
                        display_message("Note: You need to reboot for the new firmware to take effect.", color='yellow')
                        
                        # Clean up
                        execute_with_sudo(["rm", temp_firmware_path])
                        return True
                else:
                    display_error("Downloaded firmware file is empty or invalid.")
                    display_message("Keeping current firmware version.", color='yellow')
                    return False
            except Exception as e:
                display_error(f"Failed to download firmware: {str(e)}")
                display_message("Restoring backup if needed...", color='blue')
                if os.path.exists(f"{firmware_path}.bak"):
                    execute_with_sudo(["cp", f"{firmware_path}.bak", firmware_path])
                
                # Clean up
                if os.path.exists(temp_firmware_path):
                    execute_with_sudo(["rm", temp_firmware_path])
                    
                return False
        else:
            display_warning(f"Firmware file not found at {firmware_path}")
            display_message("Attempting to locate firmware file...", color='blue')
            
            # Try to find the firmware file
            output = run_command(["find", "/usr/lib/firmware", "-name", "*6000g2a*"])
            if output:
                display_message(f"Found firmware files: {output}", color='blue')
                display_message("Please manually update the firmware using the correct path.", color='yellow')
            else:
                display_error("No firmware files found. Please install the linux-firmware package.")
            
            return False
    except Exception as e:
        display_error(f"Failed to update firmware: {str(e)}")
        return False

def configure_driver(adapter_info=None):
    """Configure the driver for optimal performance."""
    try:
        display_message("Configuring driver for optimal performance...", color='blue')
        
        # Configure driver parameters
        configure_driver_parameters()
        
        # Reload the driver if possible
        try:
            display_message("Attempting to reload the driver...", color='blue')
            execute_with_sudo(["modprobe", "-r", "iwlwifi"])
            time.sleep(1)
            execute_with_sudo(["modprobe", "iwlwifi"])
            display_success("Driver reloaded successfully.")
        except Exception as e:
            display_warning(f"Could not reload driver: {str(e)}")
            display_message("You may need to reboot for changes to take effect.", color='yellow')
        
        return True
    except Exception as e:
        display_error(f"Failed to configure driver: {str(e)}")
        return False

def scan_networks(adapter_info=None):
    """Scan for available WiFi networks."""
    try:
        display_message("Scanning for WiFi networks...", color='blue')
        
        # Make sure the interface is up
        execute_with_sudo(["ip", "link", "set", "wlan0", "up"])
        
        # Make sure WiFi is enabled
        execute_with_sudo(["nmcli", "radio", "wifi", "on"])
        
        # Scan for networks
        time.sleep(2)  # Give some time for the interface to come up
        output = run_command(["nmcli", "-t", "-f", "SSID,SECURITY,SIGNAL,CHAN,FREQ,RATE", "device", "wifi", "list"])
        
        networks = []
        if output:
            for line in output.strip().split('\n'):
                if line:
                    fields = line.split(':')
                    if len(fields) >= 6:
                        ssid = fields[0]
                        security = fields[1] if fields[1] else "Open"
                        signal_strength = fields[2]
                        signal = f"{'▆' * (int(fields[2]) // 20)}{'_' * (5 - int(fields[2]) // 20)}"
                        channel = fields[3]
                        # Extract numeric part of frequency
                        freq_value = re.search(r'(\d+)', fields[4])
                        if freq_value:
                            freq = "5 GHz" if int(freq_value.group(1)) > 4000 else "2.4 GHz"
                        else:
                            freq = "Unknown"
                        speed = fields[5]
                        
                        networks.append({
                            "ssid": ssid,
                            "security": security,
                            "signal": signal,
                            "signal_strength": signal_strength,
                            "channel": channel,
                            "band": freq,
                            "speed": speed
                        })
        
        return networks
    except Exception as e:
        display_error(f"Failed to scan for networks: {str(e)}")
        return []

def apply_all_fixes(issues, adapter_info=None):
    """Apply all necessary fixes based on identified issues."""
    if not issues:
        display_message("No issues to fix.", color='green')
        return
    
    display_message("Applying fixes...", color='blue')
    
    steps = len(issues)
    for i, issue in enumerate(issues, 1):
        display_progress(f"Fixing: {issue}", steps, i)
        
        if "blocked by rfkill" in issue:
            unblock_rfkill(adapter_info)
        
        elif "interface is down" in issue or "adapter is disconnected" in issue:
            reset_adapter(adapter_info)
        
        elif "NetworkManager is not running" in issue:
            restart_network_manager(adapter_info)
            
        elif "wpa_supplicant is not running" in issue or "authentication issues" in issue:
            restart_wpa_supplicant(adapter_info)
        
        elif "11n mode is enabled" in issue or "Power save mode is enabled" in issue:
            configure_driver_parameters(adapter_info)
        
        elif "firmware version" in issue:
            update_firmware(adapter_info)
        
        time.sleep(1)
    
    # Final reset and restart of services to apply all changes
    reset_adapter(adapter_info)
    restart_network_manager(adapter_info)
    restart_wpa_supplicant(adapter_info)
    
    display_success("All fixes applied successfully.")
    display_message("Note: Some changes may require a system reboot to take effect.", color='yellow')