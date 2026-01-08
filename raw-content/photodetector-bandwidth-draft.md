# Photodetector Bandwidth Characterization (DRAFT)

*This section would be added to Week 2, with motor controller setup moved to Week 3.*

## Introduction

In Week 1, you analyzed the PDA36A datasheet and calibrated its gain and offset. You may have noticed a specification we haven't yet tested: **bandwidth**. The datasheet claims the bandwidth depends on gain setting, ranging from 10 MHz at 0 dB to just 5 kHz at 70 dB.

Why does this matter? In Week 4, you will automate beam profile measurements by moving a razor blade across the laser beam while recording the photodetector signal. If the photodetector can't respond fast enough to changes in light intensity, your measurements will be distorted.

In this section, you will:
1. Build an automated measurement system using Python and VISA
2. Measure the photodetector's frequency response at several gain settings
3. Compare your measurements to the datasheet specifications
4. Determine whether bandwidth will limit your Week 4 measurements

## Background: The Gain-Bandwidth Tradeoff

The PDA36A uses a transimpedance amplifier to convert photodiode current to voltage. A fundamental property of such amplifiers is the **gain-bandwidth product (GBP)**: as you increase gain, bandwidth decreases proportionally.

The datasheet specifies the amplifier GBP as 600 MHz. The bandwidth at each gain setting can be estimated from:

$$f_{-3dB} = \sqrt{\frac{GBP}{4\pi R_f C_D}}$$

where $R_f$ is the feedback resistance (which sets the gain) and $C_D$ is the total capacitance.

**Prelab Questions:**

1. The PDA36A gain ranges from $1.5 \times 10^3$ V/A (0 dB) to $4.75 \times 10^6$ V/A (70 dB). This is a factor of about 3000 in gain. If the gain-bandwidth product were perfectly constant, what factor of change would you expect in bandwidth?

2. Looking at the datasheet, the actual bandwidth ranges from 10 MHz to 5 kHz. Is this consistent with a constant gain-bandwidth product? What might explain any discrepancy?

3. At what frequency should the photodetector output drop to 70.7% (i.e., $1/\sqrt{2}$) of its low-frequency value? This is the definition of the -3 dB bandwidth.

## Equipment

- Thorlabs PDA36A photodetector (from Week 1)
- LED (red, ~630 nm to approximate He-Ne wavelength)
- Keysight EDU33212A function generator
- Tektronix TBS2000 oscilloscope
- BNC cables and T-connector
- Resistor for LED current limiting (~100-330 Ω)

## Part 1: Manual Measurement Setup

Before automating, verify your setup works manually.

### Wiring the LED

The function generator can directly drive a small LED through a current-limiting resistor:

```
Function Generator CH1 ──┬── 220Ω ──── LED(+) ── LED(-) ──┐
                         │                                 │
                         └─────────────────────────────────┘
```

**Important considerations:**
- Use a series resistor (100-330 Ω) to limit LED current
- The function generator has 50 Ω output impedance
- Set the function generator to "High-Z" load if using the oscilloscope to monitor

### Initial Test

1. Set the function generator to output a 1 kHz sine wave, 2 V peak-to-peak, with a 1 V DC offset (so the LED is always forward biased).

2. Position the LED close to the photodetector aperture (a few cm away). You don't need precise alignment - the goal is to get a measurable signal.

3. Set the photodetector to 50 dB gain (45 kHz bandwidth per datasheet).

4. Connect the photodetector output to the oscilloscope CH1.

5. You should see a sine wave on the oscilloscope. Adjust the LED position and function generator amplitude until you get a clean signal (not saturating the photodetector, not buried in noise).

6. Record the oscilloscope amplitude at 1 kHz. This is your "low frequency" reference.

### Manual Frequency Sweep

1. Keeping everything else constant, increase the function generator frequency in steps: 1 kHz, 5 kHz, 10 kHz, 20 kHz, 30 kHz, 40 kHz, 50 kHz.

2. At each frequency, record the oscilloscope amplitude.

3. At what frequency does the amplitude drop to approximately 70% of the 1 kHz value?

4. How does this compare to the 45 kHz bandwidth specification for 50 dB gain?

**In-Lab Questions:**

1. Did you observe any rolloff before reaching the specified bandwidth? If so, what might cause this? (Hint: LEDs also have a frequency response.)

2. What happens to the signal if you increase the frequency well beyond the -3 dB point?

## Part 2: Automated Measurement with Python

Now you will automate this measurement using Python to control the function generator and oscilloscope via VISA (Virtual Instrument Software Architecture).

### Finding Your Instruments

First, identify the VISA addresses of your instruments:

```python
import pyvisa

rm = pyvisa.ResourceManager()
print("Available instruments:")
for resource in rm.list_resources():
    print(f"  {resource}")
```

The addresses will look something like:
- `USB0::0x0957::0x0407::...::INSTR` (Keysight function generator)
- `USB0::0x0699::0x0368::...::INSTR` (Tektronix oscilloscope)

### Connecting to Instruments

```python
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time

# Connect to instruments
rm = pyvisa.ResourceManager()

# Replace with your actual VISA addresses
FUNCGEN_ADDR = "USB0::0x0957::..."  # Your function generator address
SCOPE_ADDR = "USB0::0x0699::..."     # Your oscilloscope address

funcgen = rm.open_resource(FUNCGEN_ADDR)
scope = rm.open_resource(SCOPE_ADDR)

# Verify connections
print(f"Function Generator: {funcgen.query('*IDN?')}")
print(f"Oscilloscope: {scope.query('*IDN?')}")
```

### Configuring the Function Generator

```python
def setup_funcgen(funcgen, frequency, amplitude=2.0, offset=1.0):
    """
    Configure the function generator for LED modulation.

    Parameters:
        frequency: Output frequency in Hz
        amplitude: Peak-to-peak amplitude in volts
        offset: DC offset in volts (keeps LED forward biased)
    """
    funcgen.write(f"SOURCE1:FUNCTION SIN")
    funcgen.write(f"SOURCE1:FREQUENCY {frequency}")
    funcgen.write(f"SOURCE1:VOLTAGE {amplitude}")
    funcgen.write(f"SOURCE1:VOLTAGE:OFFSET {offset}")
    funcgen.write("OUTPUT1 ON")
    time.sleep(0.1)  # Allow settling
```

### Reading Amplitude from the Oscilloscope

```python
def read_amplitude(scope, channel=1):
    """
    Read the peak-to-peak amplitude from the oscilloscope.

    Returns:
        Peak-to-peak voltage in volts
    """
    # Use the oscilloscope's built-in measurement
    scope.write(f"MEASUREMENT:MEAS1:SOURCE CH{channel}")
    scope.write("MEASUREMENT:MEAS1:TYPE PK2PK")

    # Allow measurement to stabilize
    time.sleep(0.3)

    # Read the measurement
    vpp = float(scope.query("MEASUREMENT:MEAS1:VALUE?"))
    return vpp
```

### Automated Frequency Sweep

```python
def measure_frequency_response(funcgen, scope, frequencies, settling_time=0.5):
    """
    Measure photodetector response across a range of frequencies.

    Parameters:
        frequencies: Array of frequencies to test (Hz)
        settling_time: Time to wait after each frequency change (s)

    Returns:
        amplitudes: Measured peak-to-peak voltages
    """
    amplitudes = []

    for freq in frequencies:
        # Set frequency
        setup_funcgen(funcgen, freq)

        # Wait for system to settle
        time.sleep(settling_time)

        # Measure amplitude
        vpp = read_amplitude(scope)
        amplitudes.append(vpp)

        print(f"  {freq:8.0f} Hz: {vpp:.4f} V")

    return np.array(amplitudes)


# Define frequency range
# Start below expected bandwidth, extend above it
frequencies = np.logspace(2, 5, 30)  # 100 Hz to 100 kHz, 30 points

print("Measuring frequency response...")
print("-" * 30)

amplitudes = measure_frequency_response(funcgen, scope, frequencies)

# Normalize to low-frequency value
normalized = amplitudes / amplitudes[0]
```

### Plotting and Analysis

```python
# Plot the frequency response
plt.figure(figsize=(10, 6))
plt.semilogx(frequencies, 20 * np.log10(normalized), 'b-o', markersize=4)
plt.axhline(-3, color='r', linestyle='--', label='-3 dB level')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Response (dB)')
plt.title('Photodetector Frequency Response')
plt.grid(True, alpha=0.3, which='both')
plt.legend()
plt.ylim(-20, 3)
plt.tight_layout()
plt.savefig('frequency_response.png', dpi=300)
plt.show()

# Find -3 dB frequency by interpolation
from scipy.interpolate import interp1d

response_db = 20 * np.log10(normalized)
# Find where response crosses -3 dB
interp_func = interp1d(response_db, frequencies)
try:
    f_3db = interp_func(-3)
    print(f"\nMeasured -3 dB bandwidth: {f_3db:.1f} Hz")
except:
    print("\nCould not determine -3 dB point - check frequency range")
```

### Cleanup

```python
# Turn off function generator output when done
funcgen.write("OUTPUT1 OFF")

# Close connections
funcgen.close()
scope.close()
```

## Part 3: Systematic Bandwidth Measurement

Now measure the bandwidth at multiple gain settings and compare to the datasheet.

### Exercise: Bandwidth vs. Gain

1. **Choose your gain settings.** Based on the datasheet and your LED's capabilities, select 3-4 gain settings where you expect to be able to measure the bandwidth.

   | Gain Setting | Datasheet Bandwidth | Measurable with LED? |
   |-------------|--------------------|--------------------|
   | 30 dB | 260 kHz | Probably |
   | 40 dB | 150 kHz | Yes |
   | 50 dB | 45 kHz | Yes |
   | 60 dB | 11 kHz | Yes |
   | 70 dB | 5 kHz | Yes |

2. **For each gain setting:**
   - Adjust the LED position/intensity to get a measurable signal without saturation
   - Run the frequency sweep
   - Record the measured -3 dB bandwidth
   - Save the data and plot

3. **Create a comparison table:**

   | Gain Setting | Datasheet Bandwidth | Measured Bandwidth | Ratio |
   |-------------|--------------------|--------------------|-------|
   | 40 dB | 150 kHz | ??? | ??? |
   | 50 dB | 45 kHz | ??? | ??? |
   | ... | ... | ... | ... |

4. **Save your data** for each gain setting to a CSV file:

   ```python
   import csv
   from datetime import datetime

   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   filename = f"bandwidth_{gain_setting}dB_{timestamp}.csv"

   with open(filename, 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(['Frequency (Hz)', 'Amplitude (V)', 'Normalized'])
       for freq, amp, norm in zip(frequencies, amplitudes, normalized):
           writer.writerow([freq, amp, norm])
   ```

## Part 4: Analysis and Interpretation

**Analysis Questions:**

1. How do your measured bandwidths compare to the datasheet values? Create a plot of measured vs. specified bandwidth.

2. If your measurements differ from the datasheet, list possible reasons:
   - Is the LED bandwidth limiting your measurement?
   - Are there other sources of frequency-dependent signal loss (cables, connections)?
   - Could the datasheet be wrong, or are there unit-to-unit variations?

3. At 50 dB gain (45 kHz bandwidth), what is the fastest rate of change the photodetector can accurately track? Express this as a rise time: $t_r \approx 0.35/f_{-3dB}$.

4. **Connection to Week 4:** In the automated beam profile measurement, the motor moves the razor blade at approximately 1 mm/s. If the beam width is 0.5 mm, estimate how fast the photodetector signal changes. Is the bandwidth sufficient?

5. At what gain setting would you expect bandwidth to become a problem for the beam profile measurement? What tradeoff does this create?

## Summary

In this section, you:
- Built an automated measurement system using Python and VISA
- Measured the photodetector's frequency response experimentally
- Compared measurements to manufacturer specifications
- Connected this characterization to your upcoming beam profile measurements

The skills you developed—controlling instruments programmatically, making systematic measurements, and comparing to specifications—are directly applicable to experimental physics research.

## Appendix: Troubleshooting

**No signal on oscilloscope:**
- Check that LED is forward biased (correct polarity)
- Verify function generator output is ON
- Increase function generator amplitude
- Move LED closer to photodetector

**Signal is clipped/saturated:**
- Reduce function generator amplitude
- Move LED farther from photodetector
- Use lower photodetector gain setting

**VISA connection errors:**
- Verify instrument is powered on and connected via USB
- Check that NI-VISA or Keysight IO Libraries are installed
- Try unplugging and reconnecting the USB cable
- Run `rm.list_resources()` to see available instruments

**Measured bandwidth much lower than expected:**
- Your LED may have limited bandwidth
- Try a different LED (some are faster than others)
- Check cable quality and connections
- Verify oscilloscope bandwidth is not limiting (TBS2000 should be fine)

**Noisy measurements:**
- Average multiple readings at each frequency
- Increase settling time between measurements
- Shield photodetector from ambient light
- Use shorter BNC cables
