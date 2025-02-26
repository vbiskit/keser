import os
import subprocess

def run_command(command):
    print(f"[+] Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[-] ERROR: {result.stderr.strip()}")
        exit(1)

def main():
    repo_url = "https://github.com/vbiskit/oneRise"
    clone_dir = "oneRise"
    install_path = "/usr/local/bin/oneRise"
    script_path = f"{install_path}/onerise.py"
    symlink_path = "/usr/local/bin/onerise"

    # Clone the repository
    run_command(["git", "clone", repo_url])
    
    # Move the required directory
    run_command(["sudo", "mv", f"{clone_dir}/oneRise", install_path])
    
    # Set execute permissions
    run_command(["sudo", "chmod", "+x", script_path])
    
    # Create a symbolic link
    run_command(["sudo", "ln", "-sf", script_path, symlink_path])

    print("[✅] Installation complete! You can now run 'onerise' from anywhere.")

if __name__ == "__main__":
    main()
