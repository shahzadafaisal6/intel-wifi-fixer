import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fixes import (
    reset_adapter,
    unblock_rfkill,
    restart_network_manager,
    configure_driver_parameters,
    update_firmware,
    configure_driver,
    scan_networks,
    apply_all_fixes
)

class TestFixes(unittest.TestCase):

    @patch('src.fixes.execute_with_sudo')
    @patch('src.fixes.time.sleep')
    @patch('src.fixes.display_success')
    def test_reset_adapter(self, mock_display_success, mock_sleep, mock_execute_with_sudo):
        # Test successful reset
        result = reset_adapter()
        self.assertTrue(result)
        mock_execute_with_sudo.assert_any_call(["ip", "link", "set", "wlan0", "down"])
        mock_execute_with_sudo.assert_any_call(["ip", "link", "set", "wlan0", "up"])
        mock_display_success.assert_called_once()
        
        # Test failed reset
        mock_execute_with_sudo.side_effect = Exception("Command failed")
        result = reset_adapter()
        self.assertFalse(result)

    @patch('src.fixes.execute_with_sudo')
    @patch('src.fixes.time.sleep')
    @patch('src.fixes.display_success')
    def test_unblock_rfkill(self, mock_display_success, mock_sleep, mock_execute_with_sudo):
        # Test successful unblock
        result = unblock_rfkill()
        self.assertTrue(result)
        mock_execute_with_sudo.assert_called_once_with(["rfkill", "unblock", "all"])
        mock_display_success.assert_called_once()
        
        # Test failed unblock
        mock_execute_with_sudo.side_effect = Exception("Command failed")
        result = unblock_rfkill()
        self.assertFalse(result)

    @patch('src.fixes.execute_with_sudo')
    @patch('src.fixes.time.sleep')
    @patch('src.fixes.display_success')
    def test_restart_network_manager(self, mock_display_success, mock_sleep, mock_execute_with_sudo):
        # Test successful restart
        result = restart_network_manager()
        self.assertTrue(result)
        mock_execute_with_sudo.assert_called_once_with(["systemctl", "restart", "NetworkManager"])
        mock_display_success.assert_called_once()
        
        # Test failed restart
        mock_execute_with_sudo.side_effect = Exception("Command failed")
        result = restart_network_manager()
        self.assertFalse(result)

    @patch('src.fixes.os.path.exists')
    @patch('src.fixes.run_command')
    @patch('src.fixes.execute_with_sudo')
    @patch('src.fixes.display_success')
    def test_configure_driver_parameters(self, mock_display_success, mock_execute_with_sudo, 
                                        mock_run_command, mock_path_exists):
        # Test when file exists and needs updating
        mock_path_exists.return_value = True
        mock_run_command.return_value = "options iwlwifi power_save=0"  # Missing 11n_disable=1
        
        result = configure_driver_parameters()
        self.assertTrue(result)
        mock_execute_with_sudo.assert_called_once()
        mock_display_success.assert_called_once()
        
        # Test when file doesn't exist
        mock_path_exists.return_value = False
        mock_execute_with_sudo.reset_mock()
        mock_display_success.reset_mock()
        
        result = configure_driver_parameters()
        self.assertTrue(result)
        mock_execute_with_sudo.assert_called_once()
        mock_display_success.assert_called_once()
        
        # Test when command fails
        mock_execute_with_sudo.side_effect = Exception("Command failed")
        result = configure_driver_parameters()
        self.assertFalse(result)

    @patch('src.fixes.run_command')
    @patch('src.fixes.execute_with_sudo')
    def test_scan_networks(self, mock_execute_with_sudo, mock_run_command):
        # Test successful scan with networks
        mock_run_command.return_value = "Network1:WPA2:80:1:2412:54 Mb/s\nNetwork2:WPA:60:6:5180:300 Mb/s"
        
        networks = scan_networks()
        self.assertEqual(len(networks), 2)
        self.assertEqual(networks[0]['ssid'], 'Network1')
        self.assertEqual(networks[0]['security'], 'WPA2')
        self.assertEqual(networks[1]['ssid'], 'Network2')
        self.assertEqual(networks[1]['band'], '5 GHz')
        
        # Test successful scan with no networks
        mock_run_command.return_value = ""
        networks = scan_networks()
        self.assertEqual(len(networks), 0)
        
        # Test failed scan
        mock_run_command.side_effect = Exception("Command failed")
        networks = scan_networks()
        self.assertEqual(len(networks), 0)

    @patch('src.fixes.reset_adapter')
    @patch('src.fixes.unblock_rfkill')
    @patch('src.fixes.restart_network_manager')
    @patch('src.fixes.configure_driver_parameters')
    @patch('src.fixes.update_firmware')
    @patch('src.fixes.display_message')
    @patch('src.fixes.display_success')
    @patch('src.fixes.display_progress')
    def test_apply_all_fixes(self, mock_display_progress, mock_display_success, mock_display_message,
                            mock_update_firmware, mock_configure_driver_parameters, 
                            mock_restart_network_manager, mock_unblock_rfkill, mock_reset_adapter):
        # Test with no issues
        apply_all_fixes([])
        mock_reset_adapter.assert_not_called()
        mock_unblock_rfkill.assert_not_called()
        
        # Test with rfkill issue
        issues = ["WiFi is blocked by rfkill"]
        apply_all_fixes(issues)
        mock_unblock_rfkill.assert_called_once()
        
        # Test with multiple issues
        mock_reset_adapter.reset_mock()
        mock_unblock_rfkill.reset_mock()
        mock_restart_network_manager.reset_mock()
        mock_configure_driver_parameters.reset_mock()
        
        issues = [
            "WiFi adapter is disconnected",
            "WiFi is blocked by rfkill",
            "NetworkManager is not running",
            "11n mode is enabled"
        ]
        
        apply_all_fixes(issues)
        mock_unblock_rfkill.assert_called_once()
        mock_reset_adapter.assert_called()
        mock_restart_network_manager.assert_called()
        mock_configure_driver_parameters.assert_called()

if __name__ == '__main__':
    unittest.main()