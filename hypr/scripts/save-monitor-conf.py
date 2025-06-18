#!/usr/bin/env python3

import re
import subprocess
from pathlib import Path

output_file = Path.home() / ".config/hypr/monitors.conf"
output_file.parent.mkdir(parents=True, exist_ok=True)

# Get hyprctl output
result = subprocess.run(["hyprctl", "monitors", "all"], capture_output=True, text=True)
text = result.stdout

# Split into blocks, one per monitor
blocks = re.split(r"\n(?=Monitor )", text.strip())

with output_file.open("w") as f:
    for block in blocks:
        # Check if disabled
        disabled_match = re.search(r"^\s*disabled:\s*true", block, re.MULTILINE)
        name_match = re.search(r"^Monitor (\S+)", block, re.MULTILINE)
        name = name_match.group(1) if name_match else "UNKNOWN"

        if disabled_match:
            f.write(f"{name}, disabled\n")
            continue

        mode_match = re.search(r"^\s*(\d+x\d+@\d+\.\d+)\s+at\s+(\d+x\d+)", block, re.MULTILINE)
        scale_match = re.search(r"^\s*scale:\s*([\d\.]+)", block, re.MULTILINE)
        transform_match = re.search(r"^\s*transform:\s*(\d+)", block, re.MULTILINE)
        mirror_match = re.search(r"^\s*mirrorOf:\s*(\S+)", block, re.MULTILINE)
        vrr_match = re.search(r"^\s*vrr:\s*(\S+)", block, re.MULTILINE)

        mode = mode_match.group(1) if mode_match else ""
        pos = mode_match.group(2) if mode_match else ""
        scale = scale_match.group(1) if scale_match else ""

        # transform
        transform_args = ""
        if transform_match:
            transform_args += f"transform, {transform_match.group(1)}, "

        # mirror
        mirror_args = ""
        if mirror_match:
            mirror_val = mirror_match.group(1)
            if mirror_val != "none":
                mirror_args += f"mirror, {mirror_val}, "

        # vrr
        vrr_args = ""
        if vrr_match:
            vrr_val = vrr_match.group(1)
            vrr_num = "1" if vrr_val == "true" else "0"
            vrr_args += f"vrr, {vrr_num}"

        extra_args = (transform_args + mirror_args + vrr_args).rstrip(", ")

        # Write config line
        if extra_args:
            f.write(f"{name}, {mode}, {pos}, {scale}, {extra_args}\n")
        else:
            f.write(f"{name}, {mode}, {pos}, {scale}\n")
