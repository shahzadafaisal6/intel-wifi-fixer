import os
import re
import json
from src.utils.command_runner import run_command
from src.utils.ui_helpers import display_warning

class AdapterInfo:
    def __init__(self):
        self.adapter_name = "Intel Centrino Advanced-N 6205"
        self.adapter_id = "wlan0"
        self.status = None
        self.configuration = {}
        self.specs = self._load_specs()

    def retrieve_status(self):
        """Retrieve the current status of the adapter."""
        try:
            # Try to get the status from NetworkManager using the correct field
            output = run_command(["nmcli", "-t", "device", "status"])
            if output and self.adapter_id in output:
                # Parse the output to find the status of our adapter
                for line in output.splitlines():
                    if self.adapter_id in line:
                        parts = line.split(':')
                        if len(parts) >= 3 and parts[2] == "connected":
                            self.status = "connected"
                            break
                        else:
                            self.status = "disconnected"
            else:
                # Fallback to checking if the interface is up
                output = run_command(["ip", "link", "show", self.adapter_id])
                if "UP" in output:
                    self.status = "connected"
                else:
                    self.status = "disconnected"
            
            return self.status
        except Exception as e:
            display_warning(f"Error retrieving adapter status: {str(e)}")
            return "unknown"

    def retrieve_configuration(self):
        """Retrieve the configuration of the adapter."""
        try:
            # Get the current SSID if connected
            ssid = "Not connected"
            connection_info = run_command(["nmcli", "-t", "device", "status"])
            if connection_info and self.adapter_id in connection_info:
                for line in connection_info.splitlines():
                    if self.adapter_id in line:
                        parts = line.split(':')
                        if len(parts) >= 4 and parts[2] == "connected":
                            ssid = parts[3]
                            break
            
            # Get the MAC address
            mac = run_command(["cat", f"/sys/class/net/{self.adapter_id}/address"])
            if not mac:
                mac = "Unknown"
            
            # Get the driver information
            driver_info = run_command(["ethtool", "-i", self.adapter_id])
            driver = "Unknown"
            firmware = "Unknown"
            
            if driver_info:
                driver_match = re.search(r"driver: (\w+)", driver_info)
                if driver_match:
                    driver = driver_match.group(1)
                
                firmware_match = re.search(r"firmware-version: ([\w.-]+)", driver_info)
                if firmware_match:
                    firmware = firmware_match.group(1)
            
            # Get the IP address if connected
            ip_address = run_command(["ip", "-4", "addr", "show", self.adapter_id])
            if ip_address:
                ip_match = re.search(r"inet ([\d.]+)", ip_address)
                if ip_match:
                    ip_address = ip_match.group(1)
                else:
                    ip_address = "Not assigned"
            else:
                ip_address = "Not assigned"
            
            # Get the current channel and frequency if connected
            channel_info = run_command(["iwconfig", self.adapter_id])
            channel = "Unknown"
            frequency = "Unknown"
            
            if channel_info:
                channel_match = re.search(r"Channel=(\d+)", channel_info)
                if channel_match:
                    channel = channel_match.group(1)
                
                freq_match = re.search(r"Frequency[=:](\d+\.\d+) GHz", channel_info)
                if freq_match:
                    frequency = f"{freq_match.group(1)} GHz"
            
            self.configuration = {
                "SSID": ssid,
                "MAC Address": mac,
                "Driver": driver,
                "Firmware": firmware,
                "IP Address": ip_address,
                "Channel": channel,
                "Frequency": frequency
            }
            
            return self.configuration
        except Exception as e:
            display_warning(f"Error retrieving adapter configuration: {str(e)}")
            return {
                "SSID": "Error retrieving information",
                "MAC Address": "Error retrieving information",
                "Driver": "Error retrieving information",
                "Firmware": "Error retrieving information",
                "IP Address": "Error retrieving information",
                "Channel": "Error retrieving information",
                "Frequency": "Error retrieving information"
            }

    def display_info(self):
        """Display information about the adapter."""
        status = self.retrieve_status()
        configuration = self.retrieve_configuration()
        
        print(f"\nAdapter: {self.adapter_name}")
        print(f"Status: {'Connected' if 'connected' in status else 'Disconnected'}")
        print("\nConfiguration:")
        for key, value in configuration.items():
            print(f"  {key}: {value}")
        
        if self.specs:
            print("\nSpecifications:")
            for key, value in self.specs.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for subkey, subvalue in value.items():
                        print(f"    {subkey}: {subvalue}")
                else:
                    print(f"  {key}: {value}")

    def _load_specs(self):
        """Load the adapter specifications from the JSON file."""
        try:
            specs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "data", "intel_6205_specs.json")
            
            if os.path.exists(specs_path):
                with open(specs_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default specs if file not found
                return {
                    "Model": "Intel Centrino Advanced-N 6205",
                    "Chipset": "Intel 6205",
                    "Standards": "IEEE 802.11a/b/g/n",
                    "Frequency Bands": "2.4 GHz and 5 GHz",
                    "Max Speed": "300 Mbps",
                    "Antenna Configuration": "2x2 MIMO"
                }
        except Exception as e:
            display_warning(f"Error loading adapter specifications: {str(e)}")
            return {}