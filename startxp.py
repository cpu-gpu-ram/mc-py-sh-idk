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
    """Renders a pixel-accurate Minecraft title layout with a Creeper letter A."""
    os.system('clear')
    print(f"{GOLD} █▀▄▀█ █ █▄ █ █▀▀ █▀▀ █▀█ █▀█ █▀▀ ▀█▀{RESET}")
    print(f"{GOLD} █ ▀ █ █ █ ▀█ ██▄ █▄▄ █▀▄ █▀█ █▀▄  █ {RESET}")
    print(f"{STONE} ▀   ▀ ▀ ▀  ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀  ▀ {RESET}")
    print(f"{CYAN} ─── Automated Environment Deployment Engine ───{RESET}")
    print(f"{STONE} ───────────────────────────────────────────────{RESET}")
    print(f" {GOLD}███▄ ▄███  ██  ███▄ █  ████▀  ████▀  ██▀▀▀█  █████  ████▀  ███████{RESET}")
    print(f" {GOLD}██ █▀█ ██  ██  ██ ▀█ █  ██▄    ██▄    ██▄▄▄▀  ██ █  ██▄      ██{RESET}")
    print(f" {GOLD}██ ▀▀ ██  ██  ██  ▀██  ██▀    ██▀    ██▀▀▀▄  █████  ██▀      ██{RESET}")
    # The A block below features the precise 3x3 pixel grid alignment of the Creeper snout
    print(f" {GOLD}██    ██  ██  ██   ██  ████▄  ████▄  ██   ██ ██ ▄ ▄ ████▄    ██{RESET}")
    print(f" {STONE}                                                █           {RESET}")
    print(f" {STONE}                                               ▀ ▀          {RESET}")
    print(f"{STONE} ───────────────────────────────────────────────{RESET}\n")

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
target_version = input(f" {STONE}└──{RESET} Enter Minecraft Version (
