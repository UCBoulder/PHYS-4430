---
title: "Python Resources for PHYS 4430"
layout: textlay
sitemap: false
permalink: /python-resources
---

# Python Resources for PHYS 4430

This page provides a comprehensive guide to using Python for data acquisition, analysis, and visualization in PHYS 4430. Whether you're new to Python or need a refresher, this resource will help you succeed in the lab.

## Table of Contents

{:.no_toc}

* TOC
{:toc}

---

# Getting Started

## Required Software

The lab computers have all required software pre-installed. If you want to use your own computer, follow the steps below.

### 1. Install Python (Windows)

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

### 2. Install Required Packages

Once Python is installed, install the packages needed for this course:

```bash
py -m pip install numpy matplotlib pandas scipy nidaqmx pythonnet pyvisa jupyter
```

Or download our [requirements.txt](/PHYS-4430/resources/lab-guides/gaussian-laser-beams/python/requirements.txt) and run:

```bash
py -m pip install -r requirements.txt
```

### 3. Install Hardware Drivers

* **NI-DAQmx drivers** - [Download from National Instruments](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html)
* **Thorlabs Kinesis** (for Week 4) - [Download from Thorlabs](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)

## Development Environments

You have two main options for writing and running Python code:

### Jupyter Notebooks (Recommended for Learning)

Jupyter notebooks allow you to write code in cells and see results immediately. This is ideal for:
* Learning new concepts
* Exploratory data analysis
* Creating documented analysis workflows

**To start Jupyter:**

```bash
py -m jupyter notebook
```

Or for the newer JupyterLab interface:

```bash
py -m jupyter lab
```

### VS Code (Recommended for Longer Scripts)

VS Code is a full-featured code editor, better suited for:
* Writing longer programs (like automation scripts)
* Debugging complex code
* Working with multiple files

**Recommended VS Code extensions:**
* Python (Microsoft)
* Jupyter (Microsoft)
* Pylance (Microsoft)

**Tip:** VS Code can also open and run Jupyter notebooks (`.ipynb` files) directly with the Jupyter extension installed. This gives you notebook interactivity with VS Code's powerful editing features like IntelliSense, debugging, and version control integration.

### When to Use Each

| Task | Recommended Environment |
|------|-------------------------|
| Learning a new concept | Jupyter Notebook |
| Quick data exploration | Jupyter Notebook |
| Fitting and plotting data | Either |
| Real-time data acquisition | VS Code (Python script) |
| Automated measurements | VS Code (Python script) |

---

# Python Basics Refresher

If you're new to Python or need a refresher, here are the essentials.

## Variables and Data Types

```python
# Numbers
voltage = 3.14159          # float (decimal)
num_samples = 100          # int (integer)

# Strings
filename = "data.csv"

# Lists (ordered, changeable)
measurements = [1.2, 1.3, 1.4, 1.5]

# Booleans
is_running = True
```

## Functions

```python
def calculate_energy(wavelength_nm):
    """
    Calculate photon energy from wavelength.

    Parameters:
        wavelength_nm: Wavelength in nanometers

    Returns:
        Energy in Joules
    """
    h = 6.626e-34  # Planck's constant (J·s)
    c = 3e8        # Speed of light (m/s)
    wavelength_m = wavelength_nm * 1e-9
    return (h * c) / wavelength_m

# Call the function
energy = calculate_energy(632.8)
print(f"Energy: {energy:.3e} J")
```

## Loops

```python
# For loop - iterate over a sequence
wavelengths = [400, 500, 600, 700]
for wl in wavelengths:
    print(f"Wavelength: {wl} nm")

# While loop - repeat until condition is false
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
```

## Importing Packages

```python
# Import entire package
import numpy

# Import with alias (common convention)
import numpy as np
import matplotlib.pyplot as plt

# Import specific functions
from scipy.optimize import curve_fit
```

---

# NumPy Essentials

NumPy is the foundation for numerical computing in Python. It provides fast array operations essential for scientific data.

## Creating Arrays

```python
import numpy as np

# From a list
data = np.array([1.2, 1.3, 1.4, 1.5, 1.6])

# Evenly spaced values
x = np.linspace(0, 10, 100)    # 100 points from 0 to 10
t = np.arange(0, 1, 0.01)      # 0 to 1 in steps of 0.01

# Arrays of zeros or ones
zeros = np.zeros(100)
ones = np.ones(50)
```

## Array Operations

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Element-wise operations
z = x + y           # [3, 6, 9, 12, 15]
z = x * y           # [2, 8, 18, 32, 50]
z = x ** 2          # [1, 4, 9, 16, 25]

# Mathematical functions
z = np.sin(x)
z = np.exp(x)
z = np.sqrt(x)

# Statistics
mean_val = np.mean(x)
std_val = np.std(x)
max_val = np.max(x)
```

## Loading Data from CSV

```python
import numpy as np

# Simple CSV with just numbers
data = np.loadtxt('data.csv', delimiter=',')

# CSV with header row
data = np.loadtxt('data.csv', delimiter=',', skiprows=1)

# Access columns
x = data[:, 0]  # First column
y = data[:, 1]  # Second column
```

## Saving Data to CSV

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([1.1, 2.2, 3.3, 4.4, 5.5])

# Stack columns together
data = np.column_stack((x, y))

# Save with header
np.savetxt('output.csv', data, delimiter=',',
           header='x,y', comments='')
```

---

# Plotting with Matplotlib

Matplotlib is the standard plotting library for Python.

## Basic Line Plot

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.title('Sine Wave')
plt.grid(True)
plt.show()
```

## Scatter Plot

```python
import matplotlib.pyplot as plt

x_data = [1, 2, 3, 4, 5]
y_data = [2.1, 3.9, 6.2, 7.8, 10.1]

plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, marker='o', color='blue')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot')
plt.grid(True)
plt.show()
```

## Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
y_err = np.array([0.2, 0.3, 0.2, 0.4, 0.3])  # Uncertainties

plt.figure(figsize=(10, 6))
plt.errorbar(x, y, yerr=y_err, fmt='o', capsize=5,
             label='Data with uncertainties')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data with Error Bars')
plt.legend()
plt.grid(True)
plt.show()
```

## Multiple Plots and Legends

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), label='sin(x)')
plt.plot(x, np.cos(x), label='cos(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Multiple Functions')
plt.legend()
plt.grid(True)
plt.show()
```

## Subplots

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(x, np.sin(x))
ax1.set_ylabel('sin(x)')
ax1.set_title('Sine')
ax1.grid(True)

ax2.plot(x, np.cos(x))
ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')
ax2.set_title('Cosine')
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## Saving Figures

```python
import matplotlib.pyplot as plt

# ... create your plot ...

# Save as PNG (high resolution)
plt.savefig('my_plot.png', dpi=300, bbox_inches='tight')

# Save as PDF (vector format, good for publications)
plt.savefig('my_plot.pdf', bbox_inches='tight')
```

---

# Curve Fitting with SciPy

Fitting data to a model is one of the most common tasks in experimental physics.

## Basic Curve Fitting

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the model function
def linear(x, m, b):
    """Linear function: y = mx + b"""
    return m * x + b

# Sample data
x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

# Perform the fit
popt, pcov = curve_fit(linear, x_data, y_data)

# Extract fit parameters
m_fit, b_fit = popt
print(f"Slope: {m_fit:.3f}")
print(f"Intercept: {b_fit:.3f}")

# Plot data and fit
x_fit = np.linspace(0, 6, 100)
y_fit = linear(x_fit, m_fit, b_fit)

plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_fit, y_fit, 'r-', label='Fit')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
```

## Getting Uncertainties from the Fit

The covariance matrix `pcov` contains information about parameter uncertainties:

```python
import numpy as np
from scipy.optimize import curve_fit

# ... perform fit to get popt, pcov ...

# Parameter uncertainties are square root of diagonal elements
perr = np.sqrt(np.diag(pcov))

m_fit, b_fit = popt
m_err, b_err = perr

print(f"Slope: {m_fit:.3f} ± {m_err:.3f}")
print(f"Intercept: {b_fit:.3f} ± {b_err:.3f}")
```

## Nonlinear Fitting Example: Gaussian

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Gaussian function
def gaussian(x, amplitude, center, width):
    return amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))

# Generate sample data (with noise)
x_data = np.linspace(-5, 5, 50)
y_true = gaussian(x_data, 10, 0, 1)
y_data = y_true + np.random.normal(0, 0.5, len(x_data))

# Initial guesses (important for nonlinear fits!)
p0 = [8, 0.5, 1.5]  # [amplitude, center, width]

# Perform fit
popt, pcov = curve_fit(gaussian, x_data, y_data, p0=p0)
perr = np.sqrt(np.diag(pcov))

print(f"Amplitude: {popt[0]:.2f} ± {perr[0]:.2f}")
print(f"Center: {popt[1]:.2f} ± {perr[1]:.2f}")
print(f"Width: {popt[2]:.2f} ± {perr[2]:.2f}")
```

## Weighted Fitting (Using Uncertainties)

When you have uncertainties on your data points, use weighted fitting:

```python
import numpy as np
from scipy.optimize import curve_fit

x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
y_err = np.array([0.2, 0.3, 0.2, 0.4, 0.3])  # Uncertainties

def linear(x, m, b):
    return m * x + b

# Use sigma parameter for weighted fit
# absolute_sigma=True means y_err are actual standard deviations
popt, pcov = curve_fit(linear, x_data, y_data,
                       sigma=y_err, absolute_sigma=True)
```

## Plotting Residuals

Residuals help you assess the quality of your fit:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ... perform fit ...

# Calculate residuals
y_fit = linear(x_data, *popt)
residuals = y_data - y_fit

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8),
                               gridspec_kw={'height_ratios': [3, 1]})

# Top plot: data and fit
ax1.scatter(x_data, y_data, label='Data')
ax1.plot(x_fit, linear(x_fit, *popt), 'r-', label='Fit')
ax1.set_ylabel('y')
ax1.legend()
ax1.grid(True)

# Bottom plot: residuals
ax2.scatter(x_data, residuals)
ax2.axhline(y=0, color='r', linestyle='--')
ax2.set_xlabel('x')
ax2.set_ylabel('Residuals')
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## Calculating Chi-Squared

Chi-squared ($\chi^2$) quantifies the goodness of fit:

```python
import numpy as np

def calculate_chi_squared(y_data, y_fit, y_err, num_params):
    """
    Calculate chi-squared and reduced chi-squared.

    Parameters:
        y_data: Measured data points
        y_fit: Fitted values at same x positions
        y_err: Uncertainties on data points
        num_params: Number of fit parameters

    Returns:
        chi2: Chi-squared value
        chi2_red: Reduced chi-squared (chi2 / degrees of freedom)
    """
    residuals = y_data - y_fit
    chi2 = np.sum((residuals / y_err) ** 2)
    dof = len(y_data) - num_params  # degrees of freedom
    chi2_red = chi2 / dof
    return chi2, chi2_red

# Example usage
chi2, chi2_red = calculate_chi_squared(y_data, y_fit, y_err, num_params=2)
print(f"Chi-squared: {chi2:.2f}")
print(f"Reduced chi-squared: {chi2_red:.2f}")
# For a good fit, reduced chi-squared should be close to 1
```

---

# Hardware Interfacing

## NI-DAQmx: Data Acquisition

### Listing Available Devices

```python
import nidaqmx
import nidaqmx.system

def list_daq_devices():
    """List all connected NI-DAQ devices."""
    system = nidaqmx.system.System.local()

    print("Available NI-DAQ devices:")
    print("-" * 40)
    for device in system.devices:
        print(f"Name: {device.name}")
        print(f"Type: {device.product_type}")
        print(f"Serial: {device.serial_num}")
        print("-" * 40)

list_daq_devices()
```

### Reading a Single Voltage

```python
import nidaqmx

def read_voltage(device="Dev1", channel="ai0"):
    """Read a single voltage measurement."""
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"{device}/{channel}")
        voltage = task.read()
    return voltage

# Read and print voltage
voltage = read_voltage()
print(f"Voltage: {voltage:.4f} V")
```

### Reading Multiple Samples

```python
import nidaqmx
import numpy as np

def read_samples(num_samples=1000, sample_rate=1000,
                 device="Dev1", channel="ai0"):
    """
    Read multiple voltage samples.

    Parameters:
        num_samples: Number of samples to acquire
        sample_rate: Samples per second (Hz)
        device: DAQ device name
        channel: Analog input channel

    Returns:
        times: Array of time values
        voltages: Array of voltage values
    """
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"{device}/{channel}")
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=num_samples
        )
        voltages = np.array(task.read(number_of_samples_per_channel=num_samples))

    times = np.arange(num_samples) / sample_rate
    return times, voltages

# Acquire 1000 samples at 1000 Hz (1 second of data)
times, voltages = read_samples(num_samples=1000, sample_rate=1000)
```

### Continuous Acquisition with Real-Time Plotting

```python
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt

def continuous_acquisition(duration=10, sample_rate=1000):
    """
    Acquire data continuously and plot in real-time.

    Parameters:
        duration: Total acquisition time in seconds
        sample_rate: Samples per second
    """
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title('Real-Time Data Acquisition')
    ax.grid(True)

    all_data = []
    samples_per_read = 100

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS
        )
        task.start()

        total_samples = int(duration * sample_rate)
        while len(all_data) < total_samples:
            data = task.read(number_of_samples_per_channel=samples_per_read)
            all_data.extend(data)

            # Update plot
            times = np.arange(len(all_data)) / sample_rate
            line.set_data(times, all_data)
            ax.set_xlim(0, max(times[-1], 1))
            ax.set_ylim(min(all_data) - 0.5, max(all_data) + 0.5)
            plt.pause(0.01)

    plt.ioff()
    plt.show()
    return np.array(all_data)
```

## Thorlabs Motor Control

For Week 4, you'll use Thorlabs KCube controllers via the Kinesis SDK. The full automation script is provided in the Week 4 lab guide.

### Basic Connection Test

```python
import clr
import time

# Add Thorlabs Kinesis .NET libraries
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.KCube.StepperMotorCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper

# Build device list
DeviceManagerCLI.BuildDeviceList()

# Your serial number (found on device)
serial_no = "26004813"  # Replace with your device's serial number

# Create and connect
device = KCubeStepper.CreateKCubeStepper(serial_no)
device.Connect(serial_no)
time.sleep(0.25)

# Get device info
info = device.GetDeviceInfo()
print(f"Connected to: {info.Description}")
print(f"Serial Number: {info.SerialNumber}")

# Clean up
device.Disconnect()
```

---

# Troubleshooting

## Import Errors

**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:** Install the missing package:

```bash
pip install numpy
```

## DAQ Device Not Found

**Problem:** `DaqError: Device identifier is invalid`

**Solutions:**

1. Check that the DAQ is plugged in via USB
2. Run `list_daq_devices()` to see available devices
3. Verify the device name (might be "Dev1", "Dev2", etc.)
4. Ensure NI-DAQmx drivers are installed

## Thorlabs Motor Not Connecting

**Problem:** `Device not connected` or timeout errors

**Solutions:**

1. Check USB connection
2. Verify the serial number matches your device
3. Ensure Kinesis software is installed
4. Try power cycling the motor controller
5. Check Windows Device Manager for driver issues

## Plot Not Showing

**Problem:** `plt.show()` does nothing

**Solutions:**

1. In Jupyter: Add `%matplotlib inline` at the top of your notebook
2. In VS Code: Make sure you're not running in a non-interactive environment
3. Try `plt.savefig('plot.png')` to save instead of display

---

# Additional Resources

## Python Learning

- [Python Tutorial](https://docs.python.org/3/tutorial/) - Official Python documentation
* [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
* [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
* [SciPy Curve Fitting](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

## Hardware Documentation

- [NI-DAQmx Python Documentation](https://nidaqmx-python.readthedocs.io/)
* [NI USB-6009 Specifications](https://www.ni.com/en-us/support/model.usb-6009.html)
* [Thorlabs Kinesis Documentation](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)

## Course-Specific

- [Download Python Examples](resources/lab-guides/gaussian-laser-beams/python/)
