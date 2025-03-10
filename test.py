import os
import sys
import shutil
import subprocess

def install_keser():
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the paths
    script_path = os.path.join(current_dir, "keser.py")
    
    # The path where we want to install the command globally
    destination_path = '/usr/local/bin/keser'

    # Check if the tool is already installed
    if os.path.exists(destination_path):
        print(f"Tool already installed at {destination_path}. Skipping installation.")
    else:
        # Create a wrapper script that runs the Python script
        wrapper_script = f"""#!/bin/bash
python3 {script_path} "$@"
"""
        
        # Write the wrapper script to a file in /usr/local/bin
        with open(destination_path, 'w') as f:
            f.write(wrapper_script)

        # Make the wrapper script executable
        subprocess.run(['chmod', '+x', destination_path], check=True)

        print(f"Installation complete. You can now run 'keser' from anywhere!")

def uninstall_keser():
    # Path to remove the installed tool
    destination_path = '/usr/local/bin/keser'

    # Remove the tool if it exists
    if os.path.exists(destination_path):
        print(f"Uninstalling tool from {destination_path}...")
        os.remove(destination_path)
        print("Uninstallation complete.")
    else:
        print("Tool not found. Nothing to uninstall.")

if __name__ == '__main__':
    # Check arguments and run the appropriate function
    if len(sys.argv) < 2:
        print("Usage: python setup.py install | uninstall")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == 'install':
        install_keser()
    elif action == 'uninstall':
        uninstall_keser()
    else:
        print("Invalid action. Please use 'install' or 'uninstall'.")
        sys.exit(1)
