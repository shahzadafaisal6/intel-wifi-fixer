"""
Multi-Connection Management Module

This module provides functionality for managing multiple WiFi connections,
including load balancing and failover configuration.
"""

import os
import re
import time
import subprocess
from utils.command_runner import run_command, execute_with_sudo
from utils.ui_helpers import display_message, display_success, display_error, display_warning

def list_connections():
    """
    List all configured WiFi connections.
    
    Returns:
        list: A list of connection dictionaries
    """
    try:
        output = run_command(["nmcli", "-t", "-f", "NAME,TYPE,DEVICE,ACTIVE", "connection", "show"])
        
        connections = []
        if output:
            for line in output.strip().split('\n'):
                if line:
                    fields = line.split(':')
                    if len(fields) >= 4 and fields[1] == "wifi":
                        connections.append({
                            "name": fields[0],
                            "device": fields[2] if fields[2] else "None",
                            "active": fields[3] == "yes"
                        })
        
        return connections
            
    except Exception as e:
        display_error(f"Error listing connections: {str(e)}")
        return []

def get_connection_details(connection_name):
    """
    Get details of a specific connection.
    
    Args:
        connection_name: The name of the connection
        
    Returns:
        dict: A dictionary of connection details
    """
    try:
        output = run_command(["nmcli", "-t", "-f", "all", "connection", "show", connection_name])
        
        details = {}
        if output:
            for line in output.strip().split('\n'):
                if line and ":" in line:
                    key, value = line.split(':', 1)
                    details[key] = value
        
        return details
            
    except Exception as e:
        display_error(f"Error getting connection details: {str(e)}")
        return {}

def activate_connection(connection_name, device="wlan0"):
    """
    Activate a WiFi connection.
    
    Args:
        connection_name: The name of the connection
        device: The device to activate the connection on
        
    Returns:
        bool: True if the connection was activated successfully, False otherwise
    """
    try:
        display_message(f"Activating connection {connection_name} on {device}...", color='blue')
        
        result = execute_with_sudo(["nmcli", "connection", "up", connection_name, "ifname", device])
        
        if result:
            # Wait for the connection to establish
            time.sleep(5)
            
            # Check if the connection is active
            connections = list_connections()
            for conn in connections:
                if conn["name"] == connection_name and conn["active"]:
                    display_success(f"Connection {connection_name} activated successfully.")
                    return True
            
            display_warning(f"Connection {connection_name} may not be active.")
            return False
        else:
            display_error(f"Failed to activate connection {connection_name}.")
            return False
            
    except Exception as e:
        display_error(f"Error activating connection: {str(e)}")
        return False

def deactivate_connection(connection_name):
    """
    Deactivate a WiFi connection.
    
    Args:
        connection_name: The name of the connection
        
    Returns:
        bool: True if the connection was deactivated successfully, False otherwise
    """
    try:
        display_message(f"Deactivating connection {connection_name}...", color='blue')
        
        result = execute_with_sudo(["nmcli", "connection", "down", connection_name])
        
        if result:
            display_success(f"Connection {connection_name} deactivated successfully.")
            return True
        else:
            display_error(f"Failed to deactivate connection {connection_name}.")
            return False
            
    except Exception as e:
        display_error(f"Error deactivating connection: {str(e)}")
        return False

def delete_connection(connection_name):
    """
    Delete a WiFi connection.
    
    Args:
        connection_name: The name of the connection
        
    Returns:
        bool: True if the connection was deleted successfully, False otherwise
    """
    try:
        display_message(f"Deleting connection {connection_name}...", color='blue')
        
        result = execute_with_sudo(["nmcli", "connection", "delete", connection_name])
        
        if result:
            display_success(f"Connection {connection_name} deleted successfully.")
            return True
        else:
            display_error(f"Failed to delete connection {connection_name}.")
            return False
            
    except Exception as e:
        display_error(f"Error deleting connection: {str(e)}")
        return False

def configure_load_balancing(connections):
    """
    Configure load balancing between multiple WiFi connections.
    
    Args:
        connections: A list of connection names to load balance
        
    Returns:
        bool: True if load balancing was configured successfully, False otherwise
    """
    try:
        if len(connections) < 2:
            display_error("At least two connections are required for load balancing.")
            return False
        
        display_message(f"Configuring load balancing for {', '.join(connections)}...", color='blue')
        
        # Create a bond interface
        bond_name = "wifi-bond"
        
        # Check if the bond already exists
        bond_exists = run_command(["ip", "link", "show", bond_name])
        
        if not bond_exists:
            # Create the bond interface
            result = execute_with_sudo([
                "nmcli", "connection", "add", "type", "bond", "con-name", bond_name, 
                "ifname", bond_name, "bond.options", "mode=balance-rr"
            ])
            
            if not result:
                display_error("Failed to create bond interface.")
                return False
        
        # Add each connection to the bond
        for conn in connections:
            # Get the device for this connection
            conn_details = get_connection_details(conn)
            device = conn_details.get("GENERAL.DEVICES", "wlan0")
            
            # Create a bond slave connection
            slave_name = f"{conn}-bond-slave"
            
            # Check if the slave already exists
            slave_exists = run_command(["nmcli", "connection", "show", slave_name])
            
            if not slave_exists:
                result = execute_with_sudo([
                    "nmcli", "connection", "add", "type", "bond-slave", "con-name", slave_name,
                    "ifname", device, "master", bond_name
                ])
                
                if not result:
                    display_error(f"Failed to add {conn} to bond.")
                    return False
        
        # Activate the bond
        result = execute_with_sudo(["nmcli", "connection", "up", bond_name])
        
        if result:
            display_success("Load balancing configured successfully.")
            return True
        else:
            display_error("Failed to activate load balancing.")
            return False
            
    except Exception as e:
        display_error(f"Error configuring load balancing: {str(e)}")
        return False

def configure_failover(primary_connection, backup_connection):
    """
    Configure failover between a primary and backup WiFi connection.
    
    Args:
        primary_connection: The name of the primary connection
        backup_connection: The name of the backup connection
        
    Returns:
        bool: True if failover was configured successfully, False otherwise
    """
    try:
        display_message(f"Configuring failover from {primary_connection} to {backup_connection}...", color='blue')
        
        # Create a script to monitor the primary connection and switch to the backup if needed
        script_path = os.path.expanduser("~/wifi-failover.sh")
        
        script_content = f"""#!/bin/bash

# WiFi Failover Script
# This script monitors the primary WiFi connection and switches to the backup if needed

PRIMARY="{primary_connection}"
BACKUP="{backup_connection}"
PING_TARGET="8.8.8.8"
PING_COUNT=3
PING_TIMEOUT=5
CHECK_INTERVAL=60

while true; do
    # Check if the primary connection is active
    PRIMARY_ACTIVE=$(nmcli -t -f ACTIVE connection show "$PRIMARY" | grep "yes")
    
    if [ -n "$PRIMARY_ACTIVE" ]; then
        # Primary is active, check if it has internet connectivity
        ping -c $PING_COUNT -W $PING_TIMEOUT $PING_TARGET > /dev/null 2>&1
        
        if [ $? -ne 0 ]; then
            # Primary has no internet connectivity, switch to backup
            echo "$(date): Primary connection lost internet connectivity. Switching to backup."
            nmcli connection down "$PRIMARY"
            sleep 2
            nmcli connection up "$BACKUP"
        fi
    else
        # Primary is not active, check if backup is active
        BACKUP_ACTIVE=$(nmcli -t -f ACTIVE connection show "$BACKUP" | grep "yes")
        
        if [ -n "$BACKUP_ACTIVE" ]; then
            # Backup is active, try to switch back to primary
            ping -c $PING_COUNT -W $PING_TIMEOUT $PING_TARGET > /dev/null 2>&1
            
            if [ $? -eq 0 ]; then
                # Backup has internet connectivity, try to reconnect to primary
                echo "$(date): Attempting to switch back to primary connection."
                nmcli connection up "$PRIMARY"
                
                # Wait for primary to connect
                sleep 10
                
                # Check if primary is now active
                PRIMARY_ACTIVE=$(nmcli -t -f ACTIVE connection show "$PRIMARY" | grep "yes")
                
                if [ -n "$PRIMARY_ACTIVE" ]; then
                    # Primary is active, deactivate backup
                    echo "$(date): Primary connection restored. Deactivating backup."
                    nmcli connection down "$BACKUP"
                fi
            fi
        else
            # Neither connection is active, try to connect to primary
            echo "$(date): No active connection. Attempting to connect to primary."
            nmcli connection up "$PRIMARY"
            
            # Wait for primary to connect
            sleep 10
            
            # Check if primary is now active
            PRIMARY_ACTIVE=$(nmcli -t -f ACTIVE connection show "$PRIMARY" | grep "yes")
            
            if [ -z "$PRIMARY_ACTIVE" ]; then
                # Primary failed to connect, try backup
                echo "$(date): Primary connection failed. Attempting to connect to backup."
                nmcli connection up "$BACKUP"
            fi
        fi
    fi
    
    # Wait before checking again
    sleep $CHECK_INTERVAL
done
"""
        
        # Write the script to a file
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make the script executable
        os.chmod(script_path, 0o755)
        
        # Create a systemd service to run the script
        service_path = "/etc/systemd/system/wifi-failover.service"
        
        service_content = f"""[Unit]
Description=WiFi Failover Service
After=network.target

[Service]
ExecStart={script_path}
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
        
        # Write the service file
        execute_with_sudo(["bash", "-c", f"echo '{service_content}' > {service_path}"])
        
        # Reload systemd
        execute_with_sudo(["systemctl", "daemon-reload"])
        
        # Enable and start the service
        execute_with_sudo(["systemctl", "enable", "wifi-failover.service"])
        execute_with_sudo(["systemctl", "start", "wifi-failover.service"])
        
        display_success("Failover configured successfully.")
        return True
            
    except Exception as e:
        display_error(f"Error configuring failover: {str(e)}")
        return False

def configure_traffic_routing(connection, applications):
    """
    Configure traffic routing for specific applications through a specific connection.
    
    Args:
        connection: The name of the connection
        applications: A list of application names
        
    Returns:
        bool: True if routing was configured successfully, False otherwise
    """
    try:
        display_message(f"Configuring traffic routing for {', '.join(applications)} through {connection}...", color='blue')
        
        # Get the connection details
        conn_details = get_connection_details(connection)
        device = conn_details.get("GENERAL.DEVICES", "wlan0")
        
        # Create a routing table for this connection
        table_name = f"wifi_{device}"
        table_id = abs(hash(connection)) % 250 + 1  # Generate a table ID between 1 and 250
        
        # Add the table to /etc/iproute2/rt_tables
        execute_with_sudo(["bash", "-c", f"echo '{table_id} {table_name}' >> /etc/iproute2/rt_tables"])
        
        # Get the gateway for this connection
        gateway = None
        ip_route = run_command(["ip", "route", "show", "dev", device])
        if ip_route:
            gateway_match = re.search(r"default via ([\d.]+)", ip_route)
            if gateway_match:
                gateway = gateway_match.group(1)
        
        if not gateway:
            display_error(f"Could not determine gateway for {connection}.")
            return False
        
        # Add routing rules for this connection
        execute_with_sudo(["ip", "route", "add", "default", "via", gateway, "dev", device, "table", table_name])
        
        # Add rules for each application
        for app in applications:
            # Find the path to the application
            app_path = run_command(["which", app])
            
            if not app_path:
                display_warning(f"Could not find path for {app}. Skipping.")
                continue
            
            # Create a wrapper script for the application
            wrapper_path = os.path.expanduser(f"~/.local/bin/{app}_routed")
            
            wrapper_content = f"""#!/bin/bash

# Set the routing for this application
export DEVICE="{device}"
export TABLE="{table_name}"

# Run the application with the specified routing
exec ip route exec dev $DEVICE {app_path} "$@"
"""
            
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(wrapper_path), exist_ok=True)
            
            # Write the wrapper script
            with open(wrapper_path, 'w') as f:
                f.write(wrapper_content)
            
            # Make the wrapper script executable
            os.chmod(wrapper_path, 0o755)
            
            display_success(f"Created routing wrapper for {app} at {wrapper_path}")
        
        display_success("Traffic routing configured successfully.")
        display_message("To use routing, run the applications with their wrapper scripts.", color='blue')
        
        return True
            
    except Exception as e:
        display_error(f"Error configuring traffic routing: {str(e)}")
        return False