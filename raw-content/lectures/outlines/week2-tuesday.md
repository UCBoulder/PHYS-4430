# Week 2 Tuesday Lecture: Data Acquisition and Digital Sampling

**Date:** January 20, 2026
**Duration:** 50 minutes
**Purpose:** Prepare students for Lab 2 (DAQ basics, noise characterization)

---

## Learning Objectives

By the end of this lecture, students will be able to:

1. Explain what a DAQ device does and identify its key specifications
2. Write basic Python code to read voltages using `nidaqmx`
3. State the Nyquist theorem and calculate appropriate sample rates
4. Recognize aliasing and explain why it occurs
5. Identify sources of noise in photodetector measurements
6. Calculate signal-to-noise ratio and explain its importance

---

## Lecture Outline

### 1. Introduction and Context (3 min)

**Opening question:** "Last week you measured beam width by reading voltages from the photodetector. How did you actually get those voltage values into a form you could analyze?"

- Transition from manual measurements (Week 1) to automated acquisition (Week 2-4)
- Today's lecture prepares you for this afternoon's lab
- Goal: Understand the tools and concepts before you use them

**The automation path:**
```
Photodetector → DAQ Device → Computer → Python → Analysis
```

---

### 2. What is a DAQ Device? (7 min)

#### 2.1 The Basic Concept

**Analogy:** A DAQ (Data AcQuisition device) is a "computerized voltmeter" that can take readings automatically

**Key functions:**
- **Analog-to-Digital Conversion (ADC):** Converts continuous voltage to discrete numbers
- **Timed acquisition:** Takes samples at precise intervals
- **Multiple channels:** Can read several signals simultaneously

#### 2.2 The USB-6009 Specifications

| Specification | Value | What it means |
|---------------|-------|---------------|
| Resolution | 14 bits | Voltage divided into 2^14 = 16,384 levels |
| Input range | ±10 V | Full scale voltage range |
| Sample rate | 48 kS/s max | Up to 48,000 readings per second |
| Channels | 8 single-ended / 4 differential | How many signals at once |

**Calculate together:** What is the smallest voltage change the USB-6009 can detect?
- Range = 20 V (from -10 to +10)
- Resolution = 20 V / 16,384 ≈ 1.2 mV

**Question for students:** Is 1.2 mV resolution adequate for measuring photodetector signals that vary by ~1-3 V? (Yes, plenty of resolution)

#### 2.3 Single-Ended vs Differential

*[Draw diagram on board]*

- **Single-ended:** Measure voltage between signal and ground (8 channels available)
- **Differential:** Measure voltage between two signal lines (4 channels, better noise rejection)

For this lab: Single-ended is sufficient (ai0 referenced to GND)

---

### 3. Python for Data Acquisition (10 min)

#### 3.1 The nidaqmx Library

```python
import nidaqmx
```

- National Instruments' official Python library
- Talks to NI hardware through NI-DAQmx drivers
- Handles all the low-level communication

#### 3.2 Basic Pattern: Reading a Single Voltage

```python
import nidaqmx

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    voltage = task.read()
    print(f"Voltage: {voltage:.4f} V")
```

**Walk through each line:**
1. `with nidaqmx.Task() as task:` — Creates a measurement task (auto-cleanup)
2. `task.ai_channels.add_ai_voltage_chan("Dev1/ai0")` — Configure channel ai0 on device Dev1
3. `voltage = task.read()` — Take one reading
4. Result is a floating-point number in volts

#### 3.3 Reading Multiple Samples

```python
import nidaqmx
from nidaqmx.constants import AcquisitionType

SAMPLE_RATE = 1000  # Samples per second
NUM_SAMPLES = 500   # Total samples to collect

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(
        rate=SAMPLE_RATE,
        sample_mode=AcquisitionType.FINITE,
        samps_per_chan=NUM_SAMPLES
    )
    data = task.read(number_of_samples_per_channel=NUM_SAMPLES)
```

**Key parameters:**
- `rate`: How fast to sample (samples/second)
- `sample_mode`: FINITE (fixed number) or CONTINUOUS (stream until stopped)
- `samps_per_chan`: How many samples to collect

**Result:** `data` is a Python list of voltage values

#### 3.4 Quick Check (1 min)

**Ask students:** "What would you change in this code to collect 2 seconds of data at 500 samples per second?"

*[Pause for students to think]*

**Answer:** `SAMPLE_RATE = 500` and `NUM_SAMPLES = 1000` (because 500 × 2 = 1000)

#### 3.5 Live Demo (if equipment available)

*[Note: Pre-record or pre-stage to avoid live failures]*

- Connect function generator to DAQ
- Run simple acquisition script
- Plot result with matplotlib

---

### 4. Digital Sampling Fundamentals — Part 1 (10 min)

#### 4.1 The Sampling Process

*[Draw on board: continuous sine wave with sample points marked]*

**Key insight:** We only measure the signal at discrete moments in time

- Between samples, we have no information
- The sample rate determines what frequencies we can capture

#### 4.2 The Nyquist Theorem

> **Nyquist Theorem:** To accurately capture a signal of frequency $f$, you must sample at a rate of at least $2f$.

**The Nyquist frequency** is half the sample rate:
$$f_N = \frac{f_s}{2}$$

This is the **maximum frequency** that can be correctly measured.

**Example calculation:**
- Sample rate: 1000 S/s
- Nyquist frequency: 500 Hz
- Can accurately measure signals up to 500 Hz

#### 4.3 What Happens Below Nyquist (Good)

*[Draw: sine wave sampled at 10× its frequency — reconstructs well]*

- Many samples per cycle
- Can accurately reconstruct the waveform
- Frequency is correctly determined

#### 4.4 What Happens Above Nyquist: Aliasing (Bad)

*[Draw: sine wave sampled at 1.2× its frequency — looks like lower frequency]*

**Aliasing:** High-frequency signals "masquerade" as lower frequencies

**Alias frequency formula:**
$$f_{\text{alias}} = |f_{\text{signal}} - n \cdot f_{\text{sample}}|$$

where $n$ is the nearest integer to $f_{\text{signal}}/f_{\text{sample}}$

**Demonstration example:**
- Signal: 900 Hz
- Sample rate: 1000 S/s
- Alias frequency: |900 - 1000| = 100 Hz
- The 900 Hz signal appears as 100 Hz!

#### 4.5 First Practice Examples

**Work through together:**

| Signal (Hz) | Sample Rate (S/s) | Nyquist (Hz) | Appears as (Hz) |
|-------------|-------------------|--------------|-----------------|
| 100 | 1000 | 500 | 100 ✓ |
| 400 | 1000 | 500 | 400 ✓ |
| 600 | 1000 | 500 | ? |

*[For 600 Hz: Ask students to predict before revealing]*

**Answer:** 600 Hz aliases to 400 Hz (|600 - 1000| = 400)

---

### 5. Peer Discussion Break (2 min)

**Turn to your neighbor and predict:**

"A 950 Hz signal is sampled at 1000 S/s. What frequency will it appear as in your data?"

*[Give students 60-90 seconds to discuss, then ask for answers]*

**Reveal:** 950 Hz appears as 50 Hz! (|950 - 1000| = 50)

**Bonus question:** What about exactly 1000 Hz?

**Answer:** Appears as 0 Hz (DC) — the samples always catch the same point on the wave!

---

### 6. Digital Sampling Fundamentals — Part 2 (5 min)

#### 6.1 The Key Message

**Always sample at least 2× (preferably 5-10×) the highest frequency you care about**

#### 6.2 Aliasing in This Lab

**Question:** In Lab 2, you'll measure noise. Noise contains many frequencies. If you sample at 1000 S/s, what happens to noise at 1100 Hz?

**Answer:** It aliases down to 100 Hz and adds to your measured noise at that frequency.

**Practical guidance for noise measurements:**
- Noise spectrum extends to high frequencies
- Sample fast enough that aliased noise is negligible
- Or use anti-aliasing filter (low-pass before DAQ)

---

### 7. Photodetector Noise and SNR (10 min)

#### 7.1 Why Noise Matters

- Your beam width measurement precision depends on voltage precision
- Noise in voltage → uncertainty in fitted beam width
- Understanding noise helps you make better measurements

#### 7.2 Sources of Noise in Photodetectors

*[Draw block diagram: Light → Photodiode → Amplifier → Output]*

**Three main sources:**

1. **Shot noise** (photon statistics)
   - Random arrival times of photons
   - Proportional to √(signal level)
   - Fundamental limit from quantum mechanics

2. **Johnson (thermal) noise**
   - Random motion of electrons in resistors
   - Present even with no signal
   - Proportional to √(temperature × resistance)

3. **Amplifier noise**
   - The transimpedance amplifier adds its own noise
   - Specified on datasheet as "output noise"
   - Depends on gain setting

#### 7.3 The Gain-Noise Tradeoff

| Gain Setting | Voltage Gain | Signal × | Noise × | SNR |
|--------------|--------------|----------|---------|-----|
| 0 dB | 1× | 1× | 1× | baseline |
| 30 dB | ~32× | 32× | ? | ? |
| 70 dB | ~3000× | 3000× | ? | ? |

**Key question:** Does noise scale the same as signal?

**Answer:** No! Internal noise (Johnson, amplifier) gets amplified, but shot noise depends on actual photon rate. The datasheet tells you the actual output noise at each gain.

#### 7.4 Signal-to-Noise Ratio (SNR)

$$\text{SNR} = \frac{V_{\text{signal}}}{V_{\text{noise, RMS}}}$$

**Rules of thumb:**
- SNR > 10: Signal is distinguishable from noise
- SNR > 100: Precise quantitative measurements possible
- SNR > 1000: High-precision work

#### 7.5 Worked Example: Calculating SNR

**Your photodetector setup:**
- RMS noise: 5 mV (measured with beam blocked)
- Expected signal: 1.5 V (beam fully on detector)

**Calculate SNR:**
$$\text{SNR} = \frac{1.5 \text{ V}}{0.005 \text{ V}} = 300$$

**Interpretation:** SNR = 300 means your signal is 300× larger than the noise. This is excellent for precise measurements!

**Question for students:** If you increase the gain by 10×, and both signal and noise increase by 10×, what happens to the SNR?

**Answer:** SNR stays the same! (Both numerator and denominator multiply by 10)

**But:** If the amplifier adds its own noise, increasing gain may actually *decrease* SNR. This is why you'll measure it directly in lab.

#### 7.6 The Decision You'll Make

By end of lab today, you need to choose a gain setting for Week 4.

**Constraints:**
1. Signal must not saturate (stay below ~4.5 V)
2. SNR must be high enough for precise beam width extraction
3. Higher gain → more amplified noise

**Your job:** Find the sweet spot using quantitative data!

---

### 8. Summary and Lab Preview (3 min)

#### Key Takeaways

1. **DAQ devices** convert analog voltages to digital data at precise timing
2. **nidaqmx** provides Python control of NI hardware
3. **Nyquist theorem:** Sample at ≥2× the highest frequency of interest
4. **Aliasing** makes high frequencies appear as lower frequencies
5. **Noise sources** in photodetectors: shot, Johnson, amplifier
6. **SNR** determines measurement precision

#### What You'll Do This Afternoon

1. Connect DAQ and verify it works
2. Observe aliasing with function generator
3. Measure dark noise at each gain setting
4. Compare to datasheet specifications
5. Calculate SNR for your beam conditions
6. Choose and justify a gain setting

#### One Thing to Remember

> "Your sample rate determines what frequencies you can trust. Everything above the Nyquist frequency folds back down and contaminates your data."

---

## Suggested Board Work

1. DAQ signal flow diagram
2. USB-6009 specs table
3. Nyquist sampling diagram (good vs aliased)
4. Alias frequency calculation example
5. Noise sources block diagram
6. SNR calculation example

---

## Equipment for Demos (Optional)

- USB-6009 connected to instructor laptop
- Function generator
- Oscilloscope (to show "true" signal)
- Python environment with nidaqmx, numpy, matplotlib
- Pre-written demo scripts

---

## Common Student Questions

**Q: Why not just always sample as fast as possible?**
A: More data = more storage, slower processing. Also, 48 kS/s is shared across channels. Choose appropriate rates for your application.

**Q: How do I know my device name (Dev1, Dev2, etc.)?**
A: Use NI MAX (Measurement & Automation Explorer) or the Python code shown to list devices.

**Q: What if my signal has frequencies I don't know about?**
A: Use an anti-aliasing filter (low-pass filter before the DAQ) to remove frequencies above Nyquist.

**Q: Is the photodetector noise the same as DAQ noise?**
A: No! The DAQ adds its own small noise (~1 mV), but photodetector noise at high gain (tens of mV) usually dominates.
