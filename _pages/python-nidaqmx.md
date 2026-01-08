---
title: "NI-DAQmx with Python"
layout: textlay
sitemap: false
permalink: /python-nidaqmx
---

# NI-DAQmx with Python

This page covers using Python to interface with National Instruments data acquisition hardware via the `nidaqmx` package. The primary device in PHYS 4430 is the **USB-6009**.

## Table of Contents

{:.no_toc}

* TOC
{:toc}

---

# USB-6009 Specifications

| Parameter | Value |
|-----------|-------|
| Analog inputs | 8 single-ended or 4 differential |
| Resolution | 14 bits |
| Max sample rate | 48 kS/s (single channel) |
| Input range | +/-10 V, +/-5 V, +/-1 V, +/-0.2 V |
| Analog outputs | 2 (12-bit, 0-5 V) |
| Digital I/O | 12 lines |

**Important:** The 48 kS/s rate is shared across all channels. With 4 channels, each gets 12 kS/s maximum.

---

# Listing Available Devices

Before you can acquire data, verify that your DAQ is connected and recognized:

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

Typical output:
```
Available NI-DAQ devices:
----------------------------------------
Name: Dev1
Type: USB-6009
Serial: 1234567
----------------------------------------
```

---

# Reading a Single Voltage

The simplest acquisition: read one voltage value from one channel.

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

**Channel naming:**
- `Dev1/ai0` - First analog input on Dev1
- `Dev1/ai1` - Second analog input
- `Dev1/ai0:3` - Channels 0 through 3 (4 channels)

---

# Single-Ended vs Differential Inputs

The USB-6009 supports two input modes:

**Single-ended (RSE):** Measures voltage between the input pin and ground. This gives you 8 independent channels (AI0-AI7). Use this for most measurements where your signal is already referenced to ground.

```python
from nidaqmx.constants import TerminalConfiguration

task.ai_channels.add_ai_voltage_chan(
    "Dev1/ai0",
    terminal_config=TerminalConfiguration.RSE
)
```

**Differential (DIFF):** Measures voltage between two input pins (e.g., AI0+ and AI0-). This gives you 4 channels but rejects common-mode noise. Use this for small signals, long cable runs, or noisy environments.

```python
task.ai_channels.add_ai_voltage_chan(
    "Dev1/ai0",
    terminal_config=TerminalConfiguration.DIFF
)
```

| Mode | Channels | Best for |
|------|----------|----------|
| RSE (single-ended) | 8 (AI0-AI7) | Most bench measurements, signals referenced to ground |
| DIFF (differential) | 4 (AI0-AI3) | Small signals, noisy environments, floating sources |

**Common gotcha:** If you don't specify `terminal_config`, the USB-6009 may default to differential mode. If your signal's negative terminal isn't connected properly, you'll get unexpected readings (often about half the expected value).

---

# Reading Multiple Samples

To characterize noise or capture time-varying signals, acquire multiple samples:

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

print(f"Mean voltage: {np.mean(voltages):.4f} V")
print(f"Std deviation: {np.std(voltages):.4f} V")
```

---

# Continuous Acquisition

For continuous monitoring, you can read data in a loop and display a live view. The following code is designed to **visualize** continuous data in real-time—it shows the most recent samples as they arrive, but does not store every sample for later analysis. This is useful for monitoring signals, checking connections, or observing behavior before running a more careful finite acquisition.

**Note:** In Jupyter notebooks, we use `clear_output()` and `display()` to update the plot. The display updates are slower than the data acquisition rate, so we drain all available samples from the buffer each iteration to prevent overflow errors.

```python
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType
from IPython.display import display, clear_output

sample_rate = 10000
display_samples = 1000  # Number of most recent samples to show

fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [])
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage (V)')
ax.set_title('Continuous Acquisition')

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(
        rate=sample_rate,
        sample_mode=AcquisitionType.CONTINUOUS
    )

    task.start()

    try:
        while True:
            # Read ALL available samples to drain the buffer
            samples_available = task.in_stream.avail_samp_per_chan
            if samples_available > 0:
                data = task.read(number_of_samples_per_channel=samples_available)

                # Display only the most recent samples
                display_data = data[-display_samples:] if len(data) > display_samples else data

                line.set_data(range(len(display_data)), display_data)
                ax.set_xlim(0, len(display_data))
                ax.set_ylim(min(display_data) - 0.1, max(display_data) + 0.1)
                clear_output(wait=True)
                display(fig)
    except KeyboardInterrupt:
        print("Stopped by user")

plt.close(fig)
```

---

# Multiple Channels

Reading from multiple channels simultaneously:

```python
import nidaqmx
import numpy as np

def read_multiple_channels(channels=["ai0", "ai1"], num_samples=1000,
                           sample_rate=1000, device="Dev1"):
    """
    Read from multiple analog input channels.

    Returns:
        times: Array of time values
        data: 2D array, shape (num_channels, num_samples)
    """
    channel_str = ",".join([f"{device}/{ch}" for ch in channels])

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel_str)
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=num_samples
        )
        data = np.array(task.read(number_of_samples_per_channel=num_samples))

    times = np.arange(num_samples) / sample_rate
    return times, data

# Read from channels 0 and 1
times, data = read_multiple_channels(["ai0", "ai1"])

print(f"Channel 0 mean: {np.mean(data[0]):.4f} V")
print(f"Channel 1 mean: {np.mean(data[1]):.4f} V")
```

---

# Analog Output

The USB-6009 can generate analog voltages on two output channels (ao0, ao1).

**Important:** The USB-6009's analog outputs only support **0-5V** (not ±10V like the inputs). You must specify this range explicitly or you'll get an error.

```python
import nidaqmx
import time

# Output a DC voltage for 5 seconds
with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=0.0, max_val=5.0)
    task.write(2.5, auto_start=True)  # Output 2.5 V
    print("Outputting 2.5 V on AO0 for 5 seconds...")
    time.sleep(5)
    print("Done - output returns to 0V when task closes")
```

**Loopback test:** Connect AO0 to AI0 with a wire, then verify the output by reading it back:

```python
import nidaqmx
from nidaqmx.constants import TerminalConfiguration

# Write voltage
with nidaqmx.Task() as ao_task:
    ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=0.0, max_val=5.0)
    ao_task.write(3.3, auto_start=True)

    # Read it back (use RSE for single-ended measurement)
    with nidaqmx.Task() as ai_task:
        ai_task.ai_channels.add_ai_voltage_chan(
            "Dev1/ai0",
            terminal_config=TerminalConfiguration.RSE
        )
        voltage = ai_task.read()
        print(f"Set: 3.3 V, Read: {voltage:.4f} V")
```

---

# Saving Data to CSV

```python
import numpy as np

def save_acquisition(times, voltages, filename, metadata=None):
    """
    Save acquired data to CSV with optional metadata header.

    Parameters:
        times: Time array
        voltages: Voltage array
        filename: Output filename
        metadata: Dict of metadata to include in header
    """
    data = np.column_stack((times, voltages))

    header_lines = []
    if metadata:
        for key, value in metadata.items():
            header_lines.append(f"# {key}: {value}")
    header_lines.append("time_s,voltage_V")
    header = "\n".join(header_lines)

    np.savetxt(filename, data, delimiter=',', header=header, comments='')
    print(f"Saved to {filename}")

# Example usage
metadata = {
    "device": "USB-6009",
    "channel": "ai0",
    "sample_rate": 1000,
    "date": "2025-01-08"
}
save_acquisition(times, voltages, "measurement.csv", metadata)
```

---

# Troubleshooting

## Error Handling Pattern

Always include error handling in your data acquisition code:

```python
import nidaqmx
from nidaqmx.errors import DaqError

try:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        voltage = task.read()
        print(f"Voltage: {voltage:.4f} V")

except DaqError as e:
    print(f"DAQ Error: {e}")
    print("Check that:")
    print("  - The DAQ device is connected")
    print("  - The device name is correct (try 'Dev1', 'Dev2', etc.)")
    print("  - NI-DAQmx drivers are installed")
```

## Device Not Found

**Problem:** `DaqError: Device identifier is invalid`

**Solutions:**

1. Check USB connection
2. Run `list_daq_devices()` to see what's detected
3. Verify device name (might be "Dev2" if another device was connected first)
4. Ensure NI-DAQmx drivers are installed
5. Try NI MAX (Measurement & Automation Explorer) to verify device is recognized

## Sample Rate Too High

**Problem:** `DaqError: Sample rate is too high`

**Solutions:**

1. USB-6009 max is 48 kS/s total
2. With multiple channels, divide by number of channels
3. Try reducing sample rate

## Data Looks Wrong

**Check:**

1. Is the signal connected to the correct terminal?
2. Is the ground connected?
3. Is the voltage within the input range (+/-10V default)?
4. Is the sample rate high enough (Nyquist)?

---

[Back to Python Resources](/PHYS-4430/python-resources)
