"""
Captive Portal Handling UI Module

This module provides a user interface for detecting and handling captive portals.
"""

import os
import time
from utils.ui_helpers import display_header, display_message, display_success, display_error, display_warning
from captive_portal import (
    detect_captive_portal,
    check_internet_connectivity,
    get_captive_portal_url,
    open_captive_portal,
    monitor_captive_portal_session,
    handle_captive_portal
)

def captive_portal_menu():
    """Display the captive portal handling menu."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_header("Captive Portal Handling")
        
        # Check internet connectivity
        if check_internet_connectivity():
            display_message("Internet connectivity is available.", color='green')
            print("No captive portal detected.")
        else:
            display_warning("No internet connectivity.")
            print("You may be behind a captive portal.")
        
        print("\n1. Detect Captive Portal")
        print("2. Open Captive Portal in Browser")
        print("3. Check Internet Connectivity")
        print("4. Automatic Captive Portal Handling")
        print("b. Back to Advanced Options")
        
        choice = input("\nSelect an option: ").strip().lower()
        
        if choice == '1':
            detect_portal_menu()
        elif choice == '2':
            open_portal_menu()
        elif choice == '3':
            check_connectivity_menu()
        elif choice == '4':
            auto_handle_portal_menu()
        elif choice == 'b':
            break
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def detect_portal_menu():
    """Menu for detecting captive portals."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Detect Captive Portal")
    
    print("\nDetecting captive portal...")
    is_captive_portal, portal_url = detect_captive_portal()
    
    if is_captive_portal:
        display_success("Captive portal detected!")
        print(f"\nPortal URL: {portal_url}")
        
        if input("\nDo you want to open the captive portal in a browser? (y/n): ").strip().lower().startswith('y'):
            open_captive_portal(portal_url)
    else:
        if check_internet_connectivity():
            display_message("No captive portal detected. Internet connectivity is available.", color='green')
        else:
            display_warning("No captive portal detected, but internet connectivity is unavailable.")
            print("This may indicate a different network issue.")
    
    input("\nPress Enter to continue...")

def open_portal_menu():
    """Menu for opening captive portals."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Open Captive Portal")
    
    # Try to get the portal URL automatically
    is_captive_portal, portal_url = detect_captive_portal()
    
    if is_captive_portal and portal_url:
        print(f"\nDetected portal URL: {portal_url}")
        use_detected = input("Use this URL? (y/n): ").strip().lower().startswith('y')
        
        if not use_detected:
            portal_url = input("\nEnter the captive portal URL: ").strip()
    else:
        print("\nNo captive portal detected automatically.")
        portal_url = input("Enter the captive portal URL: ").strip()
    
    if portal_url:
        open_captive_portal(portal_url)
        
        print("\nMonitoring for successful authentication...")
        if monitor_captive_portal_session():
            display_success("Authentication successful!")
        else:
            display_warning("Authentication may not be complete.")
    else:
        display_error("No portal URL provided.")
    
    input("\nPress Enter to continue...")

def check_connectivity_menu():
    """Menu for checking internet connectivity."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Check Internet Connectivity")
    
    print("\nChecking internet connectivity...")
    
    if check_internet_connectivity():
        display_success("Internet connectivity is available!")
        print("\nYou are connected to the internet and can access external websites.")
    else:
        display_error("No internet connectivity.")
        print("\nYou cannot access the internet. Possible reasons:")
        print("1. You are behind a captive portal that requires authentication.")
        print("2. The network has no internet access.")
        print("3. There is a DNS or routing issue.")
        print("4. A firewall is blocking access.")
    
    input("\nPress Enter to continue...")

def auto_handle_portal_menu():
    """Menu for automatic captive portal handling."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Automatic Captive Portal Handling")
    
    print("\nThis will automatically detect and open any captive portal,")
    print("then monitor for successful authentication.")
    
    if input("\nContinue? (y/n): ").strip().lower().startswith('y'):
        print("\nHandling captive portal...")
        
        if handle_captive_portal():
            display_success("Captive portal handling complete!")
        else:
            display_warning("Captive portal handling may not be complete.")
            print("You may need to manually authenticate in the browser window.")
    
    input("\nPress Enter to continue...")