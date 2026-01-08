# Photodetector Noise Characterization (DRAFT v5)

*This section would be added to Week 2, building on Week 1's gain/offset calibration.*

## Introduction

In Week 1, you calibrated your photodetector's gain and offset at several settings. You may have noticed that at higher gain settings, the signal becomes "noisier." This is not a flaw—it's a fundamental tradeoff in amplified photodetectors.

In this section, you will:
1. Measure the noise floor at different gain settings and compare to datasheet specifications
2. Predict how signal-to-noise ratio depends on gain, then verify experimentally
3. Select and justify a gain setting for Week 4 based on quantitative analysis

This matters because in Week 4, you will measure beam profiles where the signal varies over a wide range. Choosing the right gain setting requires balancing amplification against added noise.

## Background: Noise in Amplified Photodetectors

### Sources of Noise

The photodetector datasheet specifies "Output Noise (RMS)" at each gain setting. This noise comes from several sources:

- **Shot noise**: Random arrival times of photons, proportional to √signal
- **Johnson noise**: Thermal noise in resistors, independent of signal
- **Amplifier noise**: The transimpedance amplifier adds its own noise

At low signal levels, amplifier and Johnson noise dominate. At high signal levels, shot noise becomes significant.

### The Gain-Noise Tradeoff

Higher gain amplifies your signal, but also amplifies internal noise sources.

**Important:** Your lab station has either a **PDA36A** or **PDA36A2** photodetector. These have different noise specifications! Check the label on your detector and look up the specifications in the appropriate datasheet (both are available in the lab).

**Fill in the datasheet values for YOUR detector:**

| Gain Setting | Transimpedance (V/A) | Datasheet Noise RMS | Datasheet Bandwidth |
|-------------|---------------------|---------------------|---------------------|
| 0 dB  | _______ | _______ | _______ |
| 30 dB | _______ | _______ | _______ |
| 50 dB | _______ | _______ | _______ |
| 70 dB | _______ | _______ | _______ |

**Calculate:** What is the ratio of noise at 70 dB to noise at 0 dB for your detector? _______

*Note: The PDA36A and PDA36A2 have quite different noise characteristics—the A2 version has significantly lower noise at high gain settings. The datasheet noise values assume full bandwidth at each gain setting. Higher gain settings have lower bandwidth, which actually reduces high-frequency noise. This is one reason noise doesn't scale directly with gain. For the quasi-DC measurements in this lab, bandwidth effects are negligible.*

### Signal-to-Noise Ratio (SNR)

The signal-to-noise ratio determines measurement precision:

$$\text{SNR} = \frac{V_{\text{signal}}}{V_{\text{noise, RMS}}}$$

For meaningful measurements, you generally want SNR > 10 (distinguishable from noise) or SNR > 100 (precise measurements).

**Prelab Questions:**

*Use the datasheet values you recorded in the table above.*

1. If your photodetector signal is 10 mV at 0 dB gain, what is the approximate SNR using your detector's datasheet noise value at 0 dB? *(1-2 sentences with calculation)*

2. If you increase to 30 dB gain (~32× voltage gain), predict what happens to: (a) the signal voltage, (b) the noise voltage (use your datasheet values), and (c) the SNR. Show your calculation. *(Show numerical work for each part)*

3. At what gain setting would SNR reach a maximum? What limits SNR at very high gain? *(2-3 sentences; consider what happens when signal approaches saturation)*

## Equipment

- Thorlabs PDA36A or PDA36A2 photodetector (check which model is at your station)
- He-Ne laser with your Week 1 alignment
- Neutral density (ND) filters to attenuate beam
- Tektronix TBS2000 oscilloscope
- NI USB-6009 DAQ
- BNC cables

## Part 1: Measuring the Noise Floor

### Dark Noise Measurement

You will measure the "dark noise"—the output when no light reaches the photodetector.

1. **Block all light** from reaching the photodetector using the aperture cap. Even small amounts of ambient light will affect your measurement.

2. **Configure the oscilloscope:**
   - Connect photodetector output to CH1
   - Set vertical scale to show the noise (~1 mV/div)
   - Set horizontal scale to ~1 ms/div
   - Enable RMS measurement (Measure → Type → RMS)

3. **Measure at four gain settings:** 0 dB, 30 dB, 50 dB, and 70 dB.

**Data Table:** (Transfer your datasheet values from the Background section)

| Gain | Measured Noise RMS | Datasheet Noise | Ratio (Measured/Datasheet) |
|------|-------------------|-----------------|---------------------------|
| 0 dB  | _______ mV | _______ mV | _______ |
| 30 dB | _______ mV | _______ mV | _______ |
| 50 dB | _______ mV | _______ mV | _______ |
| 70 dB | _______ mV | _______ mV | _______ |

**In-Lab Questions:**

1. How do your measured values compare to the datasheet? If they differ by more than 50%, identify possible reasons (ambient light leaks? ground loops? cable quality?).

2. What noise ratio (70 dB / 0 dB) did you measure? How does this compare to the datasheet ratio you calculated earlier? What does this tell you about the dominant noise source?

## Part 2: Signal-to-Noise Measurement

Now add a known optical signal and measure how SNR changes with gain.

### Setup

Use your Week 1 laser alignment. Insert a neutral density filter (ND 1.0 or ND 2.0) to attenuate the beam so you get a moderate signal (~0.5 V above offset at 30 dB).

### Prediction

Before measuring, predict the SNR at each gain setting. Use your prelab calculations and Week 1 calibration data.

| Gain | Predicted Signal (V) | Predicted Noise (mV) | Predicted SNR |
|------|---------------------|---------------------|---------------|
| 0 dB  | _______ | _______ | _______ |
| 30 dB | _______ | _______ | _______ |
| 50 dB | _______ | _______ | _______ |
| 70 dB | _______ | _______ | _______ |

### Measurement

Now measure and compare to your predictions:

| Gain | Measured Signal (V) | Measured Noise (mV) | Measured SNR | Prediction Correct? |
|------|--------------------|--------------------|--------------|---------------------|
| 0 dB  | _______ | _______ | _______ | _______ |
| 30 dB | _______ | _______ | _______ | _______ |
| 50 dB | _______ | _______ | _______ | _______ |
| 70 dB | _______ | _______ | _______ | _______ |

**Important:** If your predictions and measurements disagree, do NOT adjust your analysis to force agreement. Discrepancies are scientifically valuable—they reveal either a gap in your understanding or an uncontrolled variable in your experiment. Report your actual measurements honestly and investigate the cause of any disagreement.

**In-Lab Questions:**

1. At which gain setting did you measure the highest SNR? Does this match your prediction?

2. Did any measurements saturate (signal > 4.5 V)? How does saturation affect your gain choice?

3. If your predictions were wrong, identify the source of the discrepancy.

## Part 3: Automating Noise Measurements

You will write Python code to automate noise measurements using the DAQ. This uses the same DAQ you will use in Week 4, so your noise characterization will directly apply.

### Design Decisions

Before writing code, answer these questions:

1. **Sampling parameters:** How many samples do you need to get a reliable RMS estimate? What sample rate should you use? (Hint: consider the Nyquist criterion and the noise frequencies you want to capture.)

2. **Measurement statistics:** If you take N samples, what is the uncertainty in your RMS estimate? How does this scale with N?

3. **What to measure:** The DAQ returns raw voltage samples. How will you compute: (a) the DC level, and (b) the RMS noise?

### Code Framework

Write a function that measures noise using the DAQ. Your function should:

```python
import nidaqmx
import numpy as np

def measure_noise(channel="Dev1/ai0", num_samples=???, sample_rate=???):
    """
    Measure DC level and RMS noise from the photodetector.

    Parameters:
        channel: DAQ channel connected to photodetector
        num_samples: Number of samples to acquire (you decide)
        sample_rate: Sampling rate in Hz (you decide)

    Returns:
        dc_level: Mean voltage (V)
        noise_rms: RMS noise (V)
    """
    # Your implementation here
    #
    # Hints:
    # - Use nidaqmx.Task() context manager
    # - Configure with task.ai_channels.add_ai_voltage_chan()
    # - Set timing with task.timing.cfg_samp_clk_timing()
    # - Read data with task.read()
    # - Compute statistics with numpy

    pass
```

**Implementation Questions:**

1. What values did you choose for `num_samples` and `sample_rate`? Justify your choices.

2. Run your function with the photodetector dark (capped). Compare the DAQ noise measurement to your oscilloscope measurement from Part 1. Do they agree? If not, why might they differ?

3. **Measure the DAQ's intrinsic noise floor:** Disconnect the photodetector and short the DAQ input (connect the signal wire to ground). Measure the RMS noise. This is the DAQ's contribution, independent of the photodetector. At which photodetector gain settings does this DAQ noise become significant compared to the photodetector noise?

## Part 4: Choosing Your Week 4 Gain Setting

In Week 4, you will measure beam profiles where signal varies from near-zero (beam blocked) to maximum (full beam). You need to choose a gain setting that works across this entire range.

### Your Signal Range

From your Week 1 measurements (without ND filter):

- Maximum signal (full beam): _______ V at 0 dB gain
- This corresponds to: _______ V at 30 dB, _______ V at 50 dB, _______ V at 70 dB

### The Constraints

You face two competing constraints:

1. **Saturation limit:** Signal must stay below ~4.5 V
2. **Noise floor:** Signal must be detectable above noise (SNR > 10)

### Analysis

Answer these questions to determine your optimal gain:

1. **Saturation:** At which gain settings would your maximum signal saturate? (Show calculation.)

2. **Noise floor:** During a beam profile scan, the minimum signal occurs when the beam is nearly blocked. Estimate the smallest signal you need to measure (hint: think about the Gaussian tail at 2-3 beam widths from center). At each gain setting, would this minimum signal have SNR > 10?

3. **The tradeoff:** Based on your answers, which gain setting(s) satisfy both constraints? If multiple settings work, which would you choose and why?

4. **Propagation to beam width:** This is the critical connection. Your beam width $w$ is extracted from fitting the error function to your profile data. If your voltage measurements have uncertainty $\sigma_V$ due to noise, this propagates to uncertainty $\sigma_w$ in beam width.

   For an error function fit, the uncertainty in the width parameter scales approximately as:

   $$\sigma_w \approx \frac{\sigma_V}{|dV/dx|_{\text{max}}}$$

   where $|dV/dx|_{\text{max}}$ is the maximum slope of your profile (at the beam center).

   *Note: This approximation captures the dominant effect of noise on fit precision. A rigorous treatment would use the full covariance matrix from the least-squares fit, which accounts for the number of data points and correlations between parameters. You will encounter this in Week 3's curve fitting analysis.*

   Using your Week 1 beam width measurement (~0.5 mm) and the voltage swing across the profile, estimate $\sigma_w$ for your chosen gain setting. Is this acceptable for your Week 4 measurements?

### Your Decision

**Selected gain setting for Week 4:** _______ dB

**Justification (2-3 sentences):**

_______________________________________________

_______________________________________________

## Part 5: Week 4 Validation (To Complete in Week 4)

Before your first automated beam profile scan, validate your gain choice:

1. With the beam fully blocked, acquire 100 samples. Record the mean and RMS.

2. With the beam fully exposed, acquire 100 samples. Record the mean and RMS.

3. Calculate your actual SNR at maximum signal. Does it match your Week 2 prediction?

4. If your SNR is significantly different from predicted, identify why and decide whether to adjust your gain setting.

| Measurement | Week 2 Prediction | Week 4 Actual | Agreement? |
|-------------|------------------|---------------|------------|
| Dark noise RMS | _______ mV | _______ mV | _______ |
| Max signal | _______ V | _______ V | _______ |
| SNR at max | _______ | _______ | _______ |

**Reflection Question:** What did you learn from this predict-measure-compare cycle? Consider: Was your Week 2 prediction useful for Week 4? What would you do differently if characterizing a new piece of equipment in the future?

_______________________________________________

_______________________________________________

This validation step closes the loop on your experimental decision-making process.

## Summary

In this section, you:

1. **Characterized** the photodetector's noise floor and compared to specifications
2. **Predicted and verified** how SNR depends on gain setting
3. **Made a quantitative decision** about Week 4 gain based on your measurements
4. **Connected noise to measurement uncertainty** through error propagation

The key insight: more gain is not always better. The optimal choice depends on your signal level and measurement requirements.

## Appendix: Troubleshooting

**Noise much higher than datasheet:**
- Check for ambient light leaks (cap the aperture completely)
- Verify BNC cables are properly shielded
- Check for ground loops (try different USB ports, isolate equipment)

**DAQ and oscilloscope give different noise values:**
- Different input impedances (oscilloscope 1 MΩ vs DAQ variable)
- Different sampling rates capture different noise frequencies
- DAQ has its own noise floor (you measured this in Part 3)

**SNR doesn't improve at higher gain:**
- You may be in the shot-noise-limited regime (signal-dominated noise)
- This is actually good—it means the signal is strong

**Predictions don't match measurements:**
- Check that signal isn't saturating
- Verify ND filter is properly positioned
- Account for any changes in laser alignment from Week 1
