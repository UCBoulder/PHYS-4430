---
title: "Gaussian Beams - Week 3"
---

# Where We Are in the Sequence

**Week 3 of 4: Theory, First Automated Measurement, and Analysis**

Last week you characterized your photodetector's noise and chose an optimal gain setting. This week you'll learn the theoretical foundation for Gaussian beams, set up the motor controller, take your first automated beam profile, and apply error propagation to your real data.

**Last week:** Learned DAQ programming, characterized noise, chose gain setting
**This week:** Learn Gaussian beam theory → Set up motor → Take beam profile → Analyze with error propagation
**Next week:** Multiple beam profiles → Test Gaussian beam model → Investigate lens effects

# Overview

This week connects theory to practice. In the prelab, you'll derive the Gaussian beam equations from Maxwell's equations and develop physical intuition for beam propagation. In lab, you'll set up the motor controller and take your first motor-controlled beam profile. Then you'll apply error propagation to your actual data—not abstract examples—to predict uncertainties in your Week 4 measurements. By the end of this week, you'll have tested your entire measurement system and made quantitative predictions for next week.

# Learning Goals

After completing the prelab, you will be able to:

1. Derive the paraxial wave equation from Maxwell's equations by applying the slowly-varying envelope approximation.
2. Explain the physical meaning of Gaussian beam parameters ($w_0$, $w(z)$, $R(z)$, $\zeta(z)$) and how they relate to observable properties.
3. Predict how beam width changes with position using the Gaussian beam equations.

After completing the lab, you will be able to:

1. Set up and operate the motor controller for automated measurements.
2. Take a complete beam profile using motor-controlled positioning.
3. Fit beam profile data to extract beam width with uncertainty.
4. Propagate uncertainties from measured quantities to derived quantities.
5. Make quantitative predictions for Week 4 measurements based on your data.

# Overview of Your Work

This week has three phases:

**Phase 1 - Theory (Prelab, ~75 min):** Derive the Gaussian beam equations from Maxwell's equations and build physical intuition. You'll understand *why* beams have the shape they do.

**Phase 2 - Measurement (Lab, ~60 min):** Set up the motor controller and take a complete beam profile. This is your first automated measurement—a trial run before Week 4's systematic data collection.

**Phase 3 - Analysis (Lab, ~60 min):** Apply error propagation to your actual beam width measurement. Fit your data, calculate uncertainties, and make predictions for Week 4. This is where theory meets your measurements.

*See the detailed deliverables checklist at the end of this guide.*

# Prelab

This week's prelab focuses on the theoretical foundation for Gaussian laser beams. You'll derive the equations that describe how laser beams propagate and develop physical intuition for the key parameters. Error propagation will be covered in lab, where you'll apply it directly to your measurements.

## Gaussian beam theory

Light is a propagating oscillation of the electromagnetic field. The general principles which govern electromagnetic waves are Maxwell's equations. From these general relations, a vector wave equation can be derived.

$$ \nabla^2\vec{E}=\mu_0\epsilon_0 \frac{\partial^2\vec{E}}{\partial t^2}\text{.}$$ {#eq:1}


One of the simplest solutions is that of a plane wave propagating in the $\hat{z}$ direction:

$$\vec{E}(x,y,z,t)=E_x\hat{x}cos(kz-\omega t+\phi_x)+E_y\hat{y}cos(kz-\omega t+\phi_y)\text{.}\quad\quad$$ {#eq:2}

But as the measurements from the first week showed, our laser beams are commonly well approximated by a beam shape with a Gaussian intensity profile. Apparently, since these Gaussian profile beams exist, they must be solutions of the wave equation. The next section will discuss how we derive the Gaussian beam electric field, and give a few key results.

## Paraxial wave equation {#sec:wave-eqn}

One important thing to note about the beam output from most lasers is that the width of the beam changes very slowly compared to the wavelength of light. Assume a complex solution, where the beam is propagating in the $\hat{z}$-direction, with the electric field polarization in the $\hat{x}$-direction:

$$\vec{E}(x,y,z,t)=\hat{x}A(x,y,z)e^{i(kz-\omega t)}\text{.}$$ {#eq:3}

The basic idea is that the spatial pattern of the beam, described by the function $A(x,y,z)$, does not change much over a wavelength. In the case of the He-Ne laser output, the function $A(x,y,z)$ is a Gaussian profile that changes its width as a function of $z$. If we substitute the trial solution in Equation @eq:3 into the wave equation in Equation @eq:1 we get

$$\hat{x} \left[ \left(\frac{\partial^2A}{\partial x^2} +\frac{\partial^2A}{\partial y^2} +\frac{\partial^2A}{\partial z^2} \right) +2ik\frac{\partial A}{\partial z} - k^2A \right]e^{i(kz-\omega t)}=\hat{x}\mu_0\epsilon_oA(-\omega^2)e^{i(kz-\omega t)}\text{.}\quad\quad$$ {#eq:4}

This can be simplified recognizing that $k^2=\omega^2/c^2=\mu_0\epsilon_0\omega^2$, where the speed of light is related to the permeability and permittivity of free space by $c=(\mu_0\epsilon_0)^{-1/2}$. Also, the $\hat{x}e^{i(kz-\omega t)}$ term is common to both sides and can be dropped, which results in

$$\left(\frac{\partial^2A}{\partial x^2} +\frac{\partial^2A}{\partial y^2} +\frac{\partial^2A}{\partial z^2} \right) +2ik\frac{\partial A}{\partial z}=0\text{.}\quad\quad$$ {#eq:5}

So far, we have made no approximation to the solution or the wave equation, but now we apply the assumption that $\partial{A}(x,y,z)/\partial{z}$ changes slowly over a wavelength $\lambda = 2\pi /k$, so we neglect the term

$$\left| \frac{\partial^2A}{\partial z^2} \right| \ll \left|2k\frac{\partial A}{\partial z}\right|\text{.}$$ {#eq:6}

Finally, we get the paraxial wave equation,

$$\frac{\partial^2A}{\partial x^2} +\frac{\partial^2A}{\partial y^2} + 2ik\frac{\partial A}{\partial z}=0\text{.}$$ {#eq:7}

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

*You will fit actual beam width data in lab today using these modified equations.*

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
pip install pythonnet uncertainties
```

- `pythonnet`: Required for interfacing with Thorlabs Kinesis motor control
- `uncertainties`: Required for error propagation calculations in the analysis section

(You should already have `nidaqmx`, `numpy`, `scipy`, and `matplotlib` from Week 2.)

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

# Taking Your First Automated Beam Profile

Now that you have the motor controller working, take a complete beam profile measurement. This serves two purposes: (1) verify your entire measurement system works end-to-end, and (2) generate real data for the analysis section.

## Measurement Procedure

1. **Position the knife-edge assembly** at a known distance from the laser (measure and record this distance—you'll need it for analysis).

2. **Set up the measurement:**
   - Ensure the photodetector is receiving the full beam when the knife-edge is retracted
   - Use the gain setting you determined in Week 2
   - Verify DAQ is reading reasonable voltages

3. **Take the beam profile:**
   - Move the knife-edge across the beam in steps of 0.05-0.1 mm
   - At each position, record the motor position and photodetector voltage
   - Continue until the beam is fully blocked (voltage reaches dark level)
   - Aim for 20-30 data points across the transition

4. **Save your data** with a descriptive filename including the date and z-position.

**Tip:** If using manual motor commands, you can automate data collection with a simple loop:

```python
import time
import numpy as np
import nidaqmx

# Configuration
positions = np.arange(0, 3, 0.1)  # 0 to 3 mm in 0.1 mm steps
data = []

for pos in positions:
    # Move motor to position (use your motor control code)
    # motor.MoveTo(pos)
    time.sleep(0.3)  # Wait for motor to settle

    # Read voltage
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        voltage = np.mean(task.read(number_of_samples_per_channel=100))

    data.append([pos, voltage])
    print(f"Position: {pos:.2f} mm, Voltage: {voltage:.4f} V")

# Save data
np.savetxt('beam_profile_week3.csv', data, delimiter=',',
           header='Position (mm), Voltage (V)', comments='')
```

## Quick Check

Before proceeding to analysis, verify your data looks reasonable:
- Does the voltage transition smoothly from high to low?
- Is the transition region clearly visible?
- Do you have enough points in the transition region (where the voltage changes)?

If the data looks noisy or the transition is unclear, retake the measurement with smaller step sizes or more averaging.

# Applying Theory to Your Measurements

This section connects the Gaussian beam theory from your prelab to your actual measurements. You'll learn error propagation by applying it to your own data—not abstract examples.

## Error Propagation: From Measured to Derived Quantities

The quantity of interest in an experiment is often derived from other measured quantities. For example, you'll derive beam width $w$ from your knife-edge data, then use $w$ at multiple positions to determine the beam waist $w_0$.

### The General Formula

Suppose you want to derive a quantity $z$ from measured quantities $a, b, c, ...$. The mathematical function is $z = z(a, b, c, ...)$. The propagated uncertainty in $z$ is:

$$\sigma_z^2 = \left( \frac{\partial z}{\partial a}\right)^2\sigma_a^2+\left( \frac{\partial z}{\partial b}\right)^2\sigma_b^2+\left( \frac{\partial z}{\partial c}\right)^2\sigma_c^2+ \ ...\text{.}$$

This comes directly from calculus—it's the linear approximation of how fluctuations in inputs cause fluctuations in outputs.

### Error Propagation in Python

For complex calculations, the `uncertainties` package automatically tracks error propagation:

```python
from uncertainties import ufloat
from uncertainties.umath import sqrt

# Define values with uncertainties
V = ufloat(5.0, 0.1)   # 5.0 ± 0.1 V
I = ufloat(0.5, 0.02)  # 0.5 ± 0.02 A

# Calculate - uncertainty propagates automatically
R = V / I
print(f"R = {R}")  # Shows value ± uncertainty
```

## Fitting Your Beam Profile Data

Now fit your beam profile data to extract the beam width.

### Step 1: Load and Plot Your Data

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf

# Load your data
data = np.loadtxt('beam_profile_week3.csv', delimiter=',', skiprows=1)
position = data[:, 0]  # mm
voltage = data[:, 1]   # V

# Plot raw data
plt.figure(figsize=(10, 6))
plt.plot(position, voltage, 'bo', label='Data')
plt.xlabel('Position (mm)')
plt.ylabel('Voltage (V)')
plt.title('Beam Profile - Week 3')
plt.grid(True, alpha=0.3)
plt.show()
```

### Step 2: Define and Fit the Error Function Model

The knife-edge measurement gives an integrated Gaussian, which is the error function:

$$V(x) = \frac{V_{max} - V_{min}}{2} \left[1 - \text{erf}\left(\frac{\sqrt{2}(x - x_0)}{w}\right)\right] + V_{min}$$

```python
def beam_profile(x, V_max, V_min, center, width):
    """Error function model for knife-edge beam profile.

    Parameters:
        x: position (mm)
        V_max: maximum voltage when beam is unblocked (V)
        V_min: minimum voltage when beam is blocked (V)
        center: beam center position (mm)
        width: beam width w (mm)

    Note: This form uses V_max/V_min instead of amplitude/offset
    for physical clarity. The forms are equivalent:
        amplitude = (V_max - V_min) / 2
        offset = (V_max + V_min) / 2
    """
    return (V_max - V_min) / 2 * (1 - erf(np.sqrt(2) * (x - center) / width)) + V_min

# Initial guesses
V_max_guess = np.max(voltage)
V_min_guess = np.min(voltage)
center_guess = position[len(position)//2]
width_guess = 0.5  # mm

p0 = [V_max_guess, V_min_guess, center_guess, width_guess]

# Fit the data
popt, pcov = curve_fit(beam_profile, position, voltage, p0=p0)
perr = np.sqrt(np.diag(pcov))

# Extract results
V_max, V_min, center, width = popt
V_max_err, V_min_err, center_err, width_err = perr

print(f"Beam width: w = {width:.4f} ± {width_err:.4f} mm")
print(f"Beam center: x0 = {center:.4f} ± {center_err:.4f} mm")
```

### Step 3: Plot the Fit

```python
# Generate smooth curve for plotting
x_fit = np.linspace(position.min(), position.max(), 200)
v_fit = beam_profile(x_fit, *popt)

plt.figure(figsize=(10, 6))
plt.plot(position, voltage, 'bo', label='Data')
plt.plot(x_fit, v_fit, 'r-', label=f'Fit: w = {width:.3f} ± {width_err:.3f} mm')
plt.xlabel('Position (mm)')
plt.ylabel('Voltage (V)')
plt.title('Beam Profile with Error Function Fit')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('beam_profile_fit.png', dpi=150)
plt.show()
```

**Record in your notebook:**
- Beam width: $w = $ _______ $\pm$ _______ mm
- Measurement position: $z = $ _______ m from laser

**Connection to Week 2:** The uncertainty in your fit parameters depends on the noise level in your voltage measurements. Your Week 2 noise characterization tells you what σ_V to expect at your gain setting. Look at the residuals (data minus fit)—does their scatter match your predicted noise level? If the residuals are much larger than expected, you may have additional noise sources (vibration, beam drift) affecting your measurement.

## Predicting Week 4 Results

Now use your measured beam width to make predictions for Week 4. This is where error propagation becomes practical.

### Step 1: Estimate Beam Waist from Your Measurement

Using the Gaussian beam equation:

$$w(z) = w_0\sqrt{1+\left(\frac{\lambda (z - z_w)}{\pi w_0^2}\right)^2}$$

If we assume $z_w \approx 0$ (beam waist at laser output), we can estimate $w_0$ from a single measurement. Rearranging:

```python
from uncertainties import ufloat
from uncertainties.umath import sqrt
import numpy as np

# Your measured values (replace with your actual data)
w_measured = ufloat(0.52, 0.03)  # mm - USE YOUR VALUE
z_measured = ufloat(1.5, 0.01)   # m - USE YOUR VALUE
wavelength = 632.8e-9  # m (He-Ne laser)

# Convert w to meters
w_m = w_measured * 1e-3

# For a beam at distance z from waist, we can estimate w0
# This is approximate - assumes z >> z_R (far from waist)
# w ≈ w0 * z * λ / (π * w0²) = z * λ / (π * w0)
# So w0 ≈ z * λ / (π * w)
w0_approx = z_measured * wavelength / (np.pi * w_m)

print(f"Approximate beam waist: w0 ≈ {w0_approx*1e6:.1f} μm")
```

### Step 2: Predict Beam Widths at Other Positions

Use error propagation to predict what you'll measure in Week 4:

```python
# Predict beam width at different positions
positions = [0.5, 1.0, 1.5, 2.0]  # meters

print("\nPredicted beam widths for Week 4:")
print("-" * 40)
for z in positions:
    z_val = ufloat(z, 0.01)
    z_R = np.pi * w0_approx**2 / wavelength
    w_pred = w0_approx * sqrt(1 + (z_val / z_R)**2)
    print(f"z = {z:.1f} m:  w = {w_pred*1e3:.3f} mm")
```

### Step 3: Record Your Predictions

Fill in this table in your notebook:

| Position $z$ | Predicted $w(z)$ | Predicted uncertainty |
|-------------|------------------|----------------------|
| 0.5 m | _______ mm | ± _______ mm |
| 1.0 m | _______ mm | ± _______ mm |
| 1.5 m | _______ mm | ± _______ mm |
| 2.0 m | _______ mm | ± _______ mm |

**Prediction reflection:** If your Week 4 measurements differ significantly from these predictions, what are the most likely causes? List at least two possibilities, and for each one, describe what signature in your Week 4 data would distinguish that cause from the others. (For example: Would the discrepancy be systematic across all positions? Would it affect near-field and far-field measurements differently?)

## Comparing Manual vs. Motor-Controlled Measurements

If you took beam width measurements manually in Week 1, compare them to today's motor-controlled measurement:

| Method | Beam width | Uncertainty | Notes |
|--------|-----------|-------------|-------|
| Week 1 (manual) | _______ mm | ± _______ mm | |
| Week 3 (motor) | _______ mm | ± _______ mm | |

Are they consistent within uncertainties? If not, what might explain the difference?

# Deliverables and Assessment

Your lab notebook should include the following for this week:

## Prelab (complete before lab, ~75 min)

1. **Paraxial wave equation derivation**: show the key steps from Maxwell's equations to Equation 7
2. **Physical Intuition Check**: answers to all 5 questions
3. **Gaussian beam model questions**: answers to questions 1-4 in "Trying out the Gaussian beam model"
4. **Beyond Beam Width reflection**: when might you need to measure $R(z)$ or $\zeta(z)$ directly?

## In-Lab Documentation

### Phase 2: Measurement (~60 min)
1. **Motor controller verification**:
   - Completed setup checklist (DAQ, motor connection, movement test)
   - Motor serial number recorded
   - Troubleshooting reflection
2. **Beam profile data**:
   - Raw data file saved
   - Position of measurement from laser: $z = $ _______ m
   - Quick check: does data show clean transition?

### Phase 3: Analysis (~60 min)
3. **Beam profile fit**:
   - Fit plot showing data and error function model
   - Extracted beam width: $w = $ _______ $\pm$ _______ mm
4. **Error propagation and predictions**:
   - Estimated beam waist $w_0$
   - Predicted beam widths at 4 positions for Week 4
   - Prediction reflection (what could cause disagreement?)
5. **Comparison** (if Week 1 data available):
   - Manual vs. motor-controlled beam width comparison

## Code Deliverables

1. Motor communication test script
2. Beam profile fitting script

## Reflection Questions

1. What was the dominant source of uncertainty in your beam width measurement? How could you reduce it?

2. Based on your motor controller setup experience, what was the most challenging part? How would you help a classmate who encountered the same issue?

3. Look at your predicted beam widths for Week 4. Which measurement position will have the largest *relative* uncertainty (σ_w / w)? Why?
