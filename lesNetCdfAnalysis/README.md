# lesNetCfdAnalysis - Analysing LES data from NetCFD
Analysing LES data from NetCFD for cloud properties and other statistics.

## Installation
Clone the repository using
```
git clone "https://github.com/statisdisc/dataAnalysis"
```
or
```
git clone "https://github.com/statisdisc/dataAnalysis/lesNetCdfAnalysis"
```
Use the package manager ```pip``` to install the Python modules which are required:

```pip install -r requirements.txt```
or
```pip3 install -r requirements.txt```


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

### Properties of different features
By splitting the data into clouds/thermals (red) and downdraft regions, we can see that these features have substantially different properties.
<div style="display:inline-block"><img width="40%" src="/readmeImages/profile_w.png"><img width="40%" src="/readmeImages/histogram_w_25.png"></div>
<div style="display:inline-block"><img width="40%" src="/readmeImages/profile_ql.png"><img width="40%" src="/readmeImages/histogram_qv_66.png"></div>
