# Week 2 Noise Lab Redesign Notes

**Date:** January 2026
**Context:** Redesigning the noise characterization portion of Week 2 lecture/lab based on equipment limitations discovered during slide review.

## The Problem Discovered

The original lab asked students to measure photodetector noise and compare to datasheet specs. However, the equipment can't actually do this:

| Gain | PDA36A Datasheet Noise | Oscilloscope Floor | DAQ Floor |
|------|------------------------|-------------------|-----------|
| 0 dB | 300 µV | ~100-500 µV | ~5 mV |
| 30 dB | 260 µV | ~100-500 µV | ~5 mV |
| 50 dB | 400 µV | ~100-500 µV | ~5 mV |
| 70 dB | 1.1 mV | ~100-500 µV | ~5 mV |

**Key insight:** At most gain settings, students would be measuring instrument noise, not photodetector noise. The DAQ noise (~5 mV) exceeds photodetector noise at ALL gain settings.

## PER Mentor Recommendations

Consulted the PER (Physics Education Research) mentor agent twice. Key guidance:

### 1. Be Transparent, Not a "Gotcha"
- Don't set students up to "discover" they can't measure what we asked
- Frame authentically: "Instruments have limitations. Characterizing them IS experimental physics."

### 2. Pivot to DAQ Noise Characterization
**Instead of:** "Measure photodetector noise and compare to datasheet"
**Do:** "Characterize the DAQ noise floor - this is what actually limits your Week 4 measurements"

This is pedagogically BETTER because:
- DAQ noise is measurable (students can actually do it)
- It's the real limitation for Week 4 beam profiling
- It's authentic experimental practice

### 3. Gain Choice Still Matters (Reframed)
Original framing: "Choose gain to minimize noise"
New framing: "Given fixed DAQ noise (~5 mV), choose gain to maximize SNR without saturating"

| Factor | How Gain Helps |
|--------|----------------|
| SNR | Signal increases, DAQ noise stays fixed → SNR improves |
| Dynamic range | Higher gain uses more ADC bits |
| Saturation | Limits maximum usable gain |

### 4. Oscilloscope as Reference Instrument
- Use oscilloscope (lower noise floor) to verify DAQ behavior
- Oscilloscope scripting with Python: make it OPTIONAL/extension, not core
- Avoid cognitive overload in Week 2

### 5. Revised Learning Objectives
1. Quantify DAQ noise characteristics (measure, compare to specs)
2. Identify which component limits system noise
3. Choose gain to optimize SNR with quantitative justification
4. Use oscilloscope as reference to validate DAQ measurements

### 6. Key Framing
> "Every instrument has limitations. Expert experimentalists characterize those limitations and design around them."

Don't frame the DAQ as "bad" - it's doing its job. The lesson is understanding your measurement chain.

## Files That Need Updating

### Lecture Slides (slides.md)
- [ ] Fix the Q&A that claims DAQ noise is "~1 mV" (it's ~5 mV)
- [ ] Update noise slides to focus on DAQ characterization
- [ ] Reframe the gain-noise tradeoff discussion
- [ ] Add transparency about what's measurable vs not

### Lab Guide (gaussian-beams-2-raw.md)
- [ ] Revise "Photodetector Noise Characterization" section
- [ ] Add DAQ noise floor measurement step (input shorted)
- [ ] Restructure predict-measure-compare around DAQ noise
- [ ] Update data tables to include "dominant noise source" column
- [ ] Revise prelab questions that assume photodetector noise is measurable

### Figure Generation (generate_figures.py)
- [ ] Update noise sources diagram - changed "From datasheet" to "Noise (RMS)" and added range
- [x] Removed legend from noise sources figure

## Predict-Measure-Compare Cycle (Revised)

### Phase 1: Characterize the DAQ
**Predict:** Calculate expected quantization noise (LSB = 20V/16384 ≈ 1.2 mV)
**Measure:** Short DAQ input, record noise statistics
**Compare:** Measured (~5 mV) vs quantization limit - why higher?

### Phase 2: Characterize Signal Chain
**Predict:** With gain G and light level L, what signal and SNR?
**Measure:** Record signal at multiple gains, calculate SNR
**Compare:** Does SNR improve with gain as predicted? Where does saturation limit?

### Phase 3: Validate with Oscilloscope
**Predict:** Oscilloscope has ~100-500 µV floor - what should we see that DAQ can't?
**Measure:** Same signal chain with oscilloscope
**Compare:** Does oscilloscope reveal structure hidden by DAQ noise?

## Other Changes Made This Session

### Slides (slides.md)
- Updated shot noise description to be more accurate (discrete charge, not just photons)
- Changed "output noise" to "Noise (RMS)" to match datasheet terminology
- Added actual noise range (~250 µV to ~1.1 mV) from datasheet

### Figures (generate_figures.py)
- Fixed aliasing phase issues (600 Hz and 900 Hz aliases need negative sign)
- Added sample rate info to aliasing figure
- Reduced 900 Hz figure size to fit on slide
- Increased font sizes on sampling comparison figure
- Removed legend from noise sources block diagram
- Color-coded sampling comparison titles (red/orange for marginal, green for good)

## References from PER Mentor
- Holmes, N. G., Wieman, C. E., & Bonn, D. A. (2015). Teaching critical thinking. PNAS
- Holmes, N. G., & Wieman, C. E. (2018). Introductory physics labs: We can do better. Physics Today
- Lewandowski, H. J., et al. (2017). Characterizing student difficulties with measurements. PRPER
