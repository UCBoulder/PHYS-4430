# Week 2 Thursday Lecture: Gaussian Beam Theory

**Date:** January 22, 2026
**Duration:** 50 minutes
**Purpose:** Prepare students for Week 3 prelab (deriving paraxial wave equation, understanding Gaussian beam parameters)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Explain why laser beams have a Gaussian profile (it's a solution to the wave equation)
2. Apply the slowly-varying envelope approximation to simplify the wave equation
3. Derive the paraxial wave equation from Maxwell's equations
4. Identify and interpret the four Gaussian beam parameters: $w_0$, $w(z)$, $R(z)$, $\zeta(z)$
5. Calculate the Rayleigh range and explain its physical significance
6. Predict how beam width changes with propagation distance

---

## Lecture Outline

### 1. Introduction and Motivation (5 min)

#### Opening Question

"In Week 1, you measured a beam profile and found it was Gaussian. But *why* is it Gaussian? Why not some other shape?"

**Answer preview:** The Gaussian profile isn't arbitrary—it's a fundamental solution to Maxwell's equations under the conditions present in a laser cavity.

#### Why This Matters

- Week 3 prelab: You'll derive these equations yourself
- Week 4 lab: You'll test whether the model matches reality
- Understanding the physics helps you interpret disagreements between theory and data

#### The Big Picture

```
Maxwell's Equations
       ↓
   Wave Equation
       ↓
   Slowly-Varying Envelope Approximation
       ↓
   Paraxial Wave Equation
       ↓
   Gaussian Beam Solution
```

---

### 2. From Maxwell to the Wave Equation (8 min)

#### 2.1 Maxwell's Equations (Quick Review)

In free space, Maxwell's equations lead to the **vector wave equation**:

$$\nabla^2 \vec{E} = \mu_0 \epsilon_0 \frac{\partial^2 \vec{E}}{\partial t^2}$$

**Physical meaning:** Changes in the electric field propagate through space at the speed of light, where $c = 1/\sqrt{\mu_0 \epsilon_0}$.

#### 2.2 Plane Wave Solution

The simplest solution is a **plane wave** propagating in the $z$-direction:

$$\vec{E}(z,t) = \vec{E}_0 \cos(kz - \omega t)$$

where:
- $k = 2\pi/\lambda$ is the wave number
- $\omega = 2\pi f$ is the angular frequency
- $k$ and $\omega$ are related by $\omega = ck$

*[Draw on board: plane wave with flat wavefronts perpendicular to z]*

**Problem:** Plane waves extend infinitely in $x$ and $y$. Real laser beams are localized.

#### 2.3 We Need Something Better

**Observation from Week 1:** Your laser beam has:
- Finite width (~0.5 mm)
- Gaussian intensity profile
- Width that changes slowly with $z$

**Question:** What solution to the wave equation describes this?

---

### 3. The Slowly-Varying Envelope Approximation (10 min)

#### 3.1 The Key Insight

Real laser beams look like a plane wave with a slowly-varying "envelope":

$$\vec{E}(x,y,z,t) = \hat{x} \, A(x,y,z) \, e^{i(kz - \omega t)}$$

- The $e^{i(kz-\omega t)}$ part oscillates rapidly (wavelength ~633 nm)
- The $A(x,y,z)$ part (the envelope) changes slowly (over millimeters)

*[Draw on board: rapidly oscillating wave inside a slowly-varying Gaussian envelope]*

#### 3.2 Substituting into the Wave Equation

Substitute our trial solution into $\nabla^2 \vec{E} = \mu_0 \epsilon_0 \frac{\partial^2 \vec{E}}{\partial t^2}$

After calculating derivatives (done in prelab):

$$\left( \frac{\partial^2 A}{\partial x^2} + \frac{\partial^2 A}{\partial y^2} + \frac{\partial^2 A}{\partial z^2} \right) + 2ik\frac{\partial A}{\partial z} = 0$$

**Note:** The $k^2 A$ and $\omega^2 A$ terms canceled because $k^2 = \omega^2/c^2$

#### 3.3 The Approximation

**The slowly-varying envelope approximation:**

$$\left| \frac{\partial^2 A}{\partial z^2} \right| \ll \left| 2k \frac{\partial A}{\partial z} \right|$$

**Physical meaning:** The envelope $A$ doesn't change much over one wavelength.

**Quantitative check:**
- Wavelength: $\lambda = 633$ nm
- Beam width changes over: ~millimeters to centimeters
- Ratio: ~10,000 wavelengths per significant change

The approximation is excellent for laser beams!

#### 3.4 The Paraxial Wave Equation

Dropping the $\partial^2 A/\partial z^2$ term:

$$\boxed{\frac{\partial^2 A}{\partial x^2} + \frac{\partial^2 A}{\partial y^2} + 2ik\frac{\partial A}{\partial z} = 0}$$

This is the **paraxial wave equation**—the foundation for Gaussian beam optics.

**"Paraxial"** means "near the axis"—valid when the beam stays close to the optical axis (small angles).

---

### 4. The Gaussian Beam Solution (15 min)

#### 4.1 The Solution Exists

The paraxial wave equation has many solutions (Gauss-Hermite modes). The simplest and most common is the **fundamental Gaussian mode**:

$$\vec{E}(x,y,z,t) = \vec{E}_0 \frac{w_0}{w(z)} \exp\left(-\frac{x^2+y^2}{w^2(z)}\right) \exp\left(ik\frac{x^2+y^2}{2R(z)}\right) e^{-i\zeta(z)} e^{i(kz-\omega t)}$$

**Don't panic!** Let's break this down piece by piece.

#### 4.2 The Four Key Parameters

| Symbol | Name | Physical Meaning |
|--------|------|------------------|
| $w_0$ | Beam waist | Minimum beam radius (at focus) |
| $w(z)$ | Beam radius | How wide the beam is at position $z$ |
| $R(z)$ | Radius of curvature | How curved the wavefronts are |
| $\zeta(z)$ | Gouy phase | Extra phase shift through focus |

*[Draw on board: Gaussian beam showing w₀, w(z), and diverging wavefronts]*

#### 4.3 Beam Width: $w(z)$

$$w(z) = w_0 \sqrt{1 + \left(\frac{\lambda z}{\pi w_0^2}\right)^2}$$

**Key features:**
- At $z = 0$: $w(0) = w_0$ (the minimum, called the "waist")
- As $z \to \infty$: $w(z) \approx \frac{\lambda z}{\pi w_0}$ (linear growth = constant angle)

*[Draw on board: beam width vs. z, hyperbolic shape]*

#### 4.4 The Rayleigh Range: $z_R$

Define the **Rayleigh range**:

$$\boxed{z_R = \frac{\pi w_0^2}{\lambda}}$$

This is the distance where $w(z_R) = \sqrt{2} \, w_0$ (beam area doubles).

**Rewrite beam width using $z_R$:**

$$w(z) = w_0 \sqrt{1 + \left(\frac{z}{z_R}\right)^2}$$

Much cleaner! The Rayleigh range sets the length scale for beam evolution.

#### 4.5 Example Calculation

**Given:** He-Ne laser, $\lambda = 633$ nm, $w_0 = 0.5$ mm

**Calculate $z_R$:**

$$z_R = \frac{\pi (0.5 \times 10^{-3})^2}{633 \times 10^{-9}} = \frac{\pi \times 2.5 \times 10^{-7}}{6.33 \times 10^{-7}} \approx 1.24 \text{ m}$$

**Interpretation:** The beam stays relatively collimated (within $\sqrt{2}$ of minimum width) for about 1.2 meters on either side of the waist.

#### 4.6 Radius of Curvature: $R(z)$

$$R(z) = z \left(1 + \left(\frac{z_R}{z}\right)^2\right)$$

**Key features:**
- At $z = 0$: $R \to \infty$ (flat wavefronts at the waist)
- At $z = z_R$: $R = 2z_R$ (curved wavefronts)
- As $z \to \infty$: $R \approx z$ (spherical wavefronts centered on waist)

*[Draw on board: wavefront curvature at different z positions]*

**Physical picture:** The wavefronts are flat at the waist and become increasingly spherical (like they're expanding from a point) far from the waist.

#### 4.7 Gouy Phase: $\zeta(z)$

$$\zeta(z) = \arctan\left(\frac{z}{z_R}\right)$$

**What it means:** An extra phase shift (totaling $\pi$ from $-\infty$ to $+\infty$) that occurs when passing through a focus.

**You probably won't measure this** in this lab, but it has real consequences:
- Affects laser cavity resonance frequencies
- Important in nonlinear optics
- Detectable with interferometry

#### 4.8 What Can You Measure?

| Parameter | Measurable with knife-edge? | Why/why not? |
|-----------|----------------------------|--------------|
| $w(z)$ | ✓ Yes | Intensity profile gives width directly |
| $R(z)$ | ✗ No | Requires phase measurement (interferometry) |
| $\zeta(z)$ | ✗ No | Requires phase measurement |

**Good news:** If you measure $w(z)$ at multiple positions, you can determine $w_0$ and calculate everything else!

---

### 5. Physical Intuition (10 min)

#### 5.1 The Uncertainty Principle Connection

There's a deep reason beams diverge:

$$\Delta x \cdot \Delta p_x \geq \frac{\hbar}{2}$$

A narrow waist ($\Delta x$ small) requires a spread in transverse momentum ($\Delta p_x$ large), which means divergence.

**Result:** Tighter focus → faster divergence. You can't beat diffraction!

#### 5.2 Divergence Angle

In the far field ($z \gg z_R$), the beam diverges at a constant half-angle:

$$\theta = \frac{\lambda}{\pi w_0}$$

**Smaller waist → larger divergence** (inverse relationship)

#### 5.3 Scaling Relationships — Think-Pair-Share

**Activity 1:** (90 seconds)

*[Display on screen: $z_R = \pi w_0^2/\lambda$ and $\theta = \lambda/(\pi w_0)$]*

**Turn to your neighbor and work out:** If you double the beam waist $w_0$, what happens to:
- The Rayleigh range $z_R$?
- The divergence angle $\theta$?

*[Give students 60-90 seconds to discuss, then ask for volunteers]*

**Answers:**
- $z_R$ **quadruples** ($z_R \propto w_0^2$)
- $\theta$ **halves** ($\theta \propto 1/w_0$)

**Physical meaning:** A wider beam stays collimated longer but eventually diverges less. You can't have both small waist AND slow divergence!

---

**Activity 2:** (60 seconds)

**Quick poll — raise your hand:**

You switch from red light ($\lambda = 633$ nm) to blue light ($\lambda = 450$ nm), keeping $w_0$ the same.

Does the beam diverge **faster** or **slower**?

*[Take a show of hands, then reveal]*

**Answer:** The beam diverges **slower** with blue light (smaller $\lambda$ means smaller $\theta$).

Also, $z_R$ is **longer** ($z_R \propto 1/\lambda$) — the beam stays collimated over a longer distance.

**Practical note:** This is why blue lasers can create tighter focus spots in optical data storage (Blu-ray vs DVD).

#### 5.4 Energy Conservation Check

As the beam expands, width $w(z)$ increases. Total power is constant.

**Question:** How does peak intensity $I_{max}$ scale with $z$?

**Answer:** Intensity $\propto$ Power/Area $\propto 1/w^2(z)$

At large $z$: $w \propto z$, so $I_{max} \propto 1/z^2$ (inverse square law!)

---

### 6. Connecting to Your Measurements (3 min)

#### What You'll Do in Week 3-4

1. **Measure** $w$ at multiple positions $z$
2. **Fit** to $w(z) = w_0\sqrt{1 + ((z-z_w)/z_R)^2}$
3. **Extract** $w_0$ (waist size) and $z_w$ (waist position)
4. **Test** whether the model describes your beam

#### The Fitting Function

The waist might not be at $z = 0$, so use:

$$w(z) = w_0 \sqrt{1 + \left(\frac{z - z_w}{z_R}\right)^2}$$

where $z_w$ is the waist position and $z_R = \pi w_0^2/\lambda$.

**Two fit parameters:** $w_0$ and $z_w$ (since $\lambda$ is known)

---

### 7. Summary (2 min)

#### Key Takeaways

1. **Gaussian beams are solutions** to Maxwell's equations under the paraxial approximation
2. **Slowly-varying envelope approximation:** Beam shape changes slowly compared to wavelength
3. **Four parameters** describe the beam: $w_0$, $w(z)$, $R(z)$, $\zeta(z)$
4. **Rayleigh range** $z_R = \pi w_0^2/\lambda$ sets the length scale
5. **Tighter focus = faster divergence** (you can't beat diffraction)
6. **$w(z)$ is what you'll measure**; from it, you can calculate everything else

#### For the Prelab

You will:
- Work through the derivation yourself (Equations 1-7 in the lab guide)
- Answer physical intuition questions
- Modify equations for waist at arbitrary position $z_w$

The prelab guides you step-by-step. Today's lecture gives you the roadmap.

---

## Suggested Board Work

1. Wave equation and plane wave solution
2. Trial solution with slowly-varying envelope
3. Paraxial wave equation (boxed)
4. Gaussian beam diagram with $w_0$, $w(z)$, wavefronts
5. $w(z)$ formula and graph (hyperbolic shape)
6. Rayleigh range calculation example
7. Scaling relationships table

---

## Key Equations to Display/Derive

| Equation | Number | Derive or State? |
|----------|--------|------------------|
| Wave equation | (1) | State |
| Trial solution with envelope | (3) | State |
| After substitution | (5) | Show key step |
| Slowly-varying approximation | (6) | Explain |
| Paraxial wave equation | (7) | **Derive** |
| Gaussian beam E-field | (8) | State, explain terms |
| Beam width $w(z)$ | (9) | **Emphasize** |
| Radius of curvature $R(z)$ | (10) | State |
| Gouy phase $\zeta(z)$ | (11) | Mention briefly |
| Rayleigh range $z_R$ | — | **Derive/Define** |

---

## Common Student Questions

**Q: Why is it called "paraxial"?**
A: From Greek "para" (beside) + "axis". The approximation is valid for rays/beams that stay close to the optical axis, traveling nearly parallel to it.

**Q: What if the slowly-varying approximation breaks down?**
A: For very tightly focused beams (small $w_0$, large angles), you need full vector diffraction theory. This matters for microscope objectives with high numerical aperture.

**Q: Is the Gaussian beam the only solution?**
A: No! There are higher-order Gauss-Hermite and Gauss-Laguerre modes. Lasers usually operate in the fundamental Gaussian mode because it has the lowest loss.

**Q: How does a laser produce a Gaussian beam?**
A: The laser cavity (two mirrors) selects the mode that best matches the mirror curvature. The fundamental Gaussian mode typically has the lowest loss and dominates.

**Q: What's the relationship between beam width $w$ and the FWHM I might see elsewhere?**
A: FWHM (full width at half maximum) $\approx 1.18 \times w$ for a Gaussian. Our $w$ is the $1/e^2$ radius of intensity.

---

## Connections to Other Courses

- **E&M (PHYS 3310):** Maxwell's equations, wave equation
- **Optics (PHYS 3330):** Interference, diffraction
- **Quantum Mechanics (PHYS 3220):** Same math as harmonic oscillator solutions; uncertainty principle connection
- **Math Methods:** Partial differential equations, separation of variables

---

## Optional: Demonstration Ideas

1. **Beam profiler camera:** Show real-time Gaussian profile on screen
2. **Translate camera along beam:** Show width changing with $z$
3. **Compare two lasers:** Different $w_0$, different divergence
4. **Tight focus with lens:** Show rapid divergence after focus
