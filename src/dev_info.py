"""
Developer Information Module

This module contains information about the developer and the project.
"""

DEV_INFO = {
    "name": "Shahzada Faisal Abbas",
    "company": "Hamn-Tec",
    "github_username": "shahzadafaisal6",
    "github_url": "https://github.com/shahzadafaisal6/intel-wifi-fixer",
    "version": "1.0.0",
    "license": "MIT",
    "year": "2025"
}

def get_dev_info():
    """Return the developer information."""
    return DEV_INFO

def get_project_url():
    """Return the project URL."""
    return DEV_INFO["github_url"]

def get_version():
    """Return the project version."""
    return DEV_INFO["version"]

def get_license_info():
    """Return the license information."""
    return f"© {DEV_INFO['year']} {DEV_INFO['name']} ({DEV_INFO['company']}). Licensed under {DEV_INFO['license']}."

def get_footer():
    """Return a formatted footer with developer information."""
    return f"Intel WiFi Fixer v{DEV_INFO['version']} | {DEV_INFO['github_url']} | © {DEV_INFO['year']} {DEV_INFO['name']}"