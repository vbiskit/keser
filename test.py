]import os
import sys
import shutil
import subprocess

def install_keser():
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    tool_name = "keser"
    script_path = os.path.join(current_dir, "keser.py")
    wrapper_path = os.path.join(current_dir, "keser_wrapper")

    # Path to install the tool to /usr/local/bin
    destination_path = '/usr/local/bin/keser'

    # Check if tool is already installed
    if os.path.exists(destination_path):
        print(f"Tool already installed at {destination_path}. Skipping installation.")
    else:
        # Create a wrapper file that calls the python script
        with open(wrapper_path, 'w') as f:
            f.write(f"#!/bin/bash\npython3 {script_path} \"$@\"")

        # Copy the wrapper to /usr/local/bin
        shutil.copy(wrapper_path, destination_path)

        # Make the wrapper file executable
        subprocess.run(['chmod', '+x', destination_path], check=True)

        # Remove the temporary wrapper from the local directory
        os.remove(wrapper_path)

        print(f"Installation complete. You can now run 'keser' from anywhere!")

def uninstall_keser():
    # Path where the tool is installed
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
