"""
Captive Portal Detection and Handling Module

This module provides functionality for detecting and handling captive portals
on WiFi networks, which are commonly found in hotels, airports, and cafes.
"""

import os
import re
import time
import socket
import subprocess
import webbrowser
from utils.command_runner import run_command, execute_with_sudo
from utils.ui_helpers import display_message, display_success, display_error, display_warning

# Define test URLs for captive portal detection
TEST_URLS = [
    "http://connectivitycheck.gstatic.com/generate_204",
    "http://www.google.com/generate_204",
    "http://detectportal.firefox.com/success.txt",
    "http://www.apple.com/library/test/success.html",
    "http://www.msftncsi.com/ncsi.txt"
]

def detect_captive_portal():
    """
    Detect if the current network has a captive portal.
    
    Returns:
        tuple: (bool, str) - (is_captive_portal, portal_url)
    """
    try:
        display_message("Detecting captive portal...", color='blue')
        
        # Check if we have internet connectivity
        if not check_internet_connectivity():
            display_message("No internet connectivity. Checking for captive portal...", color='blue')
            
            # Try to detect the captive portal URL
            portal_url = get_captive_portal_url()
            
            if portal_url:
                display_success(f"Captive portal detected at: {portal_url}")
                return True, portal_url
            else:
                display_warning("No captive portal detected, but internet connectivity is unavailable.")
                return False, None
        else:
            display_message("Internet connectivity is available. No captive portal detected.", color='blue')
            return False, None
            
    except Exception as e:
        display_error(f"Error detecting captive portal: {str(e)}")
        return False, None

def check_internet_connectivity():
    """
    Check if we have internet connectivity.
    
    Returns:
        bool: True if we have internet connectivity, False otherwise
    """
    try:
        # Try to resolve a well-known domain
        socket.gethostbyname("www.google.com")
        
        # Try to ping a well-known IP address
        result = run_command(["ping", "-c", "1", "-W", "2", "8.8.8.8"])
        
        if result and "1 received" in result:
            return True
        
        return False
            
    except Exception:
        return False

def get_captive_portal_url():
    """
    Get the URL of the captive portal.
    
    Returns:
        str: The URL of the captive portal, or None if not found
    """
    try:
        # Try each test URL
        for url in TEST_URLS:
            try:
                # Use curl to fetch the URL and follow redirects
                result = run_command(["curl", "-s", "-L", "-I", "-m", "5", url])
                
                if result:
                    # Check for a redirect to the captive portal
                    location_match = re.search(r"Location: (http[s]?://[^\r\n]+)", result)
                    if location_match:
                        portal_url = location_match.group(1)
                        
                        # Verify that this is not a normal redirect
                        if not any(test_url in portal_url for test_url in TEST_URLS):
                            return portal_url
            except Exception:
                continue
        
        # If we couldn't find a portal URL, try to get the default gateway
        gateway = get_default_gateway()
        
        if gateway:
            return f"http://{gateway}"
        
        return None
            
    except Exception as e:
        display_error(f"Error getting captive portal URL: {str(e)}")
        return None

def get_default_gateway():
    """
    Get the default gateway IP address.
    
    Returns:
        str: The default gateway IP address, or None if not found
    """
    try:
        result = run_command(["ip", "route", "show", "default"])
        
        if result:
            match = re.search(r"default via ([\d.]+)", result)
            if match:
                return match.group(1)
        
        return None
            
    except Exception as e:
        display_error(f"Error getting default gateway: {str(e)}")
        return None

def open_captive_portal(url):
    """
    Open the captive portal in a web browser.
    
    Args:
        url: The URL of the captive portal
        
    Returns:
        bool: True if the browser was opened successfully, False otherwise
    """
    try:
        display_message(f"Opening captive portal at: {url}", color='blue')
        
        # Try to open the URL in a web browser
        if webbrowser.open(url):
            display_success("Captive portal opened in web browser.")
            return True
        else:
            display_error("Failed to open captive portal in web browser.")
            
            # Try to open the URL with xdg-open
            result = run_command(["xdg-open", url])
            
            if result is not None:
                display_success("Captive portal opened with xdg-open.")
                return True
            else:
                display_error("Failed to open captive portal with xdg-open.")
                return False
            
    except Exception as e:
        display_error(f"Error opening captive portal: {str(e)}")
        return False

def monitor_captive_portal_session():
    """
    Monitor the captive portal session to detect when authentication is complete.
    
    Returns:
        bool: True if authentication is complete, False otherwise
    """
    try:
        display_message("Monitoring captive portal session...", color='blue')
        
        # Check for internet connectivity every 5 seconds for up to 2 minutes
        for _ in range(24):
            if check_internet_connectivity():
                display_success("Internet connectivity established. Captive portal authentication complete.")
                return True
            
            time.sleep(5)
        
        display_warning("Timeout waiting for captive portal authentication.")
        return False
            
    except Exception as e:
        display_error(f"Error monitoring captive portal session: {str(e)}")
        return False

def handle_captive_portal():
    """
    Handle a captive portal by detecting it and opening it in a web browser.
    
    Returns:
        bool: True if the captive portal was handled successfully, False otherwise
    """
    try:
        is_captive_portal, portal_url = detect_captive_portal()
        
        if is_captive_portal and portal_url:
            if open_captive_portal(portal_url):
                return monitor_captive_portal_session()
            else:
                display_error("Failed to open captive portal.")
                return False
        elif not is_captive_portal:
            display_message("No captive portal detected.", color='blue')
            return True
        else:
            display_error("Captive portal detected, but URL could not be determined.")
            return False
            
    except Exception as e:
        display_error(f"Error handling captive portal: {str(e)}")
        return False