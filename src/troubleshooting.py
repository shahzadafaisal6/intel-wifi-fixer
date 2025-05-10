"""
Advanced Troubleshooting Module

This module provides advanced troubleshooting functionality for diagnosing
and resolving complex WiFi issues.
"""

import os
import re
import time
import datetime
import subprocess
from src.utils.command_runner import run_command, execute_with_sudo
from src.utils.ui_helpers import display_message, display_success, display_error, display_warning

def capture_wifi_traffic(interface="wlan0", duration=30, filename=None):
    """
    Capture WiFi traffic using tcpdump.
    
    Args:
        interface: The wireless interface to capture traffic on
        duration: The duration of the capture in seconds
        filename: The filename to save the capture to
        
    Returns:
        str: The path to the capture file, or None if the capture failed
    """
    try:
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wifi_capture_{timestamp}.pcap"
        
        capture_path = os.path.join(os.path.expanduser("~"), filename)
        
        display_message(f"Capturing WiFi traffic on {interface} for {duration} seconds...", color='blue')
        
        # Start tcpdump in the background
        process = subprocess.Popen(
            ["sudo", "tcpdump", "-i", interface, "-w", capture_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for the specified duration
        time.sleep(duration)
        
        # Stop tcpdump
        process.terminate()
        process.wait()
        
        if os.path.exists(capture_path):
            display_success(f"WiFi traffic captured and saved to {capture_path}")
            return capture_path
        else:
            display_error("Failed to capture WiFi traffic.")
            return None
            
    except Exception as e:
        display_error(f"Error capturing WiFi traffic: {str(e)}")
        return None

def analyze_wifi_interference():
    """
    Analyze WiFi interference from other networks and devices.
    
    Returns:
        dict: A dictionary of interference information
    """
    try:
        display_message("Analyzing WiFi interference...", color='blue')
        
        # Get a list of nearby networks
        networks = run_command(["nmcli", "-t", "-f", "SSID,CHAN,SIGNAL", "device", "wifi", "list"])
        
        interference = {
            "networks": [],
            "channels": {},
            "recommendations": []
        }
        
        if networks:
            for line in networks.strip().split('\n'):
                if line:
                    fields = line.split(':')
                    if len(fields) >= 3:
                        ssid = fields[0]
                        channel = fields[1]
                        signal = fields[2]
                        
                        network = {
                            "ssid": ssid,
                            "channel": channel,
                            "signal": signal
                        }
                        
                        interference["networks"].append(network)
                        
                        # Count networks per channel
                        if channel in interference["channels"]:
                            interference["channels"][channel] += 1
                        else:
                            interference["channels"][channel] = 1
        
        # Find the least congested channels
        if interference["channels"]:
            # For 2.4 GHz, recommend channels 1, 6, or 11
            channels_2g = {k: v for k, v in interference["channels"].items() if int(k) <= 14}
            best_2g = min([1, 6, 11], key=lambda c: channels_2g.get(str(c), 0))
            
            # For 5 GHz, find the least congested channel
            channels_5g = {k: v for k, v in interference["channels"].items() if int(k) > 14}
            best_5g = min(channels_5g.items(), key=lambda x: x[1])[0] if channels_5g else None
            
            if best_2g:
                interference["recommendations"].append(f"For 2.4 GHz, use channel {best_2g}")
            
            if best_5g:
                interference["recommendations"].append(f"For 5 GHz, use channel {best_5g}")
        
        return interference
            
    except Exception as e:
        display_error(f"Error analyzing WiFi interference: {str(e)}")
        return {"networks": [], "channels": {}, "recommendations": []}

def diagnose_connection_timing():
    """
    Diagnose connection timing issues.
    
    Returns:
        dict: A dictionary of timing information
    """
    try:
        display_message("Diagnosing connection timing...", color='blue')
        
        # Disconnect from the current network
        execute_with_sudo(["nmcli", "device", "disconnect", "wlan0"])
        time.sleep(2)
        
        # Start timing
        start_time = time.time()
        
        # Connect to the network
        execute_with_sudo(["nmcli", "device", "wifi", "connect", "$(nmcli -t -f SSID device wifi list | head -n 1)"])
        
        # Wait for the connection to establish
        connected = False
        timeout = 30
        elapsed = 0
        
        while not connected and elapsed < timeout:
            status = run_command(["nmcli", "-t", "-f", "STATE", "device", "show", "wlan0"])
            if status and "connected" in status:
                connected = True
            else:
                time.sleep(1)
                elapsed = time.time() - start_time
        
        # Calculate timing
        connection_time = time.time() - start_time
        
        # Get DHCP timing
        dhcp_time = None
        dhcp_log = run_command(["journalctl", "-u", "NetworkManager", "--since", f"{int(start_time)}"])
        
        if dhcp_log:
            dhcp_start = None
            dhcp_end = None
            
            for line in dhcp_log.split('\n'):
                if "dhcp4" in line and "starting" in line:
                    dhcp_start = time.time()
                elif "dhcp4" in line and "state changed" in line:
                    dhcp_end = time.time()
            
            if dhcp_start and dhcp_end:
                dhcp_time = dhcp_end - dhcp_start
        
        # Get DNS timing
        dns_time = None
        try:
            dns_start = time.time()
            subprocess.run(["dig", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            dns_time = time.time() - dns_start
        except Exception:
            pass
        
        timing = {
            "connection_time": connection_time,
            "dhcp_time": dhcp_time,
            "dns_time": dns_time,
            "connected": connected
        }
        
        return timing
            
    except Exception as e:
        display_error(f"Error diagnosing connection timing: {str(e)}")
        return {"connection_time": None, "dhcp_time": None, "dns_time": None, "connected": False}

def check_driver_debug_info():
    """
    Check driver debug information.
    
    Returns:
        str: The driver debug information
    """
    try:
        display_message("Checking driver debug information...", color='blue')
        
        # Get driver debug information from dmesg
        try:
            # Using subprocess directly to handle the pipe correctly
            debug_info = subprocess.check_output("dmesg | grep -i iwlwifi", 
                                               shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            # grep returns non-zero exit code when no matches are found
            debug_info = ""
        
        if not debug_info:
            debug_info = "No driver debug information found."
        
        return debug_info
            
    except Exception as e:
        display_error(f"Error checking driver debug information: {str(e)}")
        return "Error retrieving driver debug information."

def check_system_logs():
    """
    Check system logs for WiFi-related issues.
    
    Returns:
        str: The relevant system log entries
    """
    try:
        display_message("Checking system logs for WiFi-related issues...", color='blue')
        
        # Get WiFi-related log entries
        try:
            # Using subprocess directly to handle the pipe correctly
            log_entries = subprocess.check_output(
                "journalctl -u NetworkManager --since '1 hour ago' | grep -i 'wifi\\|wlan\\|iwlwifi\\|80211'", 
                shell=True, universal_newlines=True, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError:
            # grep returns non-zero exit code when no matches are found
            log_entries = ""
        
        if not log_entries:
            log_entries = "No WiFi-related log entries found."
        
        return log_entries
            
    except Exception as e:
        display_error(f"Error checking system logs: {str(e)}")
        return "Error retrieving system logs."

def run_network_diagnostics():
    """
    Run comprehensive network diagnostics.
    
    Returns:
        dict: A dictionary of diagnostic information
    """
    try:
        display_message("Running comprehensive network diagnostics...", color='blue')
        
        diagnostics = {}
        
        # Check if the interface is up
        interface_status = run_command(["ip", "link", "show", "wlan0"])
        diagnostics["interface_status"] = "UP" if "UP" in interface_status else "DOWN"
        
        # Check if the interface has an IP address
        ip_address = run_command(["ip", "addr", "show", "wlan0"])
        if ip_address:
            ip_match = re.search(r"inet ([\d.]+)", ip_address)
            if ip_match:
                diagnostics["ip_address"] = ip_match.group(1)
            else:
                # No IP address found, but interface exists
                diagnostics["ip_address"] = "None"
                display_warning("No IP address assigned to wlan0 interface")
        else:
            # Could not get interface information
            diagnostics["ip_address"] = "Unknown"
            display_warning("Could not retrieve IP address information for wlan0")
        
        # Check the routing table
        routing_table = run_command(["ip", "route"])
        diagnostics["default_gateway"] = re.search(r"default via ([\d.]+)", routing_table).group(1) if re.search(r"default via ([\d.]+)", routing_table) else "None"
        
        # Check DNS configuration
        dns_config = run_command(["cat", "/etc/resolv.conf"])
        dns_servers = re.findall(r"nameserver ([\d.]+)", dns_config)
        diagnostics["dns_servers"] = dns_servers if dns_servers else ["None"]
        
        # Check connectivity to the default gateway
        if diagnostics["default_gateway"] != "None":
            ping_gateway = run_command(["ping", "-c", "3", diagnostics["default_gateway"]])
            diagnostics["gateway_ping"] = "Success" if "3 received" in ping_gateway else "Failed"
        else:
            diagnostics["gateway_ping"] = "N/A"
        
        # Check internet connectivity
        ping_internet = run_command(["ping", "-c", "3", "8.8.8.8"])
        diagnostics["internet_ping"] = "Success" if "3 received" in ping_internet else "Failed"
        
        # Check DNS resolution
        dns_resolution = run_command(["dig", "+short", "google.com"])
        diagnostics["dns_resolution"] = "Success" if dns_resolution else "Failed"
        
        # Check WiFi signal strength
        iwconfig_output = run_command(["iwconfig", "wlan0"])
        if iwconfig_output:
            signal_match = re.search(r"Signal level=(-\d+) dBm", iwconfig_output)
            diagnostics["signal_strength"] = f"{signal_match.group(1)} dBm" if signal_match else "Unknown"
        else:
            diagnostics["signal_strength"] = "Unknown"
        
        # Check WiFi connection speed
        if iwconfig_output:
            speed_match = re.search(r"Bit Rate=([\d.]+) Mb/s", iwconfig_output)
            diagnostics["connection_speed"] = f"{speed_match.group(1)} Mb/s" if speed_match else "Unknown"
        else:
            diagnostics["connection_speed"] = "Unknown"
            
        # Check wpa_supplicant status
        wpa_status = run_command(["systemctl", "status", "wpa_supplicant.service"])
        if wpa_status:
            if "Active: active" in wpa_status:
                diagnostics["wpa_supplicant_status"] = "Running"
            else:
                diagnostics["wpa_supplicant_status"] = "Not running"
                display_warning("wpa_supplicant service is not running")
        else:
            diagnostics["wpa_supplicant_status"] = "Unknown"
        
        return diagnostics
            
    except Exception as e:
        display_error(f"Error running network diagnostics: {str(e)}")
        return {}