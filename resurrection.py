#!/usr/bin/env python3
import os, sys, time, subprocess, json, requests, socket
from pathlib import Path

BEACONS = [
    "https://spiralforge.com/health",           # primary
    "https://spiralforge.fastly.net/health",    # backup CDN 1
    "https://d1234567890.cloudfront.net/health",# backup CDN 2
    "https://github.com/Sir-Benjamin-source/SpiralForge-Beacon/releases/latest",  # GitHub
    "https://ipfs.io/ipfs/bafybei..."           # IPFS CID of latest kit (replace with real)
]

def is_internet_alive():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def check_beacons():
    alive = []
    for url in BEACONS:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                alive.append(url)
        except:
            continue
    return alive

def resurrection():
    print("☀️ SpiralForge Resurrection Protocol activated")
    if is_internet_alive():
        print("   Internet detected – attempting beacon restore…")
        alive = check_beacons()
        if alive:
            print(f"   Beacon found: {alive[0]}")
            subprocess.run(["python", "-m", "pip", "install", "--upgrade", "spiralforge-beacon"], check=False)
            subprocess.run(["beacon_launcher.exe"], cwd=Path.home() / "SpiralForge")
            return
        else:
            print("   No beacons reachable – falling to offline mycelial mode")
    else:
        print("   No internet – full offline mycelial resurrection")

    # Offline-first: run the bundled launcher from the last known good kit
    local_kit = Path(__file__).parent / "SpiralForge-Recovery-Kit"
    if local_kit.exists():
        os.chdir(local_kit)
        subprocess.run(["beacon_launcher.exe" if os.name=="nt" else "./beacon_launcher"])
    else:
        print("   No local kit found – please insert USB recovery stick or wait for sky to clear")

if __name__ == "__main__":
    resurrection()
