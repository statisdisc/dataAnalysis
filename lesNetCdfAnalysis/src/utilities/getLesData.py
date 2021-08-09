import netCDF4
from scipy.io import netcdf
from ..objects.lesData import lesData

def getLesData(filename, id="LEM", indicatorType="shallow", indicatorFunction="plume", thetaMeanProfiles=None):
    "Get LES data from NetCDF file"
    
    # data = netcdf.NetCDFFile(filename, 'r')
    data = netCDF4.Dataset(filename)
    les = lesData(
        data, 
        id = id, 
        indicatorType = indicatorType, 
        indicatorFunction = indicatorFunction, 
        thetaMeanProfiles = thetaMeanProfiles
    )
    data.close()
    
    return les