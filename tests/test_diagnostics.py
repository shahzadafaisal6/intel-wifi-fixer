import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.diagnostics import (
    check_adapter_status,
    check_rfkill,
    check_driver_status,
    check_firmware_version,
    check_signal_strength,
    check_network_manager_status,
    check_interface_status,
    check_driver_parameters,
    gather_diagnostics,
    identify_issues
)

class TestDiagnostics(unittest.TestCase):

    @patch('src.diagnostics.run_command')
    def test_check_adapter_status(self, mock_run_command):
        # Test connected status
        mock_run_command.return_value = "wlan0: connected to MyWiFi"
        status = check_adapter_status()
        self.assertEqual(status, "Connected")
        
        # Test disconnected status
        mock_run_command.return_value = "wlan0: disconnected"
        status = check_adapter_status()
        self.assertEqual(status, "Disconnected")
        
        # Test error handling
        mock_run_command.side_effect = Exception("Command failed")
        status = check_adapter_status()
        self.assertEqual(status, "Unknown")

    @patch('src.diagnostics.run_command')
    def test_check_rfkill(self, mock_run_command):
        # Test not blocked
        mock_run_command.return_value = "Soft blocked: no\nHard blocked: no"
        status = check_rfkill()
        self.assertEqual(status, "Not blocked")
        
        # Test soft blocked
        mock_run_command.return_value = "Soft blocked: yes\nHard blocked: no"
        status = check_rfkill()
        self.assertEqual(status, "Soft blocked")
        
        # Test hard blocked
        mock_run_command.return_value = "Soft blocked: no\nHard blocked: yes"
        status = check_rfkill()
        self.assertEqual(status, "Hard blocked")
        
        # Test error handling
        mock_run_command.side_effect = Exception("Command failed")
        status = check_rfkill()
        self.assertEqual(status, "Not blocked")

    @patch('src.diagnostics.run_command')
    def test_check_driver_status(self, mock_run_command):
        # Test driver loaded
        mock_run_command.return_value = "iwlwifi 123456 0 - Live 0xffffffffa0000000"
        status = check_driver_status()
        self.assertEqual(status, "Driver loaded")
        
        # Test driver not loaded
        mock_run_command.return_value = "other_module 123456 0 - Live 0xffffffffa0000000"
        status = check_driver_status()
        self.assertEqual(status, "Driver not loaded")
        
        # Test error handling
        mock_run_command.side_effect = Exception("Command failed")
        status = check_driver_status()
        self.assertEqual(status, "Driver not loaded")

    @patch('src.diagnostics.run_command')
    def test_check_firmware_version(self, mock_run_command):
        # Test firmware version found
        mock_run_command.return_value = "iwlwifi 0000:24:00.0: loaded firmware version 18.168.6.1"
        version = check_firmware_version()
        self.assertEqual(version, "18.168.6.1")
        
        # Test firmware version not found
        mock_run_command.return_value = "iwlwifi 0000:24:00.0: some other message"
        version = check_firmware_version()
        self.assertEqual(version, "Unknown")
        
        # Test error handling
        mock_run_command.side_effect = Exception("Command failed")
        version = check_firmware_version()
        self.assertEqual(version, "Unknown")

    @patch('src.diagnostics.gather_diagnostics')
    def test_identify_issues(self, mock_gather_diagnostics):
        # Test with no issues
        mock_gather_diagnostics.return_value = {
            "Adapter Status": "Connected",
            "RFKill Status": "Not blocked",
            "Driver Status": "Driver loaded",
            "Firmware Version": "18.168.6.1",
            "Signal Strength": "80%",
            "NetworkManager Status": "Running",
            "Interface Status": "Up",
            "Driver Parameters": "options iwlwifi 11n_disable=1 power_save=0"
        }
        issues = identify_issues(mock_gather_diagnostics.return_value)
        self.assertEqual(len(issues), 0)
        
        # Test with multiple issues
        mock_gather_diagnostics.return_value = {
            "Adapter Status": "Disconnected",
            "RFKill Status": "Soft blocked",
            "Driver Status": "Driver not loaded",
            "Firmware Version": "Unknown",
            "Signal Strength": "0%",
            "NetworkManager Status": "Not running",
            "Interface Status": "Down",
            "Driver Parameters": "No custom parameters set"
        }
        issues = identify_issues(mock_gather_diagnostics.return_value)
        self.assertGreater(len(issues), 0)
        self.assertIn("WiFi adapter is disconnected", issues)
        self.assertIn("WiFi is blocked by rfkill", issues)
        self.assertIn("WiFi driver is not loaded", issues)

if __name__ == '__main__':
    unittest.main()