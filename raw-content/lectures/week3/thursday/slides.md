---
marp: true
theme: cu-physics
math: mathjax
paginate: true
footer: '![logo](../../themes/Physics_rev_left.png)'
---

<!-- _class: title -->
<!-- _paginate: false -->

# Lenses and Gaussian Beams

## PHYS 4430 — Week 3 Thursday
January 29, 2026

<!--
Total lecture time: 50 minutes
Purpose: Prepare students for Lab 4 prelab (lens predictions, thin lens equation for Gaussian beams)
-->

---

## Where We Are

**Weeks 1–3:** Characterized the beam, automated measurements, learned error propagation

**This week (ongoing):** Automated beam profiles at one $z$ position

**Next week (Lab 4):** Test Gaussian beam model AND investigate lens effects

<!--
TIMING: ~3 minutes for intro
Students are mid-way through their beam characterization work.
-->

---

## Today's Focus

You'll add a lens to your beam path next week.

**Key questions:**
1. How does a lens change a Gaussian beam?
2. Can we use the familiar thin lens equation?
3. What are the limits of this approach?

---

<!-- _class: section -->

# Part 1: The Thin Lens Equation

---

## The Ray Picture (Geometric Optics)

![h:320 Thin lens ray diagram](figures/thursday_01_thin_lens.png)

In geometric optics, light travels as rays. A lens bends rays to form an image.

<!--
TIMING: ~8 minutes for thin lens review
Most students have seen this before, but quick review establishes vocabulary.
-->

---

## The Thin Lens Equation

$$\boxed{\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}}$$

| Symbol | Meaning |
|--------|---------|
| $S_1$ | Object distance (from lens) |
| $S_2$ | Image distance (from lens) |
| $f$ | Focal length |

---

## Example Calculation

**Given:** Lens with $f = 100$ mm, object at $S_1 = 500$ mm

**Find:** Image location $S_2$

$$\frac{1}{500} + \frac{1}{S_2} = \frac{1}{100}$$

$$\frac{1}{S_2} = \frac{1}{100} - \frac{1}{500} = \frac{5-1}{500} = \frac{4}{500}$$

$$S_2 = 125 \text{ mm}$$

The image forms 125 mm beyond the lens.

---

## Special Cases to Remember

| Configuration | Object at... | Image at... |
|---------------|-------------|-------------|
| Collimated input | $S_1 = \infty$ | $S_2 = f$ (at focus) |
| Object at focus | $S_1 = f$ | $S_2 = \infty$ (collimated) |
| Object at 2f | $S_1 = 2f$ | $S_2 = 2f$ (1:1 imaging) |

---

<!-- _class: section -->

# Part 2: Gaussian Beams Through Lenses

---

## What Is the "Object" for a Gaussian Beam?

**In ray optics:** object is a point source, image is where rays converge.

**For a Gaussian beam:**
- The **"object"** is the beam waist (where $w = w_0$)
- The **"image"** is the new beam waist after the lens

<!--
TIMING: ~10 minutes for conceptual picture
This is the key insight: waist → lens → new waist
-->

---

## Gaussian Beam Transformation

![h:380 Gaussian beam through lens](figures/thursday_02_beam_lens.png)

The lens transforms one Gaussian beam into another Gaussian beam.

---

## What Changes, What Stays the Same

**After a lens, the beam has:**

| Changes | Stays Same |
|---------|------------|
| Waist size $w_0 \to w_0'$ | Wavelength $\lambda$ |
| Waist position $z_w \to z_w'$ | Gaussian profile |

The Gaussian form is preserved (for ideal thin lens in paraxial regime).

---

## When Does the Thin Lens Equation Apply?

The approximation works when:

| Condition | Physical Meaning |
|-----------|-----------------|
| Lens diameter $\gg w(z_{lens})$ | Beam isn't clipped |
| Beam width at lens $\gg \lambda$ | Paraxial regime |
| Focal length $\gg \lambda$ | Lens isn't microscopic |

For He-Ne laser ($\lambda = 633$ nm) and typical lenses ($f \sim 100$ mm):
**These conditions are easily satisfied!**

---

<!-- _class: section -->

# Part 3: Making Predictions

---

## Applying the Thin Lens Equation

**Treat the beam waist as the "object":**

If the waist is at distance $S_1$ from the lens, the new waist forms at $S_2$:

$$\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}$$

> "object" = original waist, "image" = new waist

**Important:** This is an approximation for Gaussian beams — it ignores diffraction. We'll discuss when it breaks down shortly.

<!--
TIMING: ~15 minutes for quantitative predictions
This is where Tuesday's error propagation skills come in!
-->

---

## Example: Predicting New Waist Location

**Given:**
- He-Ne beam with $w_0 = 0.5$ mm at laser output
- Lens with $f = 150$ mm placed 1.0 m from laser

**Find:** Where does the new waist form?

$$S_1 = 1000 \text{ mm}$$

$$\frac{1}{S_2} = \frac{1}{150} - \frac{1}{1000} = \frac{850}{150000}$$

$$S_2 = \frac{150000}{850} \approx 176 \text{ mm}$$

---

## Estimating the New Waist Size

In geometric optics, the magnification is $M = -S_2/S_1$ (negative sign = image is inverted). For beam waist size we only care about the magnitude:

$$w_0' \approx \left| \frac{S_2}{S_1} \right| w_0 = |M| \cdot w_0$$

> We use $|M|$ because beam radius is always positive — the sign of $M$ tells you about image orientation, which doesn't apply to a Gaussian beam profile.

**Continuing the example:**

$$w_0' \approx \frac{176}{1000} \times 0.5 \text{ mm} = 88 \text{ μm}$$

The beam focuses to a much smaller waist!

---

## Propagating Uncertainty

**This is where Tuesday's lecture pays off!**

```python
from uncertainties import ufloat

# Known values
S1 = ufloat(1000, 10)  # mm, ± 1 cm uncertainty
f = ufloat(150, 2)      # mm, lens spec ± 2 mm

# Calculate S2 using thin lens equation
S2 = 1 / (1/f - 1/S1)

print(f"Image distance: {S2:.1f} mm")
```

**Output:** `Image distance: 176.5+/-3.5 mm`

---

<!-- _class: section -->

# Part 4: Limitations and the Diffraction Limit

---

## When Does the Thin Lens Equation Break Down?

The thin lens equation is a ray optics result — it ignores diffraction. The approximation is good when $z_R \ll |S_1 - f|$, where $z_R = \pi w_0^2 / \lambda$ is the Rayleigh range.

| Beam / Setup | $z_R$ | Compare to $\|S_1 - f\|$ | Thin lens equation... |
|-------------|--------|--------------------------|-----------------|
| Tightly focused ($w_0 \sim 50$ μm) | ~12 mm | $z_R \ll \|S_1 - f\|$ | Works well |
| Typical He-Ne ($w_0 \sim 0.5$ mm) | ~1.2 m | $z_R \sim \|S_1 - f\|$ | Use with caution |
| Collimated ($w_0 \sim 2$ mm) | ~20 m | $z_R \gg \|S_1 - f\|$ | Fails badly |

**Your beam is in the middle row.** Calculate $z_R$ for your measured $w_0$ and compare it to $|S_1 - f|$ for your setup — this tells you how much to trust your thin lens prediction.

**Your predictions may not agree with your measurements.** That's expected — and the discrepancy is part of what you'll investigate in Week 4.

<!--
TIMING: ~7 minutes for limitations
Managing expectations for Week 4.
-->

---

## Other Sources of Discrepancy

Even beyond the thin lens approximation, watch for:

| Observation | Possible Cause |
|-------------|----------------|
| $S_2$ offset from prediction | Waist not where you assumed |
| Beam not Gaussian after lens | Clipping, damaged optics, etc. |
| Thick lens effects | Principal planes not coincident |

**The goal in Week 4:** Make predictions, test them, and determine whether discrepancies come from measurement error, the thin lens approximation, or other systematic effects.

---

## How Small Can You Focus?

There's a fundamental limit: the **diffraction limit**.

$$\boxed{w_0^{min} \approx \frac{\lambda}{\pi \cdot NA}}$$

where **NA** (numerical aperture) characterizes the lens:

$$NA \approx \frac{D}{2f}$$

($D$ = lens diameter, $f$ = focal length)

<!--
TIMING: ~5 minutes for diffraction limit
-->

---

## Diffraction Limit Example

**Given:** He-Ne ($\lambda = 633$ nm), lens with $D = 25$ mm, $f = 50$ mm

$$NA = \frac{25}{2 \times 50} = 0.25$$

$$w_0^{min} = \frac{633 \times 10^{-9}}{\pi \times 0.25} = 0.8 \text{ μm}$$

**In practice:** This assumes the beam fills the lens. Your He-Ne beam ($w \sim 1$ mm) uses only a small fraction of the 25 mm aperture, so the effective NA is much smaller ($\text{NA}_{eff} \approx w/f$) and the focused spot is ~50–100 μm.

---

## Tradeoffs in Focusing

| Want tighter focus? | But... |
|---------------------|--------|
| Shorter focal length | Working distance shrinks |
| Larger lens diameter | More expensive, harder to mount |
| Fill more of lens aperture | Alignment more critical |

**This is why microscope objectives are complex!**

---

<!-- _class: section -->

# Part 5: Preparing for Week 4

---

## What the Prelab Asks You to Do

1. **Transfer predictions** from Week 3 (beam width vs. position)
2. **Predict lens effects** using the thin lens equation
3. **Create uncertainty budget** for your measurements

---

## The Prediction Exercise

Choose a lens ($f \approx 100–200$ mm) and predict:

| Quantity | Symbol | Method |
|----------|--------|--------|
| New waist position | $S_2$ | Thin lens equation |
| New waist size | $w_0'$ | Magnification |
| Rayleigh range | $z_R$ | $\pi w_0^2 / \lambda$ |
| Uncertainties | $\sigma_{S_2}$, $\sigma_{w_0'}$ | Error propagation |

Also calculate $z_R$ and compare to $|S_1 - f|$ — how reliable do you expect your prediction to be?

---

## Code Template for Predictions

```python
from uncertainties import ufloat

# Your measurements (adjust values!)
w0 = ufloat(0.5, 0.02)    # mm, from Week 3 fit
S1 = ufloat(1000, 10)     # mm, measured distance
f = ufloat(150, 2)        # mm, lens focal length

# Thin lens equation
S2 = 1 / (1/f - 1/S1)

# Magnification and new waist
M = S2 / S1
w0_new = abs(M) * w0

print(f"New waist at: {S2:.1f} mm from lens")
print(f"New waist size: {w0_new*1000:.1f} μm")
```

---

## Connecting Theory to Experiment

**In Week 4 lab, you will:**

1. Complete beam waist measurement (finish Week 3 work)
2. Add lens and measure new waist location and size
3. Compare to your thin lens equation predictions
4. Investigate discrepancies — are they measurement error or model limitations?

> Write predictions **before** you measure!

---

## Summary

1. **Thin lens equation** applies to Gaussian beams (as an approximation):
   $$\frac{1}{S_1} + \frac{1}{S_2} = \frac{1}{f}$$
   where "object" = original waist, "image" = new waist

2. **New waist size** follows magnification: $w_0' \approx |M| \cdot w_0$

3. **This is approximate** — it ignores diffraction. Expect discrepancies when $z_R \gtrsim |S_1 - f|$

4. **Uncertainty propagation** is essential for testable predictions

5. **Diffraction limit** sets minimum spot size: $w_0^{min} \approx \lambda/(\pi \cdot NA)$

---

<!-- _class: title -->
<!-- _paginate: false -->

# Questions?

## We are here to help!

<!--
COMMON STUDENT QUESTIONS:

Q: Why doesn't the wavelength appear in the thin lens equation?
A: The thin lens equation is pure geometry (rays). Wavelength enters through
   diffraction effects (the Rayleigh range z_R = π w₀²/λ), which is why the
   equation is only approximate for Gaussian beams.

Q: What if the beam waist is inside the laser?
A: S1 might be negative (virtual object) or you need to estimate waist position.
   Week 4 fitting will find the actual waist location.

Q: How do I know if my lens is "thin enough"?
A: For our lenses (few mm thick, f ~ 50-200 mm), thin lens is good to ~1%.

Q: Does the Gaussian beam stay Gaussian after a lens?
A: Yes, as long as no clipping and paraxial regime. This is a key property!

Q: What if I want to collimate a beam?
A: Place lens so waist is at focal point (S1 = f). Then S2 → ∞.
-->
