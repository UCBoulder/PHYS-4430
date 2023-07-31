---
title: "Gaussian Beams - Week 3"
---

# Overview

The third week of the Gaussian Beams lab will be building upon the VI you created in the second week. We will focus on properly setting up the VI and using it to its full potential for data collection in future experiments. We will then add and use spectral analysis tools that will do the Fourier Transform for us in real time. This will allow us to quickly vary parameters and see how they affect the Fourier Transform. Be sure to document all of your work in your lab notebook (either by taking a photo or saving the data and plotting it in Mathematica).

# Goals

In the first part of this week's lab, you will…

1. …extend your previously developed VI to add functionality.
2. …be able to appropriately choose DAQ parameters like sample rate.
3. …explain what the DAQ measures when the sample rate is chosen differently.

The primary objectives of this second part pf this week's lab are to gain a conceptual and computational knowledge Fourier Transforms. Many methods of calculating the Fourier Transform lie within programs you are already familiar with. LabVIEW can calculate a Fourier Transform of a wave in real-time. A dataset imported into a data analysis program like Mathematica can also calculate the Fourier Transform of imported data. This lab focuses on methods that have come up in many labs in this course and in professional research.

You will gain and understanding of Fourier Transforms by…

1. …connecting mathematical formalism to basic concepts of Fourier Transforms
2. …adding spectral analysis to a LabVIEW VI to compute Fourier Transforms in real time.
3. …computing Fourier Transforms in data analysis software (Mathematica).

# Prelab 

This week's prelab builds upon our exploration in measurement uncertainty from the previous two weeks. Here we will focus on error propagation and how to display data with these uncertainties.

## Error propagation - from measured to derived quantities

The quantity of interest in an experiment is often derived from other measured quantities. An example is estimating the resistance of a circuit element from measurements of current and voltage, using Ohm’s law ($R=V/I$) to convert our measured quantities (voltage and current) into a derived quantity (resistance).

Error propagation comes in when we want to estimate the uncertainty in the derived quantity based on the uncertainties in the measured quantities. Keeping things general, suppose we want to derive a quantity $z$ from a set of measured quantities $a,b,c, \ ... \ $. The mathematical function which gives us $z$ is $z=z(a,b,c, \ ... \ )$. In general, any fluctuation in the measured quantities $a,b,c, \ ... \ $ will cause a fluctuation in $z$ according to

$$\delta z = \left( \frac{\partial z}{\partial a}\right)\delta a+\left( \frac{\partial z}{\partial b}\right)\delta b+\left( \frac{\partial z}{\partial c}\right)\delta c+ \ ...\text{.}\quad\quad$$

This equation comes straight from basic calculus. It’s like the first term in a Taylor series. It’s the linear approximation of $z(a,b,c, \ ... \ )$ near $(a_0,b_0,c_0, \ ... \ )$. However, we don’t know the exact magnitude or sign of the fluctuations, rather we just can estimate the spread in $\delta a, \delta b, \delta c, \ ... \ $, which we often use the standard deviations $\sigma_a, \sigma_b, \sigma_c, \ ... \ $ In this case, the propagated uncertainty in $z$ is:

$$\sigma_z^2 = \left( \frac{\partial z}{\partial a}\right)^2\sigma_a^2+\left( \frac{\partial z}{\partial b}\right)^2\sigma_b^2+\left( \frac{\partial z}{\partial c}\right)^2\sigma_c^2+ \ ...\text{.}\quad\quad$$

There are standard equations provided in courses like the introductory physics lab for the error in the sum, difference, product, quotient. These are all easily derived from this general formula.

## Error propagation in Mathematica

So far we have explored the use of Mathematica for basic data analysis and plotting, but Mathematica also has powerful symbolic math capabilities. One example where this can be helpful is for complicated error propagation calculations. This [Mathematica notebook](../resources/Gaussian-Laser-Beams/Uncertainty_Propagation.nb) can calculate the propagated variance in the derived quantity symbolically.

![Example of Mathematica code for error propagation.](../resources/Gaussian-Laser-Beams/error-prop-mathematica.png){#fig:error-prop-mathematica width="20cm"}

In next week's prelab, we will model a Gaussian beam’s width $w(z)$ as:

$$w(z) = w_0\sqrt{1+\left(\frac{z-z_0}{\pi w_0^2/\lambda}\right)^2}\text{.}$$

For the output beam of one of the lasers in the lab, a fit of beam width versus position gave the following fit parameters:

$$z_0 = -0.03 \pm 0.04 \ m$$

$$w_0=(1.90 \pm 0.09)\times 10^{-6} \ m$$

The wavelength is given by $\lambda = 632.8 \pm 0.1 \ nm$. 

1. Use Mathematica to estimate the uncertainty in the derived width $w(z)$ when $z$ is a distance of $2.000 \pm 0.005 \ m$ from the waist position. You will probably find it helpful to copy and modify the code given in the example Mathematica notebook.

## Error bars

The error bar is a graphical way to display the uncertainty in a measurement. In order to put error bars on a plot you must first estimate the error for each point. Anytime you include error bars in a plot you should explain how the uncertainty in each point was estimated (e.g., you “eyeballed” the uncertainty, or you sampled it $N$ times and took the standard deviation of the mean, etc.)

### Error bars in Mathematica

Creating plots with error bars in Mathematica requires the use of the `ErrorBarPlots` package. Suppose you had estimated the uncertainty at every point in a width measurement of your Gaussian laser beam to be $0.04 \ V$. This error was chosen to demonstrate the mechanics of making a plot with error bars, but the uncertainty in the actual data was probably smaller than this. Also, there is no reason to believe it was the same at low and high voltages. The data and uncertainty form a three column data set as seen in Table @tbl:example-data.

<center>

| Micrometer Position (inches) | Photodetector Voltage (V) | Estimated uncertainty (V) |
| :--------------------------: | :-----------------------: | :-----------------------: |
|            0.410             |           0.015           |           0.04            |
|            0.412             |           0.016           |           0.04            |
|            0.414             |           0.017           |           0.04            |
|            0.416             |           0.026           |           0.04            |
|            0.418             |           0.060           |           0.04            |
|            0.420             |           0.176           |           0.04            |
|            0.422             |           0.460           |           0.04            |
|            0.424             |           0.849           |           0.04            |
|            0.426             |           1.364           |           0.04            |
|            0.428             |           1.971           |           0.04            |
|            0.430             |           2.410           |           0.04            |
|            0.432             |           2.703           |           0.04            |
|            0.434             |           2.795           |           0.04            |
|            0.436             |           2.861           |           0.04            |
|            0.438             |           2.879           |           0.04            |
|            0.440             |           2.884           |           0.04            |

Table: Table of data with a fixed uncertainty used to illustrate creating plots with error bars built in to Mathematica. {#tbl:example-data}

</center>

<br>

The Mathematica code for plotting with error bars will look something like this:

```
Needs["ErrorBarPlots`"];
d = Import[“gaussian_data_with_errors.txt”, “TSV”]; 
dNew = Table[{ {d[[i,1]], d[[i,2]]}, ErrorBar[2*d[[i,3]]] }, {i,2,Length[d]}];
ErrorListPlot[dNew, FrameLabel->{"Position, x (inches)", "Photodetector output (V)"}]
```

The first line loads the `ErrorBarPlots` package. The second line is important because the error bars have to be input in a certain format. The following table gives a comparison of plotting data with and without error bars in Mathematica.

<center>

|                     No error bars                      |                       With error bars                        |
| :----------------------------------------------------: | :----------------------------------------------------------: |
| ` {% raw %}d = {{x1,y1}, {x2, y2}, ...} {% endraw %} ` | `{% raw %}d = {{{x1, y1}, ErrorBar[e1]}, {{x2, y2}, ErrorBar[e2]}, ...}{% endraw %}` |
|                  (built in function)                   |               ``` Needs["ErrorBarPlots`"];```                |
|                     `ListPlot[d]`                      |                     ` ErrorListPlot[d] `                     |

Table: Comparison of code for plotting with and without error bars in Mathematica. {#tbl:eb-comp}

</center>

<br>

### Example: Gaussian laser beam width measurement

Import [this data set](../resources/Gaussian-Laser-Beams/gaussian_data_with_errors.txt) with the uncertainties into Mathematica. Use the `ErrorBarPlots` package to reproduce a plot like Figure @fig:gauss-example.

![Plot of the provided Gaussian Beam data showing error bars.](../resources/Gaussian-Laser-Beams/gauss-example.png){#fig:gauss-example width="15cm"}

# Digital Sampling of Data

## Improving the usefulness of you existing VI

1. Modify the LabVIEW VI you created last week so that the *Number of Samples* and *Sample Rate* are now inputs on the front panel. 
2. Set up a function generator to produce a 1 kHz sine wave.
3. Connect the function generator’s output to both the oscilloscope and the DAQ to record data.

## Initial measurements

1. Set the sample rate in the LabVIEW VI to 500 samples per second and the number of samples such that it records 1 second of data.
2. Record and plot a dataset with both the oscilloscope and the DAQ. Make sure that the time range on the oscilloscope is set such that it is on the same order as the data being recorded by the DAQ.
3. Compare the two plots. What are the major differences between the two?
4. Why might one or both of these plots be giving an incorrect result? Think about the wave you are measuring and the result you are getting. How do they relate?

## Enhanced understanding

This section will guide you to understanding of Nyquist’s theorem and a more appropriate sample rate for digital data collection using the DAQ and your VI.

1. Why do you think the data from the DAQ produced a wave of lower frequency?
2. Adjust the sample rate in a way you think might provide a more accurate measurement of the wave. What do you think the measured waveform will look like this time?
3. Take a dataset, record and plot it. Did it match your predictions?
4. Now record another dataset with the function generator set to the same parameters but the sample rate set to 3000 samples per second and the number of samples set to record 1 second of data.
5. Plot this new dataset. What is the frequency of the new dataset?
6. What are the fundamental differences between the first, second, and third datasets?

## Nyquist frequency

The discrepancies between the sampled wave forms in sections above 4 can be explained by Nyquist’s theorem. It states that to accurately measure a signal by discrete sampling methods (like the DAQ) that the sampling rate must be at least twice that of the measured signal. If this were not the case, a measurement might not be taken at every interval of oscillation, a situation called “undersampling.” Sampling the signal at least twice as fast as the maximum frequency of interest ensures that at least two data points are recorded each period. 

**Definition:**

The *Nyquist Frequency* is defined to be half the sample rate.

1. **Predict** the *apparent* period (in Hz) of the signal recorded by the DAQ. **Observe** what really happens using your waveform generator, DAQ, and LabVIEW VI. **Explain** the result. Suppose the DAQ is set to 1 kS/s sample rate in all of the cases, while the waveform generator is set to:

   1. 1000 Hz
   2. 998 Hz
   3. 1004 Hz
   4. 1500 Hz
   5. 2000 Hz
   6. 1997 Hz
   7. 2005 Hz

   In understanding what is going on, it may help to draw a few periods of the wave and then indicate where the DAQ will sample the wave form.

2. You *want* to measure the random fluctuations (noise) in a signal from 0-100 Hz. 

   1. If you set the sample rate at 200 Hz, what set of frequency ranges will contribute to the noise measurement? 
   2. If you set the sample rate at 1000 Hz, what set of frequency ranges will contribute to the noise measurement? 
   3. How could you help achieve the desired measurement in 2.1 using a combination of changing the sample rate and adding filtering? Explain why your choice of sample rate and signal filter would work better. 

3. **Undersampling on the oscilloscope.** Undersampling is an issue with any device that samples data at regular discrete time intervals. This question requires the use of a Rigol DS1052E oscilloscope and a waveform generator.

   1. Figure @fig:scope-menu is copied from the Rigol Oscilloscope manual. The Horizontal menu allows you to view the actual sample rate “Sa Rate” of the digital acquisition on the scope. 
   2. Predict what should you observe if you set the waveform generator to the same frequency as the sample rate? Try it out, compare with your prediction, and explain your observations.
   3. What happens if you change the oscilloscope time scale? Or change the waveform generator frequency slightly? Try to explain what you observe.

![The horizontal menu on the Rigol DS1052E Oscilloscope.](../resources/Gaussian-Laser-Beams/scope-menu.png){#fig:scope-menu width="20cm"}

# Fourier Analysis Techniques

## Fourier Transforms

The discrete Fourier Transform of a set of data $\{y_0,y_1, ... , y_{N-1}\}$ is given by

$$Y_m=\displaystyle \sum_{n=0}^{N-1}y_n\cdot e^{-2\pi i \frac{m}{n}N}$$

The basic idea is that a Fourier Transform decomposes the data into a set of different frequency components, so the amplitude of $Y_m$ tells you how much of your signal was formed by an oscillation at the $m$-th frequency.

### Basic Fourier concepts {#sec:basic-fourier}

1. How do the units of the Fourier Transform array $Y_m$ relate to the units of the data $y_n$?
2. Does the data $y_n$ have to be taken at equally spaced intervals?
3. Is it possible for two different sets of data to have the same Fourier Transform?
4. If data set has $N$ elements, how long is the discrete Fourier Transform?

## Modifying your LabVIEW VI

Now we want to modify the LabVIEW VI we have been developing to provide a real time spectral analysis. This tool computes the Fourier Transform and scales it automatically. To do this, in the block diagram in LabVIEW, right click to get the functions palette, select express, signal analysis, then select the spectral tool. Wire the input of this block to the output from the DAQ. 

The next thing we want to do is to make the VI function more like an oscilloscope and run in real time.

### Setting up real-time spectral analysis in LabVIEW.

1.  Create a new VI or modify and old one to have the following functionality
   1. Set up a VI to take $N$ samples inside a loop (continuous acquisition).
   2. Have front panel inputs for the sample rate and number of samples.
   3. Performs a spectral analysis on the data using the “Spectral analysis assistant” during each loop.
   4. Has a stop button to end the loop.
   5. Saves the last data set acquired after pressing the stop button.

## Using your VI

This section will familiarize you with your VIs limitations as well as helping you to gain an understanding of how different parameters relate to the Fourier Transform and Fourier Space.

### Spectral analysis basics

1. Use a waveform generator to output a waveform of your choice at a frequency in the tens of kHz range and view the output on the oscilloscope and the DAQ.
2. Look at the spectral analysis in LabVIEW. How do the **frequency resolution** (frequency step size between data in the spectrum) and **maximum frequency** relate to the **sample rate** and **number of samples**? Try to find an algebraic relationship. (Hint: You may want to turn off the auto scale function on the charts axes and adjust the scale manually to see the clearest results)
3. If the data is sampled for 2 seconds at 100 Hz sample rate, what frequency does the $m$-th component of the Fourier Transform  correspond to?
4. How many points are shown in the spectral analysis plot? How does this compare to the number of points you expected in the Fourier transform (see Section @sec:basic-fourier\.4)? **Note**: The data acquired from the DAQ is always a sequence of real numbers $\{y_n\}$. Under the condition that the signal is only real numbers, it can be proved that $Y_m=Y_{N-M}^*$ so $|Y_M|=|Y_{N-m}|$, meaning the spectrum is symmetric about the $N/2$-th data point, which corresponds to the Nyquist frequency. For this reason, LabVIEW by default only plots the first half of the Fourier spectrum up to the Nyquist frequency. 

### Real-time spectral analysis of different waveforms

1. How do you expect the spectrum of a sine wave to look? How should it change as you vary the amplitude and frequency on the waveform generator? Try it.
2. How do you expect the spectrum of a square wave to look? How should it change as you vary the amplitude and frequency on the waveform generator? Try it.

(Hint: you can look up or calculate the Fourier Series of a square wave to see if the observed amplitudes agree with the mathematical prediction.)

## Fourier Analysis in Mathematica

While it is convenient and quick to use LabVIEW’s built in spectral analysis tools, sometimes you may want to analyze data after it is saved or analyze data not generated in LabVIEW. In these situations, it is good to know how to use a tool like Mathematica or MATLAB to compute the Fourier Transform. 

The Mathematica function for taking discrete Fourier Transforms of data is `Fourier[data]`, where `data` is the 1D array of your signal values. Don’t include any time column when using `Fourier`. See the Mathematica help for examples.

1. Import into Mathematica any saved data set of a period function saved from the DAQ or the oscilloscope.
2. Use the `Fourier` function to compute the discrete Fourier Transform of the signal (don’t take the Fourier Transform of the time column). 
   1. Do you expect the `Fourier` output to be real-valued or complex-valued?
3. Plot the output of the `Fourier` function. If the output is complex-valued, you want to plot `Abs[]` or `Abs[]^2`.
   1. What is the x-axis range and step-size in the plot?
   2. What frequency range and step size should be displayed on the x-axis? Answers to earlier questions might help this.

4. In Mathematica, you manually have to add the frequency column to the data. LabVIEW does it automatically. Add a frequency column to the data set (perhaps using the `Table` function) so you create a plot of the spectrum vs. frequency.
5. Does the spectral analysis you do in LabVIEW show the same spectrum at the same frequencies as you found in LabVIEW or that you expect from the settings on the waveform generator?

There are multiple ways to define the discrete Fourier transform, so it is important to know how Mathematica calculates it so that you get agreement with other software programs that also can do spectral analysis.

6. According to the Mathematica help on the `Fourier` function, what does the option `FourierParameters->{a,b}` do (see the “More Information” section)?

If you want the `Fourier` function to compute a Fourier Transform that agrees with MATLAB’s default settings, then set `FourierParameters->{-1,1}`. 

