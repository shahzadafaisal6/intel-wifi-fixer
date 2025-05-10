"""
Enterprise WiFi Configuration Module

This module provides functionality for configuring enterprise WiFi connections
including EAP-TLS, PEAP, and TTLS authentication methods.
"""

import os
import re
import time
from utils.command_runner import run_command, execute_with_sudo
from utils.ui_helpers import display_message, display_success, display_error, display_warning

# Define supported EAP methods
EAP_METHODS = {
    "1": {"name": "PEAP (MSCHAPv2)", "value": "peap", "inner_auth": "mschapv2"},
    "2": {"name": "TTLS (PAP)", "value": "ttls", "inner_auth": "pap"},
    "3": {"name": "TTLS (MSCHAPv2)", "value": "ttls", "inner_auth": "mschapv2"},
    "4": {"name": "TLS", "value": "tls", "inner_auth": None}
}

def configure_enterprise_wifi(ssid, eap_method, username=None, password=None, 
                             ca_cert=None, client_cert=None, private_key=None, 
                             private_key_password=None):
    """
    Configure an enterprise WiFi connection.
    
    Args:
        ssid: The SSID of the network
        eap_method: The EAP method to use (peap, ttls, tls)
        username: The username for authentication
        password: The password for authentication
        ca_cert: Path to the CA certificate
        client_cert: Path to the client certificate (for TLS)
        private_key: Path to the private key (for TLS)
        private_key_password: Password for the private key (for TLS)
        
    Returns:
        bool: True if the configuration was successful, False otherwise
    """
    try:
        display_message(f"Configuring enterprise WiFi connection for {ssid}...", color='blue')
        
        # Build the nmcli command based on the EAP method
        cmd = ["nmcli", "connection", "add", "type", "wifi", "con-name", f"{ssid}-enterprise", 
               "ifname", "wlan0", "ssid", ssid, "wifi-sec.key-mgmt", "wpa-eap"]
        
        # Add EAP method specific configuration
        if eap_method["value"] == "peap" or eap_method["value"] == "ttls":
            cmd.extend(["802-1x.eap", eap_method["value"], 
                        "802-1x.phase2-auth", eap_method["inner_auth"],
                        "802-1x.identity", username])
            
            if password:
                cmd.extend(["802-1x.password", password])
            
            if ca_cert:
                cmd.extend(["802-1x.ca-cert", ca_cert])
                
        elif eap_method["value"] == "tls":
            cmd.extend(["802-1x.eap", "tls", 
                        "802-1x.identity", username])
            
            if ca_cert:
                cmd.extend(["802-1x.ca-cert", ca_cert])
            
            if client_cert:
                cmd.extend(["802-1x.client-cert", client_cert])
            
            if private_key:
                cmd.extend(["802-1x.private-key", private_key])
            
            if private_key_password:
                cmd.extend(["802-1x.private-key-password", private_key_password])
        
        # Execute the command
        result = execute_with_sudo(cmd)
        
        if result:
            display_success(f"Enterprise WiFi connection for {ssid} configured successfully.")
            return True
        else:
            display_error(f"Failed to configure enterprise WiFi connection for {ssid}.")
            return False
            
    except Exception as e:
        display_error(f"Error configuring enterprise WiFi: {str(e)}")
        return False

def verify_certificate(cert_path):
    """
    Verify that a certificate file is valid.
    
    Args:
        cert_path: Path to the certificate file
        
    Returns:
        bool: True if the certificate is valid, False otherwise
    """
    try:
        if not os.path.exists(cert_path):
            display_error(f"Certificate file not found: {cert_path}")
            return False
        
        # Use openssl to verify the certificate
        result = run_command(["openssl", "x509", "-in", cert_path, "-text", "-noout"])
        
        if result:
            display_success(f"Certificate is valid: {cert_path}")
            return True
        else:
            display_error(f"Invalid certificate: {cert_path}")
            return False
            
    except Exception as e:
        display_error(f"Error verifying certificate: {str(e)}")
        return False

def list_enterprise_connections():
    """
    List all configured enterprise WiFi connections.
    
    Returns:
        list: A list of enterprise connection names
    """
    try:
        # Get all connections
        output = run_command(["nmcli", "-t", "-f", "NAME,TYPE,802-1X.EAP", "connection", "show"])
        
        enterprise_connections = []
        if output:
            for line in output.strip().split('\n'):
                if line and "802-1x.eap" in line:
                    fields = line.split(':')
                    if len(fields) >= 2:
                        enterprise_connections.append(fields[0])
        
        return enterprise_connections
            
    except Exception as e:
        display_error(f"Error listing enterprise connections: {str(e)}")
        return []

def delete_enterprise_connection(connection_name):
    """
    Delete an enterprise WiFi connection.
    
    Args:
        connection_name: The name of the connection to delete
        
    Returns:
        bool: True if the deletion was successful, False otherwise
    """
    try:
        display_message(f"Deleting enterprise WiFi connection: {connection_name}...", color='blue')
        
        result = execute_with_sudo(["nmcli", "connection", "delete", connection_name])
        
        if result:
            display_success(f"Enterprise WiFi connection {connection_name} deleted successfully.")
            return True
        else:
            display_error(f"Failed to delete enterprise WiFi connection {connection_name}.")
            return False
            
    except Exception as e:
        display_error(f"Error deleting enterprise connection: {str(e)}")
        return False

def import_certificate(cert_path, cert_type="ca"):
    """
    Import a certificate into the system certificate store.
    
    Args:
        cert_path: Path to the certificate file
        cert_type: Type of certificate (ca, client)
        
    Returns:
        bool: True if the import was successful, False otherwise
    """
    try:
        display_message(f"Importing {cert_type} certificate from {cert_path}...", color='blue')
        
        if not os.path.exists(cert_path):
            display_error(f"Certificate file not found: {cert_path}")
            return False
        
        if cert_type == "ca":
            # Import CA certificate
            dest_path = "/usr/local/share/ca-certificates/"
            cert_name = os.path.basename(cert_path)
            
            # Copy the certificate to the CA certificates directory
            execute_with_sudo(["cp", cert_path, os.path.join(dest_path, cert_name)])
            
            # Update the CA certificate store
            result = execute_with_sudo(["update-ca-certificates"])
            
            if result:
                display_success(f"CA certificate imported successfully.")
                return True
            else:
                display_error(f"Failed to import CA certificate.")
                return False
        else:
            # For client certificates, just verify and return the path
            if verify_certificate(cert_path):
                display_success(f"Client certificate is valid and ready to use.")
                return True
            else:
                return False
            
    except Exception as e:
        display_error(f"Error importing certificate: {str(e)}")
        return False

def connect_to_enterprise_network(connection_name):
    """
    Connect to an enterprise WiFi network.
    
    Args:
        connection_name: The name of the connection to connect to
        
    Returns:
        bool: True if the connection was successful, False otherwise
    """
    try:
        display_message(f"Connecting to enterprise WiFi network: {connection_name}...", color='blue')
        
        # Activate the connection
        result = execute_with_sudo(["nmcli", "connection", "up", connection_name])
        
        if result:
            # Wait for the connection to establish
            time.sleep(5)
            
            # Check if the connection is active
            output = run_command(["nmcli", "-t", "-f", "ACTIVE", "connection", "show", connection_name])
            
            if output and "yes" in output.lower():
                display_success(f"Connected to enterprise WiFi network: {connection_name}")
                return True
            else:
                display_warning(f"Connection attempt completed, but connection may not be active.")
                return False
        else:
            display_error(f"Failed to connect to enterprise WiFi network: {connection_name}")
            return False
            
    except Exception as e:
        display_error(f"Error connecting to enterprise network: {str(e)}")
        return False