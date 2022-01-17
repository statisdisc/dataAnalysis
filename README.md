# Data analysis, data science and data visualisation
This README summarises some data related projects over the years, including:
- Analysis of weather simulation data to extract the properties of clouds.
- Bespoke data visualisations for a state-of-the-art model of the atmosphere, due to be published shortly.
- Analysis of the items from the Steam Market to inform investment strategies.
- Analysis of conservation properties of numerical methods.

Explanations and examples of some of these projects are given below. Additional projects are also available to view in the [modelling and simulation repository](https://github.com/statisdisc/modellingAndSimulation).

<br>&nbsp;<br>
<br>&nbsp;<br>
# lesNetCfdAnalysis - Analysing weather simulation data
This project involves the analysis of over 150 GB of weather simulation data in order to analyse and model the properties of convective clouds and the thermals which produce them. The weather simulation data is used to diagnose the mean properties of clouds relative to the surrounding environment, as well as create statistical models for the physical processes which occur at the cloud boundaries (such as entrainment and detrainment, which can be modelled with probability density functions [as described in the Thesis: McIntyre (2020)](https://centaur.reading.ac.uk/95351/)).

## Installation
Clone the repository using
```
git clone "https://github.com/statisdisc/dataAnalysis"
```
or
```
git clone "https://github.com/statisdisc/dataAnalysis/lesNetCdfAnalysis"
```
To create gif animations, [ImageMagick](https://imagemagick.org/script/download.php) is required.
If you get a ```cache resources exhausted``` error when compiling gifs, you may need to increase the allowed resources for ImageMagick. Do this by edition the policy.xml file (which may be located in /etc/ImageMagick-VERSION/) from
```
<policy domain="resource" name="memory" value="256MiB"/>
<policy domain="resource" name="disk" value="1GiB"/>
```
to
```
<policy domain="resource" name="memory" value="1GiB"/>
<policy domain="resource" name="disk" value="4GiB"/>
```
for example, depending on your system's resources.

## Usage
Example scripts and usage is provided in the [lesNetCfdAnalysis/scripts/](scripts/) folder.
Run a script using
```
cd lesNetCfdAnalysis/scripts/
python scriptName.py
```
Image and animation outputs are located in ```lesNetCfdAnalysis/outputs/```

## Example results

### Cloud structure contours
Clouds can be visualised by plotting regions of (condensed) liquid water in the atmosphere:
<img width="100%" src="/readmeImages/contour_150_xz_cloud.png">
The underlying thermal structure or 'roots' of the clouds can be seen (red) using the methods from [Efstathiou et al. (2019)](https://link.springer.com/article/10.1007/s10546-019-00480-1):
<img width="100%" src="/readmeImages/contour_150_xz_cloud+thermal.png">
The regions of ascending air, fluid definition used by [Weller et al. (2020)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019MS001966), can also be plotted (white):
<img width="100%" src="/readmeImages/contour_150_xz_cloud+thermal+updraft.png">

<br>&nbsp;<br>
<br>&nbsp;<br>
### Properties of different features
By splitting the data into clouds/thermals (red) and downdraft regions, we can see that these features have substantially different properties. These differing properties can be modelled as a bi-Gaussian joint probability function, as described in [chapter 5 of McIntyre (2020)](https://centaur.reading.ac.uk/95351/).
<div style="display:inline-block"><img width="40%" src="/readmeImages/profile_w.png"><img width="40%" src="/readmeImages/histogram_w_25.png"></div>
<div style="display:inline-block"><img width="40%" src="/readmeImages/profile_ql.png"><img width="40%" src="/readmeImages/histogram_qv_66.png"></div>



<br>&nbsp;<br>
<br>&nbsp;<br>
# steamMarketAnalysis - Annual variation of cases on the Steam Market
Analysis and visualisation of item prices on the Steam Market to highlight trends and patterns. 
The analysis shows some clear annual trends. The main conclusion is that it is advantageous to buy items in December and sell mid-Summer.

## Prerequisites
Python 2.7 with NumPy, SciPy and Matplotlib installed.

## Output
<img src="/readmeImages/AnnualCaseVariation.png">



<br>&nbsp;<br>
<br>&nbsp;<br>
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



<br>&nbsp;<br>
<br>&nbsp;<br>
# formulaOneMySqlAnalysis - Analysing results from all formula 1 seasons
Images to be uploaded soon.
