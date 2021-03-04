# Analysis of numerical methods for multi-fluid convection
Multi-fluid convection modelling is an emerging field in Meteorology due to its consistency at both high, low and intermediate model resolutions.
However, multi-fluid schemes have numerical schemes which are very sensitive to the coupling choices between fluids.
As such, it is more important than usual to have accurate and conservative numerical schemes for the transfer processes.
This programme analyses the energy and momentum conservation properties of 20 possible numerical schemes.

These results are published in [McIntyre et al. (2020)](https://doi.org/10.1002/qj.3728).

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## Outputs

<br>&nbsp;<br>
<b>Momentum conservation properties</b>

Schemes with solid lines conserve momentum to within machine precision.

<img width="75%" src="/readmeImages/conservation_momentum.PNG">

<br>&nbsp;<br>
<br>&nbsp;<br>
<b>Energy conservation properties</b>

Schemes with solid lines are energy-diminishing - an important property for stability.

<img width="60%" src="/readmeImages/conservation_energy.PNG">
