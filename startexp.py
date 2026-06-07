#!/usr/bin/env python3
import os
import sys
import json
import time
import shutil
import platform
import threading
import subprocess
import urllib.request

# =====================================================================
# SYSTEM VISUAL CONFIGURATION
# =====================================================================
CYAN  = "\033[38;5;39m"
GOLD  = "\033[38;5;214m"
STONE = "\033[38;5;244m"
RED   = "\033[38;5;196m"
RESET = "\033[0m"

def print_master_header():
    """Renders a sharp Arch/Minecraft hybrid terminal logo layout."""
    os.system('clear')
    print(f"{CYAN}       /\        {GOLD} █▀▄▀█ █▀▀ █▄ █ █▀▀ █▀▀ █▀█ █▀█ █▀▀ ▀█▀{RESET}")
    print(f"{CYAN}      /  \       {GOLD} █ ▀ █ █▄▄ █ ▀█ ██▄ █▄▄ █▀▄ █▀█ █▀▄  █ {RESET}")
    print(f"{CYAN}     /\   \      {STONE} ▀   ▀ ▀▀▀ ▀  ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀  ▀ {RESET}")
    print(f"{CYAN}    /      \     {CYAN} ─── Automated Environment Deployment Engine ───{RESET}")
    print(f"{CYAN}   /   _    \    {STONE} ───────────────────────────────────────────────{RESET}")
    print(f"{CYAN}  /   (_)    \   {RESET}")
    print(f"{CYAN} /_▄▄▄▄▄▄▄▄▄▄_\  {RESET}\n")

# =====================================================================
# GLOBAL SPINNER ANIMATION ENGINE
# =====================================================================
class BackgroundSpinner:
    def __init__(self):
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self._thread = None
        self.message = ""

    def _spin(self):
        idx = 0
        while self.running:
            sys.stdout.write(f"\r  {CYAN}{self.frames[idx]}{RESET} {self.message}")
            sys.stdout.flush()
            idx = (idx + 1) % len(self.frames)
            time.sleep(0.08)

    def start(self, message):
        self.stop()
        self.message = message
        self.running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if self._thread:
                self._thread.join()
            sys.stdout.write("\r" + " " * (len(self.message) + 15) + "\r")
            sys.stdout.flush()

spinner = BackgroundSpinner()

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

        if current_time - self.last_update > 0.1 or percent == 100:
            bytes_since_last = downloaded - self.last_bytes
            time_since_last = current_time - self.last_update
            speed = (bytes_since_last / time_since_last) if time_since_last > 0 else 0

            if speed > 1024 * 1024:
                speed_str = f"{speed / (1024*1024):.1f} MiB/s"
            else:
                speed_str = f"{speed / 1024:.1f} KiB/s"

            width = 30
            filled_length = int(width * percent // 100)

            if percent == 100:
                bar = "█" * width
            elif filled_length > 0:
                bar = "█" * (filled_length - 1) + "►" + " " * (width - filled_length)
            else:
                bar = "►" + " " * (width - 1)

            sys.stdout.write(f"\r  {CYAN}Download{RESET} [{bar}] {percent}% ({speed_str})   ")
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

    print_master_header()
    spinner.start(f"Unresolved utilities detected: {missing}. Probing package systems...")
    time.sleep(1.2)

    if shutil.which("dnf"):
        install_cmd = ["sudo", "dnf", "install", "-y", "btop", "java-latest-openjdk-headless"]
    elif shutil.which("apt-get"):
        install_cmd = ["sudo", "apt-get", "update", "&&", "sudo", "apt-get", "install", "-y", "btop", "default-jre-headless"]
    elif shutil.which("pacman"):
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm", "btop", "jre-openjdk-headless"]
    else:
        spinner.stop()
        print(f" {RED}[✗]{RESET} Error: Unknown OS package structure. Install java and btop manually.")
        sys.exit(1)

    spinner.message = "Running root system configuration updates..."
    try:
        subprocess.run(" ".join(install_cmd), shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        spinner.stop()
    except subprocess.CalledProcessError:
        spinner.stop()
        print(f" {RED}[✗]{RESET} Installation interrupted. Please verify sudo privileges.")
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

    spinner.start(f"Verifying host processor architecture... Target: {slug}...")
    url = f"https://github.com/playit-cloud/playit-agent/releases/latest/download/{slug}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as f:
            f.write(response.read())
        os.chmod(local_path, 0o755)
        spinner.stop()
        return local_path
    except Exception as e:
        spinner.stop()
        print(f" {RED}[✗]{RESET} Failed to fetch clean playit mirror: {e}")
        sys.exit(1)

# =====================================================================
# DETECT TOTAL SYSTEM MEMORY
# =====================================================================
def get_total_ram():
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemTotal" in line:
                    kb = int(line.split()[1])
                    return f"{kb // 1024 // 1024}GB"
    except Exception:
        pass
    return "Unknown"

# =====================================================================
# MAIN RUNTIME PIPELINE
# =====================================================================
ensure_system_dependencies()
print_master_header()

# 1. Gather Parameters
print(f" {CYAN}⚙{RESET} {GOLD}Configuration Inputs Required{RESET}")
target_version = input(f" {STONE}└──{RESET} Enter Minecraft Version (e.g. 1.20.4, 1.19.4): ").strip()
if not target_version:
    print(f" {RED}[✗]{RESET} Invalid version syntax string.")
    sys.exit(1)

system_ram = get_total_ram()
print(f" {STONE}└──{RESET} Detected Hardware Host Capacity: {CYAN}{system_ram}{RESET}")
try:
    ram_input = input(f" {STONE}└──{RESET} Enter memory limit size in Gigabytes (e.g. 4, 8): ").strip()
    ram_alloc = int(ram_input)
    if ram_alloc <= 0:
        raise ValueError
except ValueError:
    print(f" {STONE}└──{RESET} Invalid choice. Using standard 4GB allocation buffer.")
    ram_alloc = 4

print(f"\n {CYAN}⚙{RESET} {GOLD}System Deployment Procedures{RESET}")
server_dir = f"mc_server_{target_version}"
os.makedirs(server_dir, exist_ok=True)

# Fetch playit with background spinning wheel active
playit_cmd = get_clean_playit_binary()

os.chdir(server_dir)

# Handle server jar file download
if not os.path.exists("server.jar"):
    spinner.start(f"Querying PaperMC engineering registries for Build: {target_version}...")
    try:
        build_url = f"https://api.papermc.io/v2/projects/paper/versions/{target_version}"
        req = urllib.request.Request(build_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            b_data = json.loads(res.read().decode('utf-8'))
            latest_build = b_data["builds"][-1]

        jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{target_version}/builds/{latest_build}/downloads/paper-{target_version}-{latest_build}.jar"

        spinner.stop()

        tracker = ArchDownloadProgress()
        urllib.request.urlretrieve(jar_url, "server.jar", reporthook=tracker.hook)
        print(f"\n {STONE}└──{RESET} Server deployment file locked as server.jar")
    except Exception as e:
        spinner.stop()
        print(f"\n {RED}[✗]{RESET} Error targeting version profile: {e}")
        sys.exit(1)

with open("eula.txt", "w") as f:
    f.write("eula=true\n")

# Start tunnel process with spinner visualization
spinner.start("Spinning up secure network tunnel loops...")
with open("playit.log", "w") as log_file:
    playit_proc = subprocess.Popen([playit_cmd], stdout=log_file, stderr=log_file)

time.sleep(3)
spinner.stop()

# Scan for setup links if user requires initial registration mapping
if os.path.exists("playit.log"):
    with open("playit.log", "r") as f:
        log_content = f.read()
        if "visit" in log_content.lower() or "claim" in log_content.lower():
            print(f"\n {GOLD}▼ FIRST TIME TUNNEL PAIRING DETECTED ▼{RESET}")
            print(f" {STONE}───────────────────────────────────────────────────────{RESET}")
            for line in log_content.splitlines():
                if "https://" in line:
                    print(f"   {CYAN}{line.strip()}{RESET}")
            print(f" {STONE}───────────────────────────────────────────────────────{RESET}")
            input(" Press [Enter] once you complete authorization on your web panel...")

# Start server engine with background spinner visualization
spinner.start(f"Loading virtual machine environment (Allocated: {ram_alloc}GB)...")
mc_cmd = ["java", f"-Xmx{ram_alloc}G", f"-Xms{ram_alloc}G", "-jar", "server.jar", "nogui"]
mc_proc = subprocess.Popen(mc_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2.5)

spinner.stop()

print(f" {CYAN}⚡{RESET} System live. Binding full-screen performance canvas...")
time.sleep(1)

try:
    subprocess.run(["btop"])
finally:
    print(f"\n\n {RED}⚡{RESET} {GOLD}System Disconnect Captured. Executing termination script...{RESET}")
    mc_proc.terminate()
    playit_proc.terminate()
    mc_proc.wait()
    playit_proc.wait()
    print(f" {CYAN}[✓]{RESET} Process trees cleaned. Host hardware loops completely restored.\n")
