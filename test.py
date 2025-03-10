import os
import sys
import shutil
import subprocess

def install_keser():
    # Get the path of the current directory where setup.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to install the executable to /usr/local/bin
    tool_name = "keser"
    tool_path = os.path.join(current_dir, 'keser.py')
    destination_path = '/usr/local/bin/' + tool_name

    # Check if the tool is already installed
    if os.path.exists(destination_path):
        print(f"Tool already installed at {destination_path}. Skipping installation.")
    else:
        # Move the tool to /usr/local/bin and set permissions
        print(f"Installing tool to {destination_path}...")
        shutil.copy(tool_path, destination_path)
        
        # Make the tool executable
        subprocess.run(['chmod', '+x', destination_path], check=True)

    print(f"Installation complete. You can now run '{tool_name}' from anywhere!")

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
