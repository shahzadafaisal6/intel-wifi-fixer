# File: /intel-wifi-fixer/intel-wifi-fixer/src/config/adapter_configs.py

class IntelCentrino6205Config:
    """Configuration settings for the Intel Centrino Advanced-N 6205 wireless adapter."""
    
    DEFAULT_SSID = "IntelCentrino6205"
    DEFAULT_CHANNEL = 36
    DEFAULT_FREQUENCY = 5.2  # in GHz
    DEFAULT_SECURITY = "WPA2-PSK"
    
    DIAGNOSTIC_TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    
    # Diagnostic checks
    CHECKS = {
        "signal_strength": {
            "enabled": True,
            "threshold": -70  # dBm
        },
        "connection_status": {
            "enabled": True
        },
        "driver_status": {
            "enabled": True
        },
        "rfkill_status": {
            "enabled": True
        }
    }
    
    # Fixes
    FIXES = {
        "reset_adapter": {
            "enabled": True,
            "description": "Reset the wireless adapter to restore connectivity."
        },
        "change_channel": {
            "enabled": True,
            "description": "Change the WiFi channel to reduce interference."
        },
        "update_driver": {
            "enabled": True,
            "description": "Update the wireless driver to the latest version."
        }
    }