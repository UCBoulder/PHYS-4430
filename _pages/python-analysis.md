---
title: "Data Analysis with Python"
layout: textlay
sitemap: false
permalink: /python-analysis
---

# Data Analysis with Python

This page covers the core Python skills for data analysis in PHYS 4430: working with arrays, making plots, fitting data to models, spectral analysis, and propagating uncertainties.

## Table of Contents

{:.no_toc}

* TOC
{:toc}

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

print(f"Slope: {m_fit:.3f} +/- {m_err:.3f}")
print(f"Intercept: {b_fit:.3f} +/- {b_err:.3f}")
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

print(f"Amplitude: {popt[0]:.2f} +/- {perr[0]:.2f}")
print(f"Center: {popt[1]:.2f} +/- {perr[1]:.2f}")
print(f"Width: {popt[2]:.2f} +/- {perr[2]:.2f}")
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

# FFT and Spectral Analysis

Fourier analysis lets you identify frequency components in your data, useful for finding noise sources (like 60 Hz interference) and understanding signal characteristics.

## Computing the FFT

```python
import numpy as np

def compute_power_spectrum(signal, sample_rate):
    """
    Compute the one-sided power spectrum of a signal.

    For real signals, the spectrum is symmetric, so we only
    need the positive frequency half.

    Parameters:
        signal: 1D array of signal values
        sample_rate: Sampling rate in Hz

    Returns:
        frequencies: Array of positive frequency values (Hz)
        power: Array of power values
    """
    n = len(signal)

    # Compute FFT
    fft_result = np.fft.fft(signal)

    # One-sided spectrum (positive frequencies only)
    n_unique = n // 2 + 1
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)[:n_unique]
    frequencies = np.abs(frequencies)

    # Power spectrum (magnitude squared, normalized)
    power = (np.abs(fft_result[:n_unique]) / n) ** 2

    # Double power for frequencies that appear twice (all except DC and Nyquist)
    power[1:-1] *= 2

    return frequencies, power
```

## Basic FFT Example

```python
import numpy as np
import matplotlib.pyplot as plt

# Generate a test signal: 50 Hz + 120 Hz + noise
sample_rate = 1000  # Hz
duration = 1.0      # seconds
n_samples = int(sample_rate * duration)

t = np.arange(n_samples) / sample_rate
signal = (np.sin(2 * np.pi * 50 * t) +
          0.5 * np.sin(2 * np.pi * 120 * t) +
          0.2 * np.random.randn(n_samples))

# Compute power spectrum
frequencies, power = compute_power_spectrum(signal, sample_rate)

# Plot time domain and frequency domain
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(t * 1000, signal, 'b-', linewidth=0.5)
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Time Domain')
ax1.set_xlim(0, 100)  # Show first 100 ms
ax1.grid(True)

ax2.plot(frequencies, power, 'r-')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Power')
ax2.set_title('Frequency Domain (Power Spectrum)')
ax2.set_xlim(0, 200)  # Show up to 200 Hz
ax2.grid(True)

plt.tight_layout()
plt.show()
```

## Understanding FFT Parameters

| Parameter | Formula | Meaning |
|-----------|---------|---------|
| Nyquist frequency | $f_N = f_s / 2$ | Maximum frequency you can measure |
| Frequency resolution | $\Delta f = f_s / N$ | Smallest frequency difference you can distinguish |
| Total duration | $T = N / f_s$ | Longer duration = better frequency resolution |

**Example:** With $f_s = 1000$ Hz and $N = 1000$ samples:
- Nyquist frequency: 500 Hz
- Frequency resolution: 1 Hz
- Duration: 1 second

## Aliasing

If your signal contains frequencies above the Nyquist frequency ($f_s/2$), they will "fold back" and appear at incorrect frequencies. This is called aliasing.

```python
import numpy as np
import matplotlib.pyplot as plt

def demonstrate_aliasing(signal_freq, sample_rate):
    """Show how undersampling causes aliasing."""
    nyquist = sample_rate / 2

    print(f"Signal: {signal_freq} Hz")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Nyquist: {nyquist} Hz")

    if signal_freq > nyquist:
        aliased = abs(signal_freq - sample_rate * round(signal_freq / sample_rate))
        print(f"ALIASED to: {aliased} Hz")
    else:
        print("No aliasing (signal below Nyquist)")

# Examples
demonstrate_aliasing(50, 1000)   # OK: 50 Hz < 500 Hz
demonstrate_aliasing(800, 1000)  # Aliased: 800 Hz > 500 Hz, appears at 200 Hz
```

**Rule of thumb:** Sample at least 2x your highest frequency of interest (preferably 5-10x).

## Identifying Noise Sources

Common frequencies to look for in your spectrum:

| Frequency | Source |
|-----------|--------|
| 60 Hz (and harmonics: 120, 180...) | Power line interference |
| Low frequency drift | Temperature changes, mechanical vibration |
| High frequency noise | Electronic noise, quantization |

---

# Error Propagation

When you calculate a result from measured quantities, uncertainties propagate through the calculation.

## Manual Error Propagation

For a function $f(x, y)$ with independent uncertainties $\sigma_x$ and $\sigma_y$:

$$\sigma_f = \sqrt{\left(\frac{\partial f}{\partial x}\right)^2 \sigma_x^2 + \left(\frac{\partial f}{\partial y}\right)^2 \sigma_y^2}$$

**Example:** For $f = x \cdot y$:

```python
import numpy as np

x = 5.0
sigma_x = 0.1
y = 3.0
sigma_y = 0.2

f = x * y  # = 15.0

# Partial derivatives: df/dx = y, df/dy = x
sigma_f = np.sqrt((y * sigma_x)**2 + (x * sigma_y)**2)

print(f"f = {f:.2f} +/- {sigma_f:.2f}")
```

## Using the Uncertainties Package

The `uncertainties` package handles error propagation automatically:

```python
from uncertainties import ufloat
import uncertainties.umath as umath

# Define values with uncertainties
x = ufloat(5.0, 0.1)  # 5.0 +/- 0.1
y = ufloat(3.0, 0.2)  # 3.0 +/- 0.2

# Arithmetic propagates uncertainties automatically
f = x * y
print(f"x * y = {f}")  # 15.0+/-1.1

g = x + y
print(f"x + y = {g}")  # 8.0+/-0.22

h = x / y
print(f"x / y = {h}")  # 1.67+/-0.12
```

## Math Functions with Uncertainties

```python
from uncertainties import ufloat
import uncertainties.umath as umath

angle = ufloat(0.5, 0.01)  # radians

# Trig functions
sin_val = umath.sin(angle)
cos_val = umath.cos(angle)

print(f"sin({angle}) = {sin_val}")
print(f"cos({angle}) = {cos_val}")

# Exponential and log
value = ufloat(2.0, 0.1)
exp_val = umath.exp(value)
log_val = umath.log(value)

print(f"exp({value}) = {exp_val}")
print(f"log({value}) = {log_val}")
```

## Working with Arrays

```python
from uncertainties import ufloat, unumpy
import numpy as np

# Create arrays with uncertainties
values = [ufloat(1.0, 0.1), ufloat(2.0, 0.15), ufloat(3.0, 0.2)]

# Or from separate arrays
nominal = np.array([1.0, 2.0, 3.0])
errors = np.array([0.1, 0.15, 0.2])
values = unumpy.uarray(nominal, errors)

# Operations work element-wise
squared = values ** 2
print(squared)

# Extract nominal values and uncertainties
print(f"Nominal: {unumpy.nominal_values(squared)}")
print(f"Std dev: {unumpy.std_devs(squared)}")
```

## Example: Beam Waist Calculation

```python
from uncertainties import ufloat
import uncertainties.umath as umath

# Measured beam width at two positions
w1 = ufloat(0.50, 0.02)  # mm
w2 = ufloat(0.75, 0.03)  # mm
z = ufloat(100.0, 1.0)   # mm between measurements

wavelength = 632.8e-6  # mm (He-Ne laser)

# Calculate beam waist (simplified formula)
# w0 = sqrt(w1 * w2) for certain geometries
w0 = umath.sqrt(w1 * w2)

print(f"Beam waist: {w0} mm")
# Output includes propagated uncertainty
```

---

# Common Troubleshooting

## Import Errors

**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:** Install the missing package:

```bash
pip install numpy
```

## Plot Not Showing

**Problem:** `plt.show()` does nothing

**Solutions:**

1. In Jupyter: Add `%matplotlib inline` at the top of your notebook
2. In VS Code: Make sure you're not running in a non-interactive environment
3. Try `plt.savefig('plot.png')` to save instead of display

## Curve Fit Not Converging

**Problem:** `OptimizeWarning: Covariance of the parameters could not be estimated`

**Solutions:**

1. Provide better initial guesses (`p0` parameter)
2. Check that your model function is appropriate for the data
3. Check for NaN or Inf values in your data
4. Try setting bounds on parameters

---

[Back to Python Resources](/PHYS-4430/python-resources)
