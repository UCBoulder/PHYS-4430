# Week 3 Thursday Lecture: Lenses and Gaussian Beams

**Date:** January 29, 2026
**Duration:** 50 minutes
**Purpose:** Prepare students for Lab 4 prelab (lens predictions, thin lens equation for Gaussian beams)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Explain how a thin lens transforms a Gaussian beam (changes waist location and size)
2. Apply the thin lens equation to predict image location for a focused beam
3. Identify when the thin lens equation is valid and when it breaks down
4. Calculate the new beam waist position and size after a lens
5. Explain the diffraction limit on focusing and its relationship to numerical aperture
6. Make quantitative predictions for Week 4's lens experiments

---

## Lecture Outline

### 1. Introduction and Context (3 min)

#### Where We Are

**Weeks 1-3 recap:**
- Week 1: Manual measurements, characterized beam profile
- Week 2: DAQ and noise characterization
- Week 3 (so far): Motor control, automated profiling, error propagation

**This week's lab (still ongoing):** Automated beam profiles at multiple $z$ positions

**Next week (Lab 4):** Test the Gaussian beam model AND investigate lens effects

#### Today's Focus

You'll add a lens to your beam path next week. To make quantitative predictions:
1. How does a lens change a Gaussian beam?
2. Can we use the familiar thin lens equation?
3. What are the limits of this approach?

---

### 2. Review: Thin Lens Equation (Geometric Optics) (8 min)

#### 2.1 The Ray Picture

*[Draw ray diagram on board: object → lens → image]*

In geometric optics, light travels in straight lines (rays). A thin lens bends rays to form an image.

**The thin lens equation:**

$$\boxed{\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}}$$

| Symbol | Meaning |
|--------|---------|
| $S_1$ | Object distance (from lens) |
| $S_2$ | Image distance (from lens) |
| $f$ | Focal length |

**Sign conventions (for this course):**
- Distances are positive when measured in the direction light travels
- Real images have positive $S_2$
- Virtual images have negative $S_2$

#### 2.2 Example Calculation

**Given:** Lens with $f = 100$ mm, object at $S_1 = 500$ mm

**Find:** Image location $S_2$

$$\frac{1}{500} + \frac{1}{S_2} = \frac{1}{100}$$

$$\frac{1}{S_2} = \frac{1}{100} - \frac{1}{500} = \frac{5-1}{500} = \frac{4}{500}$$

$$S_2 = 125 \text{ mm}$$

The image forms 125 mm beyond the lens.

#### 2.3 Special Cases

| Configuration | Object at... | Image at... |
|---------------|-------------|-------------|
| Object at infinity | $S_1 = \infty$ | $S_2 = f$ (at focal point) |
| Object at focus | $S_1 = f$ | $S_2 = \infty$ (collimated output) |
| Object at 2f | $S_1 = 2f$ | $S_2 = 2f$ (1:1 imaging) |

---

### 3. Gaussian Beams and Lenses: The Conceptual Picture (10 min)

#### 3.1 What "Object" and "Image" Mean for a Gaussian Beam

In ray optics: object is a point source, image is where rays converge.

For a Gaussian beam:
- The **"object"** is the beam waist (where $w = w_0$)
- The **"image"** is the new beam waist after the lens

*[Draw on board: Gaussian beam with waist → lens → new waist]*

**Key insight:** The lens transforms one Gaussian beam into another Gaussian beam (assuming paraxial conditions).

#### 3.2 What Changes, What Stays the Same

After a lens, the beam has:
- **New waist size** $w_0'$ (may be larger or smaller)
- **New waist position** $z_w'$
- **Same wavelength** $\lambda$ (light doesn't change color!)
- **Same Gaussian profile** (if lens is "thin" and paraxial)

#### 3.3 The Physical Picture

*[Draw beam envelope showing transformation]*

**Before lens:**
- Beam waist $w_0$ at position $z_w$
- Beam expanding with Rayleigh range $z_R = \pi w_0^2 / \lambda$

**After lens:**
- New waist $w_0'$ at position $z_w'$
- Beam now converging toward (or diverging from) new waist
- New Rayleigh range $z_R' = \pi w_0'^2 / \lambda$

#### 3.4 When Does the Thin Lens Equation Apply?

**Short answer:** When the beam at the lens is much wider than the wavelength and the angles are small.

**More precisely:**
- Lens diameter $\gg$ beam width at lens
- Beam width at lens $\gg$ wavelength
- Focal length $\gg$ wavelength

For your He-Ne laser ($\lambda = 633$ nm) and typical lenses ($f \sim 100$ mm), these conditions are easily satisfied.

---

### 4. Quantitative Predictions (15 min)

#### 4.1 Using the Thin Lens Equation for Gaussian Beams

**Approximation:** Treat the beam waist as the "object"

If the beam waist is at distance $S_1$ from the lens, the new waist will be approximately at distance $S_2$ given by:

$$\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}$$

*[This is the same equation! The physics is different, but the math works out similarly.]*

#### 4.2 Example: Predicting New Waist Location

**Given:**
- He-Ne laser beam with waist $w_0 = 0.5$ mm located at the laser output
- Lens with $f = 150$ mm placed 1.0 m from the laser

**Find:** Where does the new beam waist form?

**Solution:**
$$S_1 = 1000 \text{ mm}$$
$$\frac{1}{1000} + \frac{1}{S_2} = \frac{1}{150}$$
$$\frac{1}{S_2} = \frac{1}{150} - \frac{1}{1000} = \frac{1000 - 150}{150000} = \frac{850}{150000}$$
$$S_2 = \frac{150000}{850} \approx 176 \text{ mm}$$

**Prediction:** New waist forms about 176 mm beyond the lens.

#### 4.3 What About the New Waist Size?

The magnification in geometric optics is $M = -S_2/S_1$.

For Gaussian beams, the new waist size is approximately:

$$w_0' \approx \left| \frac{S_2}{S_1} \right| w_0 = |M| w_0$$

*[When the thin lens approximation is valid]*

**Continuing the example:**
$$w_0' \approx \frac{176}{1000} \times 0.5 \text{ mm} = 0.088 \text{ mm} = 88 \text{ μm}$$

The beam focuses down to a much smaller waist!

#### 4.4 Propagating Uncertainty

**This is where Week 3 Tuesday's lecture pays off.**

Using the `uncertainties` package:

```python
from uncertainties import ufloat

# Known values
S1 = ufloat(1000, 10)  # mm, ± 1 cm uncertainty
f = ufloat(150, 2)      # mm, lens spec ± 2 mm

# Calculate S2 using thin lens equation
# 1/S2 = 1/f - 1/S1
one_over_S2 = 1/f - 1/S1
S2 = 1 / one_over_S2

print(f"Image distance: {S2:.1f} mm")
```

**Output:** `Image distance: 176.5+/-3.5 mm`

The uncertainty in your prediction comes from uncertainties in:
- Object distance $S_1$ (how precisely did you measure it?)
- Focal length $f$ (manufacturer tolerance)

#### 4.5 Practice Problem

*[Work through with students]*

**Setup:** Lens with $f = 100 \pm 2$ mm placed 300 mm from beam waist

**Questions:**
1. Where is the new waist? ($S_2 = ?$)
2. What is the uncertainty in this prediction?
3. If original waist is $w_0 = 0.3$ mm, what is the new waist size?

**Answers:**
1. $S_2 = 150$ mm
2. Use error propagation: $\sigma_{S_2} \approx 5$ mm
3. $w_0' \approx 0.15$ mm (beam focuses to half the original waist)

---

### 5. When the Thin Lens Equation Breaks Down (7 min)

#### 5.1 The Fine Print

The thin lens equation is an approximation. It works best when:

| Condition | Physical Meaning |
|-----------|-----------------|
| $w(z_{lens}) \ll$ lens diameter | Beam isn't clipped by lens aperture |
| $S_1, S_2 \gg z_R$ | Object/image in far field of each other |
| Lens is thin | Lens thickness $\ll$ focal length |

#### 5.2 What Happens Near the Focus?

**Important subtlety:** Near the focus, the Rayleigh range matters!

If $S_1 \approx z_R$ or $S_2 \approx z_R$, the simple thin lens equation is less accurate.

**Full Gaussian beam propagation formulas exist** but are beyond this course. For our experiments, the thin lens equation gives predictions accurate enough to test.

#### 5.3 Systematic Errors You Might See

When you test the thin lens equation in Week 4, you might find disagreements. Common causes:

| Observation | Possible Cause |
|-------------|---------------|
| $S_2$ smaller than predicted | Lens aberrations, thick lens effects |
| $S_2$ larger than predicted | Beam not at waist where you thought |
| Large scatter in data | Vibrations, alignment drift |

**The goal of Week 4:** Determine whether discrepancies are measurement uncertainty or model limitations.

---

### 6. The Diffraction Limit (5 min)

#### 6.1 How Small Can You Focus?

There's a fundamental limit to how tightly you can focus a beam.

**The diffraction limit:**

$$w_0^{min} \approx \frac{\lambda}{\pi \cdot NA}$$

where $NA$ is the numerical aperture of the lens.

For a thin lens with diameter $D$ and focal length $f$:

$$NA \approx \frac{D}{2f}$$

#### 6.2 Example Calculation

**Given:** He-Ne laser ($\lambda = 633$ nm), lens with $D = 25$ mm, $f = 50$ mm

**Calculate minimum spot size:**

$$NA = \frac{25}{2 \times 50} = 0.25$$

$$w_0^{min} = \frac{633 \times 10^{-9}}{\pi \times 0.25} = 0.8 \text{ μm}$$

**In practice**, achieving this limit requires:
- Perfect lens (no aberrations)
- Beam filling the lens aperture
- Perfect alignment

Your He-Ne beam will focus to ~50-100 μm, limited by the beam size at the lens.

#### 6.3 Tradeoffs in Focusing

**Smaller focal length →** Tighter focus BUT working distance shrinks

**Larger lens diameter →** Tighter focus BUT lens is more expensive, harder to mount

**This is why microscope objectives are complex!** They're designed to maximize NA while managing aberrations.

---

### 7. Preparing for Week 4 Prelab (3 min)

#### What You'll Do

The Week 4 prelab asks you to:

1. **Transfer predictions** from Week 3 (beam width vs. position)
2. **Predict lens effects** using the thin lens equation
3. **Create uncertainty budget** for your measurements

#### The Prediction Exercise

You'll choose a lens (probably $f = 100-200$ mm) and predict:
- Where the new waist forms ($S_2$)
- The new waist size ($w_0'$)
- Uncertainty in these predictions

**Use the tools from this week:**
- Thin lens equation (today's lecture)
- Error propagation with `uncertainties` (Tuesday's lecture)

#### Connecting Theory to Experiment

In Week 4 lab, you will:
1. Measure beam waist without lens (complete the Week 3 work)
2. Add lens and measure new waist location and size
3. Compare to thin lens equation predictions
4. Investigate discrepancies

---

### 8. Summary (2 min)

#### Key Takeaways

1. **Thin lens equation** $\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}$ applies to Gaussian beams
   - "Object" = original beam waist
   - "Image" = new beam waist after lens

2. **New waist size** approximately follows magnification: $w_0' \approx |M| w_0$

3. **Uncertainty propagation** is essential for making testable predictions

4. **Thin lens equation is approximate**—expect discrepancies of a few percent

5. **Diffraction limit** sets the minimum spot size: $w_0^{min} \approx \lambda / (\pi \cdot NA)$

#### For the Prelab

- Choose a lens (record focal length and tolerance)
- Measure $S_1$ (distance from waist to lens position)
- Calculate predicted $S_2$ with uncertainty
- Prepare uncertainty budget

---

## Suggested Board Work

1. Ray diagram for thin lens imaging
2. Thin lens equation (boxed)
3. Gaussian beam through lens diagram (showing old waist → lens → new waist)
4. Example calculation: $S_1 = 1$ m, $f = 150$ mm → $S_2 = ?$
5. Error propagation example (either by hand or showing `uncertainties` output)
6. Diffraction limit formula

---

## Code Snippets to Show

### Predicting Image Location

```python
from uncertainties import ufloat

# Measured/known values
S1 = ufloat(1000, 10)  # mm
f = ufloat(150, 2)     # mm

# Thin lens equation
S2 = 1 / (1/f - 1/S1)

print(f"New waist at: {S2:.1f} mm from lens")
```

### Predicting New Waist Size

```python
w0 = ufloat(0.5, 0.02)  # mm, original waist

# Magnification
M = S2 / S1
w0_new = abs(M) * w0

print(f"New waist size: {w0_new*1000:.1f} μm")
```

---

## Common Student Questions

**Q: Why doesn't the wavelength change the image location?**
A: The thin lens equation comes from geometry (Snell's law and lens shape). Wavelength affects the *focal length* through the refractive index, but once $f$ is fixed, the imaging geometry is wavelength-independent.

**Q: What if the beam waist is inside the laser?**
A: This is common! You can still use the thin lens equation, but $S_1$ might be negative (virtual object) or you might need to estimate the waist position. In Week 4, you'll fit your beam profile data to find the actual waist location.

**Q: How do I know if my lens is "thin enough"?**
A: For the lenses in our lab (a few mm thick, focal lengths 50-200 mm), the thin lens approximation is good to within ~1%. You'd need a very thick lens or very short focal length to see significant errors.

**Q: Does the Gaussian beam stay Gaussian after a lens?**
A: Yes, as long as:
- The lens doesn't clip the beam
- We stay in the paraxial regime
- The lens has no significant aberrations
This is a key property that makes Gaussian beam optics powerful.

**Q: What if I want to collimate a beam (make it parallel)?**
A: Place the lens so that the beam waist is at the focal point ($S_1 = f$). Then $S_2 → \infty$ and the output beam is collimated. The output waist is at infinity with very large $w_0$.

---

## Connections to Lab Work

| Lecture Topic | Lab 4 Application |
|---------------|-------------------|
| Thin lens equation | Predicting new waist position |
| Waist size prediction | Estimating $w_0'$ after lens |
| Uncertainty propagation | Prelab prediction exercise |
| Conditions for validity | Interpreting discrepancies |
| Diffraction limit | Understanding focus limitations |

---

## Optional: Demonstration Ideas

1. **Show a lens:** Pass around a 100-150 mm lens, discuss focal length markings
2. **Laser pointer through lens:** Show visible focus point on card
3. **Compare focal lengths:** Shorter focal length focuses tighter (but closer)
4. **Drawing exercise:** Have students sketch Gaussian beam transformation on paper
