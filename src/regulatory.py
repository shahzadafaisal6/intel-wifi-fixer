"""
Regulatory Domain Configuration Module

This module provides functionality for configuring the regulatory domain
for the wireless adapter, which affects available channels and transmit power.
"""

import os
import re
import time
from utils.command_runner import run_command, execute_with_sudo
from utils.ui_helpers import display_message, display_success, display_error, display_warning

# Define common regulatory domains
REGULATORY_DOMAINS = {
    "00": "World",
    "US": "United States",
    "CA": "Canada",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "JP": "Japan",
    "AU": "Australia",
    "CN": "China",
    "BR": "Brazil",
    "RU": "Russia",
    "IN": "India",
    "KR": "South Korea",
    "ZA": "South Africa",
    "SG": "Singapore",
    "TW": "Taiwan"
}

def get_current_regulatory_domain():
    """
    Get the current regulatory domain.
    
    Returns:
        str: The current regulatory domain code
    """
    try:
        output = run_command(["iw", "reg", "get"])
        
        if output:
            match = re.search(r"country (\w+):", output)
            if match:
                return match.group(1)
        
        return "Unknown"
            
    except Exception as e:
        display_error(f"Error getting regulatory domain: {str(e)}")
        return "Unknown"

def set_regulatory_domain(domain_code):
    """
    Set the regulatory domain.
    
    Args:
        domain_code: The regulatory domain code (e.g., US, GB, DE)
        
    Returns:
        bool: True if the domain was set successfully, False otherwise
    """
    try:
        display_message(f"Setting regulatory domain to {domain_code}...", color='blue')
        
        # Check if the domain code is valid
        if domain_code not in REGULATORY_DOMAINS:
            display_error(f"Invalid regulatory domain code: {domain_code}")
            return False
        
        # Set the regulatory domain
        result = execute_with_sudo(["iw", "reg", "set", domain_code])
        
        if result:
            # Verify that the domain was set
            time.sleep(1)
            current_domain = get_current_regulatory_domain()
            
            if current_domain == domain_code:
                display_success(f"Regulatory domain set to {domain_code} ({REGULATORY_DOMAINS[domain_code]}).")
                return True
            else:
                display_warning(f"Regulatory domain may not have been set correctly. Current domain: {current_domain}")
                return False
        else:
            display_error(f"Failed to set regulatory domain to {domain_code}.")
            return False
            
    except Exception as e:
        display_error(f"Error setting regulatory domain: {str(e)}")
        return False

def get_available_channels():
    """
    Get the available channels for the current regulatory domain.
    
    Returns:
        dict: A dictionary of available channels by band
    """
    try:
        output = run_command(["iw", "list"])
        
        channels = {
            "2.4 GHz": [],
            "5 GHz": []
        }
        
        if output:
            # Extract the channels from the output
            in_channels_section = False
            current_band = None
            
            for line in output.split('\n'):
                if "Frequencies:" in line:
                    in_channels_section = True
                    if "2.4 GHz" in line:
                        current_band = "2.4 GHz"
                    elif "5 GHz" in line:
                        current_band = "5 GHz"
                elif in_channels_section and "* " in line and current_band:
                    # Extract the channel number
                    match = re.search(r"\[(\d+)\]", line)
                    if match:
                        channel = match.group(1)
                        channels[current_band].append(channel)
                elif in_channels_section and not line.strip():
                    in_channels_section = False
                    current_band = None
        
        return channels
            
    except Exception as e:
        display_error(f"Error getting available channels: {str(e)}")
        return {"2.4 GHz": [], "5 GHz": []}

def get_max_transmit_power():
    """
    Get the maximum transmit power for the current regulatory domain.
    
    Returns:
        dict: A dictionary of maximum transmit power by band
    """
    try:
        output = run_command(["iw", "reg", "get"])
        
        max_power = {
            "2.4 GHz": "Unknown",
            "5 GHz": "Unknown"
        }
        
        if output:
            # Extract the maximum power from the output
            for line in output.split('\n'):
                if "2.4 GHz" in line and "dBm" in line:
                    match = re.search(r"(\d+\.\d+) dBm", line)
                    if match:
                        max_power["2.4 GHz"] = f"{match.group(1)} dBm"
                elif "5 GHz" in line and "dBm" in line:
                    match = re.search(r"(\d+\.\d+) dBm", line)
                    if match:
                        max_power["5 GHz"] = f"{match.group(1)} dBm"
        
        return max_power
            
    except Exception as e:
        display_error(f"Error getting maximum transmit power: {str(e)}")
        return {"2.4 GHz": "Unknown", "5 GHz": "Unknown"}

def set_transmit_power(power_level):
    """
    Set the transmit power level.
    
    Args:
        power_level: The power level to set (auto, high, medium, low)
        
    Returns:
        bool: True if the power level was set successfully, False otherwise
    """
    try:
        display_message(f"Setting transmit power to {power_level}...", color='blue')
        
        # Map power level to iwconfig power setting
        power_map = {
            "auto": "auto",
            "high": "on",
            "medium": "15",
            "low": "10"
        }
        
        if power_level not in power_map:
            display_error(f"Invalid power level: {power_level}")
            return False
        
        # Set the power level
        result = execute_with_sudo(["iwconfig", "wlan0", "txpower", power_map[power_level]])
        
        if result:
            display_success(f"Transmit power set to {power_level}.")
            return True
        else:
            display_error(f"Failed to set transmit power to {power_level}.")
            return False
            
    except Exception as e:
        display_error(f"Error setting transmit power: {str(e)}")
        return False

def display_regulatory_info():
    """
    Display information about the current regulatory domain.
    
    Returns:
        dict: A dictionary of regulatory information
    """
    try:
        domain = get_current_regulatory_domain()
        domain_name = REGULATORY_DOMAINS.get(domain, "Unknown")
        channels = get_available_channels()
        max_power = get_max_transmit_power()
        
        info = {
            "domain": domain,
            "domain_name": domain_name,
            "channels": channels,
            "max_power": max_power
        }
        
        return info
            
    except Exception as e:
        display_error(f"Error displaying regulatory information: {str(e)}")
        return {
            "domain": "Unknown",
            "domain_name": "Unknown",
            "channels": {"2.4 GHz": [], "5 GHz": []},
            "max_power": {"2.4 GHz": "Unknown", "5 GHz": "Unknown"}
        }