#!/usr/bin/env python3
import json
import os
import subprocess

CONFIG_PATH = os.path.expanduser("~/.config/cachy-display/config.json")

def apply_saved_settings():
    if not os.path.exists(CONFIG_PATH):
        return

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    for monitor, p in config.items():
    
        subprocess.run([
            "xrandr", "--output", monitor, 
            "--brightness", f"{p['bright']:.2f}",
            "--gamma", f"{p['r']:.2f}:{p['g']:.2f}:{p['b']:.2f}"
        ], check=False)
        
        subprocess.run([
            "vibrant-cli", monitor, f"{p['sat']:.1f}"
        ], stderr=subprocess.DEVNULL, check=False)

if __name__ == "__main__":
    apply_saved_settings()
