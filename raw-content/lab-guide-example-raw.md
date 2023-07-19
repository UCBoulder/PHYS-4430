---
title: "Lab Guide Example"
---

# Math Render Test

When attempting to establish the validity of our experimental results it is always important to quantify the uncertainty. Measurement uncertainty wasn’t invented to make lab classes tedious, rather it is a core part of any experimental work that gives us a way to quantify how much we trust our results. 

A simple and rigorous way to make a measurement and estimate its uncertainty is to take $N$ measurements $\{y_1,y_2,\ ...\ ,y_N\}$ and estimate the value by the mean:

$$\overline{y} = \frac{1}{N}{\displaystyle \sum_{i=1}^{N}}y_i$$

The estimated uncertainty (standard deviation, $\sigma_y$, or variance, $\sigma_y^2$) of any one measurement is given by

$$\sigma_y^2 = \frac{1}{N-1}{\displaystyle \sum_{i=1}^{N}}(y_i-\overline{y})^2$$

While the uncertainty in the mean value $\sigma_{\overline{y}}$ is smaller and is given by

$$\sigma_{\overline{y}}^2 = \frac{\sigma_y^2}{N}$$



# Figure Reference Test

The goal of this section is to develop a measurement technique and analysis scheme to measure the width of a laser beam. The scheme will let you measure the width in one dimension. The technique is most useful for beams that have an approximately Gaussian intensity profile. You will improve and refine this technique in the upcoming weeks of this lab.

![Image link test.](../images/test/diode-characteristics.png){width="15cm"}

The basic scheme involves measuring the power in the laser beam as the beam is gradually blocked by a knife edge (razor blade) using a setup similar to Figure @fig:knife-assembley.

![Razor blade mounted on a translation stage.](https://raw.githubusercontent.com/UCBoulder/PHYS-3330/main/lab10fig/tmp.png){#fig:knife-assembley}

## Section Reference Test {#sec:analysis}

Content

## Analysis of the real data

1. Use the analysis procedures verified in section @sec:analysis to find the beam width for your data. Be sure to include the uncertainty.
2. Plot your fit together with your data to make sure it is good.

