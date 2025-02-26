import os
import subprocess
import shutil

def run_command(command):
    """Run a shell command and exit if it fails."""
    print(f"[+] Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[-] ERROR: {result.stderr.strip()}")
        exit(1)

def main():
    repo_url = "https://github.com/vbiskit/oneRise"
    clone_dir = "oneRise"
    source_dir = f"{clone_dir}/oneRise"
    install_path = "/usr/local/bin/oneRise"
    script_path = f"{install_path}/onerise.py"
    symlink_path = "/usr/local/bin/onerise"

    # Clone the repository
    run_command(["git", "clone", repo_url])

    # Ensure the source directory exists before moving
    if not os.path.exists(source_dir):
        print(f"[-] ERROR: '{source_dir}' not found! Check repo structure.")
        exit(1)

    # Remove old installation if it exists
    if os.path.exists(install_path):
        print(f"[+] Removing existing installation at {install_path}...")
        run_command(["sudo", "rm", "-rf", install_path])

    # Move the required directory
    run_command(["sudo", "mv", source_dir, install_path])

    # Ensure the script exists before chmod
    if not os.path.exists(script_path):
        print(f"[-] ERROR: '{script_path}' not found! Something went wrong.")
        exit(1)

    # Set execute permissions
    run_command(["sudo", "chmod", "+x", script_path])

    # Remove old symlink if it exists
    if os.path.islink(symlink_path) or os.path.exists(symlink_path):
        print(f"[+] Removing old symlink at {symlink_path}...")
        run_command(["sudo", "rm", "-f", symlink_path])

    # Create a symbolic link
    run_command(["sudo", "ln", "-s", script_path, symlink_path])

    print("[✅] Installation complete! You can now run 'onerise' from anywhere.")

if __name__ == "__main__":
    main()
