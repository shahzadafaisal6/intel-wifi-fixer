"""
Multi-Connection Management UI Module

This module provides a user interface for managing multiple WiFi connections.
"""

import os
import time
from utils.ui_helpers import display_header, display_message, display_success, display_error, display_warning
from multi_connection import (
    list_connections,
    get_connection_details,
    activate_connection,
    deactivate_connection,
    delete_connection,
    configure_load_balancing,
    configure_failover,
    configure_traffic_routing
)

def multi_connection_menu():
    """Display the multi-connection management menu."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_header("Multi-Connection Management")
        
        # List current connections
        connections = list_connections()
        
        if connections:
            print("\nConfigured WiFi Connections:")
            for i, conn in enumerate(connections, 1):
                status = "Active" if conn["active"] else "Inactive"
                device = conn["device"] if conn["device"] != "None" else "Not connected"
                print(f"{i}. {conn['name']} ({status} on {device})")
        else:
            print("\nNo WiFi connections configured.")
        
        print("\n1. Activate Connection")
        print("2. Deactivate Connection")
        print("3. Delete Connection")
        print("4. Configure Load Balancing")
        print("5. Configure Failover")
        print("6. Configure Traffic Routing")
        print("b. Back to Advanced Options")
        
        choice = input("\nSelect an option: ").strip().lower()
        
        if choice == '1':
            activate_connection_menu(connections)
        elif choice == '2':
            deactivate_connection_menu(connections)
        elif choice == '3':
            delete_connection_menu(connections)
        elif choice == '4':
            configure_load_balancing_menu(connections)
        elif choice == '5':
            configure_failover_menu(connections)
        elif choice == '6':
            configure_traffic_routing_menu(connections)
        elif choice == 'b':
            break
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def activate_connection_menu(connections):
    """Menu for activating a connection."""
    if not connections:
        display_warning("No WiFi connections configured.")
        input("\nPress Enter to continue...")
        return
    
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Activate Connection")
    
    print("\nSelect a connection to activate:")
    for i, conn in enumerate(connections, 1):
        status = "Active" if conn["active"] else "Inactive"
        print(f"{i}. {conn['name']} ({status})")
    
    choice = input("\nEnter connection number: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(connections):
        connection = connections[int(choice) - 1]
        
        if connection["active"]:
            display_warning(f"Connection {connection['name']} is already active.")
        else:
            device = input("\nEnter device name (default: wlan0): ").strip() or "wlan0"
            activate_connection(connection["name"], device)
    else:
        display_error("Invalid selection.")
    
    input("\nPress Enter to continue...")

def deactivate_connection_menu(connections):
    """Menu for deactivating a connection."""
    active_connections = [conn for conn in connections if conn["active"]]
    
    if not active_connections:
        display_warning("No active WiFi connections.")
        input("\nPress Enter to continue...")
        return
    
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Deactivate Connection")
    
    print("\nSelect a connection to deactivate:")
    for i, conn in enumerate(active_connections, 1):
        print(f"{i}. {conn['name']} (Active on {conn['device']})")
    
    choice = input("\nEnter connection number: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(active_connections):
        connection = active_connections[int(choice) - 1]
        deactivate_connection(connection["name"])
    else:
        display_error("Invalid selection.")
    
    input("\nPress Enter to continue...")

def delete_connection_menu(connections):
    """Menu for deleting a connection."""
    if not connections:
        display_warning("No WiFi connections configured.")
        input("\nPress Enter to continue...")
        return
    
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Delete Connection")
    
    print("\nSelect a connection to delete:")
    for i, conn in enumerate(connections, 1):
        status = "Active" if conn["active"] else "Inactive"
        print(f"{i}. {conn['name']} ({status})")
    
    choice = input("\nEnter connection number: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(connections):
        connection = connections[int(choice) - 1]
        
        if connection["active"]:
            display_warning(f"Connection {connection['name']} is active. Deactivate it first.")
            
            if input("\nDeactivate and delete? (y/n): ").strip().lower().startswith('y'):
                deactivate_connection(connection["name"])
                delete_connection(connection["name"])
        else:
            if input(f"\nAre you sure you want to delete {connection['name']}? (y/n): ").strip().lower().startswith('y'):
                delete_connection(connection["name"])
    else:
        display_error("Invalid selection.")
    
    input("\nPress Enter to continue...")

def configure_load_balancing_menu(connections):
    """Menu for configuring load balancing."""
    if len(connections) < 2:
        display_warning("At least two WiFi connections are required for load balancing.")
        input("\nPress Enter to continue...")
        return
    
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Configure Load Balancing")
    
    print("\nSelect connections for load balancing:")
    for i, conn in enumerate(connections, 1):
        status = "Active" if conn["active"] else "Inactive"
        print(f"{i}. {conn['name']} ({status})")
    
    print("\nEnter connection numbers separated by commas (e.g., 1,3):")
    choices = input().strip()
    
    selected_connections = []
    for choice in choices.split(','):
        if choice.strip().isdigit() and 1 <= int(choice.strip()) <= len(connections):
            selected_connections.append(connections[int(choice.strip()) - 1]["name"])
    
    if len(selected_connections) < 2:
        display_error("At least two connections must be selected.")
    else:
        print(f"\nSelected connections: {', '.join(selected_connections)}")
        
        if input("\nConfigure load balancing for these connections? (y/n): ").strip().lower().startswith('y'):
            configure_load_balancing(selected_connections)
    
    input("\nPress Enter to continue...")

def configure_failover_menu(connections):
    """Menu for configuring failover."""
    if len(connections) < 2:
        display_warning("At least two WiFi connections are required for failover.")
        input("\nPress Enter to continue...")
        return
    
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Configure Failover")
    
    print("\nSelect primary connection:")
    for i, conn in enumerate(connections, 1):
        status = "Active" if conn["active"] else "Inactive"
        print(f"{i}. {conn['name']} ({status})")
    
    primary_choice = input("\nEnter primary connection number: ").strip()
    
    if not primary_choice.isdigit() or int(primary_choice) < 1 or int(primary_choice) > len(connections):
        display_error("Invalid primary connection selection.")
        input("\nPress Enter to continue...")
        return
    
    primary_connection = connections[int(primary_choice) - 1]["name"]
    
    print(f"\nPrimary connection: {primary_connection}")
    print("\nSelect backup connection:")
    
    for i, conn in enumerate(connections, 1):
        if conn["name"] != primary_connection:
            status = "Active" if conn["active"] else "Inactive"
            print(f"{i}. {conn['name']} ({status})")
    
    backup_choice = input("\nEnter backup connection number: ").strip()
    
    if not backup_choice.isdigit() or int(backup_choice) < 1 or int(backup_choice) > len(connections):
        display_error("Invalid backup connection selection.")
        input("\nPress Enter to continue...")
        return
    
    backup_connection = connections[int(backup_choice) - 1]["name"]
    
    if backup_connection == primary_connection:
        display_error("Backup connection cannot be the same as primary connection.")
    else:
        print(f"\nPrimary connection: {primary_connection}")
        print(f"Backup connection: {backup_connection}")
        
        if input("\nConfigure failover between these connections? (y/n): ").strip().lower().startswith('y'):
            configure_failover(primary_connection, backup_connection)
    
    input("\nPress Enter to continue...")

def configure_traffic_routing_menu(connections):
    """Menu for configuring traffic routing."""
    if not connections:
        display_warning("No WiFi connections configured.")
        input("\nPress Enter to continue...")
        return
    
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Configure Traffic Routing")
    
    print("\nSelect a connection for traffic routing:")
    for i, conn in enumerate(connections, 1):
        status = "Active" if conn["active"] else "Inactive"
        print(f"{i}. {conn['name']} ({status})")
    
    choice = input("\nEnter connection number: ").strip()
    
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(connections):
        display_error("Invalid connection selection.")
        input("\nPress Enter to continue...")
        return
    
    connection = connections[int(choice) - 1]["name"]
    
    print(f"\nConnection: {connection}")
    print("\nEnter application names separated by commas (e.g., firefox,chrome,vlc):")
    
    applications_input = input().strip()
    applications = [app.strip() for app in applications_input.split(',') if app.strip()]
    
    if not applications:
        display_error("No applications specified.")
    else:
        print(f"\nApplications: {', '.join(applications)}")
        
        if input("\nConfigure traffic routing for these applications? (y/n): ").strip().lower().startswith('y'):
            configure_traffic_routing(connection, applications)
    
    input("\nPress Enter to continue...")