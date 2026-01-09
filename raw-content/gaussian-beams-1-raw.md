---
title: "Gaussian Beams - Week 1"
---

# Where We Are in the Sequence

**Week 1 of 4: Foundations**

This week you build the foundational skills for the entire Gaussian Beams sequence: optical alignment, photodetector operation, and beam width measurement. The calibration data and measurement techniques you develop this week will be used directly in Weeks 2-4.

**This week:** Align optics → Calibrate photodetector → Measure beam width
**Next week:** Learn data acquisition → Characterize noise → Choose optimal gain setting

# Learning Goals

After completing this week's lab, you will be able to:

1. Mount and align optical components (mirrors, lenses) using standard optomechanical hardware.
2. Walk a laser beam to achieve parallel propagation using two mirrors.
3. Explain how a photodiode converts photons to current via the photoelectric effect.
4. Calculate expected photodetector output voltage given incident power, responsivity, and gain setting.
5. Calibrate a photodetector's offset and gain and compare to manufacturer specifications.
6. Estimate measurement uncertainty using statistical sampling and explain why repeated measurements improve precision.
7. Set up a knife-edge measurement and derive the theoretical model (error function).
8. Perform a nonlinear curve fit to extract beam width from experimental data.

# Python Preparation

This lab sequence uses Python for data acquisition, analysis, and visualization. The following skills will be introduced as you progress through the weeks:

| Week | Python Skills | Resources |
|------|---------------|-----------|
| Week 1 | NumPy basics, Matplotlib plotting, file I/O | [Data Analysis](/PHYS-4430/python-analysis) |
| Week 2 | Curve fitting with SciPy, NI-DAQmx | [Data Analysis](/PHYS-4430/python-analysis), [NI-DAQmx](/PHYS-4430/python-nidaqmx) |
| Week 3 | FFT analysis, motor control | [Data Analysis](/PHYS-4430/python-analysis), [Thorlabs Motors](/PHYS-4430/python-thorlabs) |
| Week 4 | Integrated automation | All above |

**Before Week 2**, ensure you are comfortable with:
- NumPy array operations
- Basic plotting with Matplotlib
- Loading data with `np.loadtxt()`

If you need to review these skills, see the [Python Resources](/PHYS-4430/python-resources) page.

# Lab Notebook

Your lab notebook will play an important role in this course. You will use your notebook for keeping records of many things including:

- Answering prelab questions from the lab guides
- Answering in-lab question from the lab guides
- Recording data
- Including plots of data
- Analysis and results
- Diagrams and pictures
- Procedures of experiments that you design

The lab notebook will be an important part of your grade because learning to keep a good lab notebook is an important part of your professional development. 

# Definitions

**Optic** – Any optical component that manipulates the light in some way. Examples include lenses, mirrors, polarizing filters, beam splitters, etc.

**Optomechanics** – This category includes optics mounts and the components to align them. Examples in the lab include post, post holders, bases, lens mounts, adjustable mirror mounts, rotation mounts, and translation stages.

# Setting up the Laser and Mounting Optics

Your group should find an empty optical breadboard workstation in one of the five color coded optics bays in G-214. Spend some time to explore the space and familiarize yourself with the components. The shelf above the breadboard should have:

- An oscilloscope
- A waveform generator
- Triple output DC Power Supply
- Set of ball drivers
- Optics caddy to hold optics already mounted on 0.5" posts
- Set of 1/4-20 and 8-32 screws, setscrews, washers, and nuts

## Cleaning and handling of optical components

It's very important that you **do not handle optical components** (lenses, mirrors, polarizers, wave plates, beam splitters, etc.) **with your bare hands**. The oils on your skin can damage the optics and degrade the light in your experiment. Always handle these components while using **latex/nitrile gloves or finger cots**, which can be found on the top of the tool cabinets in your optics bay, or on top of the black drawer cabinets in the main lab. This [technical note](https://www.newport.com/n/how-to-clean-optics) from Newport discusses how to go about cleaning dirty optics, and is also demonstrated in [this video](https://www.youtube.com/watch?v=9Pq4SeNmFYw). For a more in-depth treatment on cleaning optics, we have a copy of ["The Proper Care of Optics: Cleaning, Handling, Storage, and Shipping" by Robert Schalck](https://spie.org/Publications/Book/2518746?SSO=1) for reference in the lab (it should be located on top of the black tool cabinets in the main lab).

## Mounting your optomech: bases, post holders, and posts

The two videos linked below provide information and tips on how to use and mount components on the optical breadboards that we have in the lab. Please watch these before proceeding.

[Mounting Your Optomech: Bases, Post Holders, and Posts | Thorlabs Insights](https://www.youtube.com/watch?v=4xZmGyMsQNo)

[Tips for Bolting Post Holders to Optical Tables, Bases, and Breadboards | Thorlabs Insights](https://www.youtube.com/watch?v=HyUXsH1zuIk)

Now, we will begin assembling the components.

1.  Get a laser and power supply from the "He-Ne Laser" drawer in the colored drawer cabinet found in your chosen or assigned optics bay. You'll also need two sets of 3D-printed laser tube mounts which you can find in the same drawer (see Figure @fig:tube-mount). The bottom mount first gets mounted to an optical post and then the top of the mount can be assembled with ¼-20 socket head cap screw and nut. After both sets of tube mounts are attached to the laser, insert the optical posts into post holders and attach the assembly to the optical table. We recommend placing the laser towards the rear of the optical table (under the shelf), oriented so the beam travels along the length of the table (parallel to the shelf). This layout leaves the front of the table clear for mounting the photodetector and translation stage you'll add later.
2. Each person in your group is responsible for assembling a mirror as shown in Figure @fig:mount-assembley. In the end, you will need at least 2 mirrors to complete the next task. **Remember to wear latex/nitrile gloves or finger cots while handling optical components.** Mount one mirror at the far end of the table (opposite the laser) and the second closer to you, so that the laser beam propagates across the table and gives you plenty of space to mount additional components.

*As you are mounting the optics, choose the heights so that the laser hits the center of each optic and the beam is parallel to the table.*

![CAD assembly showing a He-Ne laser mounted to an optical table with the 3D-printed tube mounts that can be found in the tool cabinets in the optical bays of G214.](../resources/lab-guides/gaussian-laser-beams/tube-mount.png){#fig:tube-mount width="15cm"}

## Walking a beam {#sec:walkingbeam}

Next, you will align your laser such that beam is aligned parallel to the table. You will do this by using two mirrors and a technique that is called "walking a beam". [This video](https://www.youtube.com/watch?v=qzxILY6nOmA&t=249s) provides an overview on how to do so. The most relevant information for our lab starts at 4:09 (which the above link should take you to). Also, we have 3D printed beam alignment tools that are used in place of the iris in the video (these can be found in the colored drawer cabinet in your optics bay).

1. Mount two 3D printed beam alignment discs onto the optical table at the same height above the table. 
2. Use only two mirrors to get the beam to pass through the center of each disc. Having two mirrors allows you to independently adjust the angle and position of your beam.
3. Draw a diagram in your lab notebook of the configuration of your laser, mirrors, and alignment discs.

![Mounting assemblies for a mirror (left) and a lens (right).](../resources/lab-guides/gaussian-laser-beams/mount-assembly.png){#fig:mount-assembley width="15cm"}

# Modeling Characteristics of the Photodetector

The goal of this part of the lab is to understand a lot about the specifications given on the datasheet for the Thorlabs [PDA36A](../resources/lab-guides/gaussian-laser-beams/PDA36A-Manual.pdf) (or [PDA36A2](../resources/lab-guides/gaussian-laser-beams/PDA36A2-Manual.pdf)) Switchable Gain Amplified Photodetectors (we have both in the lab, so check the model number to know which one you are using). It is important to realize that data sheets (also called spec sheets or specification sheets) provide a model for the realistic behavior of the device. This model can be tested and improved, a process more commonly called "calibration." Note that there are **two** power switches, one on the power supply and one on the photodetector. The photodetector will respond to light with the power off but it won't work well and changing the gain will have little effect.

## Basic function of the amplified photodetector

1. Spend a few minutes (no more than 10) to write an explanation using words and diagrams to explain the physical mechanism for how the photodetector converts light into voltage. You may use the manufacturer’s specifications sheet (linked to in the section above), trustworthy online resources, a book, etc.
2. Use the data sheet to estimate the conversion of watts of light into amps of current for Helium-Neon red wavelength (632.8 nm) and for the frequency doubled Nd:YAG laser (Green laser pointer wavelength, 532 nm).
   1. How would you convert “amps per watt” into “electrons per photon”? 
   2. What is the electron/photon conversion efficiency for the red HeNe laser and green doubled Nd:YAG lasers?
   3. Is this number less than, equal to, or greater than one? What does this number tell you about how the photodiode works?


## Calibrating the photodetector offset and gain
Calibrating the photodetector is especially important when you take a data set that uses multiple gain settings. Having an accurate calibration of the gain and offset will let you stitch the data together accurately.

1. The photodetector gain is specified in **decibels (dB)**, a logarithmic scale commonly used in electronics. Here's how it works:

   **The definition:** For voltage gain,
   $$dB = 20 \times \log_{10}\left(\frac{V_{out}}{V_{in}}\right)$$

   **What does log₁₀ mean?** The function $\log_{10}(x)$ asks: "10 raised to what power equals $x$?" For example:
   - $\log_{10}(10) = 1$ because $10^1 = 10$
   - $\log_{10}(100) = 2$ because $10^2 = 100$
   - $\log_{10}(1000) = 3$ because $10^3 = 1000$

   <br>

   **Converting dB to linear gain:** To find the actual gain from a dB value, invert the formula:
   $$\text{voltage gain} = 10^{dB/20}$$

   For example, 20 dB corresponds to $10^{20/20} = 10^1 = 10\times$ gain.

   **Use this tool to check your understanding:**

<div id="db-gain-interactive" style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin: 20px auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 400px;">
<div style="margin-bottom: 15px;">
<label for="db-slider" style="font-weight: bold; display: block; margin-bottom: 8px;">Gain Setting: <span id="db-value">20</span> dB</label>
<input type="range" id="db-slider" min="0" max="70" value="20" step="10" style="width: 100%; cursor: pointer;">
<div style="display: flex; justify-content: space-between; font-size: 12px; color: #666; margin-top: 4px;">
<span>0 dB</span>
<span>70 dB</span>
</div>
</div>
<div style="background: #e7f3ff; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 12px;">
<div style="font-size: 14px; color: #666; margin-bottom: 5px;">Voltage Gain</div>
<div id="voltage-gain" style="font-size: 28px; font-weight: bold; color: #0066cc;">10×</div>
</div>
<div style="background: #fff; padding: 10px; border-radius: 6px; border: 1px solid #ddd; font-size: 13px;">
<div id="calculation" style="color: #666; font-family: monospace;">20 dB → 10^(20/20) = 10×</div>
</div>
</div>

<script>
(function() {
    var slider = document.getElementById('db-slider');
    var dbValue = document.getElementById('db-value');
    var voltageGain = document.getElementById('voltage-gain');
    var calculation = document.getElementById('calculation');
    function formatGain(value) {
        if (value >= 1000) return Math.round(value).toLocaleString() + '×';
        if (value >= 100) return Math.round(value) + '×';
        if (value >= 10) return value.toFixed(1) + '×';
        return value.toFixed(2) + '×';
    }
    function updateDisplay() {
        var db = parseFloat(slider.value);
        var vGain = Math.pow(10, db / 20);
        dbValue.textContent = db;
        voltageGain.textContent = formatGain(vGain);
        var vStr = vGain >= 100 ? Math.round(vGain) : vGain.toFixed(1);
        calculation.textContent = db + ' dB → 10^(' + db + '/20) = ' + vStr + '×';
    }
    slider.addEventListener('input', updateDisplay);
    updateDisplay();
})();
</script>

   **Think about it:** The dB scale can also be defined for power: $dB = 10 \times \log_{10}(P_{out}/P_{in})$. Notice the factor is 10 instead of 20. Why does this make sense? *(Hint: How is power related to voltage in a resistive circuit?)*

   *You might not get this immediately—that's fine. Discuss with your partner or revisit after completing the calibration.*

2. Calibrating the offset voltage (the output of the photodetector when no light is incident upon the device).
   1. Calibrate the offset of the photodetector as a function of gain setting. 
   2. Quantitatively compare it to the specifications given in the table. Is your measured value within the specified range given on the PDA36A or PDA36A2 photodetector data sheet?
   3. What measures did you take to eliminate stray light? Were your measures sufficient for an accurate calibration?
3. Calibrating the gain.
   1. Is it possible to measure the $V/A$ gain for each setting, or can you only measure the change in gain as you switch the settings? Why? Note that this lab only requires relative gain.
   2. Make a measurement of the gain or relative gain for most of the gain settings. If you need to adjust the laser power, try blocking part of the beam. Note, you will need to make two measurements at one gain setting when you block the beam. What systematic error sources are of most concern?
   3. Quantitatively compare your results with the range of values given on the data sheet. Do you believe your results provide a more accurate estimate of the photodetector gain than the data sheet? Why or why not?
   4. Using the appropriate spec sheet and your measurements, what is the power of your laser? Does this agree with the laser power shown on the laser?
   5. Hypothetically, how would you measure the absolute gain?

## Follow up

1. Write mathematical expressions that converts the incident power (the light) $P_{in}$ to the photodetector voltage $V$ and the photodetector voltage $V$ to input power $P_{in}$. Take into account all relevant parameters such as the photodetector gain setting (in $dB$) and offsets.

## Reflection: Using Your Calibration

In Week 4, you will use this photodetector to measure beam profiles. Before moving on, consider how you will use your calibration results:

1. Based on your calibration, would you trust the datasheet gain values, or would you use your measured values? Under what conditions might the datasheet values be inadequate?

2. If your measured offset voltage differed significantly from the datasheet (say, by more than 50%), what would you do before proceeding?
   - (a) Repeat the measurement
   - (b) Accept the datasheet value
   - (c) Investigate the cause of the discrepancy
   - (d) Use your measured value and note the discrepancy

   There is no single correct answer—justify your choice in 2-3 sentences.

3. You will use this photodetector at a single gain setting for most of Week 4's measurements. Which gain setting would you tentatively choose based on your calibration? (You will refine this choice in Week 2 after characterizing noise.) 

# Understanding Measurement Uncertainty

You've just calibrated your photodetector and recorded voltage values. But how confident should you be in those numbers? This section introduces measurement uncertainty—a core skill you'll use throughout this course and your scientific career.

**Make sure that your laser has been turned on for at least 5 minutes so it has had the opportunity to warm up.**

## Your First Uncertainty Measurement

Connect your photodetector to the oscilloscope and observe the voltage signal from the laser.

**Step 1: Make a single measurement**

Record the voltage you see on the oscilloscope: ______ V

Now ask yourself: *How confident are you in that number? If you looked away and looked back, would you get exactly the same value?*

**Step 2: Watch the fluctuations**

Observe the signal for 10-15 seconds. You'll notice the voltage isn't perfectly constant—it fluctuates.

1. Estimate by eye: How large are the fluctuations? ±______ V
2. What might cause these fluctuations? (List 2-3 possibilities in your notebook)

**Step 3: Quantify with repeated measurements**

Take 10 voltage readings, recording each value:

| Reading | Voltage (V) |
|---------|-------------|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
| 5 | |
| 6 | |
| 7 | |
| 8 | |
| 9 | |
| 10 | |

**Step 4: Calculate statistics**

Using your 10 measurements, calculate:

1. **Mean:** $\overline{V} = \frac{1}{N}\sum V_i$ = ______ V

2. **Standard deviation:** $\sigma_V = \sqrt{\frac{1}{N-1}\sum(V_i - \overline{V})^2}$ = ______ V

   This tells you the typical size of fluctuations in a *single* measurement.

3. **Standard deviation of the mean:** $\sigma_{\overline{V}} = \frac{\sigma_V}{\sqrt{N}}$ = ______ V

   This tells you the uncertainty in your *average* value.

**Step 5: Compare methods**

Now use the oscilloscope's built-in RMS measurement function to measure the fluctuations automatically.

- Oscilloscope RMS reading: ______ V
- Your calculated standard deviation: ______ V

Do they agree? The oscilloscope's RMS function is essentially doing the same calculation you just did, but with many more samples.

## Why This Matters

**Reflection questions** (answer in your notebook):

1. Your standard deviation of the mean ($\sigma_{\overline{V}}$) is smaller than the standard deviation ($\sigma_V$). Why does averaging multiple measurements reduce uncertainty?

2. If you took 100 measurements instead of 10, how would $\sigma_{\overline{V}}$ change? (Hint: look at the formula)

3. In your beam width measurements later today, you'll record voltage at each razor position. Based on what you just learned, how could you reduce uncertainty in those measurements?

## The Key Insight

Measurement uncertainty isn't a sign of failure—it's essential information about how much you can trust your data. In Week 2, you'll learn to characterize noise more systematically and use uncertainty to make quantitative decisions about your experimental setup.

# Measuring the Beam Width

The goal of this section is to develop a measurement technique and analysis scheme to measure the width of a laser beam. The scheme will let you measure the width in one dimension. The technique is most useful for beams that have an approximately Gaussian intensity profile. You will improve and refine this technique in the upcoming weeks of this lab.

**Time management note:** This section has multiple parts with different priorities:

1. **Essential (must complete):** Derive the error function model (Section 7.1) and complete the curve fitting practice (Section 7.2). This analysis is critical preparation for Week 2.

2. **Important (complete if time allows):** Build the setup and take data (Sections 7.3-7.5). If you don't finish in Week 1, you will revisit this in Week 3.

3. **Good practice:** If you take data, complete the analysis (Section 7.6). This validates your fitting code on real data.

The basic scheme involves measuring the power in the laser beam as the beam is gradually blocked by a knife edge (razor blade) using a setup similar to Figure @fig:knife-assembley.

![Razor blade mounted on a translation stage.](../resources/lab-guides/gaussian-laser-beams/knife-assembley.png){#fig:knife-assembley width="15cm"}

1. Suppose a laser beam has a Gaussian intensity profile $I(x,y) = I_{max}e^{-2(x^2+y^2)/w^2}$, and is incident upon a photodiode. What is the expression for the power hitting the photodiode when a portion of the beam is blocked by a razor blade?
   1. Draw a diagram showing the beam and the razor.
   2. Using the above expression for $I(x,y)$, write the mathematical expression for the power incident on the photodiode as a function of razor position. Note, to address this question, you will need to become familiar with the Error Function, $erf(x)$. What assumptions, if any, did you need to make in evaluating the integral? Hint: if you are moving in the $x$ direction, what is going on in the $y$ direction?

## Before you take data: create an analysis function to fit a test set of data {#sec:analysis}

*Note: Nonlinear least squares fitting is covered in next week's prelab. See the [Python Resources](/PHYS-4430/python-resources) page for a guide to curve fitting with `scipy.optimize.curve_fit`.*

1. What is the functional form for your fit function?
2. Is it a linear or nonlinear fit function? Why?
3. What are the fit parameters? Why do you need this many?
4. How do the fit parameters relate to the beam width?
5. Download [this data set](../resources/lab-guides/gaussian-laser-beams/Test_Profile_Data.csv).
   1. Make a plot of the data.
   2. Make a fit and plot it with the data.
   3. Check that the fit looks good and you get a beam width of $w=4.52 \times 10^{-4}\ m$. If you get a different value, check with your instructor to understand the problem. What is the uncertainty on your measurement?

## Build your setup for measuring the beam width of your laser

1. Draw a detailed schematic of the setup (from the laser all the way to the photodetector).
2. After assembling your experiment, but prior to taking a lot of data, how can you quickly determine if the measurement is working?
3. Is it preferable to use a digital multimeter or oscilloscope? Why?
4. Use the measurement scheme to take data of incident power on the photodiode vs. position of the razor. Pay attention to the units of the translation stage. Pick a position where your beam has a measurable width and measure it. Justify your choice. 

## Analysis of the random uncertainty sources

1. What are possible sources of random uncertainty in the photodetector voltage?
2. How would you estimate the uncertainty in the photodetector voltage measurement?
3. What is the largest source of uncertainty? Why?

## Analysis of the real data

1. Use the analysis procedures verified in section @sec:analysis to find the beam width for your data. Be sure to include the uncertainty.
2. Plot your fit together with your data to make sure it is good.

# Postlab

## Python Preparation for Week 2

This lab sequence requires Python proficiency with NumPy, Matplotlib, and SciPy. Before Week 2, ensure you are comfortable with:

- **NumPy array operations** - See [Python Resources: Data Analysis](/PHYS-4430/python-analysis), "NumPy Essentials" section
- **Plotting with Matplotlib** - See [Python Resources: Data Analysis](/PHYS-4430/python-analysis), "Plotting with Matplotlib" section
- **Loading CSV files** with `np.loadtxt()`

If you need practice, work through the exercises on the [Python Resources](/PHYS-4430/python-resources) page. The curve fitting skills needed for beam width analysis will be covered in Week 2's prelab.

## Apply to Your Data (if you completed Section 6 in lab)

If you collected knife-edge measurement data during lab, you can optionally begin analysis now. However, the full fitting procedure will be covered in Week 2's prelab, so you may prefer to wait.

If you want to start early:

1. Plot your data (position vs. voltage) to verify it looks like an error function
2. Identify approximate values for the beam center and transition width
3. Note any unusual features (noise, asymmetry, incomplete transition)

# Deliverables and Assessment

Your lab notebook should include the following for this week:

## In-Lab Documentation (recorded during lab)

1. **Optical setup diagram** showing laser, mirrors, alignment discs, and photodetector positions
2. **Photodetector calibration data**: offset voltage vs. gain setting, relative gain measurements
3. **Uncertainty mini-lesson**: 10 voltage measurements, calculated statistics (mean, σ, σ_mean), and answers to the reflection questions
4. **Knife-edge measurement data**: position vs. voltage (if completed)

## Analysis and Questions (can be completed after lab)

1. **Photodetector physics explanation** (Section 3.1): diagram and written explanation of how the photodetector converts light to voltage
2. **Calibration comparison** (Section 3.2-3.3): quantitative comparison of your measurements to datasheet values
3. **Beam width measurement** (Section 6, if completed): fit plot, extracted beam width with uncertainty

## Postlab

1. **Python preparation**: Review [Python Resources](/PHYS-4430/python-resources) if needed for NumPy, Matplotlib, and file I/O
2. **Optional early analysis**: If you collected knife-edge data, you may begin exploring it (full fitting covered in Week 2)

## Reflection Questions

Before moving to Week 2, answer these questions:

1. Your photodetector offset voltage differs from the datasheet by 15%. What would you do before using this detector for precision measurements?
   - Options: (a) Repeat the measurement, (b) Accept the datasheet value, (c) Investigate the cause, (d) Use your measured value
   - Justify your choice in 2-3 sentences.

2. You took 10 measurements and calculated both σ (standard deviation) and σ_mean (standard deviation of the mean). Which would you report as the uncertainty in your voltage measurement? Why? 
