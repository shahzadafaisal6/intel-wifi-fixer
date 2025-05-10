import os
import sys
import time
import datetime
from importlib import util

# Try to import dev_info module
try:
    from src.dev_info import get_dev_info, get_footer, get_version
except ImportError:
    # Define fallback functions if module not found
    def get_dev_info():
        return {"name": "Shahzada Faisal Abbas", "company": "Hamn-Tec", "version": "1.0.0"}
    
    def get_footer():
        return f"Intel WiFi Fixer v1.0.0 | © 2024 Shahzada Faisal Abbas (Hamn-Tec)"
    
    def get_version():
        return "1.0.0"

def display_message(message, color='default'):
    """Display a message with color formatting."""
    color_codes = {
        'default': '\033[0m',
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'magenta': '\033[95m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'bg_blue': '\033[44m',
        'bg_green': '\033[42m',
        'bg_red': '\033[41m',
    }
    print(f"{color_codes.get(color, color_codes['default'])}{message}{color_codes['default']}")

def prompt_user(prompt):
    """Prompt the user for input."""
    return input(f"{prompt} ")

def display_header(title):
    """Display a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"{title.center(60)}")
    print(f"{'=' * 60}")

def display_error(message):
    """Display an error message."""
    display_message(f"Error: {message}", color='red')

def display_success(message):
    """Display a success message."""
    display_message(f"Success: {message}", color='green')

def display_warning(message):
    """Display a warning message."""
    display_message(f"Warning: {message}", color='yellow')

def display_banner():
    """Display the application banner."""
    version = get_version()
    dev_info = get_dev_info()
    
    banner = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                  Intel WiFi Fixer Tool v{version}                   ║
    ║                                                                  ║
    ║          Diagnose and fix Intel Centrino Advanced-N             ║
    ║                 6205 wireless adapter issues                     ║
    ║                                                                  ║
    ║  Developed by: {dev_info['name']} ({dev_info['company']})        ║
    ║  GitHub: {dev_info['github_url']}      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    display_message(banner, color='cyan')
    
def display_footer():
    """Display a footer with developer information."""
    footer = get_footer()
    terminal_width = os.get_terminal_size().columns
    
    # Create a line of dashes that spans the terminal width
    line = "─" * terminal_width
    
    # Center the footer text
    padding = max(0, (terminal_width - len(footer)) // 2)
    centered_footer = " " * padding + footer
    
    print(f"\n{line}")
    display_message(centered_footer, color='bold')

def get_user_choice(prompt, default='y'):
    """Get a yes/no choice from the user."""
    while True:
        choice = input(prompt).strip().lower()
        if choice == '':
            choice = default
        
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            display_error("Invalid choice. Please enter 'y' or 'n'.")

def display_progress(message, total_steps=10, current_step=0):
    """Display a progress bar."""
    progress = int((current_step / total_steps) * 20)
    bar = '█' * progress + '░' * (20 - progress)
    percent = int((current_step / total_steps) * 100)
    
    print(f"\r{message}: [{bar}] {percent}%", end='', flush=True)
    
    if current_step == total_steps:
        print()  # New line after completion

def display_table(headers, data):
    """Display data in a formatted table with box drawing characters."""
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Add padding to column widths
    col_widths = [w + 2 for w in col_widths]
    
    # Calculate total width
    total_width = sum(col_widths) + len(col_widths) - 1
    
    # Box drawing characters
    top_left = '┌'
    top_right = '┐'
    bottom_left = '└'
    bottom_right = '┘'
    horizontal = '─'
    vertical = '│'
    t_down = '┬'
    t_up = '┴'
    t_right = '├'
    t_left = '┤'
    cross = '┼'
    
    # Build top border
    top_border = top_left + horizontal * col_widths[0]
    for width in col_widths[1:]:
        top_border += t_down + horizontal * width
    top_border += top_right
    
    # Build header separator
    header_sep = t_right + horizontal * col_widths[0]
    for width in col_widths[1:]:
        header_sep += cross + horizontal * width
    header_sep += t_left
    
    # Build bottom border
    bottom_border = bottom_left + horizontal * col_widths[0]
    for width in col_widths[1:]:
        bottom_border += t_up + horizontal * width
    bottom_border += bottom_right
    
    # Print top border
    print(top_border)
    
    # Print headers
    header_row = vertical
    for i, h in enumerate(headers):
        header_row += f" {h.ljust(col_widths[i]-2)} {vertical}"
    print(header_row)
    
    # Print header separator
    print(header_sep)
    
    # Print data rows
    for row in data:
        data_row = vertical
        for i, cell in enumerate(row):
            data_row += f" {str(cell).ljust(col_widths[i]-2)} {vertical}"
        print(data_row)
    
    # Print bottom border
    print(bottom_border)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def display_menu(title, options, show_footer=True):
    """Display a professional-looking menu with options.
    
    Args:
        title (str): The menu title
        options (list): List of (key, description) tuples
        show_footer (bool): Whether to show the footer
    
    Returns:
        str: The user's selection
    """
    clear_screen()
    display_banner()
    display_header(title)
    
    # Calculate the maximum length of the descriptions
    max_length = max(len(desc) for _, desc in options)
    
    # Calculate the width of the menu box
    box_width = max_length + 10  # Add some padding
    
    # Print the menu options
    print()
    for key, desc in options:
        # Format the key with brackets and padding
        formatted_key = f"[{key}]"
        
        # Print the option with proper formatting
        print(f"  {formatted_key.ljust(6)} {desc}")
    
    print()
    
    if show_footer:
        display_footer()
    
    # Get user input
    choice = input("\nSelect an option: ").strip().lower()
    return choice

def display_about():
    """Display information about the application and developer."""
    clear_screen()
    display_banner()
    display_header("About Intel WiFi Fixer")
    
    dev_info = get_dev_info()
    
    print(f"\nVersion: {dev_info['version']}")
    print(f"Developer: {dev_info['name']}")
    print(f"Company: {dev_info['company']}")
    print(f"GitHub: {dev_info['github_url']}")
    print(f"License: {dev_info['license']}")
    print(f"\nCopyright © {dev_info['year']} {dev_info['name']} ({dev_info['company']})")
    print("\nThis tool is designed to diagnose and fix issues with Intel Centrino")
    print("Advanced-N 6205 wireless adapters on Linux systems. It provides automated")
    print("diagnostics and fixes for common problems, as well as advanced")
    print("troubleshooting options.")
    
    input("\nPress Enter to return to the main menu...")