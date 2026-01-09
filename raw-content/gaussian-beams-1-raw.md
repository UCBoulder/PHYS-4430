---
title: "Gaussian Beams - Week 1"
---

# Where We Are in the Sequence

**Week 1 of 4: Foundations**

This week you build the foundational skills for the entire Gaussian Beams sequence: optical alignment, photodetector operation, uncertainty estimation, and beam width measurement. The calibration data and measurement techniques you develop this week will be used directly in Weeks 2-4.

**This week:** Align optics → Calibrate photodetector → Learn uncertainty methods → Measure beam width
**Next week:** Learn data acquisition → Characterize noise → Choose optimal gain setting

# Learning Goals

After completing this week's lab, you will be able to:

1. Mount and align optical components (mirrors, lenses) using standard optomechanical hardware.
2. Walk a laser beam to achieve parallel propagation using two mirrors.
3. Explain how a photodiode converts photons to current via the photoelectric effect.
4. Calculate expected photodetector output voltage given incident power, responsivity, and gain setting.
5. Calibrate a photodetector's offset and gain and compare to manufacturer specifications.
6. Compare eyeball, statistical sampling, and instrument specification methods for estimating measurement uncertainty.
7. Report measurements with appropriate significant figures and uncertainty.
8. Set up a knife-edge measurement and derive the theoretical model (error function).
9. Perform a nonlinear curve fit to extract beam width from experimental data.

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

# Prelab: Review of Measurement Uncertainty

**Complete before arriving at lab. Time estimate: 30-45 minutes.**

In this course, you will repeatedly need to estimate measurement uncertainty. Different methods give different answers, and understanding why is critical for interpreting your results. This prelab introduces the mathematical foundations and helps you develop judgment about which methods are appropriate in different situations.

## Mathematical Foundations

When attempting to establish the validity of our experimental results, we must quantify the uncertainty. Measurement uncertainty is not invented to make lab classes tedious—it is a core part of any experimental work that gives us a way to quantify how much we trust our results.

A simple and rigorous way to make a measurement and estimate its uncertainty is to take $N$ measurements $\{y_1,y_2,\ ...\ ,y_N\}$ and estimate the value by the mean:

$$\overline{y} = \frac{1}{N}{\displaystyle \sum_{i=1}^{N}}y_i\text{.}$$

The estimated uncertainty (standard deviation, $\sigma_y$) of any single measurement is given by:

$$\sigma_y = \sqrt{\frac{1}{N-1}{\displaystyle \sum_{i=1}^{N}}(y_i-\overline{y})^2}\text{,}$$

while the uncertainty in the mean value $\sigma_{\overline{y}}$ is smaller:

$$\sigma_{\overline{y}} = \frac{\sigma_y}{\sqrt{N}}\text{.}$$

**Question 1:** In your own words, explain why the uncertainty in the mean decreases as $N$ increases, even though the standard deviation $\sigma_y$ does not. (2-3 sentences)

## Comparing Estimation Methods: A Data-Based Exercise

Download the data file [photodetector_samples.csv](../resources/lab-guides/gaussian-laser-beams/photodetector_samples.csv) containing 200 voltage measurements from a photodetector measuring a nominally constant laser signal. Each measurement was taken at 0.1-second intervals.

**Complete the following analysis using Python, a spreadsheet, or a calculator.**

### Method A: Statistical Sampling (Ground Truth)

Use all 200 data points to calculate:

1. The mean voltage $\overline{V}$
2. The standard deviation $\sigma_V$ of a single measurement
3. The standard error of the mean $\sigma_{\overline{V}}$

Record these values—they will serve as your "ground truth" for comparison.

### Method B: "Eyeballing" from a Subset

Imagine you can only see the first 10 data points: 2.352, 2.343, 2.355, 2.368, 2.341, 2.341, 2.369, 2.357, 2.338, 2.353 (all in volts).

Without performing calculations:

1. Estimate the mean by eye
2. Estimate the typical size of fluctuations (how much do values vary from your estimated mean?)

**Question 2:** Compare your eyeball estimates to the ground truth values from Method A. Were you close? Did you over- or underestimate the uncertainty?

### Method C: Max/Min Method

Using the same 10 data points:

1. Find $V_{max}$ and $V_{min}$
2. Estimate the mean as $(V_{max} + V_{min})/2$
3. Estimate the uncertainty as $(V_{max} - V_{min})/2$

**Question 3:** The max/min method gives an uncertainty estimate of approximately ______ V. Compare this to $\sigma_V$ from Method A. Does the max/min method overestimate or underestimate the true standard deviation? Why might this be? (Hint: think about what the max and min values represent statistically.)

### Method D: Instrument Specification

The Fluke 115 multimeter used in this course has a DC voltage accuracy specification of $\pm(0.5\% + 2 \text{ counts})$ at the 6V range. For a reading of 2.35 V:

1. Calculate the specification-based uncertainty
2. The "counts" refer to the least significant digit. At the 6V range, 1 count = 0.001 V.

**Question 4:** The instrument specification gives an uncertainty of approximately ______ V. How does this compare to the statistical uncertainty from Method A? Under what conditions would you use the instrument specification instead of statistical sampling?

## Understanding What Each Method Measures

Each estimation method captures different sources of uncertainty:

| Method | What it captures | What it misses |
|--------|-----------------|----------------|
| Statistical sampling | Random fluctuations in the signal | Systematic offsets, calibration errors |
| Eyeballing | Quick estimate of variability | Precise quantification, rare large deviations |
| Max/min | Extreme fluctuations | Typical behavior (biased toward outliers) |
| Instrument spec | Manufacturer's guaranteed accuracy | Actual noise in your specific measurement |

**Question 5:** In Week 1, you will measure photodetector voltage while keeping the laser power nominally constant. Suppose the room lights flicker occasionally, causing the photodetector signal to jump by 0.5 V for a few seconds out of every minute.

(a) Which estimation method(s) would capture this effect in the uncertainty?

(b) Which method(s) would miss it entirely?

(c) If you need to know whether your laser power is stable enough for precision measurements, which method would you choose? Why?

## Uncertainty and Curve Fitting (Looking Ahead)

In Week 2, you will fit experimental data to a theoretical model. The curve fitting algorithm needs to know the uncertainty in each data point to:

1. Weight the points appropriately (precise points count more)
2. Calculate the uncertainty in fit parameters
3. Test whether the fit is "good" (chi-squared test)

*Note: Week 2's prelab will explain how fitting programs calculate parameter uncertainties. For now, focus on interpreting and reporting them correctly.*

**Question 6:** A curve fitting program generated the following fit parameters:

$$a = -0.6699999999999988 \pm 0.6751049301158053$$
$$b = 2.2700000000000005 \pm 0.2035517952102936$$

(a) Rewrite these values following the convention that uncertainty should have 1-2 significant figures, and the measurement should be reported to the same decimal place as the uncertainty.

(b) Based on the uncertainties, is parameter $a$ statistically different from zero? How do you know? (Hint: compare the value to its uncertainty.)

## Reflection: Preparing for Lab

**Question 7:** In the Week 1 lab, you will compare uncertainty estimates from a multimeter and an oscilloscope viewing the same signal. Based on what you learned in this prelab:

(a) Do you expect the two instruments to give the same uncertainty estimate? Why or why not?

(b) If they differ, which one would you trust more for determining whether your laser is stable enough for beam width measurements?

## What You Should Bring to Lab

1. Your answers to Questions 1-7
2. The calculated values from Methods A-D
3. An understanding of when each estimation method is appropriate

---

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

1.  Get a laser and power supply from the “He-Ne Laser” drawer in the colored drawer cabinet found in your chosen or assigned optics bay. You’ll also need two sets of 3D-printed laser tube mounts which you can find in the same drawer (see Figure @fig:tube-mount). The bottom mount first gets mounted to an optical post and then the top of the mount can be assembled with ¼-20 socket head cap screw and nut. After both sets of tube mounts are attached to the laser, insert the optical posts into post holders and attach the assembly to the optical table.
2. Each person in your group is responsible for assembling a mirror as shown in Figure @fig:mount-assembley. In the end, you will need at least 2 mirrors to complete the next task. **Remember to wear latex/nitrile gloves or finger cots while handling optical components.** 

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

1. Here you will encounter gain values that are presented on a logarithmic $dB$ (decibel) scale, which is obtained by taking $20×log(V_{out}/V_{in})$. For example, $20\ dB$ of gain corresponds to electronic voltage amplification by a factor of 10. A $dB$ scale could also be defined as $10×log(P_{out}/P_{in})$, where $P$ is the power. Explain the conversion between these two scales and why this makes sense. 
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

# Verifying Uncertainty Methods (In-Lab)

In the prelab, you compared different uncertainty estimation methods using provided data. Now you will verify your understanding by applying these methods to real measurements with your photodetector.

**Make sure that your laser has been turned on for at least 5 minutes so it has had the opportunity to warm up.**

## Quick Verification Exercise

Using the oscilloscope to measure your photodetector output voltage:

1. **Measure using two methods:**
   - Use the oscilloscope's RMS measurement function to record the mean and RMS fluctuations
   - "Eyeball" the amplitude of fluctuations from the display

2. **Compare to your prelab predictions:**
   - In prelab Question 7, you predicted whether these methods would agree. Were you correct?
   - If they differ, which method do you trust more? Why?

3. **Record in your notebook:**
   - Mean voltage: ______ V
   - RMS fluctuation (scope measurement): ______ V
   - Estimated fluctuation (eyeball): ______ V
   - Brief note on agreement/disagreement with prelab predictions

This brief verification ensures you can apply the concepts from the prelab to real measurements. You will develop more sophisticated noise characterization skills in Week 2.

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

## Prelab (complete before arriving at lab)

1. **Uncertainty methods analysis**: Answers to Questions 1-7 from the prelab
2. **Data analysis results**: Calculated values from Methods A-D using the provided photodetector_samples.csv file

## In-Lab Documentation (recorded during lab)

1. **Optical setup diagram** showing laser, mirrors, alignment discs, and photodetector positions
2. **Photodetector calibration data**: offset voltage vs. gain setting, relative gain measurements
3. **Uncertainty verification**: Brief comparison of oscilloscope measurements to prelab predictions
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

2. Based on your prelab analysis and in-lab verification, which uncertainty estimation method would you use for your beam width measurements? Why? 
