"""
Advanced Troubleshooting UI Module

This module provides a user interface for advanced troubleshooting.
"""

import os
import time
from src.utils.ui_helpers import display_header, display_message, display_success, display_error, display_warning
from src.troubleshooting import (
    capture_wifi_traffic,
    analyze_wifi_interference,
    diagnose_connection_timing,
    check_driver_debug_info,
    check_system_logs,
    run_network_diagnostics
)
from src.fixes import restart_wpa_supplicant

def troubleshooting_menu():
    """Display the advanced troubleshooting menu."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_header("Advanced Troubleshooting")
        
        print("\n1. Capture WiFi Traffic")
        print("2. Analyze WiFi Interference")
        print("3. Diagnose Connection Timing")
        print("4. Check Driver Debug Information")
        print("5. Check System Logs")
        print("6. Run Comprehensive Network Diagnostics")
        print("7. Restart wpa_supplicant Service")
        print("b. Back to Advanced Options")
        
        choice = input("\nSelect an option: ").strip().lower()
        
        if choice == '1':
            capture_traffic_menu()
        elif choice == '2':
            analyze_interference_menu()
        elif choice == '3':
            diagnose_timing_menu()
        elif choice == '4':
            check_debug_info_menu()
        elif choice == '5':
            check_logs_menu()
        elif choice == '6':
            run_diagnostics_menu()
        elif choice == '7':
            restart_wpa_supplicant_menu()
        elif choice == 'b':
            break
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def capture_traffic_menu():
    """Menu for capturing WiFi traffic."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Capture WiFi Traffic")
    
    print("\nThis will capture WiFi traffic using tcpdump.")
    print("The capture will be saved to your home directory.")
    
    interface = input("\nEnter the wireless interface (default: wlan0): ").strip() or "wlan0"
    
    try:
        duration = int(input("Enter the capture duration in seconds (default: 30): ").strip() or "30")
    except ValueError:
        duration = 30
    
    filename = input("Enter the filename (default: auto-generated): ").strip() or None
    
    if input("\nStart capture? (y/n): ").strip().lower().startswith('y'):
        capture_path = capture_wifi_traffic(interface, duration, filename)
        
        if capture_path:
            print(f"\nCapture saved to: {capture_path}")
            print("\nYou can analyze this capture using Wireshark or other packet analysis tools.")
    
    input("\nPress Enter to continue...")

def analyze_interference_menu():
    """Menu for analyzing WiFi interference."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Analyze WiFi Interference")
    
    print("\nAnalyzing WiFi interference from nearby networks...")
    interference = analyze_wifi_interference()
    
    if interference["networks"]:
        print("\nNearby Networks:")
        for network in interference["networks"]:
            print(f"  {network['ssid']} (Channel {network['channel']}, Signal {network['signal']}%)")
        
        print("\nChannel Congestion:")
        for channel, count in interference["channels"].items():
            print(f"  Channel {channel}: {count} networks")
        
        if interference["recommendations"]:
            print("\nRecommendations:")
            for recommendation in interference["recommendations"]:
                print(f"  {recommendation}")
    else:
        display_warning("No nearby networks detected.")
    
    input("\nPress Enter to continue...")

def diagnose_timing_menu():
    """Menu for diagnosing connection timing."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Diagnose Connection Timing")
    
    print("\nThis will disconnect and reconnect to your WiFi network")
    print("to measure connection timing.")
    
    if input("\nContinue? (y/n): ").strip().lower().startswith('y'):
        print("\nDiagnosing connection timing...")
        timing = diagnose_connection_timing()
        
        if timing["connected"]:
            print("\nConnection Timing:")
            print(f"  Total Connection Time: {timing['connection_time']:.2f} seconds")
            
            if timing["dhcp_time"]:
                print(f"  DHCP Time: {timing['dhcp_time']:.2f} seconds")
            else:
                print("  DHCP Time: Unknown")
            
            if timing["dns_time"]:
                print(f"  DNS Resolution Time: {timing['dns_time']:.2f} seconds")
            else:
                print("  DNS Resolution Time: Unknown")
            
            if timing["connection_time"] > 5:
                display_warning("Connection time is longer than expected.")
                print("\nPossible issues:")
                print("1. Weak signal strength")
                print("2. Network congestion")
                print("3. DHCP server issues")
                print("4. Driver or firmware issues")
        else:
            display_error("Failed to reconnect to the network.")
    
    input("\nPress Enter to continue...")

def check_debug_info_menu():
    """Menu for checking driver debug information."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Check Driver Debug Information")
    
    print("\nRetrieving driver debug information...")
    debug_info = check_driver_debug_info()
    
    print("\nDriver Debug Information:")
    print(debug_info)
    
    input("\nPress Enter to continue...")

def check_logs_menu():
    """Menu for checking system logs."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Check System Logs")
    
    print("\nRetrieving WiFi-related system logs...")
    logs = check_system_logs()
    
    print("\nSystem Logs:")
    print(logs)
    
    input("\nPress Enter to continue...")

def run_diagnostics_menu():
    """Menu for running comprehensive network diagnostics."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Comprehensive Network Diagnostics")
    
    print("\nRunning comprehensive network diagnostics...")
    diagnostics = run_network_diagnostics()
    
    if diagnostics:
        print("\nNetwork Diagnostics:")
        print(f"  Interface Status: {diagnostics.get('interface_status', 'Unknown')}")
        print(f"  IP Address: {diagnostics.get('ip_address', 'Unknown')}")
        print(f"  Default Gateway: {diagnostics.get('default_gateway', 'Unknown')}")
        print(f"  DNS Servers: {', '.join(diagnostics.get('dns_servers', ['Unknown']))}")
        print(f"  Gateway Ping: {diagnostics.get('gateway_ping', 'Unknown')}")
        print(f"  Internet Ping: {diagnostics.get('internet_ping', 'Unknown')}")
        print(f"  DNS Resolution: {diagnostics.get('dns_resolution', 'Unknown')}")
        print(f"  Signal Strength: {diagnostics.get('signal_strength', 'Unknown')}")
        print(f"  Connection Speed: {diagnostics.get('connection_speed', 'Unknown')}")
        
        # Identify issues
        issues = []
        
        if diagnostics.get('interface_status') != "UP":
            issues.append("Interface is down")
        
        if diagnostics.get('ip_address') == "None":
            issues.append("No IP address assigned")
        
        if diagnostics.get('default_gateway') == "None":
            issues.append("No default gateway")
        
        if diagnostics.get('dns_servers') == ["None"]:
            issues.append("No DNS servers configured")
        
        if diagnostics.get('gateway_ping') == "Failed":
            issues.append("Cannot ping gateway")
        
        if diagnostics.get('internet_ping') == "Failed":
            issues.append("Cannot ping internet")
        
        if diagnostics.get('dns_resolution') == "Failed":
            issues.append("DNS resolution failed")
        
        if diagnostics.get('signal_strength', "Unknown") != "Unknown":
            try:
                signal = int(diagnostics.get('signal_strength').split()[0])
                if signal < -70:
                    issues.append("Weak signal strength")
            except (ValueError, IndexError):
                pass
        
        if issues:
            print("\nIdentified Issues:")
            for issue in issues:
                print(f"  - {issue}")
            
            print("\nRecommendations:")
            if "Interface is down" in issues:
                print("  - Bring the interface up with 'sudo ip link set wlan0 up'")
            
            if "No IP address assigned" in issues:
                print("  - Check DHCP configuration or set a static IP")
            
            if "No default gateway" in issues or "Cannot ping gateway" in issues:
                print("  - Check router connectivity and configuration")
            
            if "No DNS servers configured" in issues or "DNS resolution failed" in issues:
                print("  - Check DNS configuration or use alternative DNS servers")
            
            if "Weak signal strength" in issues:
                print("  - Move closer to the access point or use a WiFi extender")
        else:
            display_success("No issues identified in the network diagnostics.")
    else:
        display_error("Failed to run network diagnostics.")
    
    input("\nPress Enter to continue...")

def restart_wpa_supplicant_menu():
    """Menu for restarting the wpa_supplicant service."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Restart wpa_supplicant Service")
    
    print("\nThis will restart the wpa_supplicant service.")
    print("This can help resolve authentication and connection issues.")
    
    if input("\nContinue? (y/n): ").strip().lower().startswith('y'):
        print("\nRestarting wpa_supplicant service...")
        if restart_wpa_supplicant():
            display_success("wpa_supplicant service restarted successfully.")
            print("\nIf you were experiencing connection issues, try reconnecting to your WiFi network.")
        else:
            display_error("Failed to restart wpa_supplicant service.")
            print("\nYou may need to check if the service is installed or try restarting it manually.")
    
    input("\nPress Enter to continue...")