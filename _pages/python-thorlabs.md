---
title: "Thorlabs Motor Control with Python"
layout: textlay
sitemap: false
permalink: /python-thorlabs
---

# Thorlabs Motor Control with Python

This page covers using Python to control Thorlabs stepper motors via the Kinesis SDK. In PHYS 4430, we use the **KST101** controller with a **ZST225** linear translation stage.

## Table of Contents

{:.no_toc}

* TOC
{:toc}

---

# Overview

Thorlabs motor controllers are controlled via their **Kinesis SDK**, a .NET library. Python accesses this through the `pythonnet` package, which provides a bridge between Python and .NET.

**Hardware in PHYS 4430:**
- KST101 KCube Stepper Motor Controller
- ZST225 Motorized Translation Stage (25mm travel)

---

# Prerequisites

## Software Installation

1. **Thorlabs Kinesis SDK** - [Download from Thorlabs](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)

2. **Python packages:**
   ```bash
   py -m pip install pythonnet
   ```

After installing Kinesis, the required DLLs are located at:
```
C:\Program Files\Thorlabs\Kinesis\
```

## First-Time Hardware Setup

**Important:** Before using Python, the KST101 must be configured with the correct stage type. This is a one-time setup stored in the controller's memory.

1. **Without** connecting the USB cable from the KST101 to your PC, power on the KST101
2. Press the Menu button
3. Use the wheel to navigate to "10 Select Stage"
4. Press the Menu button again
5. Select your actuator type (ZST225) by using the wheel to navigate
6. Press the Menu button again to save and exit
7. Power cycle the controller using the power switch on the KST101 (unplugging it will not save the settings)
8. After power cycling, plug the USB cable from the KST101 into your PC
9. Open the Kinesis app
10. Connect to the KST101 from the Kinesis app if it's not connected automatically
11. Verify that the section in the bottom right corner of the `KCube Stepper Motor Controller` window indicates `Actuator: HS ZST225B` - if it's listed as another type, click on this section to change it 
12. Close the Kinesis app

After completing these steps, you should not need to do this again as long as you continue to use the same laptop and KST101.

---

# Finding Your Serial Number

The motor controller serial number is displayed on the **KST101 front panel LCD** (e.g., "26004813"). This 8-digit number is required to connect. We don't want the motor serial number that is on the motor connecter.

---

# Basic Connection

**Important for Jupyter users:** Run this connection code once at the start of your session. The `device` object stays connected until you explicitly disconnect. Don't disconnect until you're completely done—subsequent cells (reading position, moving, etc.) all require an active connection.

```python
import clr
import time

# Add Thorlabs Kinesis .NET libraries
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\"
    "Thorlabs.MotionControl.DeviceManagerCLI.dll"
)
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\"
    "Thorlabs.MotionControl.GenericMotorCLI.dll"
)
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\"
    "Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"
)

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper
from System import Decimal

# Your serial number (from KST101 display)
serial_no = "26004813"  # Replace with your device's serial number

# Build device list - discovers connected controllers
DeviceManagerCLI.BuildDeviceList()

# Create and connect
device = KCubeStepper.CreateKCubeStepper(serial_no)
device.Connect(serial_no)
time.sleep(0.5)

# Wait for settings to initialize
if not device.IsSettingsInitialized():
    device.WaitForSettingsInitialized(5000)

# Load motor configuration (required before position/movement commands)
device.LoadMotorConfiguration(serial_no)

# Start polling (required for position updates)
device.StartPolling(250)
time.sleep(0.25)

# Enable the device
device.EnableDevice()
time.sleep(0.5)

# Get device info
info = device.GetDeviceInfo()
print(f"Connected to: {info.Description}")
print(f"Serial Number: {info.SerialNumber}")
```

## Disconnecting

When you're completely done with the motor, clean up the connection:

```python
# Run this only when finished with all motor operations
device.StopPolling()
device.Disconnect()
print("Disconnected")
```

---

# Reading Position

```python
def get_position(device):
    """Get current motor position in mm."""
    try:
        return float(str(device.Position))
    except:
        return float(device.Position.ToDouble(None))

# After connecting...
position = get_position(device)
print(f"Current position: {position:.4f} mm")
```

---

# Moving the Motor

## Absolute Movement

```python
from System import Decimal

def move_to(device, position_mm, timeout_ms=60000):
    """Move motor to absolute position."""
    print(f"Moving to {position_mm:.4f} mm...")
    device.MoveTo(Decimal(position_mm), timeout_ms)

    # Wait for move to complete
    while device.Status.IsMoving:
        time.sleep(0.01)

    print(f"Move complete. Position: {get_position(device):.4f} mm")

# Example: move to 5 mm
move_to(device, 5.0)
```

## Relative Movement

```python
def move_relative(device, distance_mm, timeout_ms=60000):
    """Move motor by a relative distance."""
    current = get_position(device)
    target = current + distance_mm
    move_to(device, target, timeout_ms)

# Example: move forward 1 mm
move_relative(device, 1.0)

# Example: move backward 0.5 mm
move_relative(device, -0.5)
```

## Homing

Homing moves the motor to its reference position (usually one end of travel):

```python
def home(device, timeout_ms=60000):
    """Home the motor (move to reference position)."""
    print("Homing motor...")
    device.Home(timeout_ms)

    while device.Status.IsHoming:
        time.sleep(0.1)

    print(f"Homing complete. Position: {get_position(device):.4f} mm")

home(device)
```

---

# Setting Velocity

```python
from System import Decimal

def set_velocity(device, velocity_mm_s=1.0, acceleration_mm_s2=1.0):
    """Set motor velocity and acceleration."""
    vel_params = device.GetVelocityParams()
    vel_params.MaxVelocity = Decimal(velocity_mm_s)
    vel_params.Acceleration = Decimal(acceleration_mm_s2)
    device.SetVelocityParams(vel_params)
    print(f"Velocity set to {velocity_mm_s} mm/s")

# Set to 2 mm/s
set_velocity(device, 2.0)
```

---

# Complete Example: Position Scan

This example moves through a series of positions and could be combined with DAQ readings. Copy and paste the entire block—it's self-contained.

**Note:** If you already have a connection open from testing the examples above, disconnect first:

```python
device.StopPolling()
device.Disconnect()
```

```python
import clr
import time
import numpy as np

# Add Thorlabs Kinesis .NET libraries
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\"
    "Thorlabs.MotionControl.DeviceManagerCLI.dll"
)
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\"
    "Thorlabs.MotionControl.GenericMotorCLI.dll"
)
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\"
    "Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"
)

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper
from System import Decimal

def run_position_scan(serial_no, start_mm, end_mm, step_mm):
    """
    Scan through positions from start to end.

    Parameters:
        serial_no: KST101 serial number
        start_mm: Starting position (mm)
        end_mm: Ending position (mm)
        step_mm: Step size (mm)

    Returns:
        positions: List of actual positions visited
    """
    # Connect
    DeviceManagerCLI.BuildDeviceList()
    device = KCubeStepper.CreateKCubeStepper(serial_no)
    device.Connect(serial_no)
    time.sleep(0.5)

    device.WaitForSettingsInitialized(5000)
    device.LoadMotorConfiguration(serial_no)
    device.StartPolling(250)
    time.sleep(0.25)
    device.EnableDevice()
    time.sleep(0.5)

    # Generate target positions
    targets = np.arange(start_mm, end_mm + step_mm, step_mm)
    positions = []

    try:
        print(f"Scanning {len(targets)} positions...")

        for i, target in enumerate(targets):
            # Move to position
            device.MoveTo(Decimal(float(target)), 60000)
            while device.Status.IsMoving:
                time.sleep(0.01)

            # Wait for vibrations to settle
            time.sleep(0.5)

            # Record actual position
            actual = float(str(device.Position))
            positions.append(actual)
            print(f"Step {i+1}/{len(targets)}: {actual:.4f} mm")

    finally:
        device.StopPolling()
        device.Disconnect()

    return positions

# Run scan from 0 to 10 mm in 0.5 mm steps
positions = run_position_scan("26004813", 0, 10, 0.5)
```

---

# Troubleshooting

## Device Not Found

**Problem:** `Device {serial_number} not found`

**Solutions:**
1. Check USB connection
2. Verify serial number matches the KST101 display exactly
3. Ensure no other software (Kinesis, APT) is using the controller
4. Try unplugging and reconnecting the controller

## Object Reference Error

**Problem:** `Object reference not set to an instance of an object`

**Cause:** Stage type not configured on the controller

**Solution:** Configure via the KST101 front panel menu (see First-Time Hardware Setup above)

## Device Settings Not Initialized

**Problem:** `DeviceSettingsException: Device settings not initialized`

**Cause:** Motor configuration not loaded after connecting

**Solution:** Add `device.LoadMotorConfiguration(serial_no)` after waiting for settings:

```python
device.WaitForSettingsInitialized(5000)
device.LoadMotorConfiguration(serial_no)  # Add this line
device.StartPolling(250)
```

## Wrong Position Units

**Problem:** Positions don't match the KST101 display

**Cause:** Stage configuration mismatch

**Solution:**
1. Compare Python position to front panel display
2. If different, reconfigure stage type via front panel or Kinesis
3. Power cycle the controller after configuration

## Import Errors

**Problem:** `Cannot find assembly 'Thorlabs.MotionControl...'`

**Solutions:**
1. Verify Kinesis is installed
2. Check the DLL path matches your installation
3. Use full path: `C:\\Program Files\\Thorlabs\\Kinesis\\...`

## Motor Not Moving

**Check:**
1. Is the motor enabled? (`device.EnableDevice()`)
2. Is polling started? (`device.StartPolling(250)`)
3. Is the target within travel limits? (ZST225: 0-25 mm)
4. Is another program controlling the device?

---

# Resources

- [Thorlabs Kinesis Documentation](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)
- [KST101 Manual](https://www.thorlabs.com/thorproduct.cfm?partnumber=KST101)
- [ZST225 Specifications](https://www.thorlabs.com/thorproduct.cfm?partnumber=ZST225)

---

[Back to Python Resources](/PHYS-4430/python-resources)
