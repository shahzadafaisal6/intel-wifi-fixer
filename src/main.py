#!/usr/bin/env python3
import os
import sys
import time
from src.adapter_info import AdapterInfo
from src.diagnostics import run_diagnostics, gather_diagnostics, display_diagnostics
from src.fixes import apply_all_fixes, update_firmware, configure_driver, scan_networks
from src.utils.ui_helpers import (
    display_banner, get_user_choice, display_message, 
    display_header, display_success, display_error, display_warning,
    display_footer, display_menu, display_about, clear_screen
)

# Import optional modules
try:
    from src.enterprise_wifi_ui import enterprise_wifi_menu
except ImportError:
    enterprise_wifi_menu = None

try:
    from src.regulatory_ui import regulatory_domain_menu
except ImportError:
    regulatory_domain_menu = None

try:
    from src.captive_portal_ui import captive_portal_menu
except ImportError:
    captive_portal_menu = None

try:
    from src.troubleshooting_ui import troubleshooting_menu
except ImportError:
    troubleshooting_menu = None

try:
    from src.multi_connection_ui import multi_connection_menu
except ImportError:
    multi_connection_menu = None

def main_menu():
    """Display the main menu and handle user input."""
    while True:
        adapter_info = AdapterInfo()
        status = adapter_info.retrieve_status()
        
        # Define menu options
        menu_options = [
            ('1', 'Run Diagnostics'),
            ('2', 'Fix Common Issues'),
            ('3', 'Advanced Options'),
            ('4', 'Scan for Networks'),
            ('a', 'About'),
            ('q', 'Quit')
        ]
        
        # Display the menu
        clear_screen()
        display_banner()
        
        # Display adapter status in a nice format
        print(f"\n  {'Detected Adapter:':<20} {adapter_info.adapter_name}")
        
        # Display connection status with color
        if 'connected' in status:
            print(f"  {'Status:':<20} ", end='')
            display_message("Connected", color='green')
        else:
            print(f"  {'Status:':<20} ", end='')
            display_message("Disconnected", color='red')
        
        # Display the menu and get user choice
        choice = display_menu("Main Menu", menu_options)
        
        if choice == '1':
            run_diagnostics_menu(adapter_info)
        elif choice == '2':
            fix_issues_menu(adapter_info)
        elif choice == '3':
            advanced_options_menu(adapter_info)
        elif choice == '4':
            scan_networks_menu(adapter_info)
        elif choice == 'a':
            display_about()
        elif choice == 'q':
            clear_screen()
            display_message("\nExiting Intel WiFi Fixer. Goodbye!", color='cyan')
            print()
            sys.exit(0)
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def run_diagnostics_menu(adapter_info):
    """Run diagnostics and display results."""
    clear_screen()
    display_banner()
    display_header("Running Diagnostics")
    display_message("Analyzing your Intel Centrino Advanced-N 6205 adapter...", color='cyan')
    
    # Gather diagnostics
    diagnostics = gather_diagnostics()
    
    # Display diagnostics in a more professional format
    print("\nDiagnostic Report for Intel Centrino Advanced-N 6205:")
    print("═" * 70)
    
    # Convert diagnostics to table format
    headers = ["Parameter", "Status"]
    data = []
    
    for key, value in diagnostics.items():
        # Add color indicators based on status
        status_value = value
        if key == "Adapter Status" and value == "Connected":
            status_value = "Connected ✓"
        elif key == "Adapter Status" and value == "Disconnected":
            status_value = "Disconnected ✗"
        elif key == "RFKill Status" and value == "Not blocked":
            status_value = "Not blocked ✓"
        elif key == "RFKill Status" and value != "Not blocked":
            status_value = f"{value} ✗"
        elif key == "Driver Status" and value == "Driver loaded":
            status_value = "Driver loaded ✓"
        elif key == "NetworkManager Status" and value == "Running":
            status_value = "Running ✓"
        elif key == "NetworkManager Status" and value != "Running":
            status_value = f"{value} ✗"
        elif key == "WPA Supplicant Status" and value == "Running":
            status_value = "Running ✓"
        elif key == "WPA Supplicant Status" and value != "Running":
            status_value = f"{value} ✗"
        elif key == "Interface Status" and value == "Up":
            status_value = "Up ✓"
        elif key == "Interface Status" and value != "Up":
            status_value = f"{value} ✗"
            
        data.append([key, status_value])
    
    # Display the diagnostics table
    display_table(headers, data)
    
    # Run diagnostics to identify issues
    issues = run_diagnostics(adapter_info)
    
    if issues:
        print("\n")
        display_warning("Issues detected:")
        
        # Display issues in a more structured format
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n")
        if get_user_choice("Would you like to apply fixes? (y/n): "):
            print("\n")
            apply_all_fixes(issues, adapter_info)
            display_success("Fixes applied. Please check if your issues are resolved.")
        else:
            display_message("No fixes applied.", color='yellow')
    else:
        print("\n")
        display_success("No issues detected. Your Intel Centrino Advanced-N 6205 is functioning properly.")
    
    # Display footer
    display_footer()
    
    input("\nPress Enter to return to the main menu...")

def fix_issues_menu(adapter_info):
    """Menu for fixing common issues."""
    while True:
        # Define menu options
        menu_options = [
            ('1', 'Fix All Issues'),
            ('2', 'Update Firmware'),
            ('3', 'Configure Driver Parameters'),
            ('4', 'Restart wpa_supplicant Service'),
            ('5', 'Scan for Networks'),
            ('b', 'Back to Main Menu')
        ]
        
        # Display the menu and get user choice
        choice = display_menu("Fix Common Issues", menu_options)
        
        if choice == '1':
            clear_screen()
            display_header("Fixing All Issues")
            issues = run_diagnostics(adapter_info)
            apply_all_fixes(issues, adapter_info)
            display_success("All fixes applied. Please check if your issues are resolved.")
            input("\nPress Enter to continue...")
        elif choice == '2':
            clear_screen()
            display_header("Updating Firmware")
            update_firmware(adapter_info)
            input("\nPress Enter to continue...")
        elif choice == '3':
            clear_screen()
            display_header("Configuring Driver Parameters")
            configure_driver(adapter_info)
            input("\nPress Enter to continue...")
        elif choice == '4':
            clear_screen()
            display_header("Restarting wpa_supplicant Service")
            from src.fixes import restart_wpa_supplicant
            restart_wpa_supplicant(adapter_info)
            input("\nPress Enter to continue...")
        elif choice == '5':
            scan_networks_menu(adapter_info)
        elif choice == 'b':
            return
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def advanced_options_menu(adapter_info):
    """Menu for advanced options."""
    while True:
        # Define menu options
        menu_options = [
            ('1', 'Configure Enterprise WiFi'),
            ('2', 'Manage Multiple Connections'),
            ('3', 'Set Regulatory Domain'),
            ('4', 'Handle Captive Portal'),
            ('5', 'Advanced Troubleshooting'),
            ('b', 'Back to Main Menu')
        ]
        
        # Display the menu and get user choice
        choice = display_menu("Advanced Options", menu_options)
        
        if choice == '1':
            if enterprise_wifi_menu:
                enterprise_wifi_menu()
            else:
                clear_screen()
                display_header("Enterprise WiFi Configuration")
                display_error("Enterprise WiFi module not found.")
                input("\nPress Enter to continue...")
        elif choice == '2':
            if multi_connection_menu:
                multi_connection_menu()
            else:
                clear_screen()
                display_header("Multiple Connection Management")
                display_error("Multi-connection management module not found.")
                input("\nPress Enter to continue...")
        elif choice == '3':
            if regulatory_domain_menu:
                regulatory_domain_menu()
            else:
                clear_screen()
                display_header("Regulatory Domain Configuration")
                display_error("Regulatory domain module not found.")
                input("\nPress Enter to continue...")
        elif choice == '4':
            if captive_portal_menu:
                captive_portal_menu()
            else:
                clear_screen()
                display_header("Captive Portal Handling")
                display_error("Captive portal module not found.")
                input("\nPress Enter to continue...")
        elif choice == '5':
            if troubleshooting_menu:
                troubleshooting_menu()
            else:
                clear_screen()
                display_header("Advanced Troubleshooting")
                display_error("Advanced troubleshooting module not found.")
                input("\nPress Enter to continue...")
        elif choice == 'b':
            return
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def scan_networks_menu(adapter_info):
    """Scan for available WiFi networks."""
    clear_screen()
    display_banner()
    display_header("Scanning for Networks")
    display_message("Scanning for available WiFi networks...", color='cyan')
    
    networks = scan_networks(adapter_info)
    
    if networks:
        # Find the network with the strongest signal for recommendation
        strongest_network = max(networks, key=lambda x: int(x.get('signal_strength', 0)) if x.get('signal_strength', '').isdigit() else 0)
        
        # Prepare data for table display
        headers = ["#", "SSID", "Security", "Signal", "Channel", "Band", "Speed"]
        data = []
        
        for i, network in enumerate(networks):
            # Truncate SSID if too long
            ssid = network['ssid'][:20] + "..." if len(network['ssid']) > 23 else network['ssid']
            
            # Format signal strength with color indicators
            signal_strength = int(network['signal_strength']) if network['signal_strength'].isdigit() else 0
            signal_quality = ""
            if signal_strength >= 70:
                signal_quality = "Excellent"
            elif signal_strength >= 50:
                signal_quality = "Good"
            elif signal_strength >= 30:
                signal_quality = "Fair"
            else:
                signal_quality = "Poor"
                
            # Add row to data
            data.append([
                i+1,
                ssid,
                network['security'][:10],
                f"{network['signal']} ({signal_quality})",
                network['channel'],
                network['band'],
                network['speed']
            ])
        
        print("\n")
        display_table(headers, data)
        
        # Display recommendation
        recommended = f"{strongest_network['ssid']} (Ch {strongest_network['channel']})"
        print(f"\nTotal networks: {len(networks)}")
        print(f"Recommended network: {recommended[:50]}")
        
        # Display footer
        display_footer()
        
        choice = input("\nEnter number to connect, 'r' to rescan, or 'b' to go back: ").strip().lower()
        
        if choice == 'r':
            return scan_networks_menu(adapter_info)
        elif choice == 'b':
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(networks):
            selected_network = networks[int(choice) - 1]
            ssid = selected_network['ssid']
            
            clear_screen()
            display_header(f"Connecting to {ssid}")
            
            # Implement connection logic here
            print(f"\nAttempting to connect to {ssid}...")
            display_message(f"Connection to {ssid} not yet implemented.", color='yellow')
            input("\nPress Enter to continue...")
        else:
            display_error("Invalid selection.")
            time.sleep(1)
            return scan_networks_menu(adapter_info)
    else:
        display_warning("No networks found or scanning failed.")
    
    input("\nPress Enter to return to the previous menu...")

if __name__ == "__main__":
    try:
        # Check if running with sudo/admin privileges
        if os.geteuid() != 0:
            display_error("This program requires administrative privileges.")
            display_message("Please run with sudo or as administrator.", color='yellow')
            sys.exit(1)
        
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)