# PHYS 4430 Lecture Summary — Spring 2026 (Weeks 0-4)

> **Note:** Weeks 0-1 have been delivered. Weeks 2-4 are planned content.
>
> **Scheduling principle:** Thursday lectures prepare for next week's prelab; Tuesday lectures support that week's lab.

---

## Week 0 (Jan 7): Course Introduction ✓ Delivered

- Course philosophy: research standards vs. classroom standards
- Course structure: skills weeks (1-4), guided labs (5-10), final project (11-15)
- Gaussian laser beam intensity profile and error function introduction
- Lab notebook requirements and scanning quality standards
- Grading breakdown and policies
- Safety requirements (lasers, high voltage, radioactive sources)
- AI usage policy (permitted for coding, prohibited for generating data/text)
- Optomechanics handling and beam alignment basics

---

## Week 1 (Jan 13 & 15): Error Analysis ✓ Delivered

### Tuesday Lecture

- Standard format for presenting results: value ± uncertainty (units)
- Significant figure rules and uncertainty representation
- Types of errors: blunders, systematic, and statistical (random)
- Mean, standard deviation, and standard deviation of the mean (SDOM)
- Weighted averages for combining measurements
- Chauvenet's criterion for outlier identification
- Accuracy vs. precision distinction
- Ethical data handling (A₂ meson cautionary tale)

### Thursday Lecture

- Error propagation via partial derivatives
- Propagation rules for addition, multiplication, powers
- Linear least-squares fitting (y = A + Bx)
- Chi-square (χ²) minimization
- Gaussian/normal distribution and probability calculations
- Photoelectric effect fitting example
- Introduction to Gaussian beam fitting with error function

---

## Week 2 (Jan 21 & 23): DAQ and Gaussian Beam Theory — Planned

*Supports Lab 2 (DAQ, noise characterization) and prepares Week 3 prelab (Gaussian beam derivation)*

### Tuesday Lecture
*Supports Lab 2: DAQ and noise characterization*

- Python for data acquisition: `nidaqmx` library basics (~20 min)
- USB-6009 DAQ overview: channels, sample rates, resolution (~10 min)
- Digital sampling fundamentals and Nyquist theorem (~15 min)
- Photodetector noise sources and SNR introduction (~10 min)
  - Shot noise, Johnson noise, amplifier noise
  - Signal-to-noise ratio definition
  - Gain selection tradeoffs

### Thursday Lecture
*Prepares Week 3 prelab: Gaussian beam derivation*

- Maxwell's equations → wave equation (5 min review)
- Slowly-varying envelope approximation and motivation (~10 min)
- Paraxial wave equation derivation (~15 min)
- Gaussian beam solution (~15 min)
  - Beam waist w₀
  - Beam width w(z)
  - Radius of curvature R(z)
  - Gouy phase ζ(z)
- Rayleigh range and physical intuition (~10 min)

---

## Week 3 (Jan 28 & 30): Motor Control and Lenses — Planned

*Supports Lab 3 (motor control, automated profiling) and prepares Week 4 prelab (lens predictions)*

### Tuesday Lecture
*Supports Lab 3: Motor control and beam profiling*

- Motor controller basics (~15 min)
  - Thorlabs Kinesis SDK and pythonnet
  - Basic commands: connect, move, read position
  - Common troubleshooting
- Error propagation: from measurements to derived quantities (~15 min)
- The `uncertainties` package for automated propagation (~10 min)
- Making predictions with propagated uncertainty (~10 min)

### Thursday Lecture
*Prepares Week 4 prelab: Predictions with lenses*

- How lenses transform Gaussian beams (~15 min)
- Thin lens equation review (geometric optics) (~10 min)
- Predicting beam waist location/size after a lens (~15 min)
- Diffraction limits on focusing (~10 min)

---

## Week 4 (Feb 4 & 6): Model Testing and Presentations — Planned

*Supports Lab 4 (model testing) and prepares for upcoming presentations*

### Tuesday Lecture
*Supports Lab 4: Testing the Gaussian beam model*

- The predict-measure-compare cycle (~10 min)
- Systematic vs. random errors — deeper treatment (~15 min)
  - Identifying systematic errors from residual patterns
  - Common sources in optical experiments
- What to do when predictions and measurements disagree (~15 min)
- When to trust your data vs. question your model (~10 min)

### Thursday Lecture
*Prepares upcoming presentations*

- Presentation structure: 12 minutes (8-9 talk + 2-3 Q&A) (~20 min)
- Data presentation standards: "Plots, plots, plots" (~15 min)
  - Labeled axes, captions, error bars, visible fonts
  - Schematic diagrams preferred over photos
- Evaluation rubric walkthrough (~15 min)

---

## Key Equations

### Statistics and Error Analysis (Week 1)

| Topic | Formula |
|-------|---------|
| Standard deviation | σ = √[Σ(xᵢ - x̄)²/(N-1)] |
| SDOM | σ_mean = σ/√N |
| Weighted average | X_w = Σ(wᵢxᵢ)/Σwᵢ, where wᵢ = 1/σᵢ² |
| Error propagation | δz = √[Σ(∂z/∂qᵢ · δqᵢ)²] |
| Chi-square | χ² = Σ[(yᵢ - f(xᵢ))²/σ²] |

### Digital Sampling (Week 2)

| Topic | Formula |
|-------|---------|
| Nyquist frequency | f_N = f_s / 2 |
| Alias frequency | f_ali = \|f_sig - f_sam\| |
| Signal-to-noise ratio | SNR = V_signal / V_noise |

### Gaussian Beam Optics (Weeks 2-4)

| Topic | Formula |
|-------|---------|
| Gaussian beam intensity | I(x,y) = I₀ exp(-2(x²+y²)/w²) |
| Beam width vs. position | w(z) = w₀ √[1 + (λz/πw₀²)²] |
| Rayleigh range | z_R = πw₀²/λ |
| Radius of curvature | R(z) = z[1 + (πw₀²/λz)²] |
| Gouy phase | ζ(z) = arctan(λz/πw₀²) |
| Thin lens equation | 1/S₁ + 1/S₂ = 1/f |

---

## Historical Reference: 2025 Lecture Content

The following topics were covered in Spring 2025 when the course used LabVIEW instead of Python. This content is retained for reference but is **not part of the Spring 2026 curriculum**.

<details>
<summary>Click to expand 2025 content</summary>

### Week 2 2025: LabVIEW and Digital Sampling

- LabVIEW overview: Virtual Instruments (VIs), front panel, block diagram
- Graphical programming with controls and indicators
- DAQ Assistant for analog voltage measurement
- Signal analysis express palette (filtering, spectral analysis)

### Week 3 2025: Fourier Analysis

- Fourier series: decomposing periodic functions into sine/cosine harmonics
- Discrete Fourier Transform (DFT) for finite datasets
- Computing FFT in Mathematica
- Michelson interferometer data analysis example

### Week 4 2025: Presentation Guidelines

- Scientific communication framework
- Presentation evaluation rubric

</details>
