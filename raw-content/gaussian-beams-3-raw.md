---
title: "Gaussian Beams - Week 3"
---

# Where We Are in the Sequence

**Week 3 of 4: Theory and Preparation for Automation**

Last week you characterized your photodetector's noise and chose an optimal gain setting. This week you'll learn the theoretical foundation for Gaussian beams (which you'll test next week), develop spectral analysis skills to understand noise sources, and set up the motor controller for automated measurements.

**Last week:** Learned DAQ programming, characterized noise, chose gain setting
**This week:** Learn Gaussian beam theory → Analyze noise spectra → Set up motor controller
**Next week:** Automated measurements → Test Gaussian beam model → Investigate lens effects

# Overview

The third week of the Gaussian Beams lab builds upon the Python data acquisition skills you developed last week. This week's prelab covers error propagation (how uncertainties in measured quantities affect derived quantities) and introduces the theoretical foundation for Gaussian laser beams, deriving the equations you'll use in Week 4's experiments. In the lab portion, you will use spectral analysis tools to perform Fourier Transforms, set up the motor controller hardware for automated measurements, and revisit your beam width measurement. Be sure to document all of your work in your lab notebook.

# Learning Goals

After completing the prelab, you will be able to:

1. Propagate uncertainties from measured quantities to derived quantities using partial derivatives.
2. Derive the paraxial wave equation from Maxwell's equations by applying the slowly-varying envelope approximation.
3. Explain the physical meaning of Gaussian beam parameters ($w_0$, $w(z)$, $R(z)$, $\zeta(z)$) and how they relate to observable properties.
4. Fit experimental beam width data to extract beam waist $w_0$ and waist position $z_w$ with uncertainties.

After completing the lab, you will be able to:

1. Explain what a Fourier Transform reveals about a signal and interpret a power spectrum.
2. Compute and plot the power spectrum of a measured signal using NumPy's FFT functions.
3. Identify frequency components in experimental data and relate them to physical sources.
4. Set up and verify the motor controller for automated measurements.
5. Measure beam width using the knife-edge technique and compare automated vs. manual methods.

# Overview of Your Work

This week prepares you for next week's automated experiments. Your work has two parallel threads:

**Theory (Prelab):** You'll derive the Gaussian beam equations from Maxwell's equations and learn error propagation. This isn't abstract—you'll use these equations to interpret your Week 4 data, and error propagation will tell you whether your measured beam waist is consistent with theory.

**Skills (Lab):** You'll develop two capabilities needed for automation:

1. **Spectral analysis** — Use FFT to identify frequency components in signals. You'll apply this to your photodetector's noise spectrum to understand what's limiting your measurements.
2. **Motor control** — Set up the Thorlabs translation stage and verify you can command it from Python. This is the final piece for automated beam profiling.

**Complete your beam width measurement** if you didn't finish in Week 1. You'll need this data for analysis practice.

*See the detailed deliverables checklist at the end of this guide.*

# Prelab

This week's prelab covers two topics: error propagation and the theoretical foundation for Gaussian laser beams.

## Connecting to Your Week 2 Work

In Week 2, you characterized your photodetector's noise and chose a gain setting. This week, you'll learn how those noise measurements propagate through your analysis to determine the uncertainty in your final results.

The chain of uncertainty is:
1. **Voltage noise** (measured in Week 2) → determines uncertainty in each beam profile point
2. **Beam profile uncertainty** → propagates through curve fitting to give uncertainty in beam width $w$
3. **Beam width uncertainty at multiple positions** → propagates through the Gaussian beam model to give uncertainty in $w_0$ and $z_w$

This section teaches the mathematical framework for steps 2 and 3. By the end, you'll be able to predict the uncertainty in your Week 4 measurements before you take them.

## Error propagation - from measured to derived quantities

The quantity of interest in an experiment is often derived from other measured quantities. An example is estimating the resistance of a circuit element from measurements of current and voltage, using Ohm's law ($R=V/I$) to convert our measured quantities (voltage and current) into a derived quantity (resistance).

Error propagation comes in when we want to estimate the uncertainty in the derived quantity based on the uncertainties in the measured quantities. Keeping things general, suppose we want to derive a quantity $z$ from a set of measured quantities $a,b,c, \ ... \ $. The mathematical function which gives us $z$ is $z=z(a,b,c, \ ... \ )$. In general, any fluctuation in the measured quantities $a,b,c, \ ... \ $ will cause a fluctuation in $z$ according to

$$\delta z = \left( \frac{\partial z}{\partial a}\right)\delta a+\left( \frac{\partial z}{\partial b}\right)\delta b+\left( \frac{\partial z}{\partial c}\right)\delta c+ \ ...\text{.}\quad\quad$$

This equation comes straight from basic calculus. It's like the first term in a Taylor series. It's the linear approximation of $z(a,b,c, \ ... \ )$ near $(a_0,b_0,c_0, \ ... \ )$. However, we don't know the exact magnitude or sign of the fluctuations, rather we just can estimate the spread in $\delta a, \delta b, \delta c, \ ... \ $, which we often use the standard deviations $\sigma_a, \sigma_b, \sigma_c, \ ... \ $ In this case, the propagated uncertainty in $z$ is:

$$\sigma_z^2 = \left( \frac{\partial z}{\partial a}\right)^2\sigma_a^2+\left( \frac{\partial z}{\partial b}\right)^2\sigma_b^2+\left( \frac{\partial z}{\partial c}\right)^2\sigma_c^2+ \ ...\text{.}\quad\quad$$

There are standard equations provided in courses like the introductory physics lab for the error in the sum, difference, product, quotient. These are all easily derived from this general formula.

## Error propagation in Python

There are two main approaches to error propagation in Python:

### Approach 1: Manual calculation

For simple cases, you can compute partial derivatives manually:

```python
import numpy as np

# Example: R = V / I
# Measured values and uncertainties
V = 5.0      # Voltage (V)
sigma_V = 0.1  # Uncertainty in V
I = 0.5      # Current (A)
sigma_I = 0.02  # Uncertainty in I

# Calculate resistance
R = V / I

# Partial derivatives
dR_dV = 1 / I
dR_dI = -V / I**2

# Propagated uncertainty
sigma_R = np.sqrt((dR_dV * sigma_V)**2 + (dR_dI * sigma_I)**2)

print(f"R = {R:.2f} ± {sigma_R:.2f} Ω")
```

### Approach 2: Using the `uncertainties` package

For more complex calculations, the `uncertainties` package automatically tracks error propagation:

```python
from uncertainties import ufloat
from uncertainties.umath import sqrt  # Use umath for math functions

# Define values with uncertainties
V = ufloat(5.0, 0.1)   # 5.0 ± 0.1 V
I = ufloat(0.5, 0.02)  # 0.5 ± 0.02 A

# Calculate - uncertainty propagates automatically
R = V / I

print(f"R = {R}")  # Shows value ± uncertainty
```

### Exercise: Beam width uncertainty

Later in this prelab, we will model a Gaussian beam's width $w(z)$ as:

$$w(z) = w_0\sqrt{1+\left(\frac{z-z_0}{\pi w_0^2/\lambda}\right)^2}\text{.}$$

For the output beam of one of the lasers in the lab, a fit of beam width versus position gave the following fit parameters:

$$z_0 = -0.03 \pm 0.04 \ m$$

$$w_0=(1.90 \pm 0.09)\times 10^{-6} \ m$$

The wavelength is given by $\lambda = 632.8 \pm 0.1 \ nm$.

1. Use Python to estimate the uncertainty in the derived width $w(z)$ when $z$ is a distance of $2.000 \pm 0.005 \ m$ from the waist position.

   Using the `uncertainties` package:

   ```python
   from uncertainties import ufloat
   from uncertainties.umath import sqrt
   import numpy as np

   # Define parameters with uncertainties
   z0 = ufloat(-0.03, 0.04)           # m
   w0 = ufloat(1.90e-6, 0.09e-6)      # m
   wavelength = ufloat(632.8e-9, 0.1e-9)  # m
   z = ufloat(2.000, 0.005)           # m

   # Calculate beam width
   z_R = np.pi * w0**2 / wavelength  # Rayleigh range
   w = w0 * sqrt(1 + ((z - z0) / z_R)**2)

   print(f"w(z) = {w}")
   ```

## Gaussian beam theory

Light is a propagating oscillation of the electromagnetic field. The general principles which govern electromagnetic waves are Maxwell's equations. From these general relations, a vector wave equation can be derived.

$$ \nabla^2\vec{E}=\mu_0\epsilon_0 \frac{\partial^2\vec{E}}{\partial t^2}\text{.}$$ {#eq:1}


One of the simplest solutions is that of a plane wave propagating in the $\hat{z}$ direction:

$$\vec{E}(x,y,z,t)=E_x\hat{x}cos(kz-\omega t+\phi_x)+E_y\hat{y}cos(kz-\omega t+\phi_y)\text{.}\quad\quad$$ {#eq:2}

But as the measurements from the first week showed, our laser beams are commonly well approximated by a beam shape with a Gaussian intensity profile. Apparently, since these Gaussian profile beams exist, they must be solutions of the wave equation. The next section will discuss how we derive the Gaussian beam electric field, and give a few key results.

## Paraxial wave equation {#sec:wave-eqn}

One important thing to note about the beam output from most lasers is that the width of the beam changes very slowly compared to the wavelength of light. Assume a complex solution, where the beam is propagating in the $\hat{z}$-direction, with the electric field polarization in the $\hat{x}$-direction:

$$\vec{E}(x,y,z,t)=\hat{x}A(x,y,z)e^{kz-\omega t}\text{.}$$ {#eq:3}

The basic idea is that the spatial pattern of the beam, described by the function $A(x,y,z)$, does not change much over a wavelength. In the case of the He-Ne laser output, the function $A(x,y,z)$ is a Gaussian profile that changes its width as a function of $z$. If we substitute the trial solution in Equation @eq:3 into the wave equation in Equation @eq:1 we get

$$\hat{x} \left[ \left(\frac{\partial^2A}{\partial x^2} +\frac{\partial^2A}{\partial y^2} +\frac{\partial^2A}{\partial z^2} \right) +2ik\frac{\partial A}{\partial z} - k^2A \right]e^{i(kz-\omega t)}=\hat{x}\mu_0\epsilon_oA(-\omega^2)e^{i(kz-\omega t)}\text{.}\quad\quad$$ {#eq:4}

This can be simplified recognizing that $k^2=\omega^2/c^2=\mu_0\epsilon_0\omega^2$, where the speed of light is related to the permeability and permittivity of free space by $c=(\mu_0\epsilon_0)^{-1/2}$. Also, the $\hat{x}e^{i(kz-\omega t)}$ term is common to both sides and can be dropped, which results in

$$\left(\frac{\partial^2A}{\partial x^2} +\frac{\partial^2A}{\partial y^2} +\frac{\partial^2A}{\partial z^2} \right) +2ik\frac{\partial A}{\partial z}=0\text{.}\quad\quad$$ {#eq:5}

So far, we have made no approximation to the solution or the wave equation, but now we apply the assumption that $\partial{A}(x,y,z)/\partial{z}$ changes slowly over a wavelength $\lambda = 2\pi /k$, so we neglect the term

$$\left| \frac{\partial^2A}{\partial z^2} \right| \ll \left|2k\frac{\partial A}{\partial z}\right|\text{.}$$ {#eq:6}

Finally, we get the paraxial wave equation,

$$\frac{\partial^2A}{\partial x^2} +\frac{\partial^2A}{\partial y^2} +\frac{\partial^2A}{\partial z^2}=0\text{.}$$ {#eq:7}

One set of solutions to the paraxial wave equation are Gauss-Hermite beams, which have an intensity profiles like those shown in Figure @fig:gauss-hermite. These are the same solutions as for the quantum simple harmonic oscillator, a topic that could be further explored as a final project.

The simplest of these solutions is the Gaussian beam, which has an electric field given by

$$\vec{E}(x,y,z,t) = \vec{E}_0\frac{w_0}{w(z)}exp\left(-\frac{x^2+y^2}{w^2(z)}\right)exp\left(ik\frac{x^2+y^2}{2R(z)}\right)e^{-i\zeta(z)}e^{i(kz-\omega t)}\text{,}\quad\quad$$ {#eq:8}

where $\vec{E_0}$ is a time-independent vector (orthogonal to propagation direction $\hat{z}$) whose magnitude denotes the amplitude of the laser's electric field and the direction denotes the direction of polarization. The beam radius $w(z)$is given by

$$w(z)=w_0\sqrt{1+\left(\frac{\lambda z}{\pi w_0^2}\right)^2}\text{.}$$ {#eq:9}

$R(z)$,the radius of curvature of the wavefront, is given by

$$R(z)=z\left(1+\left(\frac{\pi w_0^2}{\lambda z}\right)^2\right)\text{,}$$ {#eq:10}

and the Gouy phase is given by

$$\zeta(z)=arctan\frac{\pi w_0^2}{\lambda z}\text{.}$$ {#eq:11}

The remarkable thing about all these equations is that only two parameters need to be specified to give the whole beam profile: the wavelength $\lambda$ and the beam waist $w_0$, which is the narrowest point in the beam profile. There is a more general set of Hermite Gaussian modes which are shown in Figure @fig:gauss-hermite. The laser cavity typically produces the (0,0) mode shown in the upper left corner, but an optical cavity can also be used to create these other modes – a topic that can be explored in the final projects.

![Intensity distributions for the lowest order Gauss-Hermite solutions to the paraxial wave equation. The axes are in units of the beam width, $w$.](../resources/lab-guides/gaussian-laser-beams/gauss-hermite.png){#fig:gauss-hermite width="20cm"}

## Physical Intuition Check

Before applying these equations, test your physical understanding. Answer each question without looking at the equations, then verify with a calculation.

1. **Scaling the waist:** If you double the beam waist $w_0$, what happens to:
   - The divergence angle $\theta = \lambda / (\pi w_0)$ in the far field?
   - The Rayleigh range $z_R = \pi w_0^2 / \lambda$?

   *Intuition check:* A wider waist means the beam is more collimated (less divergent). Does your answer reflect this?

2. **Distance to double:** At what distance from the waist does the beam width double (i.e., $w(z) = 2w_0$)?

   *Hint:* Set up the equation and solve for $z$ in terms of $z_R$. The answer is a simple multiple of the Rayleigh range.

3. **Wavelength dependence:** Two lasers have identical beam waists $w_0$, but one is red (633 nm) and one is blue (450 nm). Which beam diverges more rapidly? Why?

4. **Conservation of energy:** As the beam expands, the width increases but the total power stays constant. What must happen to the peak intensity $I_{max}$ as $z$ increases? Write a proportionality relationship.

5. **Beam quality check:** You measure a beam width of 0.8 mm at $z = 1$ m from the laser. Assuming $\lambda = 633$ nm, what is the minimum possible beam waist? (Hint: The waist could be inside or outside the laser cavity.)

*Record your answers in your notebook. Getting physical intuition wrong is valuable—it reveals gaps in understanding that equations alone can hide.*

## Trying out the Gaussian beam model

In the first week of the lab, we assumed the intensity profile of the Gaussian beam was given by $I(x,y)=I_{max}e^{-2(x^2+y^2)/w^2}$. The equation for the electric field of the Gaussian Beam in Equation @eq:8 looks substantially more complicated.

1. How are the expressions for electric field and intensity related?
2. Is Equation @eq:8 consistent with the simple expression for intensity $I(x,y)=I_{max}e^{-2(x^2+y^2)/w^2}$?

The Gaussian beam equations given in Equations @eq:8 -@eq:11 assume the beam comes to its narrowest width (called the beam waist, $w_0$) at $z=0$.

3.  How would you rewrite these four equations assuming the beam waist occurs at a different position $z=z_w$?
4.  One way to check your answer is to make sure the equations simplify to Equations @eq:8 -@eq:11 in the special case of $z_w=0$.
5.  Write a Python function to fit [this data set](../resources/lab-guides/gaussian-laser-beams/Test_beam_width_data.csv). Assume the wavelength is $\lambda=632.8\ nm$.
    1. What is the functional form for your fit function?
    2. What are the different fit parameters and what do they mean?
    3. Is it a linear or nonlinear fit function? Why?
6.  You should get that a beam waist of $w_0=(93.9\pm0.1)\times10^{-6}\ m$ and occurs at a position $z_w=0.3396\pm0.0003\ m$.

## Beyond Beam Width: The Unmeasured Parameters

The Gaussian beam solution contains four key quantities: the beam width $w(z)$, the wavefront radius of curvature $R(z)$, the Gouy phase $\zeta(z)$, and the peak amplitude. In Week 4, you will measure only $w(z)$ using the knife-edge technique. What about the others?

### What we can and cannot measure with a knife edge

The knife-edge profiler measures **intensity** as a function of position. This directly gives you $w(z)$, the beam width. However:

- **$R(z)$ (radius of curvature):** This describes how the wavefronts are curved—flat at the waist, increasingly curved far away. A knife edge only sees intensity, not phase, so it cannot measure $R(z)$ directly.

- **$\zeta(z)$ (Gouy phase):** This is a phase shift that accumulates as the beam passes through its waist. Like $R(z)$, it requires phase-sensitive measurements.

### How would you measure R(z)?

If you wanted to measure the wavefront curvature, you would need **interferometry**—combining your beam with a reference beam and analyzing the interference pattern. The spacing and curvature of interference fringes reveals $R(z)$.

**Think about it:** Near the waist, $R(z) \to \infty$ (flat wavefronts). Far from the waist, $R(z) \approx z$ (spherical wavefronts centered on the waist). What does this tell you about how the beam's wavefronts evolve?

### How would you measure ζ(z)?

The Gouy phase shift is subtle—it's a $\pi$ total phase change as the beam goes from $z = -\infty$ to $z = +\infty$ through the waist. Detecting it requires:

1. **Interferometry with a reference beam** that bypasses the focus
2. **Mode-matching experiments** where the Gouy phase affects coupling efficiency

The Gouy phase has practical consequences: it affects the resonant frequencies of laser cavities and the focal properties of lens systems.

### Why does w(z) suffice for this lab?

For characterizing a laser beam's propagation, $w(z)$ is often the most practically important parameter because:

1. It determines the spot size for any application (machining, microscopy, communications)
2. Combined with the wavelength $\lambda$, it uniquely determines the waist $w_0$ and waist position $z_w$
3. Once you know $w_0$, you can *calculate* $R(z)$ and $\zeta(z)$ from the equations—you don't need to measure them separately

**Reflection:** In what applications might you actually need to measure $R(z)$ or $\zeta(z)$ rather than just calculating them from $w_0$? (Hint: When might the theoretical relationship break down?)

## Prediction Exercise: What Will You Measure?

Before taking beam width measurements in Week 4, make quantitative predictions using the Gaussian beam model. This exercise strengthens the connection between the mathematical formalism you just learned and the physical measurements you will make.

**1. Sketch the expected beam profile at three positions:**

Using the beam width equation $w(z) = w_0\sqrt{1+\left(\frac{\lambda z}{\pi w_0^2}\right)^2}$, sketch the expected transverse beam profile (intensity vs. x) at:

- $z = 0.5$ m from the laser output
- $z = 1.0$ m from the laser output
- $z = 2.0$ m from the laser output

For each sketch, indicate:
- The beam width $w(z)$ on your axes
- Whether the beam is diverging, converging, or at its waist
- The approximate peak intensity relative to the $z = 0.5$ m case

**2. Calculate expected beam widths:**

Using the Gaussian beam equation and assuming $w_0 \approx 0.5$ mm and $z_w \approx 0$ (beam waist at laser output):

| Position | Predicted $w(z)$ |
|----------|------------------|
| $z = 0.5$ m | _______ mm |
| $z = 1.0$ m | _______ mm |
| $z = 2.0$ m | _______ mm |

Show your calculation for at least one position.

**3. Record your predictions** in your notebook before taking any measurements. In Week 4, you will compare these predictions to your experimental results to test the Gaussian beam model.

**4. Prediction reflection:**

If your Week 4 measurements differ significantly from these predictions, what are the most likely causes? List at least two possibilities and how you would distinguish between them.

# Fourier Analysis Techniques

In Week 2, you learned about the Nyquist frequency and how sample rate affects your ability to accurately capture signals. This week, we'll analyze signals in the **frequency domain** using Fourier Transforms. This is a powerful technique used throughout physics and engineering.

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

### Connecting FFT to Your Gaussian Beams Experiment

The spectral analysis techniques you've learned have direct applications to your beam profiling work. In this section, you'll analyze the photodetector signal to understand noise sources that could affect your Week 4 measurements.

1. **Photodetector noise spectrum.** Connect your photodetector to the DAQ (as in Week 2) with the beam blocked.

   1. Acquire 1-2 seconds of data at 10 kHz sample rate.
   2. Compute and plot the power spectrum.
   3. Are there any peaks at specific frequencies? If so, what are likely physical sources? (Common culprits: 60 Hz power line, 120 Hz rectified power, computer switching frequencies, room lighting)
   4. How does the noise spectrum change when you change the photodetector gain setting?

2. **Signal spectrum with laser.** Now unblock the beam so light hits the photodetector.

   1. Acquire data and compute the power spectrum.
   2. Compare to the dark noise spectrum. What changed?
   3. If you see new peaks, what might cause periodic variations in laser intensity?

3. **Implications for beam profiling.** Consider your Week 4 automated measurements.

   1. Your beam profiler waits 500 ms between steps and takes a single voltage reading. Based on your noise spectrum, what frequencies could affect your measurement?
   2. If you wanted to reduce the effect of 60 Hz noise, how long should you average each measurement? (Hint: averaging over an integer number of periods cancels periodic noise)
   3. Would it be better to average many fast samples or take one slow measurement? Justify your answer using your spectral analysis.

4. **Quantitative prediction for Week 4.** Based on your noise spectrum analysis:

   1. Calculate the RMS noise you expect in a 100-sample average at 10 kHz sample rate. (Hint: if your single-sample RMS noise is $\sigma$, the RMS of an N-sample average is $\sigma/\sqrt{N}$, assuming white noise.)
   2. Record this prediction in your notebook: "Predicted RMS noise with 100-sample averaging: ______ mV"
   3. You will test this prediction in Week 4 by examining the scatter in your beam profile data.

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

# Setting Up the Motor Controller

In Week 4, you will use Python to automate beam profile measurements by controlling a motorized translation stage. This section guides you through setting up and verifying the motor controller hardware. Getting this working now will save significant time later.

## Hardware Overview

The Thorlabs KST101 is a stepper motor controller that can precisely position a translation stage. You will use it to move a razor blade across the laser beam while the DAQ records the photodetector signal.

The physical connections are:

1. **Motor Controller (KST101)**:
   - Connect the USB cable from the KST101 cube to your computer
   - Connect the power supply to the KST101
   - The motor should already be mechanically connected to the translation stage with the razor

2. **Optical Setup** (for testing):
   - Position the photodetector after the knife-edge in the beam path
   - Ensure the beam passes cleanly through when the razor is fully retracted

## Software Prerequisites

### 1. Thorlabs Kinesis SDK

Download and install from the Thorlabs website:
[https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)

**Important**: Choose the correct version:
- If you have 32-bit Python: Install the 32-bit Kinesis software
- If you have 64-bit Python: Install the 64-bit Kinesis software

To check your Python version, run:

```python
import sys
print(sys.maxsize > 2**32)  # True = 64-bit, False = 32-bit
```

### 2. Python Packages

Install the required packages:

```bash
pip install pythonnet
```

(You should already have `nidaqmx`, `numpy`, and `matplotlib` from Week 2.)

## Verifying the Motor Connection

### Test that Windows Recognizes the Device

1. Connect the USB to the KST101, then turn on power
2. Open **Device Manager** and look for the device under "USB devices" or "Thorlabs APT Device"
3. Note the serial number (displayed on the KST101 screen)

If you get a driver error, you may need to disable Memory Integrity in Windows Security (ask technical staff for help if this occurs on a lab computer).

### Test Basic Motor Communication

Run this test script to verify Python can communicate with the motor:

```python
import clr
import sys
import time

# Add Kinesis .NET assemblies
sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.StepperMotorCLI")

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper

# Build device list
DeviceManagerCLI.BuildDeviceList()

# Get list of connected devices
device_list = DeviceManagerCLI.GetDeviceList()
print(f"Found {len(device_list)} device(s):")
for serial in device_list:
    print(f"  Serial: {serial}")
```

If this shows your device serial number, the connection is working.

### Test Motor Movement

**Caution**: Make sure the translation stage has room to move before running this test. Check that nothing is blocking the stage mechanically.

```python
import clr
import sys
import time
from decimal import Decimal

sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.StepperMotorCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper

# Replace with your serial number
SERIAL_NUMBER = "26004813"  # Check the display on your KST101

DeviceManagerCLI.BuildDeviceList()
device = KCubeStepper.CreateKCubeStepper(SERIAL_NUMBER)

try:
    device.Connect(SERIAL_NUMBER)
    print("Connected!")

    # Wait for settings to initialize
    device.WaitForSettingsInitialized(5000)
    device.StartPolling(50)
    time.sleep(0.5)
    device.EnableDevice()
    time.sleep(0.5)

    # Load motor configuration
    config = device.LoadMotorConfiguration(SERIAL_NUMBER)

    # Get current position
    pos = device.Position
    print(f"Current position: {pos} mm")

    # Move relative (small test movement)
    print("Moving 0.5 mm...")
    device.SetMoveRelativeDistance(Decimal(0.5))
    device.MoveRelative(60000)  # 60 second timeout

    new_pos = device.Position
    print(f"New position: {new_pos} mm")

finally:
    device.StopPolling()
    device.Disconnect()
    print("Disconnected")
```

## Motor Controller Troubleshooting

**"Device not found" Error:**
- Check USB connection
- Verify serial number matches the display on the KST101
- Make sure no other software (APT User, Kinesis) is using the motor

**Motor Doesn't Move:**
- Ensure power is connected to the KST101
- Check that the stage isn't at a travel limit
- Verify the stage type is configured correctly in Kinesis (ZST225B)

**Python Import Errors:**
- Ensure Kinesis SDK is installed and matches Python architecture (32/64-bit)
- Check that the path to Kinesis DLLs is correct

## Exercise: Verify Your Setup

Before leaving lab today, verify that:

1. [ ] The DAQ can read voltages from the photodetector
2. [ ] Python can connect to the motor controller
3. [ ] The motor moves when commanded
4. [ ] You have noted your motor's serial number: ____________

This setup will be essential for the automated measurements in Week 4.

**Note on AI assistance:** The motor control code involves interfacing with hardware libraries that have specific requirements (correct DLL paths, serial numbers, initialization sequences). You may use AI to help generate this boilerplate code. What matters is that you can (1) verify the hardware is responding correctly, (2) diagnose common connection failures, and (3) modify parameters like movement distance and velocity. The Troubleshooting Reflection below tests these skills.

## Troubleshooting Reflection

Developing systematic troubleshooting skills is essential for experimental physics. Answer this question in your notebook:

**If the motor doesn't respond to Python commands, what troubleshooting steps would you take?**

List at least three things you would check, *in order of likelihood*, and explain your reasoning. Consider:
- What are the most common failure modes?
- What's the quickest way to isolate hardware vs. software issues?
- How would you determine if the problem is with Python, the USB connection, or the motor itself?

This systematic approach to troubleshooting will serve you well in Week 4 and beyond.

# Revisit Measuring the Beam Width

Now that you have the motor controller working, you're ready to prepare for Week 4's automated measurements. Review (and complete if necessary) [section 7](/PHYS-4430/lab-guides/gaussian-beams-1#measuring-the-beam-width) from Week 1.

Make sure you can:

1. Take a complete beam profile measurement manually
2. Fit the data using the error function model
3. Extract the beam width $w$ with uncertainty
4. Create a plot showing the data and fit

This will serve as your baseline for comparison with the automated measurements next week. If time permits, try using the motor controller to take a few data points—this will give you confidence that your setup is ready for Week 4.

# Deliverables and Assessment

Your lab notebook should include the following for this week:

## Prelab (complete before lab)

1. **Error propagation exercise**: calculation of $w(z)$ uncertainty using the `uncertainties` package
2. **Paraxial wave equation derivation**: show the key steps from Maxwell's equations to Equation 7
3. **Gaussian beam model questions**: answers to questions 1-4 in "Trying out the Gaussian beam model"
4. **Beam waist fitting**: fit results for the test data set with $w_0$ and $z_w$ values

## In-Lab Documentation

1. **FFT exercises**:
   - Plots comparing time-domain and frequency-domain representations
   - Answers to frequency resolution questions
   - Analysis of sine wave, square wave, and multi-frequency signals
   - **Photodetector noise spectrum** (new section): dark noise and signal spectra with analysis of implications for beam profiling
2. **Motor controller verification**:
   - Completed setup checklist (DAQ, motor connection, movement test)
   - Motor serial number recorded
3. **Beam width measurement** (from Week 1 or new):
   - Data table: position vs. voltage
   - Fit plot with extracted beam width and uncertainty

## Code Deliverables

1. Working spectral analysis script
2. Motor communication test script

## Reflection Questions

1. Your FFT shows an unexpected peak at 120 Hz that wasn't present in your function generator signal. List three possible physical sources for this frequency and describe how you would determine which is responsible.

2. You measure a beam width of $w = 0.52 \pm 0.03$ mm at position $z = 1.5$ m. Using the Gaussian beam equations, predict $w$ at $z = 2.0$ m, including the propagated uncertainty. Show your calculation.
