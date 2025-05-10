import subprocess

def run_command(command, get_output=True):
    """Run a shell command and return its output."""
    try:
        if get_output:
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            return result.strip()
        else:
            subprocess.call(command)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.output.strip()}")
        return None

def check_command(command):
    """Check if a command is available on the system."""
    return run_command(['which', command]) is not None

def execute_with_sudo(command):
    """Execute a command with sudo privileges."""
    return run_command(['sudo'] + command)