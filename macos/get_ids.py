#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from typing import Dict, Tuple


VENDOR_ID = "046D"  # Logitech


def find_hidapitester() -> str:
    """
    Look for the hidapitester binary next to this script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(script_dir, "hidapitester")

    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        return candidate

    print(
        "ERROR: 'hidapitester' binary not found next to this script.\n"
        "Download it from 'todbot/hidapitester' releases and place the macOS binary "
        "as 'hidapitester' in the same folder as this script.\n",
        file=sys.stderr,
    )
    sys.exit(1)


def parse_devices(output: str) -> Dict[str, Tuple[str, str]]:
    """
    Parse hidapitester --list-detail output and collect Logitech devices.

    Returns a dict mapping "VID:PID" -> (product_name, raw_block).
    """
    devices: Dict[str, Tuple[str, str]] = {}

    # Split by blank lines into device blocks
    blocks = re.split(r"\r?\n\r?\n", output.strip())

    for block in blocks:
        if not block.strip():
            continue

        # Look for vendor and product IDs
        vendor_match = re.search(r"vendorId:\s*0x([0-9A-Fa-f]{4})", block)
        if not vendor_match:
            continue

        vendor = vendor_match.group(1).upper()
        if vendor != VENDOR_ID:
            continue

        product_match = re.search(r"productId:\s*0x([0-9A-Fa-f]{4})", block)
        if not product_match:
            continue

        product = product_match.group(1).upper()
        full_id = f"{vendor}:{product}"

        # Try to extract a friendly product name from lines like "046D/B378: MX_KEYS_S"
        name_match = re.search(
            rf"{VENDOR_ID}[/:]{product}:\s*(.+)", block, flags=re.IGNORECASE
        )
        product_name = name_match.group(1).strip() if name_match else "Unknown Logitech device"

        if full_id not in devices:
            devices[full_id] = (product_name, block)

    return devices


def main() -> None:
    exe = find_hidapitester()

    print("=== Scanning for Logitech HID devices (macOS) ===\n")
    try:
        result = subprocess.run(
            [exe, "--list-detail"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Failed to run hidapitester: {exc}", file=sys.stderr)
        sys.exit(1)

    devices = parse_devices(result.stdout)

    if not devices:
        print("No Logitech (vendor 046D) devices found.")
        sys.exit(0)

    for vidpid, (name, _) in devices.items():
        print("--------------------------------------------")
        print(f"Device       : {name}")
        print(f"ID to use    : {vidpid}")

    print("\nDone.")
    print(
        "Pick the ID for your keyboard (e.g. MX Keys / MX Mechanical) "
        "and the ID for your mouse (e.g. MX Master)."
    )


if __name__ == "__main__":
    main()

