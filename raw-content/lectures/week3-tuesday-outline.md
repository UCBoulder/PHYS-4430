# Week 3 Tuesday Lecture: Motor Control and Error Propagation

**Date:** January 27, 2026
**Duration:** 50 minutes
**Purpose:** Prepare students for Lab 3 (motor controller setup, automated beam profiling, error propagation)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Explain the role of motor control in automated measurements
2. Describe the software architecture for controlling Thorlabs motors from Python
3. Apply the general error propagation formula to derive uncertainties in calculated quantities
4. Use the `uncertainties` package for automatic error propagation
5. Connect measurement uncertainties to predictions for future experiments

---

## Lecture Outline

### 1. Introduction and Context (3 min)

#### Where We Are

**Weeks 1-2:** Manual measurements, learned DAQ, characterized noise, derived Gaussian beam theory

**This week:** Connect theory to automated measurement
- Set up motor controller
- Take first automated beam profile
- Apply error propagation to make predictions

**Next week:** Test the Gaussian beam model systematically

#### Today's Lecture

Two topics that directly support this afternoon's lab:
1. **Motor control** — How to automate positioning with Python
2. **Error propagation** — How to track uncertainties through calculations

---

### 2. Motor Control for Automated Measurements (15 min)

#### 2.1 Why Automate?

**Manual measurements (Week 1):**
- Turn micrometer by hand
- Read position, read voltage
- Record in notebook
- Repeat 20-30 times

**Problems:**
- Slow and tedious
- Human error in recording
- Hard to take many data points
- Fatigue affects precision

**Automated measurements (Weeks 3-4):**
- Computer controls position
- Computer records data
- Can take 100+ points easily
- Reproducible and systematic

#### 2.2 The Hardware: Thorlabs KST101

*[Show image or physical device if available]*

| Component | Function |
|-----------|----------|
| **KST101 Controller** | "Brain" that drives the motor |
| **Stepper motor** | Precise rotation in discrete steps |
| **Translation stage** | Converts rotation to linear motion |
| **USB connection** | Computer ↔ Controller communication |

**Key specifications:**
- Position resolution: ~0.05 μm (far better than you need!)
- Travel range: 25 mm
- Velocity: adjustable, typically 1-2 mm/s for beam profiling

#### 2.3 Software Architecture

```
Your Python Script
       ↓
   pythonnet (bridge to .NET)
       ↓
   Thorlabs Kinesis SDK (.NET libraries)
       ↓
   USB Driver
       ↓
   KST101 Controller
       ↓
   Motor
```

**Why so many layers?**
- Thorlabs writes their SDK for .NET (C#/Windows)
- `pythonnet` lets Python call .NET code
- This is common for scientific instruments!

#### 2.4 The Basic Pattern

```python
import clr
import sys

# 1. Tell Python where to find Thorlabs libraries
sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.StepperMotorCLI")

# 2. Import the classes we need
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper

# 3. Find and connect to device
DeviceManagerCLI.BuildDeviceList()
device = KCubeStepper.CreateKCubeStepper("26004813")  # Your serial #
device.Connect("26004813")

# 4. Initialize (required sequence)
device.WaitForSettingsInitialized(5000)
device.StartPolling(50)
device.EnableDevice()

# 5. Move!
device.MoveRelative(0.5)  # Move 0.5 mm

# 6. Clean up
device.StopPolling()
device.Disconnect()
```

**The key commands:**
- `device.Position` — Read current position (mm)
- `device.MoveTo(x)` — Move to absolute position x
- `device.MoveRelative(dx)` — Move by relative amount dx

#### 2.5 Common Failure Modes

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "Device not found" | Wrong serial number | Check display on KST101 |
| "Device not found" | Another program using it | Close Kinesis/APT software |
| Import error | Wrong Python bitness | Match 32/64-bit to Kinesis |
| Motor doesn't move | No power | Check power supply connection |
| Motor doesn't move | At travel limit | Home the stage or move other direction |

#### 2.6 Systematic Troubleshooting

**When something doesn't work, isolate the problem:**

1. **Is the hardware connected?**
   - Check Device Manager for "Thorlabs APT Device"
   - If not visible → USB/driver issue

2. **Can Python see the device?**
   - Run `DeviceManagerCLI.BuildDeviceList()` and print device list
   - If empty → Kinesis SDK or pythonnet issue

3. **Can Python move the device?**
   - If connection works but movement fails → Check power, limits, configuration

**This systematic approach saves hours of frustration!**

---

### 3. Error Propagation: The Big Picture (5 min)

#### 3.1 The Problem

You measure quantities with uncertainty:
- Position: $z = 1.50 \pm 0.01$ m
- Beam width: $w = 0.52 \pm 0.03$ mm

You calculate derived quantities:
- Rayleigh range: $z_R = \pi w_0^2 / \lambda$
- Beam waist: $w_0 = ?$

**Question:** What is the uncertainty in the derived quantities?

#### 3.2 Why This Matters

In Week 4, you will:
1. Measure $w(z)$ at multiple positions
2. Fit to extract $w_0$ and $z_w$
3. **Predict** beam width at new positions
4. Compare predictions to measurements

If you don't track uncertainties, you can't tell if theory and experiment agree!

#### 3.3 The Connection to Week 1

You already learned the formula in Week 1:

$$\sigma_z = \sqrt{\left(\frac{\partial z}{\partial a}\right)^2 \sigma_a^2 + \left(\frac{\partial z}{\partial b}\right)^2 \sigma_b^2 + \cdots}$$

Today: How to **apply** this efficiently, especially for complex calculations.

---

### 4. Error Propagation: The Math (10 min)

#### 4.1 The General Formula

For a derived quantity $z = f(a, b, c, \ldots)$:

$$\boxed{\sigma_z^2 = \left(\frac{\partial z}{\partial a}\right)^2 \sigma_a^2 + \left(\frac{\partial z}{\partial b}\right)^2 \sigma_b^2 + \left(\frac{\partial z}{\partial c}\right)^2 \sigma_c^2 + \cdots}$$

**Assumptions:**
1. Uncertainties are small (linear approximation valid)
2. Errors in $a$, $b$, $c$ are **uncorrelated** (independent)

#### 4.2 Example 1: Simple Product

**Given:** $P = IV$ where $I = 2.0 \pm 0.1$ A and $V = 5.0 \pm 0.2$ V

**Calculate $\sigma_P$:**

$$\frac{\partial P}{\partial I} = V = 5.0, \quad \frac{\partial P}{\partial V} = I = 2.0$$

$$\sigma_P = \sqrt{(5.0)^2(0.1)^2 + (2.0)^2(0.2)^2} = \sqrt{0.25 + 0.16} = 0.64 \text{ W}$$

**Result:** $P = 10.0 \pm 0.6$ W

#### 4.3 Example 2: Rayleigh Range

**Given:** $z_R = \frac{\pi w_0^2}{\lambda}$ where $w_0 = 0.10 \pm 0.01$ mm and $\lambda = 633$ nm (exact)

**Calculate $\sigma_{z_R}$:**

$$\frac{\partial z_R}{\partial w_0} = \frac{2\pi w_0}{\lambda}$$

$$\sigma_{z_R} = \left|\frac{2\pi w_0}{\lambda}\right| \sigma_{w_0} = \frac{2\pi (0.10 \times 10^{-3})}{633 \times 10^{-9}} (0.01 \times 10^{-3})$$

$$z_R = \frac{\pi (0.10 \times 10^{-3})^2}{633 \times 10^{-9}} = 0.0496 \text{ m} \approx 50 \text{ mm}$$

$$\sigma_{z_R} = \frac{2 z_R}{w_0} \sigma_{w_0} = \frac{2 \times 50}{0.10} \times 0.01 = 10 \text{ mm}$$

**Result:** $z_R = 50 \pm 10$ mm (20% relative uncertainty, because $z_R \propto w_0^2$)

**Key insight:** The relative uncertainty doubles when you square!

#### 4.4 Useful Shortcut: Relative Uncertainties

For products and quotients, add relative uncertainties in quadrature:

If $z = \frac{a \cdot b}{c}$, then:

$$\frac{\sigma_z}{|z|} = \sqrt{\left(\frac{\sigma_a}{a}\right)^2 + \left(\frac{\sigma_b}{b}\right)^2 + \left(\frac{\sigma_c}{c}\right)^2}$$

For powers: If $z = a^n$, then $\frac{\sigma_z}{|z|} = |n| \frac{\sigma_a}{|a|}$

---

### 5. The `uncertainties` Package (12 min)

#### 5.1 Why Use a Package?

For complex calculations (like Gaussian beam propagation), manual error propagation is:
- Tedious (many partial derivatives)
- Error-prone (easy to make mistakes)
- Hard to verify

The `uncertainties` package **automates** error propagation using calculus behind the scenes.

#### 5.2 Basic Usage

```python
from uncertainties import ufloat

# Create values with uncertainties
x = ufloat(5.0, 0.1)   # 5.0 ± 0.1
y = ufloat(3.0, 0.2)   # 3.0 ± 0.2

# Math operations automatically propagate uncertainty
z = x + y      # Addition
print(z)       # 8.0+/-0.22...

w = x * y      # Multiplication
print(w)       # 15.0+/-1.1...

r = x / y      # Division
print(r)       # 1.67+/-0.12...
```

**The package handles the partial derivatives for you!**

#### 5.3 Using Math Functions

```python
from uncertainties import ufloat
from uncertainties.umath import sqrt, sin, cos, exp, log

x = ufloat(2.0, 0.1)

# These all propagate uncertainty correctly
print(sqrt(x))    # sqrt(2) with propagated uncertainty
print(sin(x))     # sin(2) with propagated uncertainty
print(exp(x))     # e^2 with propagated uncertainty
```

**Important:** Use `uncertainties.umath` instead of `numpy` or `math` for uncertainty-aware functions.

#### 5.4 Example: Beam Width Calculation

```python
from uncertainties import ufloat
from uncertainties.umath import sqrt
import numpy as np

# Measured values
w0 = ufloat(0.10, 0.01)      # Beam waist: 0.10 ± 0.01 mm
z = ufloat(1.5, 0.01)        # Position: 1.5 ± 0.01 m
wavelength = 632.8e-9        # He-Ne wavelength (exact)

# Convert units
w0_m = w0 * 1e-3             # mm to m

# Calculate Rayleigh range
z_R = np.pi * w0_m**2 / wavelength
print(f"Rayleigh range: {z_R*1e3:.2f} mm")

# Calculate beam width at position z
w_z = w0_m * sqrt(1 + (z / z_R)**2)
print(f"Beam width at z={z.nominal_value}m: {w_z*1e3:.3f} mm")
```

**Output shows value ± uncertainty automatically!**

#### 5.5 Accessing Values and Uncertainties

```python
x = ufloat(5.0, 0.1)

# Get the nominal (central) value
print(x.nominal_value)  # 5.0
print(x.n)              # 5.0 (shortcut)

# Get the uncertainty (standard deviation)
print(x.std_dev)        # 0.1
print(x.s)              # 0.1 (shortcut)
```

#### 5.6 Live Demo

*[If time permits, show interactive calculation]*

```python
# Predict beam width at multiple positions
w0 = ufloat(0.10, 0.01)  # mm
wavelength = 632.8e-6    # mm

z_R = np.pi * w0**2 / wavelength

print("Predicted beam widths:")
print("-" * 35)
for z in [0.5, 1.0, 1.5, 2.0]:
    z_val = ufloat(z * 1000, 10)  # Convert m to mm, 1cm uncertainty
    w = w0 * sqrt(1 + (z_val / z_R)**2)
    print(f"z = {z:.1f} m:  w = {w:.3f} mm")
```

---

### 6. Making Predictions for Week 4 (3 min)

#### 6.1 The Predict-Measure-Compare Cycle

**Good experimental practice:**
1. **Predict** — Calculate expected results with uncertainties
2. **Measure** — Collect data
3. **Compare** — Do they agree within uncertainties?

If they disagree: Either measurement error, or the model is incomplete!

#### 6.2 What You'll Do Today

1. **Measure** beam width $w$ at one position $z$
2. **Estimate** beam waist $w_0$ (with uncertainty)
3. **Predict** beam widths at other positions for Week 4
4. **Record** predictions in your notebook

#### 6.3 Agreement and Disagreement

**How to compare prediction and measurement:**

$$\text{Discrepancy} = |x_{\text{pred}} - x_{\text{meas}}|$$

$$\text{Combined uncertainty} = \sqrt{\sigma_{\text{pred}}^2 + \sigma_{\text{meas}}^2}$$

**Rule of thumb:**
- Discrepancy < 2σ: Good agreement
- Discrepancy > 3σ: Significant disagreement (investigate!)

---

### 7. Summary (2 min)

#### Key Takeaways

1. **Motor control** enables automated, reproducible measurements
   - KST101 + pythonnet + Kinesis SDK
   - Systematic troubleshooting saves time

2. **Error propagation formula:**
   $$\sigma_z^2 = \sum_i \left(\frac{\partial z}{\partial x_i}\right)^2 \sigma_{x_i}^2$$

3. **`uncertainties` package** automates error propagation
   - `ufloat(value, uncertainty)` creates uncertain numbers
   - Math operations automatically propagate uncertainty
   - Use `uncertainties.umath` for functions

4. **Predict before you measure** — Then compare!

#### For Lab Today

1. Set up motor controller and verify communication
2. Take your first automated beam profile
3. Fit to extract beam width with uncertainty
4. Use `uncertainties` to predict Week 4 results

---

## Suggested Board Work

1. Software architecture diagram (Python → pythonnet → Kinesis → Motor)
2. Error propagation formula (boxed)
3. Example: Rayleigh range uncertainty calculation
4. `uncertainties` code snippets
5. Predict-measure-compare diagram

---

## Code Snippets to Show

### Motor Connection Test
```python
DeviceManagerCLI.BuildDeviceList()
device_list = DeviceManagerCLI.GetDeviceList()
print(f"Found devices: {list(device_list)}")
```

### Basic uncertainties Usage
```python
from uncertainties import ufloat
x = ufloat(5.0, 0.1)
y = ufloat(3.0, 0.2)
print(f"x + y = {x + y}")
print(f"x * y = {x * y}")
```

### Beam Width Prediction
```python
from uncertainties import ufloat
from uncertainties.umath import sqrt

w0 = ufloat(0.10, 0.01)  # mm
z_R = 50  # mm (simplified)
z = 1500  # mm

w = w0 * sqrt(1 + (z/z_R)**2)
print(f"Predicted width: {w} mm")
```

---

## Common Student Questions

**Q: Why can't I just use numpy with ufloat?**
A: numpy functions don't know how to propagate uncertainties. Use `uncertainties.umath` or `unumpy` for array operations.

**Q: What if my errors are correlated?**
A: The formula assumes uncorrelated errors. For correlated errors, you need the full covariance matrix treatment (beyond this course, but `uncertainties` can handle it).

**Q: How does `uncertainties` know the partial derivatives?**
A: It uses automatic differentiation — tracking how small changes in inputs affect outputs through the chain rule.

**Q: What if my uncertainty is asymmetric?**
A: `uncertainties` assumes symmetric Gaussian uncertainties. For asymmetric cases, use Monte Carlo simulation (not covered here).

**Q: Can I use uncertainties with curve_fit?**
A: Not directly for fitting, but you can convert fit results to ufloats using the covariance matrix from curve_fit.

---

## Connections to Lab Work

| Lecture Topic | Lab Application |
|---------------|-----------------|
| Motor control architecture | Setting up KST101, troubleshooting |
| Basic motor commands | Writing measurement script |
| Error propagation formula | Understanding fit uncertainties |
| `uncertainties` package | Predicting Week 4 beam widths |
| Predict-measure-compare | Evaluating your Week 3 results |
