---
title: "VISA Instrument Control with Python"
layout: textlay
sitemap: false
permalink: /python-visa
---

# VISA Instrument Control with Python

This page covers using Python to communicate with bench instruments (oscilloscopes, function generators, power supplies, DMMs) via the VISA protocol using the `pyvisa` package.

## Table of Contents

{:.no_toc}

* TOC
{:toc}

---

# Overview

**VISA** (Virtual Instrument Software Architecture) is a standard for communicating with test equipment. Most modern instruments support VISA over USB, GPIB, or Ethernet.

**Lab equipment covered:**
- Keysight EDU33212A Function Generator
- Keysight EDU36311A Power Supply
- Tektronix TBS2000 Series Oscilloscopes

---

# Prerequisites

## Software Installation

1. **NI-VISA drivers** - [Download from National Instruments](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html)

2. **Python package:**
   ```bash
   py -m pip install pyvisa
   ```

---

# Finding Your Instruments

## Listing Connected Resources

```python
import pyvisa

rm = pyvisa.ResourceManager()
resources = rm.list_resources()

print("Connected instruments:")
for resource in resources:
    print(f"  {resource}")
```

Typical output:
```
Connected instruments:
  USB0::0x0699::0x03C7::C023516::0::INSTR
  USB0::0x2A8D::0x8D01::CN62490159::0::INSTR
  USB0::0x2A8D::0x8F01::CN62240048::0::INSTR
```

## Understanding Resource Strings

USB resource strings follow this pattern:
```
USB0::0xVENDOR::0xPRODUCT::SERIAL::0::INSTR
```

| Vendor ID | Manufacturer |
|-----------|--------------|
| 0x0699 | Tektronix |
| 0x2A8D | Keysight |
| 0x05E6 | Keithley |

## Identifying Instruments

Query the instrument identification:

```python
import pyvisa

rm = pyvisa.ResourceManager()

for resource in rm.list_resources():
    try:
        inst = rm.open_resource(resource)
        inst.timeout = 2000  # 2 second timeout
        idn = inst.query("*IDN?")
        print(f"{resource}")
        print(f"  -> {idn.strip()}")
        inst.close()
    except Exception as e:
        print(f"{resource}")
        print(f"  -> Error: {e}")
```

---

# Basic Communication Pattern

All VISA instruments follow a similar pattern:

```python
import pyvisa

# Open connection
rm = pyvisa.ResourceManager()
inst = rm.open_resource("USB0::0x2A8D::0x8D01::CN62490159::0::INSTR")
inst.timeout = 5000  # 5 second timeout

try:
    # Query identification
    print(inst.query("*IDN?"))

    # Send command (no response expected)
    inst.write("*RST")

    # Query value (response expected)
    value = inst.query("MEASURE:VOLTAGE?")

finally:
    inst.close()
    rm.close()
```

**Key methods:**
- `write()` - Send command, no response expected
- `query()` - Send command and read response
- `read()` - Read response (after write)

---

# Keysight EDU33212A Function Generator

## Basic Waveform Output

```python
import pyvisa

rm = pyvisa.ResourceManager()
fgen = rm.open_resource("USB0::0x2A8D::0x8D01::CN62490159::0::INSTR")

try:
    # Reset to known state
    fgen.write("*RST")

    # Set output impedance to High-Z (important for open circuits)
    fgen.write("OUTPUT1:LOAD INF")

    # Configure sine wave: 1 kHz, 2 Vpp, 0 V offset
    fgen.write("APPLY:SIN 1000,2,0")

    # Turn on output
    fgen.write("OUTPUT1 ON")
    print("Sine wave output enabled")

finally:
    fgen.close()
```

## Different Waveforms

```python
# Sine wave: frequency (Hz), amplitude (Vpp), offset (V)
fgen.write("APPLY:SIN 1000,2,0")

# Square wave
fgen.write("APPLY:SQU 1000,2,0")

# Triangle wave
fgen.write("APPLY:TRI 1000,2,0")

# Ramp (sawtooth)
fgen.write("APPLY:RAMP 1000,2,0")

# DC voltage (just offset, no frequency)
fgen.write("APPLY:DC DEF,DEF,2.5")  # 2.5V DC
```

## Frequency Sweep Example

```python
import pyvisa
import time
import numpy as np

def frequency_sweep(fgen, start_hz, stop_hz, num_points, dwell_time_s=0.5):
    """
    Sweep frequency from start to stop.

    Parameters:
        fgen: PyVISA instrument object
        start_hz: Starting frequency
        stop_hz: Ending frequency
        num_points: Number of frequency steps
        dwell_time_s: Time at each frequency
    """
    frequencies = np.logspace(np.log10(start_hz), np.log10(stop_hz), num_points)

    fgen.write("OUTPUT1:LOAD INF")
    fgen.write("OUTPUT1 ON")

    for freq in frequencies:
        fgen.write(f"FREQUENCY {freq}")
        print(f"Frequency: {freq:.1f} Hz")
        time.sleep(dwell_time_s)

    fgen.write("OUTPUT1 OFF")

# Usage
rm = pyvisa.ResourceManager()
fgen = rm.open_resource("USB0::0x2A8D::0x8D01::CN62490159::0::INSTR")
frequency_sweep(fgen, 100, 10000, 20)  # 100 Hz to 10 kHz, 20 steps
fgen.close()
```

---

# Keysight EDU36311A Power Supply

## Basic Voltage Output

```python
import pyvisa

rm = pyvisa.ResourceManager()
psu = rm.open_resource("USB0::0x2A8D::0x8F01::CN62240048::0::INSTR")

try:
    # Reset to known state
    psu.write("*RST")

    # Select channel 1
    psu.write("INSTRUMENT:SELECT CH1")

    # Set voltage and current limit
    psu.write("VOLTAGE 5.0")    # 5V
    psu.write("CURRENT 0.1")    # 100mA limit

    # Turn on output
    psu.write("OUTPUT ON")
    print("Power supply output enabled: 5V, 100mA limit")

finally:
    psu.close()
```

## Voltage Ramp

```python
import pyvisa
import time

def voltage_ramp(psu, start_v, stop_v, step_v, dwell_time_s=0.5):
    """Ramp voltage from start to stop."""
    import numpy as np

    voltages = np.arange(start_v, stop_v + step_v, step_v)

    psu.write("OUTPUT ON")

    for v in voltages:
        psu.write(f"VOLTAGE {v}")
        print(f"Voltage: {v:.2f} V")
        time.sleep(dwell_time_s)

# Usage
rm = pyvisa.ResourceManager()
psu = rm.open_resource("USB0::0x2A8D::0x8F01::CN62240048::0::INSTR")
psu.write("INSTRUMENT:SELECT CH1")
psu.write("CURRENT 0.1")
voltage_ramp(psu, 0, 5, 0.5)  # 0 to 5V in 0.5V steps
psu.write("OUTPUT OFF")
psu.close()
```

---

# Tektronix TBS2000 Oscilloscope

## Basic Configuration

```python
import pyvisa
import time

rm = pyvisa.ResourceManager()
scope = rm.open_resource("USB0::0x0699::0x03C7::C023516::0::INSTR")
scope.timeout = 10000  # 10 second timeout

try:
    # Reset and wait
    scope.write("*RST")
    time.sleep(1)

    # Channel 1 settings
    scope.write("CH1:PROBE:GAIN 1")     # 1X probe
    scope.write("CH1:SCALE 1")          # 1V/div
    scope.write("CH1:POSITION 0")       # Center vertically

    # Horizontal (time) settings
    scope.write("HORIZONTAL:SCALE 1E-3")  # 1ms/div

    # Trigger settings
    scope.write("TRIGGER:MODE AUTO")
    scope.write("TRIGGER:SOURCE CH1")
    scope.write("TRIGGER:LEVEL 0")

    print("Oscilloscope configured")

finally:
    scope.close()
```

## Reading Measurements

```python
import pyvisa
import time

rm = pyvisa.ResourceManager()
scope = rm.open_resource("USB0::0x0699::0x03C7::C023516::0::INSTR")
scope.timeout = 10000

try:
    # Configure measurement 1: Frequency
    scope.write("MEASUREMENT:MEAS1:SOURCE CH1")
    scope.write("MEASUREMENT:MEAS1:TYPE FREQUENCY")
    scope.write("MEASUREMENT:MEAS1:STATE ON")  # Must turn ON!

    # Configure measurement 2: Peak-to-peak voltage
    scope.write("MEASUREMENT:MEAS2:SOURCE CH1")
    scope.write("MEASUREMENT:MEAS2:TYPE PK2PK")
    scope.write("MEASUREMENT:MEAS2:STATE ON")  # Must turn ON!

    # Wait for measurements to stabilize
    time.sleep(1)

    # Read measurements
    freq = float(scope.query("MEASUREMENT:MEAS1:VALUE?"))
    vpp = float(scope.query("MEASUREMENT:MEAS2:VALUE?"))

    # Check for invalid measurement (9.9e37 is Tektronix "no measurement" value)
    if freq > 1e30:
        print("Frequency: No valid measurement (check signal)")
    else:
        print(f"Frequency: {freq:.1f} Hz")

    if vpp > 1e30:
        print("Vpp: No valid measurement (check signal)")
    else:
        print(f"Vpp: {vpp:.3f} V")

finally:
    scope.close()
```

**Note:** The value `9.9e37` is Tektronix's sentinel for "invalid measurement" - it means there's no signal to measure or the measurement couldn't be computed.

## Capturing Waveform Data

```python
import pyvisa
import numpy as np
import matplotlib.pyplot as plt

def capture_waveform(scope, channel="CH1"):
    """
    Capture waveform data from oscilloscope.

    Returns:
        time_array: Time values in seconds
        voltage_array: Voltage values in volts
    """
    # Configure data transfer
    scope.write("header 0")
    scope.write("data:encdg RIBINARY")
    scope.write(f"data:source {channel}")
    scope.write("data:start 1")

    record_length = int(scope.query("wfmpre:nr_pt?"))
    scope.write(f"data:stop {record_length}")
    scope.write("wfmpre:byt_nr 1")  # 1 byte per sample

    # Acquire single shot
    scope.write("acquire:state 0")
    scope.write("acquire:stopafter SEQUENCE")
    scope.write("acquire:state 1")
    scope.query("*opc?")  # Wait for acquisition

    # Transfer binary data
    raw_data = scope.query_binary_values("curve?", datatype='b', container=np.array)

    # Get scaling factors
    t_scale = float(scope.query("wfmpre:xincr?"))
    t_zero = float(scope.query("wfmpre:xzero?"))
    v_scale = float(scope.query("wfmpre:ymult?"))
    v_offset = float(scope.query("wfmpre:yzero?"))
    v_pos = float(scope.query("wfmpre:yoff?"))

    # Create scaled arrays
    time_array = t_zero + np.arange(record_length) * t_scale
    voltage_array = (raw_data - v_pos) * v_scale + v_offset

    return time_array, voltage_array

# Usage
rm = pyvisa.ResourceManager()
scope = rm.open_resource("USB0::0x0699::0x03C7::C023516::0::INSTR")
scope.timeout = 10000

time_data, voltage_data = capture_waveform(scope, "CH1")

plt.figure(figsize=(10, 6))
plt.plot(time_data * 1000, voltage_data)  # Time in ms
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.title("Oscilloscope Capture")
plt.grid(True)
plt.show()

scope.close()
```

## Saving Screenshot

```python
import pyvisa

def save_screenshot(scope, filename="scope_screenshot.bmp"):
    """Save oscilloscope screen to BMP file."""
    # Request screenshot
    scope.write("SAVE:IMAGE:FILEFORMAT BMP")
    scope.write("HARDCOPY START")

    # Read binary data
    raw_data = scope.read_raw()

    # Save to file
    with open(filename, 'wb') as f:
        f.write(raw_data)

    print(f"Screenshot saved to {filename}")

# Usage
rm = pyvisa.ResourceManager()
scope = rm.open_resource("USB0::0x0699::0x03C7::C023516::0::INSTR")
scope.timeout = 10000
save_screenshot(scope, "my_measurement.bmp")
scope.close()
```

---

# Multi-Instrument Example: Frequency Response Measurement

This example demonstrates coordinating multiple instruments to perform an automated measurement - a common pattern for final projects and advanced experiments.

## What is a Frequency Response Measurement?

A **frequency response** (or Bode plot) shows how a circuit or system responds to different input frequencies. This is fundamental for characterizing:

- Amplifier bandwidth
- Filter cutoff frequencies
- Cable/transmission line behavior
- Sensor frequency limits

## Test Setup

```
+---------------+      +---------------+      +---------------+
|   Function    |      | Device Under  |      |  Oscilloscope |
|   Generator   |----->|  Test (DUT)   |----->|     (CH1)     |
|   (Keysight)  |      | e.g., filter  |      |  (Tektronix)  |
+---------------+      +---------------+      +---------------+
        |                                             |
        +------------ USB to Computer ----------------+
```

**Connections:**
1. Function generator output → Input of your circuit/filter
2. Output of your circuit → Oscilloscope CH1
3. Both instruments connected to computer via USB

## The Measurement Loop

The script follows this pattern at each frequency:

1. **Set frequency** on function generator
2. **Wait** for signal to stabilize (settling time)
3. **Measure** output amplitude on oscilloscope
4. **Record** the data point
5. **Repeat** for next frequency

## Complete Example

```python
import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt

def frequency_response(fgen_addr, scope_addr, frequencies, amplitude_vpp=1.0):
    """
    Measure output amplitude vs frequency for a device under test.

    This function sweeps through a range of frequencies, measuring the
    output amplitude at each point. The result can be used to create
    a Bode magnitude plot showing the frequency response.

    Parameters:
        fgen_addr: Function generator VISA address
        scope_addr: Oscilloscope VISA address
        frequencies: Array of frequencies to test (Hz)
        amplitude_vpp: Input signal amplitude (Vpp)

    Returns:
        frequencies: Input frequencies (Hz)
        amplitudes: Measured output Vpp at each frequency
    """
    rm = pyvisa.ResourceManager()
    fgen = rm.open_resource(fgen_addr)
    scope = rm.open_resource(scope_addr)
    scope.timeout = 10000

    amplitudes = []

    try:
        # ============================================
        # STEP 1: Configure function generator
        # ============================================
        fgen.write("*RST")
        fgen.write("OUTPUT1:LOAD INF")  # High-Z output
        fgen.write(f"APPLY:SIN 1000,{amplitude_vpp},0")  # Initial: 1kHz sine
        fgen.write("OUTPUT1 ON")
        print(f"Function generator: {amplitude_vpp} Vpp sine wave")

        # ============================================
        # STEP 2: Configure oscilloscope measurement
        # ============================================
        # Run autoset to get proper vertical/horizontal scaling
        scope.write("AUTOSET EXECUTE")
        time.sleep(3)  # Autoset takes a few seconds

        scope.write("MEASUREMENT:MEAS1:SOURCE CH1")
        scope.write("MEASUREMENT:MEAS1:TYPE PK2PK")
        scope.write("MEASUREMENT:MEAS1:STATE ON")  # Enable measurement!
        time.sleep(1)  # Let measurement stabilize
        print("Oscilloscope: Measuring CH1 Vpp")

        # ============================================
        # STEP 3: Sweep through frequencies
        # ============================================
        print(f"\nSweeping {len(frequencies)} frequencies...")
        print("-" * 40)

        for i, freq in enumerate(frequencies):
            # Set new frequency
            fgen.write(f"FREQUENCY {freq}")

            # Adjust horizontal scale for this frequency (show ~2-3 cycles)
            # Formula: time_per_div = (cycles_to_show / freq) / 10_divisions
            time_per_div = 0.25 / freq  # ~2.5 cycles across 10 divisions
            scope.write(f"HORIZONTAL:SCALE {time_per_div}")

            # Wait for settling (longer at low frequencies)
            settle_time = max(0.5, 10.0 / freq)  # At least 10 cycles
            time.sleep(settle_time)

            # Read measurement
            vpp = float(scope.query("MEASUREMENT:MEAS1:VALUE?"))

            # Check for valid measurement
            if vpp > 1e30:  # 9.9e37 = invalid
                vpp = np.nan
                print(f"  [{i+1}/{len(frequencies)}] {freq:8.1f} Hz: NO SIGNAL")
            else:
                print(f"  [{i+1}/{len(frequencies)}] {freq:8.1f} Hz: {vpp:.4f} Vpp")

            amplitudes.append(vpp)

    finally:
        # ============================================
        # STEP 4: Clean up
        # ============================================
        fgen.write("OUTPUT1 OFF")
        fgen.close()
        scope.close()
        rm.close()
        print("-" * 40)
        print("Measurement complete")

    return np.array(frequencies), np.array(amplitudes)


def plot_bode(frequencies, amplitudes, reference_amplitude=None):
    """
    Create a Bode magnitude plot from frequency response data.

    Parameters:
        frequencies: Array of frequencies (Hz)
        amplitudes: Array of measured amplitudes (Vpp)
        reference_amplitude: Reference for 0 dB (default: first measurement)
    """
    if reference_amplitude is None:
        reference_amplitude = amplitudes[0]

    # Convert to dB: 20 * log10(Vout / Vref)
    gain_db = 20 * np.log10(amplitudes / reference_amplitude)

    plt.figure(figsize=(10, 6))
    plt.semilogx(frequencies, gain_db, 'b-o', markersize=4)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.title("Frequency Response (Bode Magnitude Plot)")
    plt.grid(True, which="both", linestyle='-', alpha=0.7)
    plt.axhline(y=-3, color='r', linestyle='--', label='-3 dB (cutoff)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Find -3dB point (bandwidth)
    below_3db = np.where(gain_db <= -3)[0]
    if len(below_3db) > 0:
        cutoff_idx = below_3db[0]
        print(f"\n-3 dB cutoff frequency: ~{frequencies[cutoff_idx]:.0f} Hz")


# ============================================
# USAGE EXAMPLE
# ============================================
if __name__ == "__main__":
    # Define frequency range (logarithmic spacing)
    # 100 Hz to 100 kHz, 20 points
    freqs = np.logspace(2, 5, 20)

    # Replace with your instrument addresses
    # (find using rm.list_resources())
    FGEN_ADDR = "USB0::0x2A8D::0x8D01::CN62490159::0::INSTR"
    SCOPE_ADDR = "USB0::0x0699::0x03C7::C023516::0::INSTR"

    # Run measurement
    INPUT_AMPLITUDE = 1.0  # Vpp
    freqs, amps = frequency_response(FGEN_ADDR, SCOPE_ADDR, freqs, INPUT_AMPLITUDE)

    # Plot results (use known input as reference for 0 dB)
    plot_bode(freqs, amps, reference_amplitude=INPUT_AMPLITUDE)

    # Save data
    np.savetxt("frequency_response.csv",
               np.column_stack((freqs, amps)),
               delimiter=',',
               header='frequency_hz,amplitude_vpp',
               comments='')
    print("Data saved to frequency_response.csv")
```

## Understanding the Output

**Bode Magnitude Plot:**
- X-axis: Frequency (logarithmic scale)
- Y-axis: Gain in decibels (dB)
- 0 dB = same amplitude as reference (usually the low-frequency value)
- -3 dB = amplitude reduced to ~70% (the standard "cutoff" definition)
- -20 dB = amplitude reduced to 10%

**What to look for:**
- **Flat region:** Frequencies where the circuit passes signals unchanged
- **Roll-off:** Where gain starts decreasing (indicates bandwidth limit)
- **Cutoff frequency:** The -3 dB point

## Adapting This Example

This pattern can be modified for other multi-instrument measurements:

| Measurement | Generator Output | Scope Measurement |
|------------|------------------|-------------------|
| Frequency response | Sweep frequency | Vpp |
| Phase response | Sweep frequency | Phase (CH1 vs CH2) |
| Distortion vs amplitude | Sweep amplitude | THD or harmonics |
| Rise time vs frequency | Sweep frequency | Rise time |

For phase measurements, connect the function generator to CH2 as a reference and measure the phase difference between CH1 and CH2.

---

# Troubleshooting

## No Instruments Found

**Problem:** `rm.list_resources()` returns empty list

**Solutions:**
1. Check USB connections
2. Verify NI-VISA is installed
3. Run NI MAX to see if instruments are detected
4. Try unplugging and reconnecting instruments

## Timeout Errors

**Problem:** `VisaIOError: VI_ERROR_TMO`

**Solutions:**
1. Increase timeout: `inst.timeout = 10000`
2. Check that instrument is responding (try front panel)
3. Some commands take longer - add delays after write

## Garbled Responses

**Problem:** Response contains unexpected characters

**Solutions:**
1. Set encoding: `inst.encoding = 'latin_1'`
2. Set termination: `inst.read_termination = '\n'`
3. Clear errors: `inst.write('*CLS')`

## Instrument Not Responding

**Check:**
1. Is another program using the instrument?
2. Is the instrument in local/remote mode? (Press "Local" button)
3. Try `inst.write('*RST')` to reset

---

# Resources

- [PyVISA Documentation](https://pyvisa.readthedocs.io/)
- [NI-VISA Download](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html)
- Instrument programming manuals (search manufacturer website for "programming guide")

---

[Back to Python Resources](/PHYS-4430/python-resources)
