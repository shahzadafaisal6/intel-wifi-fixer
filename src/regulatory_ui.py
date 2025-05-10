"""
Regulatory Domain Configuration UI Module

This module provides a user interface for configuring the regulatory domain.
"""

import os
import time
from utils.ui_helpers import display_header, display_message, display_success, display_error, display_warning
from regulatory import (
    REGULATORY_DOMAINS,
    get_current_regulatory_domain,
    set_regulatory_domain,
    get_available_channels,
    get_max_transmit_power,
    set_transmit_power,
    display_regulatory_info
)

def regulatory_domain_menu():
    """Display the regulatory domain configuration menu."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_header("Regulatory Domain Configuration")
        
        # Display current regulatory information
        info = display_regulatory_info()
        
        print(f"\nCurrent Regulatory Domain: {info['domain']} ({info['domain_name']})")
        
        print("\nAvailable Channels:")
        print(f"  2.4 GHz: {', '.join(info['channels']['2.4 GHz'])}")
        print(f"  5 GHz: {', '.join(info['channels']['5 GHz'])}")
        
        print("\nMaximum Transmit Power:")
        print(f"  2.4 GHz: {info['max_power']['2.4 GHz']}")
        print(f"  5 GHz: {info['max_power']['5 GHz']}")
        
        print("\n1. Set Regulatory Domain")
        print("2. Set Transmit Power")
        print("3. Refresh Regulatory Information")
        print("b. Back to Advanced Options")
        
        choice = input("\nSelect an option: ").strip().lower()
        
        if choice == '1':
            set_domain_menu()
        elif choice == '2':
            set_power_menu()
        elif choice == '3':
            display_message("Refreshing regulatory information...", color='blue')
            time.sleep(1)
        elif choice == 'b':
            break
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def set_domain_menu():
    """Menu for setting the regulatory domain."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Set Regulatory Domain")
    
    print("\nAvailable Regulatory Domains:")
    
    # Display domains in columns
    domains = list(REGULATORY_DOMAINS.items())
    col_width = 25
    cols = 3
    
    for i in range(0, len(domains), cols):
        row = domains[i:i+cols]
        print("  " + "".join(f"{code}: {name}".ljust(col_width) for code, name in row))
    
    print("\nEnter the regulatory domain code (e.g., US, GB, DE)")
    domain_code = input("Domain code: ").strip().upper()
    
    if domain_code:
        if domain_code in REGULATORY_DOMAINS:
            set_regulatory_domain(domain_code)
        else:
            display_error(f"Invalid regulatory domain code: {domain_code}")
    
    input("\nPress Enter to continue...")

def set_power_menu():
    """Menu for setting the transmit power."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Set Transmit Power")
    
    print("\nAvailable Power Levels:")
    print("1. Auto (let the driver decide)")
    print("2. High (maximum allowed by regulatory domain)")
    print("3. Medium (reduced power)")
    print("4. Low (minimum usable power)")
    
    choice = input("\nSelect a power level: ").strip()
    
    power_map = {
        "1": "auto",
        "2": "high",
        "3": "medium",
        "4": "low"
    }
    
    if choice in power_map:
        set_transmit_power(power_map[choice])
    else:
        display_error("Invalid power level selection.")
    
    input("\nPress Enter to continue...")