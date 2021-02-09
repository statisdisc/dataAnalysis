from scipy.io import netcdf
from ..objects.lesData import lesData

def getLesData(filename, indicatorType="shallow", indicatorFunction="plume"):
    "Get LES data from NetCDF file"
    
    data = netcdf.NetCDFFile(filename, 'r')
    les = lesData(data, indicatorType=indicatorType, indicatorFunction=indicatorFunction)
    data.close()
    
    return les