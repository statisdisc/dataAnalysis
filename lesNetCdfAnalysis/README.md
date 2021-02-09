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
