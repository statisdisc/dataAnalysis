from scipy.io import netcdf
from ..objects.lesData import lesData

def getLesData(filename, indicatorType="shallow"):
    "Get LES data from NetCDF file"
    
    data = netcdf.NetCDFFile(filename, 'r')
    les = lesData(data, indicatorType=indicatorType)
    data.close()
    
    return les