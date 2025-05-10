"""
Enterprise WiFi Configuration UI Module

This module provides a user interface for configuring enterprise WiFi connections.
"""

import os
import time
from utils.ui_helpers import display_header, display_message, display_success, display_error, display_warning
from enterprise_wifi import (
    EAP_METHODS, 
    configure_enterprise_wifi, 
    verify_certificate, 
    list_enterprise_connections,
    delete_enterprise_connection,
    import_certificate,
    connect_to_enterprise_network
)

def enterprise_wifi_menu():
    """Display the enterprise WiFi configuration menu."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        display_header("Enterprise WiFi Configuration")
        
        print("\n1. Configure New Enterprise WiFi Connection")
        print("2. List Enterprise WiFi Connections")
        print("3. Connect to Enterprise WiFi Network")
        print("4. Delete Enterprise WiFi Connection")
        print("5. Import Certificate")
        print("6. Verify Certificate")
        print("b. Back to Main Menu")
        
        choice = input("\nSelect an option: ").strip().lower()
        
        if choice == '1':
            configure_new_connection()
        elif choice == '2':
            list_connections()
        elif choice == '3':
            connect_to_network()
        elif choice == '4':
            delete_connection()
        elif choice == '5':
            import_cert()
        elif choice == '6':
            verify_cert()
        elif choice == 'b':
            break
        else:
            display_error("Invalid option. Please try again.")
            time.sleep(1)

def configure_new_connection():
    """Configure a new enterprise WiFi connection."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Configure New Enterprise WiFi Connection")
    
    # Get SSID
    ssid = input("\nEnter the SSID of the enterprise network: ").strip()
    if not ssid:
        display_error("SSID cannot be empty.")
        time.sleep(1)
        return
    
    # Select EAP method
    print("\nSelect EAP method:")
    for key, method in EAP_METHODS.items():
        print(f"{key}. {method['name']}")
    
    eap_choice = input("\nSelect an option: ").strip()
    if eap_choice not in EAP_METHODS:
        display_error("Invalid EAP method selected.")
        time.sleep(1)
        return
    
    eap_method = EAP_METHODS[eap_choice]
    
    # Get username
    username = input("\nEnter username: ").strip()
    if not username:
        display_error("Username cannot be empty.")
        time.sleep(1)
        return
    
    # Get password (if needed)
    password = None
    if eap_method["value"] != "tls":
        password = input("\nEnter password: ").strip()
        if not password:
            display_warning("No password provided. Continuing anyway...")
    
    # Get certificate paths
    ca_cert = input("\nEnter path to CA certificate (leave empty if not needed): ").strip()
    
    client_cert = None
    private_key = None
    private_key_password = None
    
    if eap_method["value"] == "tls":
        client_cert = input("\nEnter path to client certificate: ").strip()
        if not client_cert:
            display_error("Client certificate is required for TLS authentication.")
            time.sleep(1)
            return
        
        private_key = input("\nEnter path to private key: ").strip()
        if not private_key:
            display_error("Private key is required for TLS authentication.")
            time.sleep(1)
            return
        
        private_key_password = input("\nEnter private key password (leave empty if not needed): ").strip()
    
    # Verify certificates if provided
    if ca_cert and not verify_certificate(ca_cert):
        if not input("\nContinue anyway? (y/n): ").strip().lower().startswith('y'):
            return
    
    if client_cert and not verify_certificate(client_cert):
        if not input("\nContinue anyway? (y/n): ").strip().lower().startswith('y'):
            return
    
    # Configure the connection
    success = configure_enterprise_wifi(
        ssid=ssid,
        eap_method=eap_method,
        username=username,
        password=password,
        ca_cert=ca_cert,
        client_cert=client_cert,
        private_key=private_key,
        private_key_password=private_key_password
    )
    
    if success:
        if input("\nDo you want to connect to this network now? (y/n): ").strip().lower().startswith('y'):
            connect_to_enterprise_network(f"{ssid}-enterprise")
    
    input("\nPress Enter to continue...")

def list_connections():
    """List all enterprise WiFi connections."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Enterprise WiFi Connections")
    
    connections = list_enterprise_connections()
    
    if connections:
        print("\nConfigured Enterprise WiFi Connections:")
        for i, conn in enumerate(connections, 1):
            print(f"{i}. {conn}")
    else:
        display_message("No enterprise WiFi connections configured.", color='yellow')
    
    input("\nPress Enter to continue...")

def connect_to_network():
    """Connect to an enterprise WiFi network."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Connect to Enterprise WiFi Network")
    
    connections = list_enterprise_connections()
    
    if not connections:
        display_message("No enterprise WiFi connections configured.", color='yellow')
        input("\nPress Enter to continue...")
        return
    
    print("\nAvailable Enterprise WiFi Connections:")
    for i, conn in enumerate(connections, 1):
        print(f"{i}. {conn}")
    
    choice = input("\nSelect a connection (number): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(connections):
        display_error("Invalid selection.")
        time.sleep(1)
        return
    
    connection_name = connections[int(choice) - 1]
    connect_to_enterprise_network(connection_name)
    
    input("\nPress Enter to continue...")

def delete_connection():
    """Delete an enterprise WiFi connection."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Delete Enterprise WiFi Connection")
    
    connections = list_enterprise_connections()
    
    if not connections:
        display_message("No enterprise WiFi connections configured.", color='yellow')
        input("\nPress Enter to continue...")
        return
    
    print("\nConfigured Enterprise WiFi Connections:")
    for i, conn in enumerate(connections, 1):
        print(f"{i}. {conn}")
    
    choice = input("\nSelect a connection to delete (number): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(connections):
        display_error("Invalid selection.")
        time.sleep(1)
        return
    
    connection_name = connections[int(choice) - 1]
    
    if input(f"\nAre you sure you want to delete {connection_name}? (y/n): ").strip().lower().startswith('y'):
        delete_enterprise_connection(connection_name)
    
    input("\nPress Enter to continue...")

def import_cert():
    """Import a certificate."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Import Certificate")
    
    print("\nSelect certificate type:")
    print("1. CA Certificate")
    print("2. Client Certificate")
    
    cert_type_choice = input("\nSelect an option: ").strip()
    
    if cert_type_choice not in ['1', '2']:
        display_error("Invalid certificate type selected.")
        time.sleep(1)
        return
    
    cert_type = "ca" if cert_type_choice == '1' else "client"
    
    cert_path = input("\nEnter path to certificate file: ").strip()
    if not cert_path:
        display_error("Certificate path cannot be empty.")
        time.sleep(1)
        return
    
    import_certificate(cert_path, cert_type)
    
    input("\nPress Enter to continue...")

def verify_cert():
    """Verify a certificate."""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_header("Verify Certificate")
    
    cert_path = input("\nEnter path to certificate file: ").strip()
    if not cert_path:
        display_error("Certificate path cannot be empty.")
        time.sleep(1)
        return
    
    verify_certificate(cert_path)
    
    input("\nPress Enter to continue...")