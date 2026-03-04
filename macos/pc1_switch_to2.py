#!/usr/bin/env python3
import os
import subprocess
import sys
import time


# ==============================
# CONFIGURATION SECTION
# ==============================

# Put here the IDs found with 'macos/get_ids.py'
# Example: KEYBOARD_ID = "046D:B378"
KEYBOARD_ID = "046D:C548"

# Example: MOUSE_ID = "046D:B034"
MOUSE_ID = "046D:C548"

# To which channel should the mouse switch when the keyboard leaves THIS Mac?
# 0x00 = Channel 1 (PC 1)
# 0x01 = Channel 2 (PC 2)
# 0x02 = Channel 3 (PC 3)
TARGET_FOR_MOUSE = "0x01"  # Default: send mouse to PC 2


# ==============================
# DO NOT EDIT BELOW THIS LINE
# ==============================


def find_hidapitester() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(script_dir, "hidapitester")

    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        return candidate

    print(
        "ERROR: 'hidapitester' binary not found next to this script.\n"
        "Download the macOS binary from 'todbot/hidapitester' releases, "
        "rename it to 'hidapitester' if needed and place it in the 'macos' folder.",
        file=sys.stderr,
    )
    sys.exit(1)


def keyboard_is_present(hidapitester_path: str) -> bool:
    """
    Check if the keyboard (VID:PID) is currently visible.
    """
    try:
        result = subprocess.run(
            [hidapitester_path, "--vidpid", KEYBOARD_ID, "--list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    except OSError as exc:
        print(f"Failed to run hidapitester: {exc}", file=sys.stderr)
        return False

    # hidapitester often prints IDs as 046D/B378 instead of 046D:B378
    needle = KEYBOARD_ID.replace(":", "/")
    return needle in result.stdout or KEYBOARD_ID in result.stdout


def push_mouse_to_target(hidapitester_path: str) -> None:
    """
    Send the HID command that switches the mouse to the target channel.
    """
    cmd_push = (
        f"0x11,0x00,0x0a,0x1b,{TARGET_FOR_MOUSE},"
        "0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,"
        "0x00,0x00,0x00,0x00,0x00,0x00,0x00"
    )

    try:
        subprocess.run(
            [
                hidapitester_path,
                "--vidpid",
                MOUSE_ID,
                "--usage",
                "0x0202",
                "--usagePage",
                "0xFF43",
                "--open",
                "--length",
                "20",
                "--send-output",
                cmd_push,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError as exc:
        print(f"Failed to send command to mouse: {exc}", file=sys.stderr)


def main() -> None:
    if "YOUR_KEYBOARD_ID_HERE" in KEYBOARD_ID or "YOUR_MOUSE_ID_HERE" in MOUSE_ID:
        print(
            "Please edit this file and set KEYBOARD_ID and MOUSE_ID "
            "to the values reported by 'macos/get_ids.py'.",
            file=sys.stderr,
        )
        sys.exit(1)

    hidapitester_path = find_hidapitester()
    was_present = True

    print("Monitoring keyboard presence. Press Ctrl+C to stop.")

    try:
        while True:
            is_present = keyboard_is_present(hidapitester_path)

            # Keyboard was here and is now gone -> user switched away
            if was_present and not is_present:
                push_mouse_to_target(hidapitester_path)

            was_present = is_present
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()

