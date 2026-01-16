# Week 1 Thursday Lecture: Error Propagation and Fitting

**Date:** January 15, 2026
**Duration:** 50 minutes
**Purpose:** Prepare students for Week 2 prelab (curve fitting, χ² minimization, error function model for beam profiles)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Apply error propagation rules to calculate uncertainty in derived quantities
2. Use partial derivatives to propagate uncertainty through arbitrary functions
3. Explain why least-squares fitting minimizes χ² (chi-square)
4. Perform a linear least-squares fit (y = A + Bx) and interpret the results
5. Calculate and interpret reduced χ² as a goodness-of-fit measure
6. Connect the Gaussian distribution to measurement uncertainty

---

## Lecture Outline

### 1. Introduction: From Measurements to Results (3 min)

#### 1.1 The Problem

On Tuesday, you learned to quantify uncertainty in individual measurements.

**But:** Experimental results often involve calculations:
- Beam width from fit parameters
- Gain ratio from two voltage measurements
- Power from voltage and responsivity

**Question:** If your inputs have uncertainty, what's the uncertainty in your output?

#### 1.2 Today's Goals

1. **Error propagation:** How uncertainty flows through calculations
2. **Least-squares fitting:** Finding the "best" parameters for a model
3. **χ² and goodness-of-fit:** Is the model actually good?

These tools will be essential for the Week 2 prelab and all subsequent work.

---

### 2. Error Propagation Basics (12 min)

#### 2.1 The Conceptual Idea

**Key insight:** Uncertainty "flows" through calculations.

If you're calculating $z = f(x)$ and $x$ has uncertainty $\sigma_x$:
- How much does $z$ change when $x$ changes by $\sigma_x$?
- That change is approximately $\frac{dz}{dx} \times \sigma_x$

*[Draw on board: function f(x) with a small range Δx, showing corresponding range Δz]*

**The derivative tells you sensitivity:**
- Large $\frac{dz}{dx}$ → small changes in $x$ cause big changes in $z$ → $x$'s uncertainty matters a lot
- Small $\frac{dz}{dx}$ → $x$'s uncertainty doesn't affect $z$ much

For multiple inputs, each contributes independently, so we add in quadrature (just like combining random errors on Tuesday).

#### 2.2 The General Formula

For a quantity $z = f(x, y, ...)$ calculated from measured values $x, y, ...$:

$$\boxed{\sigma_z = \sqrt{\left(\frac{\partial f}{\partial x}\right)^2 \sigma_x^2 + \left(\frac{\partial f}{\partial y}\right)^2 \sigma_y^2 + \cdots}}$$

**Physical meaning:** Each input contributes to output uncertainty, weighted by how sensitive the output is to that input (the partial derivative).

#### 2.3 Common Cases

| Operation | Formula | Uncertainty |
|-----------|---------|-------------|
| Addition/subtraction | $z = x + y$ or $z = x - y$ | $\sigma_z = \sqrt{\sigma_x^2 + \sigma_y^2}$ |
| Multiplication | $z = xy$ | $\frac{\sigma_z}{z} = \sqrt{\left(\frac{\sigma_x}{x}\right)^2 + \left(\frac{\sigma_y}{y}\right)^2}$ |
| Division | $z = x/y$ | $\frac{\sigma_z}{z} = \sqrt{\left(\frac{\sigma_x}{x}\right)^2 + \left(\frac{\sigma_y}{y}\right)^2}$ |
| Power | $z = x^n$ | $\frac{\sigma_z}{z} = n\frac{\sigma_x}{x}$ |

**Pattern for multiplication/division:** Fractional uncertainties add in quadrature.

#### 2.4 Example 1: Addition

You measure two distances:
- $d_1 = (10.0 \pm 0.3)$ cm
- $d_2 = (15.0 \pm 0.4)$ cm

**Total distance:** $d_{total} = d_1 + d_2 = 25.0$ cm

**Uncertainty:**
$$\sigma_{total} = \sqrt{0.3^2 + 0.4^2} = \sqrt{0.09 + 0.16} = 0.5 \text{ cm}$$

**Result:** $d_{total} = (25.0 \pm 0.5)$ cm

#### 2.5 Example 2: Division (Gain Ratio)

From Lab 1, you measured voltages at two gain settings:
- $V_{30dB} = (1.50 \pm 0.02)$ V
- $V_{0dB} = (0.047 \pm 0.002)$ V

**Gain ratio:** $G = V_{30dB} / V_{0dB} = 31.9$

**Fractional uncertainties:**
- $\sigma_V/V_{30dB} = 0.02/1.50 = 0.0133$
- $\sigma_V/V_{0dB} = 0.002/0.047 = 0.0426$

**Combined:**
$$\frac{\sigma_G}{G} = \sqrt{0.0133^2 + 0.0426^2} = 0.0446$$
$$\sigma_G = 0.0446 \times 31.9 = 1.4$$

**Result:** $G = 32 \pm 1$

**Note:** The less precise measurement (0 dB) dominates the uncertainty.

#### 2.6 Example 3: General Function

The beam width formula involves: $w = w_0\sqrt{1 + (z/z_R)^2}$

To find $\sigma_w$, you'd compute $\partial w/\partial w_0$, $\partial w/\partial z$, and $\partial w/\partial z_R$, then combine.

**In practice:** Use the `uncertainties` Python package (Week 3 lecture) to do this automatically.

#### 2.7 Practice Problem (2 min)

**You measure:**
- Power: $P = (5.0 \pm 0.2)$ mW
- Beam area: $A = (0.50 \pm 0.05)$ mm²

**Calculate:** Intensity $I = P/A$ with uncertainty.

*[Give students 90 seconds to work, then reveal]*

**Answer:**
- $I = 5.0/0.50 = 10$ mW/mm²
- $\sigma_I/I = \sqrt{(0.2/5.0)^2 + (0.05/0.50)^2} = \sqrt{0.0016 + 0.01} = 0.108$
- $\sigma_I = 1.1$ mW/mm²
- **Result:** $I = (10 \pm 1)$ mW/mm²

---

### 3. The Gaussian Distribution (8 min)

#### 3.1 Why Gaussian?

Random errors often follow a **Gaussian (normal) distribution**:

$$P(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

*[Draw bell curve on board]*

**Why?**
- Central Limit Theorem: sum of many small random effects → Gaussian
- Many noise sources add together
- Well-studied mathematically

#### 3.2 Key Properties

| Probability | Range |
|-------------|-------|
| 68.3% | $\mu \pm 1\sigma$ |
| 95.4% | $\mu \pm 2\sigma$ |
| 99.7% | $\mu \pm 3\sigma$ |

**Interpretation:**
- 1σ uncertainty means ~68% confidence
- 2σ means ~95% confidence
- 3σ deviation is rare (<0.3%) — something unusual is happening

#### 3.3 Connecting to Your Data

If your measurements follow a Gaussian distribution:
- The mean $\bar{x}$ estimates the true value $\mu$
- The standard deviation estimates the width σ
- The SDOM estimates uncertainty in $\bar{x}$

**When someone says "the result is 2σ from the prediction," they mean:**
- The discrepancy is twice the combined uncertainty
- About 5% chance this occurs randomly
- Worth investigating, but could be statistical fluctuation

---

### 4. Least-Squares Fitting: The Concept (10 min)

#### 4.1 The Fitting Problem

**Situation:** You have data points $(x_i, y_i)$ and a model $f(x; a, b, ...)$

**Goal:** Find parameter values that make the model "best fit" the data.

**Question:** What does "best fit" mean?

#### 4.2 Activity: Which Fit is Best? (3 min)

*[Display on screen: scatter plot with ~8 data points and error bars, plus three candidate fit lines A, B, C]*

**Prepare in advance:**
```
Create a plot showing:
- X-axis: "Position (mm)", Y-axis: "Voltage (V)"
- 8 data points with error bars (~0.1 V each)
- Line A: Goes through most points but misses one by 3 error bars
- Line B: Systematically above the data on the left, below on the right
- Line C: Balanced — some points above, some below, all within ~2 error bars
```

**Instructions:** "Rank these three fits from best to worst. Discuss with your neighbor for 90 seconds."

*[After discussion, ask for volunteers and their reasoning]*

**Common student responses:**
- "C is best because it goes through the error bars"
- "B is worst because it has a pattern — all the points on the left are below"
- "A looks good except for that one outlier"

**Key insight:** Your intuition already uses something like χ². You're:
- Looking at how far points are from the line (residuals)
- Comparing that distance to the error bars (weighting by uncertainty)
- Checking for patterns (systematic vs. random deviations)

Let's formalize this intuition.

#### 4.3 The χ² (Chi-Square) Statistic

Define:
$$\chi^2 = \sum_{i=1}^{N} \frac{(y_i - f(x_i))^2}{\sigma_i^2}$$

| Term | Meaning |
|------|---------|
| $y_i$ | Measured value |
| $f(x_i)$ | Model prediction |
| $\sigma_i$ | Uncertainty in $y_i$ |
| $y_i - f(x_i)$ | Residual (data minus model) |

**Physical meaning:** Sum of squared deviations, weighted by uncertainty.

#### 4.4 Why Minimize χ²?

**Least-squares principle:** The best fit minimizes χ².

**Why this makes sense:**
1. Large residuals are penalized (squared)
2. Points with larger uncertainty contribute less (divided by σ²)
3. If model is correct, $\chi^2 \approx N$ (one "σ" per point on average)

*[Draw on board: data points, fit line, show residuals]*

#### 4.5 Linear Least-Squares: y = A + Bx

For a straight line, the best-fit parameters have closed-form solutions:

$$B = \frac{\sum w_i (x_i - \bar{x})(y_i - \bar{y})}{\sum w_i (x_i - \bar{x})^2}$$

$$A = \bar{y} - B\bar{x}$$

where $w_i = 1/\sigma_i^2$ and bars indicate weighted averages.

**The formulas are messy—use Python!** But the concept is: find A, B that minimize χ².

#### 4.6 Uncertainties in Fit Parameters

The fitting process also gives uncertainties σ_A and σ_B.

**These tell you:**
- How well-determined each parameter is
- How changing one parameter affects χ²
- Whether parameters are correlated

---

### 5. Goodness of Fit: Reduced χ² (7 min)

#### 5.1 How Do I Know if the Fit is Good?

A small χ² is better, but how small is "good"?

**Degrees of freedom (DOF):** Number of data points minus number of fit parameters.

For $N$ data points and $p$ parameters: $DOF = N - p$

#### 5.2 Reduced Chi-Square

$$\chi^2_{red} = \frac{\chi^2}{DOF}$$

| $\chi^2_{red}$ | Interpretation |
|----------------|----------------|
| $\approx 1$ | Good fit — model matches data within uncertainties |
| $\ll 1$ | Uncertainties overestimated (or got lucky) |
| $\gg 1$ | **Bad fit** — model doesn't describe data, or uncertainties underestimated |

#### 5.3 Example Interpretation

**Scenario:** You fit 20 data points with a 2-parameter model. DOF = 18.

| $\chi^2$ | $\chi^2_{red}$ | Assessment |
|----------|----------------|------------|
| 15 | 0.83 | Good fit |
| 18 | 1.0 | Excellent fit |
| 36 | 2.0 | Marginal — investigate |
| 90 | 5.0 | Bad fit — something wrong |

#### 5.4 What to Do When $\chi^2_{red} \gg 1$

**Possible causes:**
1. Wrong model (linear fit to curved data)
2. Systematic errors in data
3. Uncertainties underestimated
4. Outliers pulling the fit

**Actions:**
1. Plot residuals — look for patterns
2. Check uncertainty estimates
3. Try a different model
4. Identify outliers

#### 5.5 Think-Pair-Share: Interpret This Fit (2 min)

*[Display a plot showing: data points with error bars, fit line, and χ²_red = 4.5]*

**Questions for discussion:**
1. Is this a good fit?
2. What might be wrong?
3. What would you check?

*[After discussion, reveal]*

**Answer:** $\chi^2_{red} = 4.5$ is too large. Possible issues:
- Model may be inappropriate (look for curvature in residuals)
- Error bars may be too small
- Systematic effect not accounted for

---

### 6. Residual Analysis (5 min)

#### 6.1 What Are Residuals?

$$r_i = y_i - f(x_i)$$

Residuals show what's "left over" after the fit.

#### 6.2 What Residuals Tell You

*[Draw examples on board]*

| Residual Pattern | Meaning |
|------------------|---------|
| Random scatter around zero | Good fit |
| Systematic trend (slope) | Model missing a term |
| Curvature | Wrong functional form |
| Outlier cluster | Data problem in that region |

#### 6.3 Always Plot Residuals!

**Good practice:** After any fit, plot residuals vs. x.

A good-looking fit line can hide systematic problems that residual plots reveal.

---

### 7. Preview: Fitting Your Beam Data (4 min)

#### 7.1 The Error Function Model

From the prelab, your knife-edge data follows:

$$P(x) = \frac{P_0}{2} \left[1 - \text{erf}\left(\frac{\sqrt{2}(x - x_0)}{w}\right)\right]$$

**Fit parameters:**
- $P_0$: total power (saturation level)
- $x_0$: beam center position
- $w$: beam width (what you want!)

#### 7.2 The Fitting Process

1. Collect $(x_i, P_i)$ data from knife-edge scan
2. Fit to error function model using least-squares
3. Extract $w$ and $\sigma_w$ from fit
4. Check $\chi^2_{red}$ — is the model appropriate?
5. Plot residuals — any systematic patterns?

#### 7.3 What the Week 2 Prelab Asks

You'll practice:
- Setting up a fit graphically (to understand χ² minimization)
- Interpreting fit results
- Creating error bar plots
- Calculating p-values from χ²

**The prelab walks you through this step by step.**

---

### 8. Summary (2 min)

#### Key Takeaways

1. **Error propagation:** Use partial derivatives to calculate output uncertainty
   - Addition: add uncertainties in quadrature
   - Multiplication/division: add fractional uncertainties in quadrature

2. **Gaussian distribution:** Random errors typically follow this shape
   - 68% within 1σ, 95% within 2σ, 99.7% within 3σ

3. **Least-squares fitting:** Minimize χ² to find best parameters
   $$\chi^2 = \sum \frac{(y_i - f(x_i))^2}{\sigma_i^2}$$

4. **Reduced χ²:** $\chi^2_{red} \approx 1$ indicates good fit
   - Much larger than 1 → problem with model or uncertainties

5. **Residual plots:** Essential for detecting systematic issues

#### For the Week 2 Prelab

You'll apply these concepts to:
- Graphical χ² minimization
- Interpreting fit parameters and uncertainties
- Creating publication-quality plots with error bars

---

## Suggested Board Work

1. Error propagation formula (boxed)
2. Addition/multiplication propagation rules
3. Gain ratio calculation example
4. Gaussian distribution sketch with 1σ, 2σ, 3σ regions
5. χ² formula and definition diagram (data, fit, residuals)
6. Residual patterns (random vs. systematic)

---

## Key Formulas Reference

| Quantity | Formula |
|----------|---------|
| Error propagation | $\sigma_z = \sqrt{\sum \left(\frac{\partial f}{\partial x_i}\right)^2 \sigma_{x_i}^2}$ |
| Addition | $\sigma_{x+y} = \sqrt{\sigma_x^2 + \sigma_y^2}$ |
| Multiplication | $\sigma_{xy}/xy = \sqrt{(\sigma_x/x)^2 + (\sigma_y/y)^2}$ |
| Chi-square | $\chi^2 = \sum \frac{(y_i - f(x_i))^2}{\sigma_i^2}$ |
| Reduced χ² | $\chi^2_{red} = \chi^2 / (N - p)$ |
| Gaussian | $P(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/2\sigma^2}$ |

---

## Common Student Questions

**Q: When do I need to use error propagation?**
A: Whenever you calculate a result from measured quantities that have uncertainty. If your inputs have error bars, your output needs error bars.

**Q: What if my measurements don't have the same uncertainty?**
A: Use weighted fitting (weights = 1/σ²). Points with smaller uncertainty contribute more to the fit.

**Q: Is χ²_red = 0.5 a problem?**
A: It suggests uncertainties are overestimated (or you got lucky). Not as serious as χ²_red >> 1, but worth noting.

**Q: How do I know what model to use?**
A: Physics dictates the model! For beam profiles, theory predicts the error function. The fitting determines the parameters, not the functional form.

**Q: What if different fit parameters have very different uncertainties?**
A: That's normal. Some parameters are well-constrained by the data; others are not. The covariance matrix captures this.

**Q: Can I do error propagation by hand for complex functions?**
A: For simple cases, yes. For complex formulas, use the `uncertainties` package in Python (covered Week 3).

---

## Connections to Lab Work

| Lecture Topic | Week 2 Prelab/Lab Application |
|---------------|-------------------------------|
| Error propagation | Calculating gain ratio uncertainties |
| χ² minimization | Fitting beam profile data |
| Reduced χ² | Assessing fit quality |
| Residual analysis | Detecting systematic errors in beam data |
| Gaussian distribution | Understanding noise statistics |

---

## Optional: The Photoelectric Effect Example

*[If time permits — connects to historical physics]*

Einstein's photoelectric equation: $E_{max} = hf - \phi$

**Data:** Maximum electron energy vs. light frequency

| f (10¹⁴ Hz) | E_max (eV) |
|-------------|------------|
| 5.5 | 0.35 |
| 6.5 | 0.78 |
| 7.5 | 1.17 |
| 8.5 | 1.59 |

**Linear fit:** $E = hf - \phi$ → slope = h, intercept = -φ

**Result:** Slope gives Planck's constant h!

This is how Millikan measured h in 1916 — and how fitting extracts physics from data.
