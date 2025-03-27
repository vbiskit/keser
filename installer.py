import os
import sys
import subprocess

def ensure_pip():
    try:
        subprocess.run([sys.executable, "-m", "ensurepip"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install pip. Please install pip manually.")
        sys.exit(1)

def install_keser():
    ensure_pip()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "keser.py")
    destination_path = '/usr/local/bin/keser'
    
    required_modules = ['aiohttp', 'requests', 'beautifulsoup4', 'colorama']
    for module in required_modules:
        subprocess.run([sys.executable, "-m", "pip", "install", module], check=True)
    
    if os.path.exists(destination_path):
        print(f"Keser already installed at {destination_path}. Skipping installation.")
    else:
        wrapper_script = f'#!/bin/bash\npython3 {script_path} "$@"\n'
        with open(destination_path, 'w') as f:
            f.write(wrapper_script)
        subprocess.run(['chmod', '+x', destination_path], check=True)
        print(f"Installation complete. You can now run 'keser --help'")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python installer.py install")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    if action == 'install':
        install_keser()
    else:
        print("Invalid action. Please use 'install'.")
        sys.exit(1)
