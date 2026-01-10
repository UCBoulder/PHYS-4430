---
title: "Fourier Analysis Module"
---

<!--
FUTURE INTEGRATION NOTES
========================
This content was extracted from gaussian-beams-3-raw.md to reduce cognitive load in Week 3.

Possible integration options:
1. Standalone signal processing module (perhaps paired with a different lab)
2. Optional enrichment for students who finish early
3. Incorporated into a lab where spectral analysis is central to the measurement
4. Week 2 extension (connects naturally to Nyquist discussion)

The "Connecting FFT to Your Gaussian Beams Experiment" section attempts to tie this
to beam profiling, but the connection is weak - students don't actually need FFT
to succeed in the Gaussian beams sequence.
-->

# Fourier Analysis Techniques

This module introduces spectral analysis using Fourier Transforms—a powerful technique used throughout physics and engineering to understand signals in the frequency domain.

## Prerequisites

Before starting this module, you should be familiar with:
- Basic Python and NumPy
- DAQ data acquisition (sample rate, number of samples)
- Nyquist frequency and aliasing

## Learning Goals

After completing this module, you will be able to:

1. Explain what a Fourier Transform reveals about a signal and interpret a power spectrum.
2. Compute and plot the power spectrum of a measured signal using NumPy's FFT functions.
3. Identify frequency components in experimental data and relate them to physical sources.
4. Understand the relationship between acquisition parameters (sample rate, number of samples) and spectral resolution.

## Introduction to Fourier Transforms

The discrete Fourier Transform of a set of data $\{y_0,y_1, ... , y_{N-1}\}$ is given by

$$Y_m=\displaystyle \sum_{n=0}^{N-1}y_n\cdot e^{-2\pi i \frac{m}{N}n}$$

The basic idea is that a Fourier Transform decomposes the data into a set of different frequency components, so the amplitude of $Y_m$ tells you how much of your signal was formed by an oscillation at the $m$-th frequency.

### Basic Fourier Concepts {#sec:basic-fourier}

1. How do the units of the Fourier Transform array $Y_m$ relate to the units of the data $y_n$?
2. Does the data $y_n$ have to be taken at equally spaced intervals?
3. Is it possible for two different sets of data to have the same Fourier Transform?
4. If a data set has $N$ elements, how long is the discrete Fourier Transform?

## Computing the Power Spectrum in Python

NumPy provides efficient FFT (Fast Fourier Transform) functions for spectral analysis:

```python
import numpy as np

def compute_spectrum(data, sample_rate):
    """
    Compute the one-sided power spectrum of a signal.

    Parameters:
        data: 1D array of signal values
        sample_rate: Sample rate in Hz

    Returns:
        frequencies: Array of frequency values
        power: Power spectrum (magnitude squared)
    """
    n = len(data)

    # Compute FFT
    fft_result = np.fft.fft(data)

    # Get positive frequencies only (real signal has symmetric spectrum)
    n_unique = n // 2 + 1
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)[:n_unique]
    frequencies = np.abs(frequencies)

    # Power spectrum (magnitude squared, normalized)
    power = (np.abs(fft_result[:n_unique]) / n) ** 2
    power[1:-1] *= 2  # Double power for frequencies with both +/- components

    return frequencies, power
```

### Frequency Resolution and Maximum Frequency

The relationship between your acquisition parameters and the spectrum is:

```python
# Frequency resolution and maximum frequency
freq_resolution = sample_rate / num_samples  # Hz per bin
max_frequency = sample_rate / 2  # Nyquist frequency

print(f"Frequency resolution: {freq_resolution} Hz")
print(f"Maximum frequency: {max_frequency} Hz")
```

**Key relationships:**

- **Frequency resolution** = Sample Rate / Number of Samples
- **Maximum frequency** (Nyquist) = Sample Rate / 2

If the data is sampled for 2 seconds at 100 Hz sample rate:
- Number of samples = 200
- Frequency resolution = 100 Hz / 200 = 0.5 Hz
- Maximum frequency = 100 Hz / 2 = 50 Hz

## Building a Real-Time Spectral Analyzer

The following script acquires data and displays both time-domain and frequency-domain views simultaneously. **This code is provided for you**—the learning goal is to *use and interpret* spectral analysis, not to write real-time plotting code from scratch.

Run this script, then complete the exercises that follow. You will modify specific aspects of the code to deepen your understanding.

```python
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType
from IPython.display import display, clear_output

# Configuration
SAMPLE_RATE = 10000  # Hz
NUM_SAMPLES = 2000
DAQ_CHANNEL = "Dev1/ai0"

def compute_spectrum(data, sample_rate):
    """Compute one-sided power spectrum."""
    n = len(data)
    fft_result = np.fft.fft(data)
    n_unique = n // 2 + 1
    frequencies = np.abs(np.fft.fftfreq(n, d=1/sample_rate)[:n_unique])
    power = (np.abs(fft_result[:n_unique]) / n) ** 2
    power[1:-1] *= 2
    return frequencies, power

# Set up plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Time domain plot
line1, = ax1.plot([], [], 'b-')
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Voltage (V)')
ax1.set_title('Time Domain')
ax1.grid(True, alpha=0.3)

# Frequency domain plot
line2, = ax2.plot([], [], 'r-')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Power')
ax2.set_title('Frequency Domain (Power Spectrum)')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, SAMPLE_RATE / 2)

plt.tight_layout()

last_data = None

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(DAQ_CHANNEL)
    task.timing.cfg_samp_clk_timing(
        rate=SAMPLE_RATE,
        sample_mode=AcquisitionType.CONTINUOUS
    )
    task.start()

    print("Acquiring data... Press Ctrl+C (or Interrupt Kernel) to stop")

    try:
        while True:
            # Drain buffer to prevent overflow
            samples_available = task.in_stream.avail_samp_per_chan
            if samples_available >= NUM_SAMPLES:
                data = task.read(number_of_samples_per_channel=samples_available)
                # Use most recent samples
                data = data[-NUM_SAMPLES:]
                last_data = np.array(data)

                # Update time domain plot
                time_ms = np.arange(len(data)) / SAMPLE_RATE * 1000
                line1.set_data(time_ms, data)
                ax1.set_xlim(0, time_ms[-1])
                ax1.set_ylim(np.min(data) - 0.1, np.max(data) + 0.1)

                # Update frequency domain plot
                frequencies, power = compute_spectrum(np.array(data), SAMPLE_RATE)
                line2.set_data(frequencies, power)
                ax2.set_ylim(0, np.max(power) * 1.1 + 0.001)

                clear_output(wait=True)
                display(fig)

    except KeyboardInterrupt:
        print("\nStopped by user")

# Save last dataset
if last_data is not None:
    np.savetxt('last_acquisition.csv',
               np.column_stack([np.arange(len(last_data))/SAMPLE_RATE, last_data]),
               delimiter=',', header='Time (s), Voltage (V)', comments='')
    print("Last dataset saved to 'last_acquisition.csv'")

plt.close(fig)
```

### Code Modification Exercises

These exercises help you understand spectral analysis by making targeted modifications to the code above. For each modification, **predict the result before running the code**.

1. **Change the sample rate.** Modify `SAMPLE_RATE` from 10000 Hz to 2000 Hz.
   - **Before running:** Predict what will change in the frequency-domain plot. What will be the new maximum frequency? What will happen to frequency resolution?
   - **After running:** Was your prediction correct? If not, explain what you learned.

2. **Change the number of samples.** Reset `SAMPLE_RATE` to 10000 Hz, then change `NUM_SAMPLES` from 2000 to 500.
   - **Before running:** How will this affect the frequency resolution? Will the maximum frequency change?
   - **After running:** Compare the spectrum to the original. Is it easier or harder to identify frequency peaks? Why?

3. **Add a deliberate bug.** Modify the `compute_spectrum` function to remove the line `power[1:-1] *= 2`:
   ```python
   # power[1:-1] *= 2  # Comment this out
   ```
   - **Before running:** What do you predict will happen to the displayed power values?
   - **After running:** Compare the magnitude of peaks to the original. Research why this factor of 2 is needed for a one-sided spectrum.

4. **Document a wrong prediction.** In your notebook, record at least one case where your prediction was incorrect. Explain:
   - What you predicted
   - What actually happened
   - Why your mental model was wrong
   - What you now understand better

**Note:** Whether you generated these modifications yourself or with AI assistance, the learning comes from making predictions and comparing to results. Always restore the original code before moving to the next exercise.

## Exercises: Spectral Analysis

### Understanding Frequency Resolution

1. Use a waveform generator to output a waveform of your choice at a frequency in the tens of Hz to kHz range and view the output on the oscilloscope and in your Python script.

2. Look at the spectral analysis. How do the **frequency resolution** (frequency step size between data in the spectrum) and **maximum frequency** relate to the **sample rate** and **number of samples**? Verify the algebraic relationship experimentally.

3. If the data is sampled for 2 seconds at 100 Hz sample rate, what frequency does the $m$-th component of the Fourier Transform correspond to?

4. How many points are shown in the spectral analysis plot? How does this compare to the number of points you expected in the Fourier transform (see Section @sec:basic-fourier\.4)?

   **Note**: The data acquired from the DAQ is always a sequence of real numbers $\{y_n\}$. Under the condition that the signal is only real numbers, it can be proved that $Y_m=Y_{N-M}^*$ so $|Y_M|=|Y_{N-m}|$, meaning the spectrum is symmetric about the $N/2$-th data point, which corresponds to the Nyquist frequency. For this reason, we typically only plot the first half of the Fourier spectrum up to the Nyquist frequency.

### Analyzing Different Waveforms

1. How do you expect the spectrum of a **sine wave** to look? How should it change as you vary the amplitude and frequency on the waveform generator? Try it.

2. How do you expect the spectrum of a **square wave** to look? How should it change as you vary the amplitude and frequency on the waveform generator? Try it.

   (Hint: you can look up or calculate the Fourier Series of a square wave to see if the observed amplitudes agree with the mathematical prediction.)

3. Generate a signal with **two frequencies** (if your function generator supports this, or use the sum of two signals). Can you identify both frequencies in the spectrum?

### Analyzing Saved Data

Sometimes you may want to analyze data after it is saved rather than in real-time:

```python
import numpy as np
import matplotlib.pyplot as plt

# Load saved data
data = np.loadtxt('saved_waveform.csv', delimiter=',', skiprows=1)
time = data[:, 0]
signal = data[:, 1]

# Determine sample rate from time data
sample_rate = 1 / (time[1] - time[0])

# Compute FFT
n = len(signal)
fft_result = np.fft.fft(signal)

# Create frequency axis
frequencies = np.fft.fftfreq(n, d=1/sample_rate)

# Get positive frequencies only
positive_mask = frequencies >= 0
freq_positive = frequencies[positive_mask]
magnitude = np.abs(fft_result[positive_mask]) / n

# Plot spectrum
plt.figure(figsize=(10, 6))
plt.plot(freq_positive, magnitude)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Fourier Transform of Saved Data')
plt.grid(True, alpha=0.3)
plt.show()
```

### Exercises with Saved Data

1. Import any saved data set of a periodic function saved from the DAQ or the oscilloscope.

2. Use NumPy's `fft` function to compute the discrete Fourier Transform of the signal.
   1. Do you expect the FFT output to be real-valued or complex-valued?

3. Plot the output of the FFT function. Since the output is complex-valued, plot `np.abs()` or `np.abs()**2`.
   1. What is the x-axis range and step-size in the plot?
   2. What frequency range and step size should be displayed on the x-axis?

4. Make sure to add the frequency column to create a proper plot of spectrum vs. frequency:

   ```python
   # Complete example
   n = len(signal)
   sample_rate = 10000  # Adjust to your actual sample rate

   # Compute FFT and frequencies
   fft_result = np.fft.fft(signal)
   frequencies = np.fft.fftfreq(n, d=1/sample_rate)

   # One-sided spectrum (positive frequencies)
   n_half = n // 2 + 1
   freq_pos = frequencies[:n_half]
   magnitude = np.abs(fft_result[:n_half]) * 2 / n  # Normalize and account for one-sided
   magnitude[0] /= 2  # DC component doesn't double

   plt.figure(figsize=(10, 6))
   plt.plot(freq_pos, magnitude)
   plt.xlabel('Frequency (Hz)')
   plt.ylabel('Magnitude')
   plt.xlim(0, sample_rate/2)
   plt.grid(True, alpha=0.3)
   plt.show()
   ```

5. Does the spectral analysis show the same spectrum at the same frequencies that you expect from the waveform generator settings?

6. NumPy's FFT uses specific conventions. You can check the documentation with:

   ```python
   help(np.fft.fft)
   ```

   The convention used is: $Y_k = \sum_{n=0}^{N-1} y_n e^{-2\pi i k n / N}$

## Application: Photodetector Noise Analysis

*This section shows how spectral analysis can be applied to understand noise sources in optical measurements. It connects to photodetector characterization work.*

### Photodetector Noise Spectrum

Connect your photodetector to the DAQ with the beam blocked.

1. Acquire 1-2 seconds of data at 10 kHz sample rate.
2. Compute and plot the power spectrum.
3. Are there any peaks at specific frequencies? If so, what are likely physical sources? (Common culprits: 60 Hz power line, 120 Hz rectified power, computer switching frequencies, room lighting)
4. How does the noise spectrum change when you change the photodetector gain setting?

### Signal Spectrum with Laser

Now unblock the beam so light hits the photodetector.

1. Acquire data and compute the power spectrum.
2. Compare to the dark noise spectrum. What changed?
3. If you see new peaks, what might cause periodic variations in laser intensity?

### Implications for Measurements

Consider how noise affects precision measurements:

1. If you wanted to reduce the effect of 60 Hz noise, how long should you average each measurement? (Hint: averaging over an integer number of periods cancels periodic noise)
2. Would it be better to average many fast samples or take one slow measurement? Justify your answer using spectral analysis.

## Reflection Questions

1. Your FFT shows an unexpected peak at 120 Hz that wasn't present in your function generator signal. List three possible physical sources for this frequency and describe how you would determine which is responsible.

2. A colleague claims that increasing the sample rate will improve their frequency resolution. Are they correct? What parameter actually controls frequency resolution?
