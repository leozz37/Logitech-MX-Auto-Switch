## Logitech MX Keys & Master - Auto Switch

A lightweight, invisible solution to **automatically switch your MX Master mouse** when you switch your **MX Keys keyboard** to another computer.

Supported platforms:
- **Windows** (PowerShell scripts)
- **MacOS** (Python scripts)

## 🚀 The Problem
Native Logitech "Easy-Switch" keys (1, 2, 3) only switch the keyboard. To switch the mouse, you have to lift it and press the button underneath, or use Logitech Flow (which requires network and software running).

## ✅ The Solution
These scripts use **hardware polling**. They detect when the keyboard disconnects from PC 1 (because you pressed "2") and immediately send a USB command to the mouse to force it to switch to PC 2 (and vice versa).

**Benefits:**
- Works even if the other PC is locked or sleeping.
- No heavy background software required (PowerShell on Windows, Python on MacOS).
- Instant switching.
- Works with **MX Keys S**, **MX Master 3S**, and likely older Bolt/Unifying devices.

## Windows Version (PowerShell)

### 📦 Prerequisites (Windows)
- 2 Windows PCs.
- `hidapitester.exe` (command line tool to talk to USB devices).
- This repository's PowerShell scripts.

### 🛠️ Installation Guide (Windows)

#### 1. Download & Prepare
1. Create a folder `C:\LogiSwitch` on **BOTH** computers.
2. Download `hidapitester_windows_x64.zip` from [`todbot/hidapitester` releases](https://github.com/todbot/hidapitester/releases) and extract `hidapitester.exe` into that folder.
3. Download the scripts from this repository (`0_Get_IDs.ps1`, `PC1_SwitchTo2.ps1`, `PC2_SwitchTo1.ps1`) and place them in the folder.

#### 2. Get your Hardware IDs (Windows)
On one of your computers:
1. Right-click `0_Get_IDs.ps1` and select **Run with PowerShell**.
2. Note the IDs for your Keyboard (e.g., `046D:B378`) and Mouse (e.g., `046D:B034`).

#### 3. Configure the Scripts (Windows)

**On PC 1 (The PC linked to Key 1)**
1. Open `PC1_SwitchTo2.ps1` with Notepad.
2. Replace `$KeyboardID` and `$MouseID` with your own codes.
3. Ensure `$TargetForMouse` is set to the correct channel for PC 2 (usually `0x01`).
4. Save.

**On PC 2 (The PC linked to Key 2)**
1. Open `PC2_SwitchTo1.ps1` with Notepad.
2. Replace `$KeyboardID` and `$MouseID` with your own codes.
3. Ensure `$TargetForMouse` is set to the correct channel for PC 1 (usually `0x00`).
4. Save.

#### 4. Auto-Start on Windows (Set and Forget)
To make it run silently in the background at startup:
1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Create a shortcut in this folder.
3. Set the shortcut target to:
   `powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\LogiSwitch\PC1_SwitchTo2.ps1"`
   *(Change the filename accordingly for PC 2).*

## MacOS Version (Python)

### 📦 Prerequisites (MacOS)
- 2 Macs (or 1 Mac + 1 Windows PC; each machine runs its own script).
- **Python 3.8+** installed (`python3` available in your terminal).
- `hidapitester` MacOS binary from [`todbot/hidapitester` releases](https://github.com/todbot/hidapitester/releases).
- This repository's `macos` Python scripts.

No extra Python packages are required (only the standard library).

### 1. Download & Prepare (MacOS)
1. Clone or download this repository.
2. Download the MacOS `hidapitester` binary from [`todbot/hidapitester` releases](https://github.com/todbot/hidapitester/releases).
3. Place the `hidapitester` binary inside the `macos` folder (next to `get_ids.py`, `pc1_switch_to2.py`, `pc2_switch_to1.py`).
4. Make it executable:
   ```bash
   cd path/to/Logitech-MX-Auto-Switch/macos
   chmod +x hidapitester
   ```

### 2. Get your Hardware IDs (MacOS)
From the `macos` folder:
```bash
cd path/to/Logitech-MX-Auto-Switch/macos
python3 get_ids.py
```

You will see a list of Logitech devices. Note:
- The ID of your **keyboard** (e.g. `046D:B378`).
- The ID of your **mouse** (e.g. `046D:B034`).

### 3. Configure the Scripts (MacOS)

You run **one Python script per Mac**, similar to the Windows setup.

**On Mac 1 (linked to Easy-Switch key 1):**
1. Open `macos/pc1_switch_to2.py` in a text editor.
2. Set:
   - `KEYBOARD_ID` to your keyboard ID (e.g. `"046D:B378"`).
   - `MOUSE_ID` to your mouse ID (e.g. `"046D:B034"`).
   - Optionally adjust `TARGET_FOR_MOUSE` if your second machine is on another channel (`0x01` = channel 2, `0x02` = channel 3).
3. Save the file.

**On Mac 2 (linked to Easy-Switch key 2):**
1. Open `macos/pc2_switch_to1.py`.
2. Set:
   - `KEYBOARD_ID` to your keyboard ID.
   - `MOUSE_ID` to your mouse ID.
   - `TARGET_FOR_MOUSE` is `"0x00"` by default (send mouse back to channel 1 / Mac 1). Adjust if needed.
3. Save the file.

### 4. Run the Scripts (MacOS)

On each Mac, from the repository root:
```bash
cd path/to/Logitech-MX-Auto-Switch/macos
python3 pc1_switch_to2.py   # on Mac 1
python3 pc2_switch_to1.py   # on Mac 2
```

Leave the script running in a terminal. It will:
- Continuously poll for the keyboard presence.
- When the keyboard **disconnects** from that Mac (you pressed another Easy-Switch key), it sends the HID command to move the mouse to the configured channel.

### 5. Auto-Start on MacOS (Optional)

You can make this run automatically at login, for example:
- Create a small shell script such as `~/logiswitch_mac1.sh`:
  ```bash
  #!/bin/bash
  cd /absolute/path/to/Logitech-MX-Auto-Switch/macos
  /usr/bin/env python3 pc1_switch_to2.py &
  ```
- Make it executable: `chmod +x ~/logiswitch_mac1.sh`.
- Add this script to **System Settings → General → Login Items**.

Repeat similarly for `pc2_switch_to1.py` on the other Mac if needed.

## ⚠️ Disclaimer
These scripts rely on `hidapitester` to send raw HID commands. Use at your own risk. This is not an official Logitech product.
