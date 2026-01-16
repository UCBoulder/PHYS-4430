---
title: "Gaussian Beams - Week 2"
---

# Where We Are in the Sequence

**Week 2 of 4: Instrumentation and Noise Characterization**

Last week you calibrated your photodetector and learned to measure beam width manually. This week you'll learn Python-based data acquisition and—critically—characterize your measurement system's noise floor. Your goal: make a quantitative, evidence-based decision about which gain setting to use for Week 4's automated measurements.

**Last week:** Aligned optics, calibrated photodetector, measured beam width manually

**This week:** Learn DAQ programming → Characterize measurement system noise → Choose optimal gain setting

**Next week:** Learn Gaussian beam theory → Set up motor controller → Take first automated measurement

# Overview

The second week of the Gaussian Beams lab introduces you to Python for data acquisition and guides you through interfacing Python with the instrumentation and data acquisition systems used in this course. You will also learn about digital sampling theory and characterize your measurement system's noise floor—a critical step for making informed measurement decisions in Week 4.

**An important discovery awaits:** The DAQ device that records your data has its own noise floor—and this is what actually limits your Week 4 measurements. Every instrument has limitations. Expert experimentalists characterize those limitations and design around them. This week, you'll do exactly that.

This week's lab is divided into two parts. In part 1 (Prelab), you will learn essential curve fitting techniques that you'll use throughout this course. In part 2 (Lab), you will learn Python programming for data acquisition using a National Instruments DAQ device, the [NI USB-6009](https://www.ni.com/docs/en-US/bundle/usb-6009-specs/page/specs.html). This multifunction USB powered device has 8 single-ended (4 differential) analog inputs (14-bit, 48 kS/s), 2 analog outputs (12-bit, 150 S/s), 12 digital I/O channels, and a 32-bit counter. You will then apply these DAQ skills to characterize your measurement system's noise floor and make a quantitative decision about optimal gain settings.

## What is Python?

Python is a versatile programming language widely used in scientific computing and data analysis. Many research labs use Python for instrument control, data acquisition, and analysis. Its advantages include:

- Free and open source
- Extensive scientific libraries (NumPy, SciPy, Matplotlib)
- Large community with excellent documentation
- Easy to learn and read
- Works on all major operating systems

You can use Python on the lab laptops where it is already installed. See the [Python Resources](/PHYS-4430/python-resources) page for installation instructions if you want to set it up on your own computer.

## Learning Goals

After completing the prelab, you will be able to:

1. Explain why we minimize the sum of squares to get the best fit.
2. Carry out a least-squares minimization graphically.
3. Plot residuals to visually inspect the goodness of a fit.
4. Interpret the uncertainty in fit parameters from `scipy.optimize.curve_fit`.
5. Compute $\chi^2$ for a fit and use it to determine if a fit is "good".
6. Create plots with error bars using Matplotlib.

After completing the lab, you will be able to:

1. Connect a USB DAQ device to a computer and confirm the analog inputs are working correctly.
2. Write a Python script to read analog voltage measurements.
3. Configure sample rate and number of samples for data acquisition.
4. Explain Nyquist's theorem and choose appropriate sample rates.
5. Recognize aliasing and understand its causes.
6. Measure the DAQ noise floor and compare to datasheet specifications.
7. Identify which component (photodetector or DAQ) limits your measurement system's noise.
8. Calculate signal-to-noise ratio and explain why gain improves SNR despite a fixed DAQ noise floor.
9. Select and justify an optimal gain setting based on quantitative analysis.
10. Confront predictions with measurements and identify sources of discrepancies.
11. Save acquired data to a CSV file.

# Overview of Your Work

This week culminates in a decision: **which gain setting will you use for Week 4's automated beam profiling?** This isn't arbitrary—you'll build the quantitative evidence to justify your choice.

**Prelab:** Develop curve-fitting skills you'll use throughout this course. You'll learn to minimize χ², interpret residuals, and assess goodness of fit. These skills are essential for extracting beam widths from your knife-edge data.

**In Lab:** You'll work through a predict-measure-compare cycle for noise characterization:

1. **Learn DAQ fundamentals** — Read voltages with Python, understand sampling theory, observe aliasing
2. **Characterize DAQ noise floor** — Measure the DAQ's intrinsic noise with input shorted, then understand what limits your measurement system
3. **Understand the measurement chain** — Discover which component (photodetector or DAQ) dominates your system noise at each gain setting
4. **Predict and measure SNR** — Before measuring, predict how signal-to-noise ratio changes with gain given a fixed DAQ noise floor. Then measure and confront your predictions.
5. **Make your decision** — Select a gain setting for Week 4 with written justification based on your data

*See the detailed deliverables checklist at the end of this guide.*

# Prelab

This week's prelab builds on the uncertainty concepts you learned during Week 1's lab (where you measured voltage fluctuations and calculated standard deviation). Now we move from estimating uncertainties in individual measurements to fitting data and propagating those uncertainties to derived quantities. This is a "user's guide" to least-squares fitting and determining the goodness of your fits. At the end of the prelab you will be able to:

1. Explain why we minimize the sum of squares to get the best fit.
2. Carry out a least-squares minimization graphically.
3. Plot residuals to visually inspect the goodness of a fit.
4. Interpret the uncertainty in fit parameters.
5. Compute $\chi^2$ for a fit and use it to determine if a fit is "good".
6. Create plots with error bars using Matplotlib.

## Useful readings

1. Taylor, J. R. (1997). *An Introduction to Error Analysis: The Study of Uncertainties in Physical Measurements* (p. 327). University Science Books. This is the standard undergraduate text for measurement and uncertainty.
2. Bevington, P. R., & Robinson, K. D. (2003). *Data Reduction and Error Analysis for the Physical Sciences* Third Edition (3rd ed.). New York: McGraw-Hill. Great for advanced undergrad error analysis. Professional physicists use it too.

## Why do we minimize the sum of squares?

**Question:** Why do we call it "least-squares" fitting?

**Answer:** Because the best fit is determined by minimizing the weighted sum of squares of the deviation between the data and the fit. Properly speaking this "sum of squares" is called "chi-squared" and is given by

$$\chi^2 = {\displaystyle \sum_{i=1}^{N}}\frac{1}{\sigma_i^2}(y_i-y(x_i,a,b,c, \ ... \ ))^2\text{,}$$ {#eq:1}

where there are where $N$ data points, $(x_i,y_i )$, and the fit function is given by $y(x_i,a,b,c, \ … \ )$ where $a, b,$ etc. are the fit parameters.

**Question:** What assumptions are made for the method to be valid?

**Answer:** The two assumptions are:

1. **Gaussian distributed.** The random fluctuations in each data point $y_i$ are Gaussian distributed with standard deviation $\sigma_i$.
2. **Uncorrelated.** The random fluctuations in any one data point are uncorrelated with those in another data point.

**Question:** Why does minimizing the sum of squares give us the best fit?

**Answer:** Given the two above assumptions, the fit that minimizes the sum of squares is the ***most likely*** function to produce the observed data. This can be proven using a little calculus and probability. A more detailed explanation is found in Taylor's *Introduction to Error Analysis* Sec. 5.5 "Justification of the Mean as Best Estimate" or Bevington and Robinson's *Data Reduction* Sec. 4.1 "Method of Least-Squares".

## Minimizing $\chi^2$ graphically {#sec:min-graph}

*You will rarely minimize $\chi^2$ graphically in a lab. However, this exercise will help you better understand what fitting routines actually do to find the best fit.*

1. Download and plot [this data set](../resources/lab-guides/gaussian-laser-beams/profile_data_without_errors.csv). It was generated by inserting a razor blade into path of a laser beam and measuring the photodetector voltage of the laser light. The $x$ column is the micrometer (razor) position in meters and the $y$ column is the photodetector voltage in volts.

   ```python
   import numpy as np
   import matplotlib.pyplot as plt

   # Load the data
   data = np.loadtxt('profile_data_without_errors.csv', delimiter=',', skiprows=1)
   x_data = data[:, 0]
   y_data = data[:, 1]

   # Plot the data
   plt.figure(figsize=(10, 6))
   plt.scatter(x_data, y_data, label='Data')
   plt.xlabel('Position (m)')
   plt.ylabel('Voltage (V)')
   plt.legend()
   plt.show()
   ```

2. Define the same fit function as:

   $$y(x,a,b,c,w) = a \ Erf\left(\frac{\sqrt{2}}{w}(x-b)\right)+c$$

   In Python, this can be written using `scipy.special.erf`:

   ```python
   from scipy.special import erf

   def beam_profile(x, amplitude, center, width, offset):
       """Error function model for knife-edge beam profile.

       Parameters:
           x: position (m)
           amplitude: half the voltage swing (V)
           center: beam center position (m)
           width: beam width w (m)
           offset: vertical offset (V)
       """
       return amplitude * erf(np.sqrt(2) * (x - center) / width) + offset
   ```

3. Reduce the fit to two free parameters. This step is only necessary because it is hard to visualize more than 3 dimensions. Assume $a_{fit}=(V_{max}-V_{min})/2 = 1.4375$ and $c_{fit} =(V_{max}+V_{min})/2 = 1.45195$. These were determined by averaging the first 6 data points to get $V_{min}$ and the last 5 to get $V_{max}$.

4. Use Equation @eq:1 to write an expression for $\chi^2$ in terms of your $w$ and $b$ parameters, and the $x$ (position) data and $y$ (voltage) data. Since you don't have any estimate for the uncertainties $\sigma_i$, assume they are all unity so $\sigma_i=1$.

   ```python
   def chi_squared(width, center, x_data, y_data, amplitude_fixed, offset_fixed):
       """Calculate chi-squared for given parameters."""
       y_fit = beam_profile(x_data, amplitude_fixed, center, width, offset_fixed)
       return np.sum((y_data - y_fit)**2)
   ```

5. **Before running any code**, answer these prediction questions in your notebook:

   1. What shape do you expect the $\chi^2$ contours to have? (Circular? Elliptical? Irregular?) Why?
   2. If the contours are elliptical, what would it mean if the ellipse is tilted (major axis not aligned with $w$ or $b$ axes)?
   3. Where in the $(w, b)$ plane should the minimum $\chi^2$ occur—at the true beam width and position, or somewhere else?

6. Make a contour plot of $\chi^2(w,b)$ and tweak the plot range until you see the minimum. You can use AI assistance or the code below. The goal is to *interpret* the result, not to write the code from scratch.

   ```python
   # Create a grid of width and center values
   width_range = np.linspace(0.0003, 0.0007, 100)
   center_range = np.linspace(0.009, 0.011, 100)
   W, C = np.meshgrid(width_range, center_range)

   # Calculate chi-squared for each combination
   amplitude_fixed = 1.4375
   offset_fixed = 1.45195
   Z = np.zeros_like(W)
   for i in range(len(center_range)):
       for j in range(len(width_range)):
           Z[i, j] = chi_squared(width_range[j], center_range[i], x_data, y_data,
                                 amplitude_fixed, offset_fixed)

   # Make contour plot
   plt.figure(figsize=(10, 8))
   plt.contour(W * 1000, C * 1000, Z, levels=20)
   plt.colorbar(label='$\\chi^2$')
   plt.xlabel('width (mm)')
   plt.ylabel('center (mm)')
   plt.title('$\\chi^2$ Contour Plot')
   plt.show()
   ```

![Contour plot example.](../resources/lab-guides/gaussian-laser-beams/contour.png){#fig:contour width="15cm"}

7. **Interpretation questions** (answer in your notebook):

   1. Were your predictions from step 5 correct? If not, explain what you learned.
   2. The contours are likely elliptical and possibly tilted. Explain in 2-3 sentences why the parameters $w$ and $b$ might be correlated (i.e., why changing one affects the best value of the other).
   3. If the noise in the data were doubled, how would the contour plot change? Would the minimum move? Would the contours spread out or contract?

8. Graphically determine the best fit parameters to 3 significant digits.

9. Compare with the best fit result from `scipy.optimize.curve_fit` (allow all 4 parameters to vary). Do the fits agree for those three digits of precision?

   ```python
   from scipy.optimize import curve_fit

   # Initial guesses: [amplitude, center, width, offset]
   p0 = [1.4375, 0.01, 0.0005, 1.45195]

   # Perform the fit
   popt, pcov = curve_fit(beam_profile, x_data, y_data, p0=p0)

   print("Best fit parameters:")
   print(f"  amplitude = {popt[0]:.6f}")
   print(f"  center    = {popt[1]:.6f}")
   print(f"  width     = {popt[2]:.6f}")
   print(f"  offset    = {popt[3]:.6f}")
   ```

## Uncertainty in the fit parameters

**Question:** Where does the uncertainty in the fit parameters come from?

**Answer:** The optimal fit parameters depend on the data points $(x_i,y_i)$. The uncertainty, $\sigma_i$, in the $y_i$ means there is a propagated uncertainty in the calculation of the fit parameters. The error propagation calculation is explained in detail in the references, especially Bevington and Robinson.

**Question:** How does `curve_fit` calculate the uncertainty in the fit parameters when no error estimate for the $\sigma_i$ is provided?

**Answer:** When no uncertainties are provided, `curve_fit` (and other fitting routines) estimate the uncertainty in the data $\sigma_y^2$ using the "residuals" of the best fit:

$$\sigma_y^2 = \frac{1}{N-n}{\displaystyle \sum_{i=1}^{N}}(y_i-y(x_i,a_0,b_0,c_0, \ ... \ ))^2\text{,}\quad\quad$$ {#eq:2}

where there are $N$ data points $y_i$ and the best fit value at each point is given by $y$, which depends on $x_i$ and the $n$ best fit parameters $a_0,b_0,c_0, \ ... \ $. It is very similar to how you would estimate the standard deviation of a repeated measurement, which for comparison's sake is given by:

$$\sigma_y^2 = \frac{1}{N-n}{\displaystyle \sum_{i=1}^{N}}(y_i-\overline{y})^2\text{.}$$ {#eq:3}

The parameter uncertainties are then extracted from the covariance matrix:

```python
# Get parameter uncertainties from the covariance matrix
perr = np.sqrt(np.diag(pcov))

print("Parameter uncertainties:")
print(f"  σ_amplitude = {perr[0]:.6f}")
print(f"  σ_center    = {perr[1]:.6f}")
print(f"  σ_width     = {perr[2]:.6f}")
print(f"  σ_offset    = {perr[3]:.6f}")
```

## Estimating the uncertainty in the data

1. Use Equation @eq:2 and your best fit parameters to estimate $\sigma_y^2$, the statistical error of each data point given by your data.

   ```python
   # Calculate residuals
   y_fit = beam_profile(x_data, *popt)
   residuals = y_data - y_fit

   # Estimate variance (N data points, n=4 parameters)
   N = len(y_data)
   n = 4
   sigma_y_squared = np.sum(residuals**2) / (N - n)
   sigma_y = np.sqrt(sigma_y_squared)

   print(f"Estimated σ_y = {sigma_y:.6f} V")
   ```

2. Compare your result with the estimate from the fit. The estimated variance can be calculated from the residuals.

3. Do the estimates agree? Why or why not?

## Goodness of fit

This section covers two ways to analyze if a fit is good.

1. Plotting the residuals.
2. Doing a $\chi^2$ test.

### Plotting the fit residuals {#sec:plot-res}

The first step is to look at the residuals. The residuals, $r_i$, are defined as the difference between the data and the fit.

$$r_i=y_i-y(x_i,a,b,c, \ ... \ )$$

1. Make a plot of the residuals:

   ```python
   # Calculate and plot residuals
   residuals = y_data - beam_profile(x_data, *popt)

   plt.figure(figsize=(10, 4))
   plt.scatter(x_data, residuals)
   plt.axhline(y=0, color='r', linestyle='--')
   plt.xlabel('Position (m)')
   plt.ylabel('Residuals (V)')
   plt.title('Fit Residuals')
   plt.grid(True, alpha=0.3)
   plt.show()
   ```

2. Since we didn't provide any estimates of the uncertainties, the fitting assumed the uncertainty of every point is the same. Based on the plot of residuals, was this a good assumption?

3. Do the residuals look randomly scattered about zero or do you notice any systematic error sources?

4. Is the distribution of residuals scattered evenly around zero? Or is there a particular range of $x$ values where the residuals are larger than others?

5. What is the most likely source of the large uncertainty as the beam is cut near the center of the beam?

### "Chi by eye" - eyeballing the goodness of fit

**Question:** If I have a good fit, should every data point lie within an error bar?

**Answer:** No. Most should, but we wouldn't expect every data point to lie within an error bar. If the uncertainty is Gaussian distributed with a standard deviation $\sigma_i$ for each data point, $y_i$, then we expect roughly 68% of the data points to lie within their error bar. This is because 68% of the probability in a Gaussian distribution lies within one standard deviation of the mean.

### $\chi^2$ and $\chi_{red}^2$ for testing the "goodness" of fit

This section answers the question "What should $\chi^2$ be for a good fit?"

Suppose the only uncertainty in the data is statistical error, with a known standard deviation $\sigma_i$, then on average each term in the sum is

$$\frac{1}{\sigma_i^2}(y_i-y(x_i,a,b,c, \ ... \ ))^2 \approx 1\text{,}$$ {#eq:4}

and the full $\chi^2$ sum of squares is approximately

$$\chi^2 = {\displaystyle \sum_{i=1}^{N}}\frac{1}{\sigma_i^2}(y_i-y(x_i,a,b,c, \ ... \ ))^2\approx N-n\text{.}\quad\quad$$ {#eq:5}


So a good fit has

$$\chi_{red}^2 \equiv \frac{\chi^2}{N-n}\approx 1\text{.}$$ {#eq:6}

1. **Fact: To find the goodness of fit test, you must first estimate the uncertainties on the data points that you are fitting.** How would you explain the reason for this in your own words?

### Choosing a strategy to estimate the uncertainty

1. Considering your answers from Section @sec:plot-res (especially @sec:plot-res\.5), which method would give you the best estimate of the uncertainty for each data point, and why?

   - Eyeballing the fluctuations in each data point.

   - Taking $N$ measurements at each razor position and then going to the next position.

   - Taking the entire data set $N$ times.


### Weighted fits

When you have estimated the uncertainty $\sigma_i$ of each data point $y_i$ you should use this information when fitting to correctly evaluate the $\chi^2$ expression in Equation @eq:1. The points with high uncertainty contribute less information when choosing the best fit parameters.

In Python's `curve_fit`, you provide uncertainties using the `sigma` parameter:

```python
# Weighted fit with known uncertainties
popt, pcov = curve_fit(
    beam_profile,
    x_data,
    y_data,
    p0=p0,
    sigma=sigma_list,        # Your uncertainty estimates
    absolute_sigma=True      # Use actual sigma values (not relative)
)
```

1. Download [this data set](../resources/lab-guides/gaussian-laser-beams/profile_data_with_errors.csv) for a beam width measurement with uncertainties. The first column is razor position in meters, the second column is photodetector output voltage, and the third column is the uncertainty on the photodetector output voltage.

   ```python
   # Load data with uncertainties
   data = np.loadtxt('profile_data_with_errors.csv', delimiter=',', skiprows=1)
   x_data = data[:, 0]
   y_data = data[:, 1]
   y_err = data[:, 2]
   ```

2. Do a weighted fit using the same fit function as in Section @sec:min-graph. Use the uncertainty estimates in the third column.

   ```python
   # Weighted fit
   popt, pcov = curve_fit(
       beam_profile, x_data, y_data,
       p0=[1.4, 0.01, 1.45, 0.0005],
       sigma=y_err,
       absolute_sigma=True
   )
   perr = np.sqrt(np.diag(pcov))
   ```

3. Calculate $\chi^2$:

   ```python
   # Calculate chi-squared
   y_fit = beam_profile(x_data, *popt)
   chi2 = np.sum(((y_data - y_fit) / y_err)**2)
   dof = len(y_data) - len(popt)  # degrees of freedom
   chi2_red = chi2 / dof

   print(f"Chi-squared: {chi2:.2f}")
   print(f"Degrees of freedom: {dof}")
   print(f"Reduced chi-squared: {chi2_red:.2f}")
   ```

4. How close is the reduced chi-squared to 1?

5. **The "chi-squared test".** This part helps us understand if the value of $\chi^2$ is statistically likely or not. The following graph gives the probability of exceeding a particular value of $\chi^2$ for $\nu=𝑁−𝑛=22$ degrees of freedom. It can be calculated using the Cumulative Density Function (CDF) for the chi-squared distribution. Use the graph to estimate the likelihood this value of $\chi^2$ occurred by chance.

   ```python
   from scipy import stats

   # Calculate p-value (probability of getting this chi2 or higher by chance)
   p_value = 1 - stats.chi2.cdf(chi2, dof)
   print(f"P-value: {p_value:.4f}")
   ```

![Cumulative Density Function (CDF) for the chi-squared distribution.](../resources/lab-guides/gaussian-laser-beams/cdf.png){#fig:cdf width="15cm"}

### Why is it often bad to overestimate uncertainties?

1. Why can overestimating the uncertainty make your fit appear good (i.e., $\frac{\chi^2}{N-n}\approx 1$)?

Overestimating the uncertainties makes the fit seem good (according to a $\chi^2$ test), even when it might be obviously a bad fit. It is best to do the $\chi^2$ test using an honest estimate of your uncertainties. If the $\chi^2$ is larger than expected $(\chi^2>𝑁−𝑛)$, then you should consider both the possibility of systematic error sources and the quality of your estimates of the uncertainties. On the other hand, if the $\chi^2$ test is good $(\chi^2\approx 𝑁−𝑛)$, then it shows you have a good handle on the model of your system, and your sources of uncertainty. Finally, if $\chi^2\ll (𝑁−𝑛)$, this likely indicates overestimated uncertainties.

### When does `curve_fit` underestimate the true uncertainty?

The uncertainty reported by `curve_fit` comes from the covariance matrix and assumes:

1. The only source of error is statistical noise in your voltage measurements
2. This noise is independent for each data point
3. Your model perfectly describes the underlying physics

In real experiments, these assumptions often fail. Consider these scenarios relevant to your beam width measurements:

**Systematic errors in position:**
- If your micrometer has a 0.01 mm systematic offset, this affects all measurements the same way
- `curve_fit` doesn't know about this, so it can't include it in the parameter uncertainty
- The true uncertainty in beam width includes uncertainty in position calibration

**Model limitations:**
- The error function model assumes a perfectly Gaussian beam
- Real laser beams may have slight deviations from Gaussian
- The fit uncertainty assumes the model is exact

**Correlated noise:**
- If 60 Hz interference affects multiple adjacent points similarly, they're not independent
- `curve_fit` assumes independent errors, so it underestimates uncertainty

**Reflection questions:**

1. Under what conditions might the `curve_fit` uncertainty be a good estimate of your true measurement uncertainty?

2. In Week 4, you'll extract beam waist $w_0$ from fits at multiple positions. Besides statistical noise in voltage measurements, what other sources of uncertainty should you consider? List at least two.

### Statistical vs. Systematic Uncertainties

Understanding the distinction between statistical and systematic uncertainties is crucial for proper error analysis. This distinction becomes especially important in Week 4 when you construct an uncertainty budget.

**Statistical uncertainties** (also called "random uncertainties") are unpredictable fluctuations that vary from measurement to measurement. They average out over many measurements—take 100 readings and compute the mean, and the statistical uncertainty in that mean decreases by $\sqrt{100} = 10$.

Examples from this lab:
- Voltage noise on the photodetector (varies each reading)
- Thermal fluctuations in electronic components
- Shot noise from photon arrival times

**Systematic uncertainties** are consistent biases that affect all measurements the same way. They do NOT average out—take 100 readings and the systematic error remains exactly the same.

Examples from this lab:
- Micrometer calibration offset (if it reads 0.02 mm high, ALL positions are 0.02 mm high)
- DAQ voltage offset (shifts all readings by a fixed amount)
- Beam not perfectly perpendicular to knife edge (consistent underestimate of width)

**Why this matters for fitting:**

`curve_fit` only sees statistical scatter around your fit function. It has no way to detect systematic offsets. If your micrometer is miscalibrated by 0.1 mm, the fit will find parameters that are systematically shifted, and `curve_fit` will not include this in the reported uncertainty.

**Quick self-test:** Classify each of these as statistical (St) or systematic (Sy):

1. The photodetector gain knob is actually at 28 dB when the label says 30 dB: _____
2. 60 Hz pickup causing voltage fluctuations: _____
3. The laser power slowly drifting over 30 minutes: _____ (tricky—think about whether it averages out)
4. Room lights flickering: _____

*Answers: 1=Sy, 2=St (if averaging over many cycles), 3=Sy (drift is correlated, doesn't average out), 4=St*

In Week 4, when you construct your uncertainty budget, you will need to identify the dominant sources of both statistical AND systematic uncertainty, and combine them appropriately.

## Error bars

The error bar is a graphical way to display the uncertainty in a measurement. In order to put error bars on a plot you must first estimate the error for each point. Anytime you include error bars in a plot you should explain how the uncertainty in each point was estimated (e.g., you "eyeballed" the uncertainty, or you sampled it $N$ times and took the standard deviation of the mean, etc.)

### Error bars in Python with Matplotlib

Creating plots with error bars in Python is straightforward using `plt.errorbar()`:

```python
import numpy as np
import matplotlib.pyplot as plt

# Load data with uncertainties
data = np.loadtxt('gaussian_data_with_errors.txt', skiprows=1)
x = data[:, 0]      # Position
y = data[:, 1]      # Voltage
y_err = data[:, 2]  # Uncertainty

# Create plot with error bars
plt.figure(figsize=(10, 6))
plt.errorbar(x, y, yerr=y_err, fmt='o', capsize=3,
             label='Data with uncertainties')
plt.xlabel('Micrometer Position (inches)')
plt.ylabel('Photodetector Voltage (V)')
plt.title('Gaussian Beam Width Measurement')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

The `errorbar()` function parameters:
- `x`, `y`: Data points
- `yerr`: Uncertainty values (can also use `xerr` for horizontal error bars)
- `fmt='o'`: Marker style (circles)
- `capsize=3`: Size of error bar caps

### Example: Gaussian laser beam width measurement

Suppose you had estimated the uncertainty at every point in a width measurement of your Gaussian laser beam to be $0.04 \ V$. This error was chosen to demonstrate the mechanics of making a plot with error bars, but the uncertainty in the actual data was probably smaller than this.

<center>

| Micrometer Position (inches) | Photodetector Voltage (V) | Estimated uncertainty (V) |
| :--------------------------: | :-----------------------: | :-----------------------: |
|            0.410             |           0.015           |           0.04            |
|            0.412             |           0.016           |           0.04            |
|            0.414             |           0.017           |           0.04            |
|            0.416             |           0.026           |           0.04            |
|            0.418             |           0.060           |           0.04            |
|            0.420             |           0.176           |           0.04            |
|            0.422             |           0.460           |           0.04            |
|            0.424             |           0.849           |           0.04            |
|            0.426             |           1.364           |           0.04            |
|            0.428             |           1.971           |           0.04            |
|            0.430             |           2.410           |           0.04            |
|            0.432             |           2.703           |           0.04            |
|            0.434             |           2.795           |           0.04            |
|            0.436             |           2.861           |           0.04            |
|            0.438             |           2.879           |           0.04            |
|            0.440             |           2.884           |           0.04            |

Table: Table of data with a fixed uncertainty used to illustrate creating plots with error bars. {#tbl:example-data}

</center>

<br>

Download [this data set](../resources/lab-guides/gaussian-laser-beams/gaussian_data_with_errors.txt) and create a plot with error bars like Figure @fig:gauss-example.

```python
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = np.loadtxt('gaussian_data_with_errors.txt', skiprows=1)
position = data[:, 0]
voltage = data[:, 1]
uncertainty = data[:, 2]

# Create plot
plt.figure(figsize=(10, 6))
plt.errorbar(position, voltage, yerr=uncertainty,
             fmt='o', capsize=3, markersize=5)
plt.xlabel('Position (inches)')
plt.ylabel('Photodetector Output (V)')
plt.title('Gaussian Beam Width Measurement')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

![Plot of the provided Gaussian Beam data showing error bars.](../resources/lab-guides/gaussian-laser-beams/gauss-example.png){#fig:gauss-example width="15cm"}

## Prelab Exercise: Error Function Fitting Practice

Now that you understand curve fitting, apply it to beam width analysis. This exercise prepares you for analyzing your own knife-edge measurements.

**Note on AI assistance:** You may use AI tools to help write your curve fitting code. However, the learning goal is to understand what the code does and why. Be prepared to explain: (1) what the fit parameters mean physically, (2) why the error function is the appropriate model, and (3) how to interpret the uncertainties reported by `curve_fit`.

### The Error Function Model

In Week 1, you derived that blocking a Gaussian beam with a knife edge produces a signal described by:

$$P(x) = \frac{P_0}{2}\left[1 + \text{erf}\left(\frac{\sqrt{2}(x-x_0)}{w}\right)\right]$$

where $w$ is the beam width, $x_0$ is the beam center position, and $P_0$ is the total power.

For fitting, we use a slightly more general form that accounts for offsets:

$$y(x) = a \cdot \text{erf}\left(\frac{\sqrt{2}}{w}(x-b)\right) + c$$

where:
- $a$ = amplitude (half the voltage swing)
- $b$ = beam center position
- $w$ = beam width (what we want!)
- $c$ = vertical offset

### Practice Exercise

Download [Test_Profile_Data.csv](../resources/lab-guides/gaussian-laser-beams/Test_Profile_Data.csv) and complete the following:

1. **Plot the raw data** (position vs. voltage). Does it look like an error function?

2. **Define the fit function** (same as used earlier):
   ```python
   from scipy.special import erf

   def beam_profile(x, amplitude, center, width, offset):
       """Error function model for knife-edge beam profile.

       Parameters:
           x: position (m)
           amplitude: half the voltage swing (V)
           center: beam center position (m)
           width: beam width w (m)
           offset: vertical offset (V)
       """
       return amplitude * erf(np.sqrt(2) * (x - center) / width) + offset
   ```

3. **Perform the fit:**
   ```python
   from scipy.optimize import curve_fit

   # Load data
   data = np.loadtxt('Test_Profile_Data.csv', delimiter=',', skiprows=1)
   x = data[:, 0]  # Position (m)
   y = data[:, 1]  # Voltage (V)

   # Initial guesses (estimate from your plot)
   # Order: [amplitude, center, width, offset]
   p0 = [1.0, 0.001, 0.0005, 0.5]

   # Fit
   popt, pcov = curve_fit(beam_profile, x, y, p0=p0)
   perr = np.sqrt(np.diag(pcov))  # Standard errors

   print(f"Beam width w = {popt[2]:.2e} ± {perr[2]:.2e} m")
   ```

4. **Verify your result:** You should get $w = 4.52 \times 10^{-4}$ m (approximately 0.45 mm).

5. **Plot data and fit together** to verify the fit is reasonable.

6. **Interpret the uncertainties:** What is the fractional uncertainty in your beam width? Is this uncertainty dominated by statistical noise or could there be systematic effects?

*Save your fitting code—you will use this same procedure to analyze your own knife-edge data in lab.*

# Introduction to Python for Data Acquisition

In this part of the lab, you will learn to use Python for data acquisition. We'll use the `nidaqmx` library to interface with National Instruments DAQ devices.

## Development Environment

For this lab, we recommend starting with **Jupyter Notebook** for interactive exploration, then transitioning to **VS Code** or another editor for writing reusable scripts. See the [Python Resources](/PHYS-4430/python-resources) page for setup instructions.

## Connect the USB-6009 and verify it is working

1. Ensure the NI-DAQmx drivers are installed (they should already be on lab computers). If needed, download from [NI-DAQmx](https://www.ni.com/en-us/support/downloads/drivers/download.ni-daq-mx.html).

2. Connect the USB cable to your computer and the USB-6009.

3. Open NI Measurement & Automation Explorer (NI-MAX) to verify the device is recognized:
   - The device should appear under "Devices and Interfaces"
   - Right-click and run "Self-Test" to verify the connection
   - Open the "Test Panel" to test analog inputs manually

4. Use Python to list available DAQ devices:

   ```python
   import nidaqmx
   from nidaqmx.system import System

   # List all connected DAQ devices
   system = System.local()
   for device in system.devices:
       print(f"Device: {device.name}")
       print(f"  Product Type: {device.product_type}")
       print(f"  AI Channels: {[ch.name for ch in device.ai_physical_chans]}")
   ```

5. Connect the 5V power rail to `AI0+` and ground to `AI0-`. You must connect both wires since the device measures a potential difference between the two terminals.

6. Read a voltage to verify the connection:

   ```python
   with nidaqmx.Task() as task:
       task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
       voltage = task.read()
       print(f"Measured voltage: {voltage:.4f} V")
   ```

## Reading Multiple Samples

To capture time-varying signals, you need to configure the sample rate and number of samples.

### Understanding Sample Rate and Samples to Read

When acquiring data, you must specify:

- **Sample Rate**: How many samples per second (Hz)
- **Samples to Read**: Total number of samples to acquire

For example, to capture 5 periods of a 1 kHz sine wave with 20 samples per period:

- Samples to Read = 5 periods × 20 samples/period = 100 samples
- Total time = 5 periods / 1000 Hz = 5 ms
- Sample Rate = 100 samples / 0.005 s = 20,000 Hz

### Acquiring Multiple Samples {#sec:analogmeas}

```python
import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType

# Configuration
sample_rate = 20000  # Hz
samples_to_read = 100

# Acquire data
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(
        rate=sample_rate,
        sample_mode=AcquisitionType.FINITE,
        samps_per_chan=samples_to_read
    )

    data = task.read(number_of_samples_per_channel=samples_to_read)

# Create time array
time = np.arange(samples_to_read) / sample_rate

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(time * 1000, data)  # Time in ms
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('Acquired Signal')
plt.grid(True, alpha=0.3)
plt.show()
```

### Exercise: Capture a Waveform

*Equipment: Use the Tektronix TBS 2000 Series oscilloscope and Keysight EDU33212A waveform generator at your station. These are the same instruments you used in PHYS 3330.*

1. Connect your waveform generator to both an oscilloscope and your DAQ device.
2. Set the waveform generator to output a sine wave at a frequency compatible with your sample rate calculation.
3. Modify the sample rate and samples to read to capture approximately 5 complete periods.
4. Run the acquisition and compare the Python plot with the oscilloscope display. Are they compatible?
5. Add to your notebook: the Python code, the resulting plot, and the oscilloscope output. Explain how they all make sense together.

# Digital Sampling and Nyquist Frequency

Now that you can acquire data with the DAQ, it's important to understand how the choice of sample rate affects your measurements. This section explores what happens when you sample a signal too slowly.

## Exploring Sample Rate Effects

1. Modify your Python script so that the *Number of Samples* and *Sample Rate* are easily configurable variables at the top:

   ```python
   import nidaqmx
   import numpy as np
   import matplotlib.pyplot as plt
   from nidaqmx.constants import AcquisitionType

   # Configuration - easily adjustable
   SAMPLE_RATE = 500     # Samples per second
   NUM_SAMPLES = 500     # Total samples (1 second of data)
   DAQ_CHANNEL = "Dev1/ai0"

   def acquire_data(sample_rate, num_samples, channel):
       """Acquire data from DAQ with specified parameters."""
       with nidaqmx.Task() as task:
           task.ai_channels.add_ai_voltage_chan(channel)
           task.timing.cfg_samp_clk_timing(
               rate=sample_rate,
               sample_mode=AcquisitionType.FINITE,
               samps_per_chan=num_samples
           )
           data = task.read(number_of_samples_per_channel=num_samples)
       return np.array(data)
   ```

2. Set up a function generator to produce a **1 kHz sine wave**.

3. Connect the function generator's output to both the oscilloscope and the DAQ.

## Initial Measurements

1. Set the sample rate in your Python script to **500 samples per second** and the number of samples such that it records 1 second of data.

2. Record and plot a dataset with both the oscilloscope and the DAQ. Make sure that the time range on the oscilloscope is set such that it is on the same order as the data being recorded by the DAQ.

   ```python
   # Acquire and plot data
   data = acquire_data(SAMPLE_RATE, NUM_SAMPLES, DAQ_CHANNEL)
   time = np.arange(NUM_SAMPLES) / SAMPLE_RATE

   plt.figure(figsize=(10, 6))
   plt.plot(time, data)
   plt.xlabel('Time (s)')
   plt.ylabel('Voltage (V)')
   plt.title(f'Acquired Signal ({SAMPLE_RATE} Hz sample rate)')
   plt.grid(True, alpha=0.3)
   plt.show()
   ```

3. Compare the two plots. What are the major differences between the two?

4. Why might one or both of these plots be giving an incorrect result? Think about the wave you are measuring and the result you are getting. How do they relate?

## Enhanced Understanding

This section will guide you to an understanding of Nyquist's theorem and a more appropriate sample rate for digital data collection.

1. Why do you think the data from the DAQ produced a wave of lower frequency?

2. Adjust the sample rate in a way you think might provide a more accurate measurement of the wave. What do you think the measured waveform will look like this time?

3. Take a dataset, record and plot it. Did it match your predictions?

4. Now record another dataset with the function generator set to the same parameters but the sample rate set to **3000 samples per second** and the number of samples set to record 1 second of data.

5. Plot this new dataset. What is the frequency of the new dataset?

6. What are the fundamental differences between the first, second, and third datasets?

## Nyquist Frequency

The discrepancies between the sampled waveforms can be explained by **Nyquist's theorem**. It states that to accurately measure a signal by discrete sampling methods (like the DAQ) the sampling rate must be at least twice that of the measured signal. If this were not the case, a measurement might not be taken at every interval of oscillation, a situation called "undersampling." Sampling the signal at least twice as fast as the maximum frequency of interest ensures that at least two data points are recorded each period.

**Definition:**

The *Nyquist Frequency* is defined to be half the sample rate.

### Aliasing Exercises

1. **Predict** the *apparent* frequency (in Hz) of the signal recorded by the DAQ. **Observe** what really happens using your waveform generator, DAQ, and Python script. **Explain** the result. Suppose the DAQ is set to 1 kS/s sample rate in all of the cases, while the waveform generator is set to:

   1. 1000 Hz
   2. 998 Hz
   3. 1004 Hz
   4. 1500 Hz
   5. 2000 Hz
   6. 1997 Hz
   7. 2005 Hz

   In understanding what is going on, it may help to draw a few periods of the wave and then indicate where the DAQ will sample the waveform.

2. You *want* to measure the random fluctuations (noise) in a signal from 0-100 Hz.

   1. If you set the sample rate at 200 Hz, what set of frequency ranges will contribute to the noise measurement?
   2. If you set the sample rate at 1000 Hz, what set of frequency ranges will contribute to the noise measurement?
   3. How could you help achieve the desired measurement in 2.1 using a combination of changing the sample rate and adding filtering? Explain why your choice of sample rate and signal filter would work better.

3. **Undersampling on the oscilloscope.** Undersampling is an issue with any device that samples data at regular discrete time intervals. This question requires the use of a Tektronix TBS 2000 Series oscilloscope and the Keysight EDU33212A waveform generator.

   1. The oscilloscope's sample rate depends on the time/div setting. On the Tektronix TBS 2000, you can see acquisition information by pressing **Acquire** on the front panel. The sample rate changes as you adjust the horizontal (time) scale—slower time scales use lower sample rates.
   2. Predict what you should observe if you set the waveform generator to the same frequency as the oscilloscope's sample rate. Try it out, compare with your prediction, and explain your observations.
   3. What happens if you change the oscilloscope time scale? Or change the waveform generator frequency slightly? Try to explain what you observe.

   *Note: You may need to use the waveform generator's "Sync/Trigger out" connector to trigger the oscilloscope externally for stable display at certain frequencies.*

# Noise Floor Characterization

In Week 1, you calibrated your photodetector's gain and offset at several settings. This week, you'll characterize your measurement system's noise floor—and make an important discovery about what actually limits your measurements.

**Connection to Week 1:** In Week 1, you measured voltage fluctuations and calculated standard deviation. The "RMS noise" you measure this week IS the standard deviation of repeated voltage measurements. When we say the DAQ has "5 mV RMS noise," we mean that if you take many samples of a constant input, the standard deviation of those samples will be about 5 mV. The DAQ noise floor therefore becomes the minimum achievable uncertainty ($\sigma_V$) for any voltage measurement you make with this instrument.

In this section, you will:

1. Measure the DAQ's intrinsic noise floor and compare to datasheet specifications
2. Identify which component (photodetector or DAQ) dominates your system noise
3. Predict how signal-to-noise ratio depends on gain given a fixed noise floor, then verify experimentally
4. Select and justify a gain setting for Week 4 based on quantitative analysis

This matters because in Week 4, you will measure beam profiles where the signal varies over a wide range. Understanding your actual noise floor—not just the datasheet specs—is essential for making informed measurement decisions.

## Background: Understanding Your Measurement Chain

### The Complete Signal Path

Before characterizing noise, you need to understand where noise enters your measurement. Here's your complete signal chain:

```
Laser → Photodetector → BNC Cable → DAQ → Computer
         (amplifies)                 (digitizes)
```

**Each component contributes noise:**

| Component | Noise Source | Typical Level |
|-----------|-------------|---------------|
| Photodetector (PDA36A) | Amplifier, thermal | 0.3 – 1.1 mV RMS (gain dependent) |
| BNC Cable | Pickup, interference | Usually negligible |
| DAQ (USB-6009) | Quantization, thermal | ~5 mV RMS |

**Critical insight:** The DAQ's noise floor (~5 mV) is higher than the photodetector's noise at ALL gain settings. When you measure "photodetector noise" through the DAQ, you're actually measuring DAQ noise.

This is authentic experimental physics—you characterize what you CAN measure and design your experiment around instrumental limitations.

### Why DAQ Noise Dominates

The USB-6009 DAQ has:
- 14-bit resolution over ±10 V range
- Least Significant Bit (LSB) = 20 V / 2^14 ≈ 1.2 mV
- Additional noise from amplifiers, thermal effects: ~5 mV RMS total

Meanwhile, the PDA36A photodetector datasheet specifies:
- 0 dB gain: ~300 µV RMS noise
- 70 dB gain: ~1.1 mV RMS noise

**The DAQ noise (5 mV) exceeds photodetector noise (0.3–1.1 mV) at every gain setting.** This means:

1. You cannot directly measure photodetector noise with this DAQ
2. Your Week 4 measurements will be limited by DAQ noise, not photodetector noise
3. Gain still matters! Higher gain amplifies your *signal* relative to the fixed DAQ noise floor

**Why this matters:** You might initially feel frustrated that you "can't measure what the lab was supposed to measure." This frustration is authentic—real experimentalists regularly encounter instrumental limitations that force them to redesign their approach. The skill you're developing here—characterizing what you CAN measure and designing around limitations—is more valuable than simply confirming a datasheet specification. When you join a research lab or start a job, this ability to identify and work within instrumental constraints will set you apart.

### Signal-to-Noise Ratio (SNR) with Fixed Noise

The signal-to-noise ratio determines measurement precision:

$$\text{SNR} = \frac{V_{\text{signal}}}{V_{\text{noise, RMS}}}$$

**Key insight:** If your noise floor is fixed at ~5 mV (DAQ-limited), then:

| Factor | Effect of Higher Gain |
|--------|----------------------|
| Signal voltage | Increases with gain |
| Noise voltage | Stays fixed at ~5 mV (DAQ floor) |
| SNR | Signal / 5 mV → **improves with gain!** |
| Limitation | Saturation (signal must stay < 4.5 V) |

This is why gain optimization matters: you want the highest gain that doesn't saturate.

For meaningful measurements, you generally want SNR > 10 (distinguishable from noise) or SNR > 100 (precise measurements).

## Part 1: Characterize the DAQ Noise Floor

In this section, you'll measure the DAQ's intrinsic noise—isolated from any other source.

### Phase 1: Predict

Before measuring, make quantitative predictions by working through these calculations:

1. **Quantization noise (theoretical minimum):** An ideal ADC's noise floor comes from digitization. For a 14-bit ADC with ±10 V range:
   - Calculate the LSB (Least Significant Bit): LSB = 20 V / 2^14 = _____ mV
   - Quantization noise RMS: $\sigma_{\text{quantization}} = \frac{\text{LSB}}{\sqrt{12}}$ = _____ mV

   *This is the absolute minimum noise you could ever achieve with this DAQ.*

2. **Expected actual noise (from datasheet):** Real ADCs have additional noise sources (thermal, amplifier) beyond quantization. Look up the USB-6009 datasheet specifications:
   - Find the "Absolute Accuracy" specification for the ±10 V range: _____ mV
   - Absolute accuracy includes both systematic offset and random noise. A reasonable estimate is that RMS noise is roughly 50-70% of absolute accuracy.
   - Your predicted RMS noise: _____ mV

   *Show your reasoning for this estimate.*

**Your Prediction:** If you short the DAQ input and measure RMS noise, you expect approximately _____ mV. This should be significantly higher than quantization noise alone because: _______________________

### Phase 2: Measure

You'll measure the DAQ's intrinsic noise with the input shorted—this isolates the DAQ from all other noise sources.

1. **Disconnect** the photodetector from the DAQ.

2. **Short the DAQ input:** Connect AI0+ to AI0- (or connect AI0+ to ground GND). This ensures zero input signal.

3. **Write a noise measurement function:**

```python
import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType

def measure_noise(channel="Dev1/ai0", num_samples=1000, sample_rate=10000):
    """
    Measure DC level and RMS noise from a DAQ channel.

    Parameters:
        channel: DAQ channel to measure
        num_samples: Number of samples to acquire
        sample_rate: Sampling rate in Hz

    Returns:
        dc_level: Mean voltage (V)
        noise_rms: RMS noise (V)
    """
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel)
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=num_samples
        )

        data = np.array(task.read(number_of_samples_per_channel=num_samples))

        dc_level = np.mean(data)
        noise_rms = np.std(data)  # Standard deviation = RMS of AC component

    return dc_level, noise_rms
```

4. **Measure DAQ noise:** Run your function with the input shorted.

```python
dc, noise = measure_noise()
print(f"DC level: {dc*1000:.2f} mV")
print(f"RMS noise: {noise*1000:.2f} mV")
```

5. **Record your measurement:** DAQ noise (input shorted) = _______ mV RMS

### Phase 3: Compare

**Analysis Questions:**

1. **Measured vs. quantization limit:** Your measured noise (_____ mV) vs. your calculated quantization noise (_____ mV from Phase 1). The ratio is _____×. Why is actual noise higher than quantization alone? *(List at least two reasons)*

2. **Measured vs. prediction:** How does your measured RMS noise compare to your Phase 1 prediction? If they differ by more than 50%, identify possible reasons.

3. **Measured vs. datasheet:** Compare your measurement to the absolute accuracy you found in the datasheet. Is your RMS noise consistent with being 50-70% of absolute accuracy as estimated?

4. **Implications for Week 4:** Your DAQ noise floor is _____ mV. This means any signal smaller than about _____ mV (SNR < 1) will be buried in noise. At your typical signal levels (several volts), what SNR do you expect?

## Part 2: Signal Chain Characterization

Now add the photodetector and measure the complete system noise. The key question: does adding the photodetector change the measured noise?

### Setup

1. **Connect** the photodetector to the DAQ via BNC cable.
2. **Cap the photodetector** to block all light (measuring dark noise).

### Measurement

Measure noise at each gain setting with the photodetector connected but dark:

| Gain | Measured Noise RMS | DAQ Noise (Part 1) | Datasheet PD Noise | Dominant Source |
|------|-------------------|-------------------|-------------------|-----------------|
| 0 dB  | _______ mV | _______ mV | 0.3 mV | _______ |
| 30 dB | _______ mV | _______ mV | 0.5 mV | _______ |
| 50 dB | _______ mV | _______ mV | 0.7 mV | _______ |
| 70 dB | _______ mV | _______ mV | 1.1 mV | _______ |

**Key Question:** Does the measured noise change significantly with gain?

- If **NO** (noise stays ~constant at all gains): DAQ noise dominates. The photodetector noise is too small to detect through the DAQ.
- If **YES** (noise increases at high gain): Photodetector noise is becoming visible at high gain settings.

**Analysis Questions:**

1. At which gain setting(s), if any, does photodetector noise become comparable to DAQ noise? Show your comparison.

2. What is the "dominant noise source" for each gain setting? Fill in the last column of the table above.

3. Why does this matter for Week 4? If DAQ noise dominates at all gains, how does that affect your gain selection strategy?

## Part 3: SNR Optimization with Fixed Noise Floor

Given that your noise floor is fixed at ~5 mV (DAQ-limited), how do you maximize SNR? The answer: use higher gain to amplify your signal!

### The Gain-SNR Relationship

| Gain | Signal Multiplication | Noise | SNR = Signal/Noise |
|------|----------------------|-------|-------------------|
| 0 dB (1×) | V₀ | 5 mV | V₀/5 mV |
| 10 dB (3.2×) | 3.2 × V₀ | 5 mV | 3.2 × V₀/5 mV |
| 20 dB (10×) | 10 × V₀ | 5 mV | 10 × V₀/5 mV |
| 30 dB (32×) | 32 × V₀ | 5 mV | 32 × V₀/5 mV |

**SNR improves linearly with gain** because signal increases while noise stays fixed.

**The limit:** Saturation. The DAQ clips at ±10 V, so your signal must stay below ~4.5 V to avoid saturation effects.

### Prediction

Use your Week 1 calibration data and your measured DAQ noise floor to predict SNR at each gain.

Assume you have a weak optical signal giving V₀ = _____ V at 0 dB gain. (Use a value from Week 1, or assume 50 mV for practice.)

| Gain | Predicted Signal (V) | Predicted Noise (mV) | Predicted SNR |
|------|---------------------|---------------------|---------------|
| 0 dB  | _______ | _______ (DAQ floor) | _______ |
| 30 dB | _______ | _______ (DAQ floor) | _______ |
| 50 dB | _______ | _______ (DAQ floor) | _______ |
| 70 dB | _______ | _______ (DAQ floor) | _______ |

**Note:** Use your measured DAQ noise floor (~5 mV) for all predictions, since DAQ noise dominates.

### Measurement

Set up your Week 1 laser alignment. Insert a neutral density filter (ND 1.0 or ND 2.0) to attenuate the beam so you get a moderate signal (~0.5 V at 30 dB).

Measure and compare to your predictions:

| Gain | Measured Signal (V) | Measured Noise (mV) | Measured SNR | Prediction Match? |
|------|--------------------|--------------------|--------------|-------------------|
| 0 dB  | _______ | _______ | _______ | _______ |
| 30 dB | _______ | _______ | _______ | _______ |
| 50 dB | _______ | _______ | _______ | _______ |
| 70 dB | _______ | _______ | _______ | _______ |

**Important:** If your predictions and measurements disagree, do NOT adjust your analysis to force agreement. Discrepancies are scientifically valuable—they reveal either a gap in your understanding or an uncontrolled variable in your experiment. Report your actual measurements honestly and investigate the cause of any disagreement.

**Analysis Questions:**

1. Does SNR improve with gain as predicted? Calculate the actual improvement factor from 0 dB to 30 dB.

2. Did any measurements saturate (signal > 4.5 V)? How does saturation affect your gain choice?

3. At which gain setting did you achieve the best SNR without saturating?

### Understanding Your Code (Required)

Whether you wrote the code yourself or with AI assistance, answer these questions in your notebook:

1. **Parameter justification:** Explain in 2-3 sentences why you chose your `sample_rate` and `num_samples`. What would happen if you used 100 Hz instead of 10000 Hz? What about only 10 samples?

2. **Verification test:** Describe a simple test to verify your function is working correctly. (Hint: compare DAQ measurements to oscilloscope, or test with a known DC voltage from the 5V rail.)

3. **Extension:** How would you modify this function to automatically measure noise at multiple gain settings? (You don't need to implement this—just describe the approach.)

### Debugging Exercise: Find the Bugs

The following code was generated by an AI assistant to measure noise, but it contains THREE bugs. Find and fix each one, then explain what was wrong.

```python
import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType

def measure_noise_buggy(channel="Dev1/ai0", num_samples=1000, sample_rate=10000):
    """Measure DC level and RMS noise. Contains 3 bugs!"""
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(channel)
        task.timing.cfg_samp_clk_timing(
            rate=sample_rate,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=num_samples
        )

        data = task.read(number_of_samples_per_channel=100)  # Bug #1

        dc_level = np.mean(data)
        noise_rms = np.mean((data - dc_level)**2)  # Bug #2

    return dc_level, noise_rms  # Bug #3
```

**Hints:**
- Bug #1 is a mismatch between what you asked for and what you read
- Bug #2 is a mathematical error in computing RMS
- Bug #3 is a subtle issue with units/interpretation

**In your notebook:**
1. Identify each bug and explain what's wrong
2. Write the corrected line of code for each
3. Explain how you would detect each bug if you didn't know it was there (what test would reveal the problem?)

This exercise tests your understanding of the code, not just your ability to run it. Being able to debug code—whether AI-generated or your own—is an essential skill.

## Part 4: Choosing Your Week 4 Gain Setting

In Week 4, you will measure beam profiles where signal varies from near-zero (beam blocked) to maximum (full beam). You need to choose a gain setting that works across this entire range.

### Your Signal Range

From your Week 1 measurements (without ND filter):

- Maximum signal (full beam): _______ V at 0 dB gain
- This corresponds to: _______ V at 30 dB, _______ V at 50 dB, _______ V at 70 dB

### The Constraints (Updated)

You face two competing constraints:

1. **Saturation limit:** Signal must stay below ~4.5 V
2. **SNR requirement:** Given ~5 mV noise floor (DAQ-limited), signal must be >> 5 mV for good SNR

**Optimal strategy:** Use the highest gain that doesn't saturate your maximum signal.

### Analysis

Answer these questions to determine your optimal gain:

1. **Saturation:** At which gain settings would your maximum signal saturate? (Show calculation.)

2. **SNR at minimum signal:** During a beam profile scan, the minimum signal occurs when the beam is nearly blocked. Estimate the smallest signal you need to measure (hint: think about the Gaussian tail at 2-3 beam widths from center). Given your ~5 mV DAQ noise floor, what is the SNR for this minimum signal at each gain?

3. **The optimization:** Based on your answers, what is the optimal gain setting? (Highest gain that doesn't saturate, giving best SNR at minimum signal.)

4. **Propagation to beam width:** This is the critical connection. Your beam width $w$ is extracted from fitting the error function to your profile data. If your voltage measurements have uncertainty $\sigma_V$ due to noise, this propagates to uncertainty $\sigma_w$ in beam width.

   For an error function fit, the uncertainty in the width parameter scales approximately as:

   $$\sigma_w \approx \frac{\sigma_V}{|dV/dx|_{\text{max}}}$$

   where $|dV/dx|_{\text{max}}$ is the maximum slope of your profile (at the beam center).

   *Note: This approximation captures the dominant effect of noise on fit precision. A rigorous treatment would use the full covariance matrix from the least-squares fit, which accounts for the number of data points and correlations between parameters. You learned about the covariance matrix earlier in this week's prelab (see "Uncertainty in the fit parameters" section), and you'll apply it to your real data in Week 3.*

   Using your Week 1 beam width measurement (~0.5 mm), your signal amplitude at your chosen gain, and your ~5 mV noise floor, estimate $\sigma_w$. Is this acceptable for your Week 4 measurements?

### Your Decision

**Selected gain setting for Week 4:** _______ dB

**Justification (2-3 sentences referencing your quantitative analysis):**

_______________________________________________

_______________________________________________

**Key numbers supporting your decision:**
- Maximum signal at this gain: _______ V (below 4.5 V saturation limit? ☐ Yes ☐ No)
- SNR at maximum signal: _______ (using 5 mV DAQ noise floor)
- Expected uncertainty in beam width: _______ mm

## Peer Comparison: Gain Setting Choices

Compare your gain setting decision with another group. This discussion builds scientific argumentation skills—in research, different groups often make different but equally valid experimental choices.

1. **Share your selected gain setting** and the key reasoning behind your choice.

2. **Compare approaches:** Did they weight the tradeoffs (saturation vs. SNR) differently? Did they consider factors you overlooked?

3. **Explore disagreements:** If you chose different settings, discuss whether both choices can be valid. What measurement conditions favor one choice over the other?

4. **Document briefly** in your notebook:
   - The other group's chosen gain setting: _______ dB
   - Their primary justification (1 sentence): _______________________
   - One insight from the discussion that changed or confirmed your thinking: _______________________

*In science, disagreements are productive when they are grounded in evidence. Your goal is not to determine who is "right" but to understand why reasonable approaches can differ.*

## Part 5: Week 4 Validation (To Complete in Week 4)

Before your first automated beam profile scan, validate your gain choice:

1. With the beam fully blocked, acquire 100 samples. Record the mean and RMS.

2. With the beam fully exposed, acquire 100 samples. Record the mean and RMS.

3. Calculate your actual SNR at maximum signal. Does it match your Week 2 prediction?

4. If your SNR is significantly different from predicted, identify why and decide whether to adjust your gain setting.

| Measurement | Week 2 Prediction | Week 4 Actual | Agreement? |
|-------------|------------------|---------------|------------|
| Noise floor RMS | _______ mV | _______ mV | _______ |
| Max signal | _______ V | _______ V | _______ |
| SNR at max | _______ | _______ | _______ |

**Reflection Question:** What did you learn from this predict-measure-compare cycle? Consider: Was your Week 2 characterization useful for Week 4? Did understanding that DAQ noise dominates help you make better decisions?

_______________________________________________

_______________________________________________

This validation step closes the loop on your experimental decision-making process.

## Looking Ahead: Connecting Noise to Uncertainty

The noise measurements you made today will directly inform your Week 4 analysis. Here's how the pieces connect:

1. **Week 2 (today):** You characterized the DAQ noise floor (~5 mV) that limits your measurements
2. **Week 3 (next week):** You'll learn error propagation—how uncertainties in measurements become uncertainties in derived quantities
3. **Week 4:** The DAQ noise floor you measured here determines the uncertainty in each beam profile point, which propagates through your curve fit to give uncertainty in beam width $w$ and waist position $z_w$

Keep your noise characterization data accessible—you'll need it when propagating uncertainties in Week 3's prelab exercises.

## Optional Extension: Oscilloscope Comparison

The oscilloscope has a much lower noise floor than the DAQ (~100-500 µV vs ~5 mV). This makes it useful for revealing details that the DAQ cannot see.

**If time permits:** Repeat the photodetector noise measurements from Part 2 using the oscilloscope instead of the DAQ.

1. Can you now see the photodetector noise increase with gain (as predicted by the datasheet)?
2. At what gain setting does photodetector noise become visible above the oscilloscope noise floor?
3. Why can't you use the oscilloscope for automated Week 4 measurements? (Hint: think about what automation requires.)

This comparison validates your understanding of the measurement chain: different instruments reveal different noise sources.

## Noise Characterization Troubleshooting

**DAQ noise much higher than expected (~5 mV):**

- Check for proper grounding—is the DAQ input truly shorted?
- Try a different USB port (some have more electrical noise)
- Verify no other signals are connected to the DAQ

**Noise doesn't change with gain (expected):**

- This confirms DAQ noise dominates—your characterization is correct!
- The photodetector noise is below the DAQ noise floor

**Noise changes slightly with gain:**

- At high gain (70 dB), photodetector noise (1.1 mV) approaches DAQ noise (5 mV)
- You may see a small increase in measured noise at 70 dB

**SNR doesn't improve as much as predicted:**

- Check that signal isn't saturating at high gain
- Verify no ND filter or obstruction is reducing your signal
- Account for any changes in laser alignment from Week 1

**Predictions don't match measurements:**

- Re-check your calculations—are you using the correct gain factors?
- Verify your noise floor measurement (Part 1) is accurate
- Account for any systematic offsets in your DAQ readings

# Saving Data and Additional DAQ Features

## Saving Data to a File

Save your acquired data to a CSV file for later analysis:

```python
import numpy as np
from datetime import datetime

# After acquiring data...
# Create a timestamp for the filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data_{timestamp}.csv"

# Create time array
time = np.arange(len(data)) / sample_rate

# Save to CSV
np.savetxt(
    filename,
    np.column_stack([time, data]),
    delimiter=',',
    header='Time (s), Voltage (V)',
    comments=''
)

print(f"Data saved to {filename}")
```

### Exercise: Save and Reload Data

1. Acquire a waveform and save it to a CSV file.
2. Load the data back and plot it:

   ```python
   # Load data
   loaded_data = np.loadtxt(filename, delimiter=',', skiprows=1)
   time_loaded = loaded_data[:, 0]
   voltage_loaded = loaded_data[:, 1]

   # Plot
   plt.figure(figsize=(10, 6))
   plt.plot(time_loaded * 1000, voltage_loaded)
   plt.xlabel('Time (ms)')
   plt.ylabel('Voltage (V)')
   plt.title('Loaded Data')
   plt.show()
   ```

3. Verify the loaded data matches your original acquisition.

## Generating an Analog Output

The USB-6009 can also generate analog voltages (though at a limited rate of 150 S/s). Note that the USB-6009's analog outputs have a range of 0-5V only, so we must specify this range explicitly:

```python
import nidaqmx

# Output a DC voltage
with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=0.0, max_val=5.0)
    task.write(2.5, auto_start=True)  # Output 2.5 V
    print("Outputting 2.5 V on AO0")
    input("Press Enter to stop...")
```

### Exercise: Test Analog Output

1. Configure your DAQ to output a voltage on `AO0`.
2. Connect `AO0` to `AI0` (loopback test).
3. Write a script that:
   - Outputs a voltage on `AO0`
   - Reads the voltage on `AI0`
   - Verifies they match

## Error Handling

Always include error handling in your data acquisition code:

```python
import nidaqmx
from nidaqmx.errors import DaqError

try:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        voltage = task.read()
        print(f"Voltage: {voltage:.4f} V")

except DaqError as e:
    print(f"DAQ Error: {e}")
    print("Check that:")
    print("  - The DAQ device is connected")
    print("  - The device name is correct (try 'Dev1', 'Dev2', etc.)")
    print("  - NI-DAQmx drivers are installed")
```

# Summary

In this lab, you learned to:

1. Connect and verify a USB DAQ device
2. Read single and multiple voltage samples
3. Configure sample rate and acquisition timing
4. Explain Nyquist's theorem and recognize aliasing
5. Choose appropriate sample rates for your signals
6. Characterize the DAQ noise floor and understand its role in your measurement chain
7. Identify which component (photodetector or DAQ) dominates system noise
8. Calculate and measure signal-to-noise ratio with a fixed noise floor
9. Make a quantitative decision about optimal gain for Week 4 measurements
10. Save data to CSV files
11. Generate analog output voltages
12. Handle common errors

**Key takeaway:** You discovered that the DAQ noise floor (~5 mV) limits your measurements, not the photodetector noise. This authentic discovery—that instrument limitations differ from datasheet specs in important ways—is central to experimental physics. Your gain setting decision, informed by this understanding, will directly impact the quality of your Week 4 beam profile data.

See the [Python Resources](/PHYS-4430/python-resources) page and the example scripts in the `python/` folder for more detailed examples.

# Deliverables and Assessment

Your lab notebook should include the following for this week:

## Prelab (complete before lab)

1. **Least-squares fitting exercises**: contour plot of $\chi^2$, graphical minimization results
2. **Residuals analysis**: plot of residuals, answers to goodness-of-fit questions
3. **Weighted fit**: results using data with uncertainties, $\chi^2$ test calculation
4. **Error bars plot**: reproduction of the example plot with error bars

## In-Lab Documentation

1. **DAQ verification**: screenshot or plot showing successful voltage reading
2. **Waveform capture**: comparison of Python plot vs. oscilloscope display
3. **Aliasing exercises**: completed prediction-observation-explanation for all frequency cases
4. **Noise characterization tables** (Parts 1-4):
   - DAQ noise floor measurement (input shorted) with prediction comparison
   - Signal chain characterization (photodetector connected, capped) at each gain
   - Identification of dominant noise source at each gain setting
   - SNR predictions AND measurements using fixed DAQ noise floor
5. **Gain setting decision**: your selected gain with written justification referencing your quantitative data
6. **Peer comparison**: other group's gain setting, their justification, and insight from discussion

## Key Data Tables

Make sure these tables are completed in your notebook:

**Part 1: DAQ Noise Floor**

| Measurement | Predicted | Measured | Ratio |
|-------------|-----------|----------|-------|
| DAQ noise (shorted) | ~5 mV | _______ mV | _______ |

**Part 2: Signal Chain Characterization**

| Gain | Measured Noise | DAQ Noise | Datasheet PD Noise | Dominant Source |
|------|---------------|-----------|-------------------|-----------------|
| 0 dB  | _______ mV | _______ mV | 0.3 mV | _______ |
| 30 dB | _______ mV | _______ mV | 0.5 mV | _______ |
| 50 dB | _______ mV | _______ mV | 0.7 mV | _______ |
| 70 dB | _______ mV | _______ mV | 1.1 mV | _______ |

**Part 3: SNR Optimization**

| Gain | Predicted SNR | Measured SNR | Agreement? |
|------|---------------|--------------|------------|
| ... | ... | ... | ... |

## Code Deliverables

1. Working `measure_noise()` function with your chosen parameters
2. Python script for waveform acquisition and plotting

## Reflection Questions

1. You predicted that DAQ noise would dominate at all gain settings. Did your measurements confirm this? If measured noise changed with gain, explain what this tells you about the noise sources in your system.

2. Given that the DAQ noise floor is fixed at ~5 mV, explain in 2-3 sentences why using higher gain improves SNR. What limits how high you can set the gain?

3. How would your gain selection strategy change if you had a DAQ with 10× lower noise floor (0.5 mV)? Would photodetector noise become important?
