import os
import sys
import shutil
import subprocess

def install_keser():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    script_path = os.path.join(current_dir, "keser.py")
    
    destination_path = '/usr/local/bin/keser'

    if os.path.exists(destination_path):
        print(f"Tool already installed at {destination_path}. Skipping installation.")
    else:
        wrapper_script = f"""#!/bin/bash
python3 {script_path} "$@"
"""
        
        with open(destination_path, 'w') as f:
            f.write(wrapper_script)

        subprocess.run(['chmod', '+x', destination_path], check=True)

        print(f"Installation complete. You can now run 'keser' from anywhere!")

def uninstall_keser():
    destination_path = '/usr/local/bin/keser'

    if os.path.exists(destination_path):
        print(f"Uninstalling tool from {destination_path}...")
        os.remove(destination_path)
        print("Uninstallation complete.")
    else:
        print("Tool not found. Nothing to uninstall.")

if __name__ == '__main__':
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
