# Week 4 Tuesday Lecture: Model Testing and Systematic Errors

**Date:** February 3, 2026
**Duration:** 50 minutes
**Purpose:** Support Lab 4 (testing Gaussian beam model, interpreting discrepancies between predictions and measurements)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Execute the predict-measure-compare cycle as a systematic experimental methodology
2. Distinguish between random and systematic errors from data characteristics
3. Identify systematic errors from residual patterns in fits
4. Determine whether a discrepancy indicates measurement error or model limitations
5. Apply quantitative criteria for "agreement" between prediction and measurement
6. Troubleshoot common sources of systematic error in optical experiments

---

## Lecture Outline

### 1. Introduction: The Scientific Method in Practice (5 min)

#### Where We Are

**The journey so far:**
- Week 1: Learned techniques, made first beam measurements
- Week 2: Characterized instrumentation (noise, gain selection)
- Week 3: Developed theory, made predictions with uncertainties

**Today:** The payoff — testing whether theory matches reality

#### The Core Question

You have:
- **Predictions** from Gaussian beam theory (with uncertainties)
- **Measurements** from automated beam profiling (with uncertainties)

**Do they agree?**

This seems like a simple question, but answering it rigorously is at the heart of experimental physics.

#### Today's Lecture

Three connected topics:
1. The predict-measure-compare framework
2. Systematic vs. random errors (deeper treatment)
3. What to do when things don't agree

---

### 2. The Predict-Measure-Compare Cycle (10 min)

#### 2.1 Why Predict First?

**Bad approach:** Take data, then find a theory that fits it.

**Problem:** You can always find *some* theory to match data. This doesn't test anything.

**Good approach:** Make predictions *before* measuring, then compare.

**Why this works:**
- Predictions constrain what you expect to see
- Disagreement has scientific meaning
- You can't unconsciously bias your measurements toward expected results

#### 2.2 The Three Steps

**Step 1: PREDICT**
- Use your model to calculate expected results
- Propagate uncertainties through the calculation
- Record predictions *before* taking data

**Step 2: MEASURE**
- Collect data using validated techniques
- Estimate measurement uncertainties
- Don't peek at predictions while measuring!

**Step 3: COMPARE**
- Calculate discrepancy: $\Delta = |x_{pred} - x_{meas}|$
- Calculate combined uncertainty: $\sigma_{comb} = \sqrt{\sigma_{pred}^2 + \sigma_{meas}^2}$
- Evaluate: Is $\Delta < 2\sigma_{comb}$? (agreement) or $\Delta > 3\sigma_{comb}$? (disagreement)

#### 2.3 Quantitative Agreement Criteria

| Discrepancy | Interpretation | Action |
|-------------|----------------|--------|
| $\Delta < 1\sigma$ | Excellent agreement | Model validated at this precision |
| $1\sigma < \Delta < 2\sigma$ | Good agreement | Consistent with statistical fluctuations |
| $2\sigma < \Delta < 3\sigma$ | Marginal | Worth investigating, might be chance |
| $\Delta > 3\sigma$ | Significant disagreement | Something needs explaining |

**Important:** "3σ disagreement" means only 0.3% chance of occurring by random chance. If you see this, something real is happening.

#### 2.4 Example from Your Lab

**Prediction (from Week 3):**
- Beam width at $z = 1.5$ m: $w = 0.82 \pm 0.05$ mm

**Measurement (from Week 4):**
- Beam width at $z = 1.5$ m: $w = 0.78 \pm 0.03$ mm

**Comparison:**
- $\Delta = |0.82 - 0.78| = 0.04$ mm
- $\sigma_{comb} = \sqrt{0.05^2 + 0.03^2} = 0.058$ mm
- $\Delta / \sigma_{comb} = 0.04/0.058 = 0.69$

**Conclusion:** Less than 1σ — excellent agreement!

---

### 3. Random vs. Systematic Errors: A Deeper Look (18 min)

#### 3.1 Quick Review (from Week 1)

| Type | Behavior | Effect on Mean | Effect on Scatter |
|------|----------|----------------|-------------------|
| **Random** | Varies unpredictably | Averages out | Increases scatter |
| **Systematic** | Consistent bias | Shifts mean | May not affect scatter |

**Week 1 focused on random errors.** Today we tackle the harder problem: systematic errors.

#### 3.2 Why Systematic Errors Are Harder

**Random errors:**
- Can be reduced by averaging
- Standard deviation quantifies their size
- Statistical theory handles them well

**Systematic errors:**
- Don't average out (same bias every time)
- Hard to detect from data alone
- Require physical understanding to identify

*[This is why careful experimentalists worry about systematics more than statistics!]*

#### 3.3 Common Sources in Optical Experiments

| Source | Effect | How to Detect |
|--------|--------|---------------|
| **Alignment drift** | Measurements shift over time | Compare early vs. late data |
| **Stray light** | Adds offset to all readings | Check dark readings, shield detector |
| **Position calibration** | All positions shifted by constant | Use independent position reference |
| **Lens aberrations** | Focus not where expected | Compare multiple lens positions |
| **Thermal effects** | Slow drifts in beam pointing | Monitor room temperature, equilibration time |
| **Clipping** | Beam edge cut off | Check if beam fits on all optics |

#### 3.4 Detecting Systematics from Residuals

**Residuals** = Data - Fit

*[Draw on board: data points, fit line, residual plot]*

**Random errors produce:** Residuals scattered randomly around zero

**Systematic errors produce:** Patterns in residuals

| Residual Pattern | Likely Cause |
|------------------|--------------|
| All positive or all negative | Offset error (wrong zero point) |
| Trend (slope) | Scale factor error or model missing a term |
| Curvature | Wrong functional form |
| Oscillation | Periodic systematic (e.g., backlash in motor) |
| Outlier cluster | Something changed during that measurement set |

#### 3.5 Activity: Reading Residuals (3 min)

*[Prepare this plot in advance and display on screen]*

**Setup:** Show students a residual plot from a beam width fit. The plot should show:
- X-axis: Position z (m)
- Y-axis: Residual = w_measured - w_fit (mm)
- ~10 data points with error bars
- Clear pattern: residuals positive at small z, negative at large z

**Instructions to students:**

"Look at this residual plot from a beam width fit. Work with your neighbor for 90 seconds to answer:
1. Is there a pattern, or are the residuals random?
2. If there's a pattern, what might be causing it?
3. What would you do to investigate?"

*[Give students 90 seconds to discuss]*

**Debrief — ask for volunteer answers, then reveal:**

**What the plot shows:**
- Clear trend: residuals go from positive to negative
- This is NOT random scatter

**What it means:**
- The model is systematically too low at small $z$ and too high at large $z$
- The fit "tilts" the wrong way

**Possible causes:**
- Beam waist not actually at $z = 0$ (forgot to include $z_w$ as fit parameter)
- Wrong value of $\lambda$ used in model
- Additional optical element affecting the beam

**Action:** Re-examine assumptions, add $z_w$ as a fit parameter, re-fit.

---

*[Suggested prepared plot description for instructor:]*

```
Create a scatter plot with:
- X: [0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1] (position in m)
- Y: [0.04, 0.03, 0.02, 0.01, 0.00, -0.01, -0.02, -0.03, -0.04, -0.05] (residual in mm)
- Error bars: ±0.015 mm on each point
- Horizontal dashed line at y = 0
- The pattern should be obvious: a clear downward trend
```

#### 3.6 The "Chi-Square per DOF" Diagnostic

Recall from Week 1: $\chi^2 = \sum \frac{(y_i - f(x_i))^2}{\sigma_i^2}$

**Degrees of freedom (DOF):** Number of data points minus number of fit parameters

**The diagnostic:**

$$\chi^2_{reduced} = \frac{\chi^2}{DOF}$$

| $\chi^2_{reduced}$ | Interpretation |
|--------------------|----------------|
| $\approx 1$ | Fit is consistent with uncertainties |
| $\ll 1$ | Uncertainties overestimated |
| $\gg 1$ | **Fit is poor** — systematics or underestimated uncertainties |

**If $\chi^2_{reduced} > 2$:** Look for systematic errors!

---

### 4. When Predictions and Measurements Disagree (12 min)

#### 4.1 The Decision Tree

*[Draw flowchart on board]*

```
                Disagreement observed
                        |
        ----------------+----------------
        |                               |
  Check uncertainties            Check for blunders
        |                               |
  Are they realistic?            Data entry errors?
        |                         Equipment issues?
        |                               |
        +---------------+---------------+
                        |
            Uncertainties seem OK
                        |
        ----------------+----------------
        |                               |
  Look for systematic              Consider model
  errors in measurement            limitations
        |                               |
  Alignment? Calibration?        Is this regime
  Stray light? Drift?            where model applies?
```

#### 4.2 Step 1: Check for Blunders

Before blaming physics, check for mistakes:

- [ ] Units correct? (mm vs m, Hz vs kHz)
- [ ] Sign conventions consistent?
- [ ] Right data file analyzed?
- [ ] Equipment connected properly?
- [ ] Correct serial numbers, channel numbers?

**These seem trivial but cause ~30% of initial disagreements!**

#### 4.3 Step 2: Verify Uncertainties

**Common uncertainty mistakes:**

| Mistake | Result |
|---------|--------|
| Forgot to include systematic uncertainty | $\sigma$ too small |
| Used standard deviation instead of SDOM | $\sigma$ too large |
| Didn't propagate uncertainty through calculation | Missing uncertainty |
| Assumed uncertainty, didn't measure it | Could be way off |

**Quick check:** Do your Week 2 noise measurements predict your Week 4 scatter? If not, revisit uncertainties.

#### 4.4 Step 3: Investigate Systematic Errors

If blunders and uncertainties are ruled out, look for systematics:

**For beam width measurements:**
- Is the razor blade aligned perpendicular to the beam?
- Is there backlash in the motor stage?
- Is stray light entering the detector?
- Has the alignment drifted since you started?

**For thin lens predictions:**
- Did you measure $S_1$ to the beam waist, or to the laser aperture?
- Is the lens truly at the position you measured?
- Is the focal length accurate (check lens markings)?

#### 4.5 Step 4: Question the Model

If everything else checks out, maybe the model has limitations:

**Gaussian beam model assumptions:**
- Paraxial approximation (small angles)
- No aberrations
- Monochromatic light
- TEM₀₀ mode (fundamental Gaussian)

**Thin lens equation assumptions:**
- Thin lens (thickness $\ll f$)
- Object/image in far field of each other
- No aberrations
- Beam doesn't clip on lens aperture

**Ask:** Which assumptions might not hold in your experiment?

#### 4.6 Documenting Disagreement

**Good experimental practice:** Don't hide disagreements!

In your notebook, document:
1. What the prediction was
2. What you measured
3. The size of the discrepancy (in σ)
4. What you investigated
5. Your best explanation (or "unexplained")

**Unexplained discrepancies are valuable data** — they point to physics you don't yet understand or experimental effects you haven't characterized.

---

### 5. Case Study: The Thin Lens Test (5 min)

*[Connect directly to this afternoon's lab]*

#### The Setup

You predict where the new beam waist should form using:
$$\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}$$

You measure where it actually forms by fitting $w(z)$ data.

#### Common Findings

| Observation | Possible Explanations |
|-------------|----------------------|
| $S_2$ matches prediction (within uncertainties) | Thin lens equation works! |
| $S_2$ shorter than predicted | Lens aberrations, thick lens effects |
| $S_2$ longer than predicted | Beam waist not where you thought |
| Large uncertainty in measured $S_2$ | Not enough data points near waist |

#### What to Do

1. **If they agree:** Great! Quote the precision of agreement.

2. **If they disagree by 2-3σ:**
   - Calculate how many mm the discrepancy is
   - Consider: Is this within lens tolerance? Position measurement error?
   - Report the discrepancy honestly

3. **If they disagree badly (>3σ):**
   - Look for systematic errors
   - Consider whether you measured $S_1$ correctly
   - Check if the lens focal length is as labeled
   - This is interesting! Document carefully.

---

### 6. Summary (2 min)

#### Key Takeaways

1. **Predict-measure-compare** is the core of experimental physics
   - Make predictions before measuring
   - Compare using combined uncertainties
   - $\Delta < 2\sigma$: agreement; $\Delta > 3\sigma$: investigate

2. **Systematic errors** are the hard ones
   - Don't average out
   - Produce patterns in residuals
   - Require physical understanding to identify

3. **When things disagree:**
   - First check for blunders (units, data entry)
   - Then verify uncertainties are realistic
   - Then look for systematic errors
   - Finally, consider model limitations

4. **Document everything** — unexplained discrepancies are scientifically valuable

#### For This Afternoon

- Validate your automated setup against manual measurements
- Measure $w(z)$ at multiple positions
- Test thin lens equation prediction
- If predictions and measurements disagree: investigate!

---

## Suggested Board Work

1. Predict-measure-compare flowchart
2. Agreement criteria table ($1\sigma$, $2\sigma$, $3\sigma$)
3. Example comparison calculation
4. Residual patterns diagram (random vs. systematic)
5. $\chi^2_{reduced}$ formula and interpretation
6. Decision tree for disagreement

---

## Common Student Questions

**Q: What if my prediction has much larger uncertainty than my measurement?**
A: That's fine — it means your measurement is more precise than your prediction. The combined uncertainty will be dominated by the prediction uncertainty. Consider whether you can improve the prediction (better input values, more careful propagation).

**Q: What counts as "close enough" agreement?**
A: Use the quantitative criteria: $\Delta < 2\sigma_{comb}$ is good agreement. Don't rely on "it looks close" — calculate the numbers.

**Q: What if I find a systematic error partway through my experiment?**
A: Fix it if you can, then decide whether to discard the affected data or keep it with a note. Document what happened and when. This is normal experimental practice.

**Q: How do I know if my uncertainties are correct?**
A: Check whether your $\chi^2_{reduced} \approx 1$. If it's much larger than 1, your uncertainties are probably underestimated. If it's much less than 1, they're overestimated. Also verify against Week 2 noise measurements.

**Q: What if I can't find the cause of a disagreement?**
A: Document it honestly as "unexplained discrepancy of Xσ." Suggest possible causes you considered. This is valid scientific reporting — not every puzzle gets solved immediately.

**Q: Is it bad if my data doesn't match the theory?**
A: Not necessarily! Disagreement with theory is how we learn new physics. But first, work hard to rule out experimental errors. If the discrepancy survives scrutiny, it's interesting.

---

## Connections to Lab Work

| Lecture Topic | Lab 4 Application |
|---------------|-------------------|
| Predict-measure-compare | Comparing Week 3 predictions to Week 4 measurements |
| Systematic error identification | Interpreting beam width fit residuals |
| Quantitative agreement criteria | Evaluating thin lens equation test |
| Uncertainty verification | Comparing Week 2 noise predictions to Week 4 data |
| Documentation of disagreement | Reflection questions in lab guide |

---

## Quantitative Examples

### Example 1: Good Agreement

**Prediction:** $w_0 = 0.45 \pm 0.03$ mm
**Measurement:** $w_0 = 0.47 \pm 0.02$ mm

$\Delta = 0.02$ mm
$\sigma_{comb} = \sqrt{0.03^2 + 0.02^2} = 0.036$ mm
$\Delta/\sigma_{comb} = 0.56$

**Conclusion:** Excellent agreement (less than 1σ). Model validated.

### Example 2: Marginal Agreement

**Prediction:** $S_2 = 180 \pm 5$ mm
**Measurement:** $S_2 = 168 \pm 4$ mm

$\Delta = 12$ mm
$\sigma_{comb} = \sqrt{5^2 + 4^2} = 6.4$ mm
$\Delta/\sigma_{comb} = 1.9$

**Conclusion:** About 2σ discrepancy. Worth noting but not definitive evidence of a problem. Could be statistical fluctuation.

### Example 3: Significant Disagreement

**Prediction:** $z_w = 0.85 \pm 0.02$ m
**Measurement:** $z_w = 0.78 \pm 0.01$ m

$\Delta = 0.07$ m = 70 mm
$\sigma_{comb} = \sqrt{0.02^2 + 0.01^2} = 0.022$ m = 22 mm
$\Delta/\sigma_{comb} = 3.2$

**Conclusion:** >3σ disagreement. This needs investigation! Possible causes: wrong assumption about beam waist position, systematic error in position measurement, or model limitation.
