# Week 0 Thursday Lecture: Course Introduction

**Date:** January 7, 2026
**Duration:** 50 minutes
**Purpose:** Introduce course philosophy, structure, and expectations; preview key concepts for Week 1 lab

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Articulate the difference between "classroom standards" and "research standards" for experimental work
2. Describe the three-phase structure of the course (skills, guided labs, final project)
3. Explain why laser beams have Gaussian intensity profiles and recognize the error function
4. Identify safety requirements for working with lasers and other lab equipment
5. Demonstrate proper handling of optomechanical components
6. Locate course resources (Canvas, website, lab guides)

---

## Lecture Outline

### 1. Welcome and Course Philosophy (10 min)

#### 1.1 What is Advanced Lab?

**This course is different from other physics courses.**

In most courses:
- Problems have "right answers"
- Procedures are prescribed step-by-step
- Uncertainty is an afterthought

In Advanced Lab:
- You design experiments to test models
- Unexpected results are scientifically valuable
- Uncertainty analysis is the core skill

#### 1.2 Research Standards vs. Classroom Standards

| Classroom Standard | Research Standard |
|-------------------|-------------------|
| "Close enough" answers | Results with quantified uncertainty |
| Follow instructions | Design your own approach |
| Answer provided in back of book | Nobody knows the "right" answer |
| Graded on getting correct result | Evaluated on methodology and reasoning |

**Key message:** We're training you to do real experimental physics, not to complete exercises.

#### 1.3 The Predict-Measure-Compare Cycle

*[Draw on board: Theory → Prediction → Measurement → Comparison → (Theory refinement)]*

**The core methodology:**
1. Use theory to make a quantitative prediction (with uncertainty)
2. Design and perform a measurement (with uncertainty)
3. Compare: Do they agree within uncertainties?
4. If not: Is it measurement error or model limitation?

This cycle appears in every lab this semester.

---

### 2. Course Structure (8 min)

#### 2.1 Three Phases

| Phase | Weeks | Focus |
|-------|-------|-------|
| **Skills Development** | 1-4 | Techniques, tools, error analysis |
| **Guided Labs** | 5-10 | Two multi-week experiments |
| **Final Project** | 11-15 | Independent research project |

#### 2.2 Weekly Schedule

- **Prelabs due:** Monday 11:59 PM (before lab week begins)
- **Tuesday lecture:** Supports that week's lab work
- **Tuesday afternoon:** Lab session (3 hours)
- **Thursday lecture:** Prepares next week's prelab

**The Thursday-Monday connection:** What we cover Thursday helps you complete the prelab due the following Monday.

#### 2.3 The Gaussian Beams Sequence (Weeks 1-4)

| Week | Lab Focus | Key Skills |
|------|-----------|------------|
| 1 | Alignment, photodetector calibration | Manual measurements, uncertainty |
| 2 | Data acquisition, noise characterization | Python/DAQ, fitting basics |
| 3 | Automated beam profiling | Motor control, error propagation |
| 4 | Model testing with lenses | Predict-measure-compare |

**Why this sequence?** You'll build a complete experimental system piece by piece, ending with a real test of Gaussian beam theory.

---

### 3. Gaussian Beams: A First Look (12 min)

#### 3.1 Why Laser Beams?

*[If available: turn on He-Ne laser, show beam on card]*

Lasers produce light that:
- Is highly directional (doesn't spread much)
- Has a specific wavelength (color)
- Has a characteristic intensity profile

**Question:** What shape is the cross-section of a laser beam?

*[Show photo or diagram of beam profile]*

**Answer:** Gaussian — brightest at center, fading smoothly toward edges.

#### 3.2 The Gaussian Intensity Profile

$$I(x, y) = I_0 \exp\left(-\frac{2(x^2 + y^2)}{w^2}\right)$$

| Symbol | Meaning |
|--------|---------|
| $I_0$ | Peak intensity (at center) |
| $w$ | Beam width (radius where intensity drops to $1/e^2$ of peak) |
| $x, y$ | Transverse coordinates |

*[Draw Gaussian profile on board: bell curve shape]*

**Physical meaning:** Most of the light is concentrated within a circle of radius $w$.

#### 3.2.1 Think-Pair-Share: Blocking the Beam (2 min)

*[After showing Gaussian profile]*

**Question:** If you place an opaque edge exactly at the beam center ($x = 0$), what fraction of the total power is transmitted?

*[Give 30 seconds for individual thought, 60 seconds for pair discussion]*

**Answer:** Exactly 50% — because a Gaussian is symmetric about its center. Half the light is on each side.

**Follow-up question:** What shape will you see if you plot transmitted power vs. edge position?

*[Take a few responses]*

**Preview:** You'll get an S-shaped curve — starting at 100% (edge far from beam), ending at 0% (beam fully blocked), with 50% right at the center. That S-curve is the error function.

#### 3.3 How Will You Measure Beam Width?

**The knife-edge technique:**

1. Block the beam with a sharp edge (razor blade)
2. Move the edge across the beam in small steps
3. Measure transmitted power at each position

*[Draw on board: Gaussian beam partially blocked by edge]*

**What you measure:** The integral of the Gaussian from the edge position to infinity.

#### 3.4 The Error Function Preview

The transmitted power follows the **error function**:

$$P(x) = \frac{P_0}{2} \left[1 - \text{erf}\left(\frac{\sqrt{2}(x - x_0)}{w}\right)\right]$$

*[Draw on board: S-shaped curve of error function]*

**The structure of this equation:**
- $P_0/2$: Normalization factor (gives 50% power when edge is centered)
- $\text{erf}(...)$: The error function — an S-shaped curve that's the integral of a Gaussian
- The argument $(x - x_0)/w$ scales by beam width

In the prelab, you'll derive this step by step. Right now, focus on one thing: **the S-curve shape comes from integrating a Gaussian.**

**Key insight:** By fitting your data to this function, you can extract $w$ (the beam width).

---

### 4. Lab Notebooks and Documentation (5 min)

#### 4.1 Why Lab Notebooks Matter

- **Legal record:** In industry, notebooks establish intellectual property
- **Reproducibility:** Someone else (or future you) must be able to repeat your work
- **Debugging:** When things go wrong, the notebook helps diagnose why

#### 4.2 Notebook Requirements

**Every session should include:**
- Date and time
- Equipment used (serial numbers, settings)
- Procedures and observations
- Data (or clear reference to data files)
- Preliminary analysis and interpretation

**Scan quality matters:** Your notebook will be graded. Ensure scans are legible.

#### 4.3 Electronic Data

- Save data files with descriptive names (not `data1.csv`, `data2.csv`)
- Include metadata in file headers or companion text files
- Back up to course server or cloud storage

---

### 5. Safety Requirements (8 min)

#### 5.1 Laser Safety

**Class 3B lasers (He-Ne, 5-50 mW):**
- Never look directly into the beam
- Remove reflective jewelry
- Block stray reflections with beam stops
- Post warning signs when laser is operating

**Eye damage is permanent.** There is no safe exposure to a direct beam.

#### 5.2 Electrical Safety

- Never open equipment cases while powered
- Use proper grounding
- Report damaged cables or connectors
- High voltage sources (photomultipliers, etc.) require specific training

#### 5.3 Other Hazards

| Hazard | Labs Involved | Precautions |
|--------|---------------|-------------|
| Radioactive sources | Nuclear/particle labs | Dosimeter, handling protocols |
| High voltage | PMT experiments | Training, interlocks |
| Cryogenics | Low-temperature labs | Gloves, ventilation |
| Heavy equipment | Optics tables | Two-person lifts |

**Required:** Complete safety training modules before your first lab session.

---

### 6. Optomechanics Handling (5 min)

#### 6.1 The Equipment is Expensive

A single mirror mount costs $100-300. A motorized stage costs $1000+.

**Rule:** Handle optomechanical components with care.

#### 6.2 Key Practices

**DO:**
- Set components down gently
- Tighten screws gradually and evenly
- Keep optical surfaces clean (use lens tissue, not fingers)
- Return components to storage after use

**DON'T:**
- Over-tighten screws (strips threads)
- Touch optical surfaces
- Leave components on table edges
- Force parts that don't fit

#### 6.3 Beam Alignment Basics

*[Brief demonstration if equipment available]*

**"Walking the beam":**
1. Use two mirrors to steer the beam
2. First mirror: controls position at target
3. Second mirror: controls angle at target
4. Iterate until beam hits both alignment references

You'll practice this technique on Tuesday.

---

### 7. Course Resources and Policies (3 min)

#### 7.1 Where to Find Things

| Resource | Location |
|----------|----------|
| Lab guides, prelabs | Course website |
| Lecture slides, grades | Canvas |
| Python resources | Website → Resources |
| Equipment manuals | Lab binder or website |

#### 7.2 AI Usage Policy

**Permitted:**
- Using AI tools for debugging code
- Getting explanations of programming concepts
- Learning syntax for unfamiliar libraries

**Prohibited:**
- Having AI generate your data analysis code wholesale
- Using AI to write lab report text
- Having AI interpret your experimental results

**Philosophy:** AI is a tool for learning, not a substitute for understanding.

#### 7.3 Getting Help

- **Lab time:** Instructors circulate — ask questions!
- **Office hours:** Posted on Canvas
- **Piazza/Discussion board:** For questions between sessions

---

### 8. Summary and What's Next (2 min)

#### Key Takeaways

1. **Research standards:** Quantitative uncertainty, predict-measure-compare
2. **Course structure:** Skills → Guided labs → Final project
3. **Gaussian beams:** Intensity profile is Gaussian; you'll measure width using knife-edge technique
4. **Safety first:** Lasers can cause permanent eye damage
5. **Handle equipment carefully:** It's expensive and delicate

#### Exit Ticket (1 min)

*[Hand out index cards or use digital poll]*

**Write one sentence answering:** Why does the knife-edge measurement produce an S-shaped curve instead of a bell-shaped curve?

*[Collect as students leave — review before next class to identify misconceptions]*

**Target answer:** Because we're measuring the *integral* (cumulative sum) of the Gaussian profile, not the profile itself.

#### For the Week 1 Prelab (due Monday 11:59 PM)

The prelab asks you to:
- Review photodiode physics (photoelectric effect)
- Derive the knife-edge measurement model (error function)
- Practice basic Python: loading files, plotting data
- Answer conceptual questions about uncertainty

**Start early!** The derivation takes time.

---

## Suggested Board Work

1. Predict-measure-compare cycle diagram
2. Course structure timeline
3. Gaussian intensity profile (bell curve)
4. Knife-edge measurement setup diagram
5. Error function S-curve sketch

---

## Common Student Questions

**Q: How much Python do I need to know?**
A: Basic programming: variables, loops, functions, arrays. The prelab includes practice problems. If you struggle, come to office hours early.

**Q: What if I've never used a laser before?**
A: No prior experience required. Week 1 lab starts with guided alignment practice.

**Q: Can I work with a partner?**
A: You'll work in pairs during lab, but each student submits individual prelabs and analysis.

**Q: What calculator/software do I need?**
A: Calculations should be done in Python (provided on lab computers). A scientific calculator is fine for quick estimates.

**Q: How long are the lab sessions?**
A: Scheduled for 3 hours. Some students finish early; some need the full time. Don't schedule conflicts immediately after lab.

---

## Connections to Week 1 Lab

| Lecture Topic | Lab 1 Application |
|---------------|-------------------|
| Gaussian beam profile | Understanding what you're measuring |
| Error function | Fitting your knife-edge data |
| Safety requirements | Working with He-Ne laser |
| Optomechanics handling | Setting up alignment |
| Lab notebook standards | Recording your work |

---

## Optional: Demonstration Ideas

1. **Turn on He-Ne laser:** Show beam path, proper blocking
2. **Beam profile on card:** Show Gaussian shape (brighter center)
3. **Knife-edge demo:** Block beam with card, show power variation
4. **Optomechanics handling:** Demonstrate proper mount technique
5. **Show beam profiler output:** If available, display real Gaussian profile on screen
