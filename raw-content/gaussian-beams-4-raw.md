---
title: "Gaussian Beams - Week 4"
---

# Goals

In week one, we measured the profile of the laser and found it to be Gaussian to a good approximation. However, we don't have any model for how the profile changes as the beam propagates and we will work to improve our model. Also, we will apply automation to more rapidly take data. The full set of learning goals includes:

1. Automated data acquisition.
   - Python with Thorlabs Kinesis SDK
   - USB DAQ (NI USB-6009) with nidaqmx

2. Fitting and analysis of data in Python
3. Using a predictive model of Gaussian laser beams
   - Contrast Gaussian beams with geometric optics

4. Measure profiles of a Gaussian beam, and extract the Gaussian beam parameters
5. Effect of a lens on Gaussian beams.
   - Is it still Gaussian?
   - Does the thin lens equation apply to Gaussian beams?
   - What limits the minimum achievable spot size?

# Prelab

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

## Trying out the gaussian beam model

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

# Automation of the Measurement

Before we begin this week's lab, reflect on your experience from week one (and perhaps refer to your lab notebook entry to help guide your memory).

1. In week one, how long did the total process of data taking through analysis take to make a measurement of the beam width $w$?
2. In this lab, you may have to take 20-30 beam profiles in order to measure $w_0$ and $z_w$. How long would this take with your current method?
3. What are the most time consuming portions of the process? Which parts of the process would benefit from automation?

In the next step, you will use Python and your NI USB-6009 data acquisition device to automate the procedure for measuring the width of the laser beam. You can do this with your own laptop or with the laptops in the lab.

In order to set up your measurement automation you will use a Python script that controls the motor and reads the photodetector. Instructions can be found in the Appendix @sec:python-automation.

4. Test and run the automated Python program and evaluate the result using the same Python analysis from week one.
5. Before you go on, make sure the automated acquisition and analysis routine gives the same result as the method you used in week one.
6. How long does your new measurement method take? (2-3 minutes per $w$ measurement is very good.)

# The Experiment

The Gaussian beam model of light is useful because it often describes the beam of light created by lasers. This section will test the validity of the model for our He-Ne laser beam. Also, the effect of a lens on a Gaussian beam will be tested, and the Gaussian beam model will be compared with predictions from the simpler ray theory. Lastly, the Gaussian beam theory can be used to describe the minimum possible focus size for a beam and a lens.

## Measuring the beam profile of your He-Ne laser without any lenses

There is a straight-forward reason that a He-Ne laser should produce a Gaussian beam. The laser light builds up between two mirrors, and the electromagnetic mode that best matches the shape of the mirrors is the Gaussian beam.

1. Considering Equations @eq:8 -@eq:11, which aspects of the Gaussian beam model can you test? Are there any parts of the model you cannot test?
2. Measure the beam width $w$ at various distances from the laser. Consider carefully what distance should be varying. Is it the distance from laser to razor, the distance from razor to photodetector, or the distance from laser to photodetector? How did you decide what positions $z$ to measure the width at (meter sticks and other measurement tools are available in the lab)?
3. Fit the data to $w(z)$, the predicted expression for a Gaussian beam given in Equation @eq:9.
4. What is the value of the beam waist $w_0$ (including uncertainty)? Where does the beam waist $z_w$ occur relative to the laser?

## How does a lens change a Gaussian beam?

Pick a non-compound lens (not the fancy camera lenses) with focal length in the range 100-200 mm and assemble it in a lens mount with a retaining ring (see Figure @fig:mount-assembley). Recall that it's very important that you **do not handle optical components** (lenses, mirrors, polarizers, wave plates, beam splitters, etc.) **with your bare hands**. The oils on your skin can damage the optics and degrade the light in your experiment. Always handle these components while using **latex/nitrile gloves or finger cots**.

Design and carry out an experiment to quantitatively answer the questions below. Consider carefully where to put the lens. Your data for this section can be used in the next section.

1. Insert a lens (after the mirrors) into the beam path to change the divergence/convergence of the beam but keep its propagation direction the same.
2. When this condition (the beam propagation direction is unchanged) is met, where does the beam intersect the lens? *Note: This is the preferred method of adding a lens to an optical set up.*
3. Does the beam retain a Gaussian profile after the lens?
4. What is the new beam waist $w_0$ and where does it occur?
5. What factors affect the beam profile after the lens?
6. Does the measured $w(z)$ match the Gaussian beam prediction given in Equation @eq:9?

![Mounting assemblies for a mirror (left) and a lens (right).](../resources/lab-guides/gaussian-laser-beams/mount-assembly.png){#fig:mount-assembley width="15cm"}

## Quantitatively modeling the effect of a lens

One of the simplest ways to model the effect of a lens is the thin lens equation, which is based on a ray model of light (see Figure @fig:ray-diagram).

$$ \frac{1}{S_1}+\frac{1}{S_2}=\frac{1}{f}$$

1. Redraw Figure @fig:ray-diagram to show how it would change when the light is modeled as a Gaussian beam, rather than rays. In particular, where should the beam waists occur? What determines the relative width of the beam waist?
2. Experimentally test the accuracy of the thin lens equation for the imaging of Gaussian beams. Your data from the previous question can probably be used. Is the agreement within the estimated uncertainties?
3. Systematic errors: Under what conditions should the thin lens equation be most valid? How do these conditions compare to conditions of your actual measurements? Can you get better agreement?

![Diagram showing the focusing of light by a thin lens in the ray approximation. The diagram identifies the quantities in the thin lens equation: image distance, object distance, and focal length.](../resources/lab-guides/gaussian-laser-beams/ray-diagram.png){#fig:ray-diagram width="15cm"}

# Appendix: Python Automation Guide {#sec:python-automation}

This appendix guides you through setting up and running the automated beam profile measurement using Python. The script controls the Thorlabs KST101 motor controller to move the knife-edge while simultaneously reading voltage from the photodetector via the NI-DAQmx.

## Hardware Setup

The physical connections are:

1. **Motor Controller (KST101)**:
   - Connect the USB cable from the KST101 cube to your computer
   - Connect the power supply to the KST101
   - The motor should already be mechanically connected to the translation stage with the razor

2. **Data Acquisition (NI USB-6009)**:
   - Connect the USB cable from the DAQ to your computer
   - Connect the photodetector BNC output to the analog input terminals:
     - Positive signal to AI0+ (pin 2)
     - Ground to AI0- (pin 1 or GND)

3. **Optical Setup**:
   - Position the photodetector after the knife-edge in the beam path
   - Ensure the beam passes cleanly through when the razor is fully retracted

## Software Prerequisites

Before running the automation script, you need to install:

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
pip install pythonnet nidaqmx numpy matplotlib
```

### 3. NI-DAQmx Drivers

If not already installed, download from:
[https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html)

## Verifying the Setup

### Test the Motor Connection

First, verify that Windows recognizes the motor controller:

1. Connect the USB to the KST101, then turn on power
2. Open **Device Manager** and look for the device under "USB devices" or "Thorlabs APT Device"
3. Note the serial number (displayed on the KST101 screen)

If you get a driver error, you may need to disable Memory Integrity in Windows Security (ask technical staff for help if this occurs on a lab computer).

### Test the DAQ Connection

Run this quick test to verify DAQ communication:

```python
import nidaqmx

# List available devices
system = nidaqmx.system.System.local()
for device in system.devices:
    print(f"Found: {device.name}")

# Test reading a voltage
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    voltage = task.read()
    print(f"Voltage: {voltage:.4f} V")
```

If no device is found, check the USB connection and ensure NI-DAQmx drivers are installed.

## Running the Beam Profiler

The automation script is available at:
`resources/lab-guides/gaussian-laser-beams/python/04_beam_profiler.py`

### Basic Usage

Navigate to the script directory and run:

```bash
python 04_beam_profiler.py
```

The script will prompt you for:

1. **Motor serial number**: Found on the KST101 display (e.g., "26004813")
2. **Step size (mm)**: How far to move between measurements (recommend 0.05 mm)
3. **Wait time (ms)**: Delay after each step (recommend 500 ms)
4. **Direction**: "forward" or "backward"

### Choosing Parameters

**Step Size**: Smaller step sizes give higher resolution but take longer:
- 0.05 mm is a good starting point for most beams
- Use smaller steps (0.02-0.03 mm) for tightly focused beams
- You can use larger steps (0.1 mm) for initial alignment

**Wait Time**: This ensures measurements are taken after vibrations settle:
- Use kinematic equation to estimate: $x = \frac{1}{2}at^2$
- For 0.05 mm step and 1 mm/s² acceleration: $t = \sqrt{2 \times 0.05/1} \approx 316$ ms
- Add safety margin: 500 ms is usually sufficient
- Increase if you see noisy data

### Output Files

The script automatically generates two files with timestamps:

1. **CSV data file**: `beam_profile_YYYYMMDD_HHMMSS.csv`
   - Two columns: Position (mm), Voltage (V)
   - Ready for analysis with your fitting code from Week 1

2. **Plot image**: `beam_profile_YYYYMMDD_HHMMSS.png`
   - Quick visualization of the measured profile

## Understanding the Code Structure

The beam profiler script uses a class-based structure. Here are the key components:

### The `BeamProfiler` Class

```python
class BeamProfiler:
    def __init__(self, serial_number, daq_device="Dev1", daq_channel="ai0"):
        """Initialize with motor serial number and DAQ settings."""

    def connect(self):
        """Connect to motor controller, configure velocity."""

    def get_position(self):
        """Read current position in mm."""

    def move_to(self, position_mm):
        """Move to absolute position."""

    def read_voltage(self):
        """Read single voltage from DAQ."""

    def run_scan(self, step_size_mm, wait_time_ms, direction, max_steps):
        """Execute the automated scan with real-time plotting."""
```

### The Main Measurement Loop

The core logic in `run_scan()` follows this pattern:

```python
for step_num in range(max_steps):
    # 1. Read current position
    position = self.get_position()

    # 2. Read photodetector voltage
    voltage = self.read_voltage()

    # 3. Save data point immediately
    writer.writerow([position, voltage])

    # 4. Update real-time plot
    # (matplotlib code)

    # 5. Move to next position
    self.move_to(position + step)

    # 6. Wait for vibrations to settle
    time.sleep(wait_time_ms / 1000)
```

This is essentially the same logic you would use when taking data manually, just automated.

## Customizing the Script

### Changing the DAQ Channel

If your photodetector is connected to a different channel (e.g., AI1):

```python
profiler = BeamProfiler(serial_number, daq_channel="ai1")
```

### Modifying Velocity Settings

The default velocity is 1 mm/s with 1 mm/s² acceleration. To change this, modify the `connect()` method:

```python
vel_params.MaxVelocity = Decimal(2.0)  # 2 mm/s
vel_params.Acceleration = Decimal(2.0)  # 2 mm/s²
```

### Adding Averaging

For noisy signals, you can modify `read_voltage()` to average multiple samples:

```python
def read_voltage(self, num_samples=10):
    """Read averaged voltage from DAQ."""
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(
            f"{self.daq_device}/{self.daq_channel}"
        )
        voltages = task.read(number_of_samples_per_channel=num_samples)
        return np.mean(voltages)
```

## Troubleshooting

### "Device not found" Error

- Check USB connection
- Verify serial number matches the display on the KST101
- Make sure no other software (APT User, Kinesis) is using the motor

### Motor Doesn't Move

- Ensure power is connected to the KST101
- Check that the stage isn't at a travel limit
- Verify the stage type is configured correctly in Kinesis (ZST225B)

### Voltage Reads Zero

- Check photodetector power
- Verify BNC cable connections to DAQ
- Make sure the beam actually hits the photodetector

### Python Import Errors

- **pythonnet error**: Ensure Kinesis SDK is installed and matches Python architecture (32/64-bit)
- **nidaqmx error**: Install NI-DAQmx drivers from NI website

### Noisy Data

- Increase wait time between steps
- Check for mechanical vibrations in your setup
- Shield the photodetector from ambient light
- Average multiple DAQ readings per point

## Tips for Good Measurements

1. **Starting Position**: Position the razor so the beam is fully unblocked. Use the manual jog controls on the KST101 to find a good starting point.

2. **Scan Range**: Make sure your scan covers the full transition from unblocked to fully blocked. Include some data before and after the transition.

3. **Real-Time Monitoring**: Watch the live plot as data comes in. You can press Ctrl+C to stop early if something looks wrong.

4. **Data Validation**: Before collecting many profiles, take one measurement manually and one with automation. Compare results to ensure consistency.

5. **File Organization**: The script includes timestamps in filenames, but consider adding descriptive prefixes (e.g., by modifying the `filename` variable) to help organize your data.
