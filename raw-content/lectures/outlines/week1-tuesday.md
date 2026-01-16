# Week 1 Tuesday Lecture: Error Analysis Fundamentals

**Date:** January 13, 2026
**Duration:** 50 minutes
**Purpose:** Establish statistical foundations for Lab 1 (photodetector calibration, uncertainty characterization)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Present experimental results in standard format: value ± uncertainty (units)
2. Apply significant figure rules for reporting measurements and uncertainties
3. Distinguish between blunders, systematic errors, and random (statistical) errors
4. Calculate mean, standard deviation, and standard deviation of the mean (SDOM)
5. Combine measurements using weighted averages
6. Apply Chauvenet's criterion to identify outliers
7. Explain the difference between accuracy and precision

---

## Lecture Outline

### 1. Introduction: Why Error Analysis? (5 min)

#### 1.1 Opening Question

*[Display measurement on screen: "The beam width is 0.523847291 mm"]*

**Ask students:** "What's wrong with this result?"

*[Pause for responses]*

**Problems:**
- Too many significant figures (implies impossible precision)
- No uncertainty (how good is this number?)
- No context (how was it measured?)

#### 1.2 The Goal of Error Analysis

**Every experimental result has uncertainty.** Our job is to:
1. Quantify the uncertainty
2. Understand its sources
3. Communicate results honestly

**A measurement without uncertainty is not a measurement—it's a guess.**

#### 1.3 Connection to This Afternoon

Today you'll calibrate a photodetector:
- Measure voltage at different gain settings
- Observe fluctuations in repeated readings
- Calculate statistical quantities

This lecture gives you the tools to interpret what you see.

---

### 2. Presenting Results: The Standard Format (8 min)

#### 2.1 The Basic Format

$$\text{result} = (\text{value} \pm \text{uncertainty}) \text{ units}$$

**Examples:**
- Beam width: $w = (0.52 \pm 0.03)$ mm
- Voltage: $V = (1.847 \pm 0.012)$ V
- Time: $t = (45.3 \pm 0.8)$ s

**Note:** Parentheses indicate the uncertainty applies to the value; units go outside.

#### 2.2 Significant Figures for Uncertainty

**Rule of thumb:** Express uncertainty to 1-2 significant figures.

| Calculated Uncertainty | Report As |
|-----------------------|-----------|
| 0.0234 | 0.02 or 0.023 |
| 0.567 | 0.6 or 0.57 |
| 12.8 | 13 or 12.8 |

**Then:** Round the value to match the uncertainty's decimal place.

#### 2.3 Example Practice

**Calculated result:** 3.14159265 ± 0.08743

*[Ask students how to report this]*

**Step 1:** Round uncertainty → 0.09 (or 0.087)
**Step 2:** Match value → 3.14 (or 3.141)
**Final:** $(3.14 \pm 0.09)$ or $(3.141 \pm 0.087)$

**Not acceptable:** 3.14159265 ± 0.09 (value has false precision)

---

### 3. Types of Errors (12 min)

#### 3.1 Three Categories

| Type | Definition | Example | Can We Eliminate It? |
|------|------------|---------|---------------------|
| **Blunders** | Mistakes | Misreading meter, wrong units | Yes — be careful! |
| **Systematic** | Consistent bias | Miscalibrated instrument, alignment error | Yes — identify and correct |
| **Random (Statistical)** | Unpredictable variation | Electrical noise, vibrations | No — but we can quantify it |

#### 3.2 Blunders

**What they are:** Human errors, equipment failures, procedural mistakes.

**Examples:**
- Recording "1.5 V" when meter shows "1.5 mV"
- Using wrong channel on DAQ
- Forgetting to subtract dark offset

**How to handle:** Double-check everything. If you catch a blunder, discard that data point and repeat.

**Blunders are not errors—they're mistakes.** Don't include them in uncertainty analysis.

#### 3.3 Systematic Errors

**What they are:** Consistent biases that shift all measurements in the same direction.

**Examples in today's lab:**
- Photodetector offset voltage (non-zero reading with no light)
- Gain ratio different from datasheet specification
- Stray light reaching detector

**Key property:** Taking more data doesn't help! The bias remains.

**How to handle:**
1. Identify potential sources
2. Measure and correct for them
3. Or estimate their contribution to uncertainty

#### 3.4 Random Errors

**What they are:** Unpredictable fluctuations that vary from measurement to measurement.

**Examples:**
- Electronic noise in detector circuit
- Mechanical vibrations
- Air currents affecting laser pointing

**Key property:** Taking more data *does* help — random errors average out.

**How to handle:** Take multiple measurements, use statistics.

#### 3.5 Think-Pair-Share: Classify These Errors (2 min)

*[Display list on screen]*

**Classify each as blunder, systematic, or random:**

1. You forgot to turn on the laser amplifier
2. The voltmeter reads 0.02 V with no input connected
3. Repeated voltage readings fluctuate by ± 5 mV
4. You wrote "3.5" but the display showed "5.3"
5. All your beam widths are 10% larger than expected

*[Give students 90 seconds to discuss with neighbor, then go through answers]*

**Answers:**
1. Blunder (procedural mistake)
2. Systematic (offset error — affects all readings)
3. Random (noise — varies unpredictably)
4. Blunder (transcription error)
5. Systematic (consistent bias — investigate cause)

---

### 4. Statistics of Repeated Measurements (12 min)

#### 4.1 Why Repeat Measurements?

If measurements have random uncertainty, repeating helps us:
1. Estimate the "true" value (using the mean)
2. Quantify the scatter (using standard deviation)
3. Determine how well we know the mean (using SDOM)

#### 4.2 The Mean (Average)

$$\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i$$

**Physical meaning:** Best estimate of the "true" value from N measurements.

**Example:** Five voltage readings: 1.52, 1.48, 1.51, 1.49, 1.50 V

$$\bar{V} = \frac{1.52 + 1.48 + 1.51 + 1.49 + 1.50}{5} = 1.50 \text{ V}$$

#### 4.3 Standard Deviation

$$\sigma = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N} (x_i - \bar{x})^2}$$

**Physical meaning:** Typical spread of individual measurements around the mean.

**Interpretation:** About 68% of measurements fall within $\bar{x} \pm \sigma$.

**For the example:**

| $x_i$ | $x_i - \bar{x}$ | $(x_i - \bar{x})^2$ |
|-------|-----------------|---------------------|
| 1.52 | +0.02 | 0.0004 |
| 1.48 | -0.02 | 0.0004 |
| 1.51 | +0.01 | 0.0001 |
| 1.49 | -0.01 | 0.0001 |
| 1.50 | 0.00 | 0.0000 |

$$\sigma = \sqrt{\frac{0.0010}{4}} = 0.016 \text{ V}$$

#### 4.4 Standard Deviation of the Mean (SDOM)

$$\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{N}}$$

**Physical meaning:** Uncertainty in the mean itself (not in individual measurements).

**Key insight:** The more measurements you take, the better you know the mean.

**For the example:**
$$\sigma_{\bar{V}} = \frac{0.016}{\sqrt{5}} = 0.007 \text{ V}$$

**Report:** $V = (1.500 \pm 0.007)$ V

#### 4.5 When to Use σ vs. SDOM

| Use σ when... | Use SDOM when... |
|---------------|------------------|
| Describing scatter of data | Reporting uncertainty in the mean |
| Predicting range of next measurement | Comparing to a theoretical prediction |
| Characterizing noise | Final result of an experiment |

**Common mistake:** Reporting σ as the uncertainty in your result. Usually you want SDOM!

#### 4.6 Guided Practice: Calculate It Yourself (4 min)

*[Display on screen: Five voltage readings: 2.34, 2.41, 2.37, 2.39, 2.38 V]*

**Work through these steps with a neighbor:**

| Step | Task | Time |
|------|------|------|
| 1 | Calculate the mean | 30 sec |
| 2 | **Predict:** Will σ be closer to 0.01 V, 0.03 V, or 0.1 V? | 15 sec |
| 3 | Calculate σ (use the table method) | 90 sec |
| 4 | Calculate SDOM | 30 sec |
| 5 | Write the result in standard format | 15 sec |

*[Circulate during calculation to assist pairs who are stuck]*

**Work through on board after ~3 minutes:**

1. Mean: $\bar{V} = (2.34 + 2.41 + 2.37 + 2.39 + 2.38)/5 = 2.378$ V

2. Prediction check: The values span about 0.07 V, so σ should be smaller than that — 0.03 V is reasonable.

3. Standard deviation:

| $V_i$ | $V_i - \bar{V}$ | $(V_i - \bar{V})^2$ |
|-------|-----------------|---------------------|
| 2.34 | -0.038 | 0.00144 |
| 2.41 | +0.032 | 0.00102 |
| 2.37 | -0.008 | 0.00006 |
| 2.39 | +0.012 | 0.00014 |
| 2.38 | +0.002 | 0.00000 |

$$\sigma = \sqrt{\frac{0.00266}{4}} = 0.026 \text{ V}$$

4. SDOM: $\sigma_{\bar{V}} = 0.026/\sqrt{5} = 0.012$ V

5. **Final result:** $V = (2.38 \pm 0.01)$ V

**Reflection:** Was your prediction for σ close? If not, what threw you off?

#### 4.7 Scaling Check (1 min)

**Quick question:** If you took 20 measurements instead of 5 (with the same σ), how would SDOM change?

*[Pause for responses]*

**Answer:** SDOM = 0.026/√20 = 0.006 V — cut roughly in half!

To halve your uncertainty, you need to quadruple your measurements.

---

### 5. Weighted Averages (5 min)

#### 5.1 When Measurements Have Different Uncertainties

Sometimes you combine measurements with different precision:
- Same quantity measured with different instruments
- Different experimental conditions

**The question:** How do you average them?

#### 5.2 The Formula

$$\bar{x}_w = \frac{\sum_i w_i x_i}{\sum_i w_i}$$

where the weights are:

$$w_i = \frac{1}{\sigma_i^2}$$

**Physical meaning:** More precise measurements (smaller σ) contribute more to the average.

#### 5.3 Example

Two measurements of beam width:
- Method A: $w = 0.50 \pm 0.05$ mm
- Method B: $w = 0.45 \pm 0.02$ mm

**Calculate weights:**
- $w_A = 1/(0.05)^2 = 400$
- $w_B = 1/(0.02)^2 = 2500$

**Weighted average:**
$$\bar{w} = \frac{400 \times 0.50 + 2500 \times 0.45}{400 + 2500} = \frac{1325}{2900} = 0.457 \text{ mm}$$

**Uncertainty in weighted average:**
$$\sigma_w = \frac{1}{\sqrt{\sum_i w_i}} = \frac{1}{\sqrt{2900}} = 0.019 \text{ mm}$$

**Final result:** $w = (0.46 \pm 0.02)$ mm

**Note:** The more precise measurement (B) dominates, which makes physical sense.

---

### 6. Chauvenet's Criterion for Outliers (4 min)

#### 6.1 When to Suspect an Outlier

Sometimes one measurement looks suspicious — far from the others.

**Danger:** You can't just throw out data you don't like!

**Chauvenet's criterion** provides an objective test.

#### 6.2 The Test

1. Calculate mean and standard deviation (including the suspect point)
2. Calculate how many σ the suspect point is from the mean: $|x_{suspect} - \bar{x}|/\sigma$
3. Look up the probability of this deviation occurring by chance
4. If expected occurrences < 0.5, the point may be rejected

**In practice:** For N ≈ 10-20, points beyond ~2σ may be outliers; for larger N, the threshold increases.

| N | Rejection threshold |
|---|---------------------|
| 4 | 1.54σ |
| 10 | 1.96σ |
| 25 | 2.33σ |
| 50 | 2.57σ |

#### 6.3 Important Caution

**Chauvenet's criterion should be used sparingly.** Before rejecting data:
1. Look for a physical cause (equipment glitch, blunder)
2. Never reject more than one or two points
3. Document what you rejected and why

**If many points fail the test, your uncertainty estimate is probably wrong.**

---

### 7. Accuracy vs. Precision (3 min)

#### 7.1 Definitions

*[Draw target analogy on board]*

| Term | Meaning | Visualization |
|------|---------|---------------|
| **Precision** | Reproducibility — small scatter | Tight grouping |
| **Accuracy** | Correctness — close to true value | Centered on bullseye |

#### 7.2 The Four Combinations

| | High Accuracy | Low Accuracy |
|---|---------------|--------------|
| **High Precision** | Ideal | Systematic error |
| **Low Precision** | Lucky average | Random + systematic |

**Key insight:** High precision with low accuracy indicates a systematic error!

#### 7.3 Connection to Lab Work

- **Random errors** limit precision
- **Systematic errors** limit accuracy
- **Good experimental design** minimizes both

---

### 8. Summary and Lab Preview (2 min)

#### Key Takeaways

1. **Standard format:** result = (value ± uncertainty) units
2. **Three error types:** blunders (eliminate), systematic (correct for), random (quantify)
3. **Standard deviation (σ):** measures scatter of individual measurements
4. **SDOM (σ/√N):** uncertainty in the mean — use this for final results
5. **Weighted average:** combine measurements with different uncertainties
6. **Chauvenet's criterion:** objective test for outliers (use sparingly)
7. **Accuracy vs. precision:** different issues requiring different solutions

#### For This Afternoon (Lab 1)

You will:
1. Take repeated voltage readings and observe fluctuations
2. Calculate mean, σ, and SDOM
3. Measure photodetector offset (a systematic effect)
4. Measure gain ratios and compare to specifications

**Apply what you learned today!**

---

## Suggested Board Work

1. Standard format example: $(0.52 \pm 0.03)$ mm
2. Three error types table
3. σ calculation worked example
4. SDOM formula and interpretation
5. Weighted average example
6. Accuracy vs. precision target diagrams

---

## Key Formulas Reference

| Quantity | Formula |
|----------|---------|
| Mean | $\bar{x} = \frac{1}{N} \sum x_i$ |
| Standard deviation | $\sigma = \sqrt{\frac{\sum(x_i - \bar{x})^2}{N-1}}$ |
| SDOM | $\sigma_{\bar{x}} = \sigma / \sqrt{N}$ |
| Weighted average | $\bar{x}_w = \frac{\sum w_i x_i}{\sum w_i}$, where $w_i = 1/\sigma_i^2$ |

---

## Common Student Questions

**Q: Why N-1 in the standard deviation formula?**
A: Using N-1 (Bessel's correction) gives an unbiased estimate of the true population standard deviation from a sample. With N in the denominator, we'd systematically underestimate σ.

**Q: How many measurements should I take?**
A: Depends on required precision. Remember: SDOM = σ/√N. To halve uncertainty, quadruple N. Often 5-10 measurements is reasonable; sometimes 20-50 for precision work.

**Q: What if my data isn't normally distributed?**
A: Mean and standard deviation still make sense, but the "68% within 1σ" rule doesn't apply. For this course, we'll assume approximately normal distributions.

**Q: Should I report σ or SDOM?**
A: Report SDOM as your uncertainty in the final result. Report σ if you're characterizing the measurement process itself (e.g., "typical noise level is 5 mV RMS").

**Q: What counts as a "systematic error"?**
A: Any effect that biases all measurements the same way. If correcting for it would shift your answer, it's systematic.

---

## Connections to Lab 1

| Lecture Topic | Lab 1 Application |
|---------------|-------------------|
| Mean and SDOM | Reporting voltage measurements |
| Systematic errors | Photodetector offset correction |
| Random errors | Voltage fluctuations (noise) |
| Significant figures | Reporting gain ratios |
| Chauvenet's criterion | Identifying anomalous readings |

---

## Ethical Note: The A₂ Meson Story

*[Time permitting — about 1-2 min]*

In the 1960s, a particle physics experiment reported evidence for the A₂ meson. Later analysis suggested the original data had been "cleaned" — outliers removed without clear criteria.

**The lesson:**
- Always document your data handling
- Use objective criteria (like Chauvenet) for outlier rejection
- Never adjust data to match expectations

**Science depends on honest uncertainty reporting.**
