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

# Sample Rate and Nyquist

The **Nyquist theorem** states that to accurately capture a signal at frequency $f$, you must sample at least $2f$ Hz. In practice, sample at 5-10x your highest frequency of interest.

```python
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt

def demonstrate_nyquist(signal_freq, sample_rates):
    """
    Show how sample rate affects signal reconstruction.

    In the lab, use a function generator to create the input signal
    and observe how different sample rates affect measurement.
    """
    duration = 0.1  # 100 ms

    fig, axes = plt.subplots(len(sample_rates), 1, figsize=(12, 3*len(sample_rates)))

    for ax, fs in zip(axes, sample_rates):
        n = int(duration * fs)
        t = np.arange(n) / fs

        # This simulates what you'd see - in lab, use actual DAQ
        # The signal generator output would be: signal_freq Hz sine wave
        measured = np.sin(2 * np.pi * signal_freq * t)

        ax.plot(t * 1000, measured, 'o-', markersize=3)
        ax.set_ylabel('Voltage (V)')
        ax.set_title(f'Sample rate: {fs} Hz (Nyquist: {fs/2} Hz)')
        ax.grid(True)

        if signal_freq > fs / 2:
            ax.set_title(f'Sample rate: {fs} Hz - ALIASED!')

    axes[-1].set_xlabel('Time (ms)')
    plt.tight_layout()
    plt.show()

# Example: 100 Hz signal sampled at different rates
demonstrate_nyquist(100, [50, 100, 200, 1000])
```

---

# Continuous Acquisition

For long-duration measurements or real-time monitoring:

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

# Run for 10 seconds
data = continuous_acquisition(duration=10, sample_rate=1000)
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
