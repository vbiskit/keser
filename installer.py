# run the installer 

import os
import sys
import subprocess
import getpass
import shutil

PACKAGE_NAME = "onerise"
SCRIPT_NAME = "onerise.py"
INSTALL_PATH = f"/usr/local/bin/{PACKAGE_NAME}"
SUDOERS_RULE = f"{getpass.getuser()} ALL=(ALL) NOPASSWD: /bin/mv {os.getcwd()}/{SCRIPT_NAME} {INSTALL_PATH}"

REQUIRED_PACKAGES = [
    "aiohttp",
    "requests",
    "beautifulsoup4",
    "colorama",
]

def install_requirements():
    """Install Python dependencies."""
    print("[+] Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install"] + REQUIRED_PACKAGES, check=True)

def make_executable():
    """Make the Python script executable."""
    print(f"[+] Setting execute permissions for {SCRIPT_NAME}...")
    subprocess.run(["chmod", "+x", SCRIPT_NAME], check=True)

def configure_sudoers():
    """Configure sudoers file to bypass password prompt for moving script."""
    if os.geteuid() != 0:
        print("[!] This step requires root privileges. Please run the script with sudo.")
        sys.exit(1)

    print("[+] Configuring sudoers to bypass password prompt for mv...")
    with open("/etc/sudoers.d/onerise", "w") as sudoers_file:
        sudoers_file.write(SUDOERS_RULE + "\n")
    print("[+] sudoers file updated.")

def move_script():
    """Move the script to /usr/local/bin/."""
    print(f"[+] Moving {SCRIPT_NAME} to {INSTALL_PATH}...")
    subprocess.run(["sudo", "mv", SCRIPT_NAME, INSTALL_PATH], check=True)
    print("[+] Installation complete. You can now run 'onerise' from anywhere.")

def main():
    install_requirements()

    make_executable()

    if os.geteuid() != 0:
        print("[+] Re-running with sudo to move script to /usr/local/bin/")
        subprocess.run(["sudo", sys.executable] + sys.argv)
        sys.exit(0)

    configure_sudoers()

    move_script()

if __name__ == "__main__":
    main()
