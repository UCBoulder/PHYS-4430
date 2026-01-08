---
title: "Python Resources for PHYS 4430"
layout: textlay
sitemap: false
permalink: /python-resources
---

# Python Resources for PHYS 4430

This page provides resources for using Python for data acquisition, analysis, and visualization in PHYS 4430.

---

## Getting Started

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1.5rem 0;">

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
<h3 style="margin-top: 0;"><a href="/PHYS-4430/python-setup">Setup & Installation</a></h3>
<p>Install Python, packages, and hardware drivers (NI-DAQmx, NI-VISA, Thorlabs Kinesis).</p>
</div>

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
<h3 style="margin-top: 0;"><a href="/PHYS-4430/python-workflows">Workflows</a></h3>
<p>Choose between JupyterLab, VS Code, and Jupyter in VS Code. When to use each.</p>
</div>

</div>

---

## Data Analysis

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 1.5rem 0;">
<h3 style="margin-top: 0;"><a href="/PHYS-4430/python-analysis">Data Analysis with Python</a></h3>
<p>Core skills for experimental physics:</p>
<ul style="margin-bottom: 0;">
<li>Python basics, NumPy arrays, file I/O</li>
<li>Plotting with Matplotlib (error bars, subplots, saving figures)</li>
<li>Curve fitting with SciPy (weighted fits, chi-squared, residuals)</li>
<li>FFT and spectral analysis</li>
<li>Error propagation with the <code>uncertainties</code> package</li>
</ul>
</div>

---

## Hardware Interfacing

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1.5rem 0;">

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
<h3 style="margin-top: 0;"><a href="/PHYS-4430/python-nidaqmx">NI-DAQmx</a></h3>
<p>Interface with the USB-6009 DAQ for voltage measurements, sampling, and continuous acquisition.</p>
</div>

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
<h3 style="margin-top: 0;"><a href="/PHYS-4430/python-visa">VISA Instruments</a></h3>
<p>Control oscilloscopes, function generators, and power supplies via PyVISA. Covers Keysight and Tektronix equipment.</p>
</div>

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem;">
<h3 style="margin-top: 0;"><a href="/PHYS-4430/python-thorlabs">Thorlabs Motors</a></h3>
<p>Control stepper motors via the Kinesis SDK for automated positioning and scanning.</p>
</div>

</div>

---

## Additional Resources

### Python Learning

- [Python Tutorial](https://docs.python.org/3/tutorial/) - Official Python documentation
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [SciPy Curve Fitting](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

### Hardware Documentation

- [NI-DAQmx Python Documentation](https://nidaqmx-python.readthedocs.io/)
- [NI USB-6009 Specifications](https://www.ni.com/en-us/support/model.usb-6009.html)
- [PyVISA Documentation](https://pyvisa.readthedocs.io/)
- [Thorlabs Kinesis Documentation](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control)

### Course Resources

- [Download Python Examples](/PHYS-4430/resources/lab-guides/gaussian-laser-beams/python/)
