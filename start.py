#!/usr/bin/env python3
import os
import sys
import json
import time
import shutil
import platform
import subprocess
import urllib.request

# =====================================================================
# DYNAMIC ARCH-INSPIRED PROGRESS TRACKER
# =====================================================================
class ArchDownloadProgress:
    def __init__(self):
        self.start_time = time.time()
        self.last_update = time.time()
        self.last_bytes = 0

    def hook(self, count, block_size, total_size):
        current_time = time.time()
        downloaded = count * block_size

        if total_size <= 0:
            total_size = 45000000  # Fallback approximation (~45MB)

        percent = min(100, int(downloaded * 100 / total_size))

        # Performance frame-cap: Update layout every 100ms
        if current_time - self.last_update > 0.1 or percent == 100:
            bytes_since_last = downloaded - self.last_bytes
            time_since_last = current_time - self.last_update
            speed = (bytes_since_last / time_since_last) if time_since_last > 0 else 0

            # Human-readable network speeds
            if speed > 1024 * 1024:
                speed_str = f"{speed / (1024*1024):.1f} MiB/s"
            else:
                speed_str = f"{speed / 1024:.1f} KiB/s"

            # Arch-inspired sharp arrowhead ASCII geometry design
            width = 30
            filled_length = int(width * percent // 100)

            if percent == 100:
                bar = "█" * width
            elif filled_length > 0:
                bar = "█" * (filled_length - 1) + "►" + " " * (width - filled_length)
            else:
                bar = "►" + " " * (width - 1)

            # Print localized status update vector
            sys.stdout.write(f"\r  \033[38;5;39mDownload\033[0m [{bar}] {percent}% ({speed_str})   ")
            sys.stdout.flush()

            self.last_update = current_time
            self.last_bytes = downloaded

# =====================================================================
# AUTO-DEPENDENCY SYSTEM PACKAGE INSTALLER
# =====================================================================
def ensure_system_dependencies():
    missing = []
    if not shutil.which("java"): missing.append("java")
    if not shutil.which("btop"): missing.append("btop")

    if not missing:
        return

    print(f"Missing system utilities: {missing}. Detecting package manager...")
    if shutil.which("dnf"):
        install_cmd = ["sudo", "dnf", "install", "-y", "btop", "java-latest-openjdk-headless"]
    elif shutil.which("apt-get"):
        install_cmd = ["sudo", "apt-get", "update", "&&", "sudo", "apt-get", "install", "-y", "btop", "default-jre-headless"]
    elif shutil.which("pacman"):
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm", "btop", "jre-openjdk-headless"]
    else:
        print("Error: Unknown package manager. Please install java and btop manually.")
        sys.exit(1)

    try:
        subprocess.run(" ".join(install_cmd), shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Installation failed. Ensure you have sudo privileges.")
        sys.exit(1)

# =====================================================================
# ARCHITECTURE-ACCURATE PLAYIT AGENT FETCH
# =====================================================================
def get_clean_playit_binary():
    arch = platform.machine().lower()
    if "x86_64" in arch or "amd64" in arch:
        slug = "playit-linux-amd64"
    elif "aarch64" in arch or "arm64" in arch:
        slug = "playit-linux-aarch64"
    elif "armv7" in arch or "armhf" in arch:
        slug = "playit-linux-armv7"
    else:
        slug = "playit-linux-amd64"

    local_path = os.path.abspath("./playit")
    if os.path.exists(local_path):
        try: os.remove(local_path)
        except Exception: pass

    url = f"https://github.com/playit-cloud/playit-agent/releases/latest/download/{slug}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as f:
            f.write(response.read())
        os.chmod(local_path, 0o755)
        return local_path
    except Exception as e:
        print(f"Failed to fetch clean playit mirror: {e}")
        sys.exit(1)

# =====================================================================
# MAIN RUNTIME PIPELINE
# =====================================================================
ensure_system_dependencies()

target_version = input("Enter Target Minecraft Version (e.g. 1.20.4, 1.19.4): ").strip()
if not target_version:
    print("Invalid version syntax string.")
    sys.exit(1)

server_dir = f"mc_server_{target_version}"
os.makedirs(server_dir, exist_ok=True)

# Pre-fetch playit directly into our initialization path
playit_cmd = get_clean_playit_binary()

os.chdir(server_dir)

# Handle server artifact engine download with our sharp Arch tracker hook
if not os.path.exists("server.jar"):
    print(f"Scanning PaperMC remote archives for Version: {target_version}...")
    try:
        build_url = f"https://api.papermc.io/v2/projects/paper/versions/{target_version}"
        req = urllib.request.Request(build_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            b_data = json.loads(res.read().decode('utf-8'))
            latest_build = b_data["builds"][-1]

        jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{target_version}/builds/{latest_build}/downloads/paper-{target_version}-{latest_build}.jar"

        # Fire download tracking pipeline with Arch ASCII template hook
        tracker = ArchDownloadProgress()
        req_dl = urllib.request.Request(jar_url, headers={'User-Agent': 'Mozilla/5.0'})
        with open("server.jar", "wb") as out_file:
            # We bypass high-level context blocks to keep native tracking metrics active
            urllib.request.urlretrieve(jar_url, "server.jar", reporthook=tracker.hook)
        print("\nDownload finished and saved cleanly to server.jar.")
    except Exception as e:
        print(f"\nError fetching version build target: {e}")
        sys.exit(1)

with open("eula.txt", "w") as f:
    f.write("eula=true\n")

print("Starting playit.gg encryption tunnel link...")
with open("playit.log", "w") as log_file:
    playit_proc = subprocess.Popen([playit_cmd], stdout=log_file, stderr=log_file)

time.sleep(3)

# Scan for setup links
if os.path.exists("playit.log"):
    with open("playit.log", "r") as f:
        log_content = f.read()
        if "visit" in log_content.lower() or "claim" in log_content.lower():
            print("\n=======================================================")
            print(" FIRST TIME SETUP: Link your account to find your IP:")
            for line in log_content.splitlines():
                if "https://" in line:
                    print(f"  \033[38;5;39m{line.strip()}\033[0m")
            print("=======================================================\n")
            input("Press Enter AFTER you have linked your account on the website...")

print(f"Booting up Minecraft server {target_version} engine...")
mc_cmd = ["java", "-Xmx4G", "-Xms4G", "-jar", "server.jar", "nogui"]
mc_proc = subprocess.Popen(mc_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

print("Deploying core system btop overlay...")
try:
    subprocess.run(["btop"])
finally:
    print("\nMonitor closed. Cleaning environment run variables...")
    mc_proc.terminate()
    playit_proc.terminate()
    mc_proc.wait()
    playit_proc.wait()
    print("All system buffers cleanly closed.")
