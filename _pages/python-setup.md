---
title: "Python Setup for PHYS 4430"
layout: textlay
sitemap: false
permalink: /python-setup
---

# Python Setup

The lab computers have all required software pre-installed. If you want to use your own computer, follow the steps below.

---

## Install Python (Windows)

We recommend using the **Python Install Manager**, the official tool from python.org for managing Python on Windows.

**Option A: Download from python.org (Recommended)**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click **"Download Python install manager"**
3. Run the installer and follow the prompts

**Option B: Install from Microsoft Store**

Search for "Python Install Manager" in the [Microsoft Store](https://apps.microsoft.com/detail/9nq7512cxl7t) and install it.

> **Troubleshooting:** If `py list --online` gives an error about "legacy py.exe", open **Settings → Apps → Installed Apps**, search for "Python Launcher", and uninstall it.

**After installation**, open a terminal (PowerShell or Command Prompt) and install Python:

```bash
py install 3.12
```

You can verify the installation with:

```bash
py --version
```

To see all available Python versions:

```bash
py list --online
```

---

## Install Required Packages

Once Python is installed, install the packages needed for this course:

```bash
py -m pip install uv numpy pandas matplotlib scipy nidaqmx jupyterlab pyvisa pyserial pythonnet uncertainties
```

Or download our [requirements.txt](/PHYS-4430/resources/lab-guides/gaussian-laser-beams/python/requirements.txt) and run:

```bash
py -m pip install -r requirements.txt
```

**Faster alternative with uv:** After installing `uv`, you can use it for much faster package installs:

```bash
uv pip install -r requirements.txt
```

---

## Install Hardware Drivers

### NI-DAQmx (for data acquisition)

Required for the USB-6009 and other NI DAQ devices.

[Download NI-DAQmx from National Instruments](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html)

After installation, verify by running in Python:

```python
import nidaqmx
print(nidaqmx.system.System.local().driver_version)
```

### NI-VISA (for instrument communication)

Required for communicating with bench instruments (oscilloscopes, function generators, power supplies, DMMs).

[Download NI-VISA from National Instruments](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html)

After installation, verify by running in Python:

```python
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())  # Lists all connected instruments
```

### Thorlabs Kinesis (for motor control)

Required for Week 4 of the Gaussian Beams lab (automated beam profiling).

[Download Thorlabs Kinesis](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)

After installation, the Kinesis DLLs will be located at:
```
C:\Program Files\Thorlabs\Kinesis\
```

---

## Verifying Your Setup

Run this quick test to verify everything is installed correctly:

```python
# Test core packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat

print("Core packages: OK")

# Test DAQ (only works if hardware connected)
try:
    import nidaqmx
    system = nidaqmx.system.System.local()
    print(f"NI-DAQmx version: {system.driver_version}")
except Exception as e:
    print(f"NI-DAQmx: {e}")

# Test VISA
try:
    import pyvisa
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    print(f"VISA resources found: {len(resources)}")
except Exception as e:
    print(f"PyVISA: {e}")

print("\nSetup complete!")
```

---

[Back to Python Resources](/PHYS-4430/python-resources)
