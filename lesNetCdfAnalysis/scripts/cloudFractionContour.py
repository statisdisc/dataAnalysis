'''
Script for producing the horizontally-averaged cloud fraction
'''
import os
import sys
import time
import numpy as np
from scipy.io import savemat

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.checkFolder import getFilesInFolder
from src.utilities.makeGif import makeGif
from src.utilities.getLesData import getLesData
from src.utilities.timeElapsed import timeElapsed
from src.plots.plotCloudFraction import plotCloudFraction

# Get the cloud cover
def calculateCloudCover(cloud, axis=(0)):
    return np.mean(np.sum(cloud, axis=axis) > 0)

# Get the vertical profile
def horizontalAverage(field, axis=(1,2)):
    return np.mean(field, axis=axis)

# Get the vertical profile for regions where the fluid is defined (I)
def conditionalAverage(field, I, axis=(1,2)):
    return np.sum(field*I, axis=axis)/np.sum(I, axis=axis)

@timeElapsed
def cloudFractionContour(generateGif=False, id="LEM", indicatorFunction="basic", netcdfFile=None):
    
    
    # Fetch folders for code structure
    if id == "LEM":
        folder = folders(
            id = id,
            folderScripts = os.path.dirname(os.path.realpath(__file__)),
            folderData = "/mnt/f/Desktop/LES_Data"
        )
    elif id == "MONC":
        folder = folders(
            id = id,
            folderScripts = os.path.dirname(os.path.realpath(__file__)),
            folderData = "/mnt/c/MONC_ARM"
        )
    else:
        raise ValueError(f"id {id} is not valid.")
    
    if netcdfFile:
        files = [os.path.join(folder.data, netcdfFile)]
    else:
        # Get all available NetCFD files
        files = getFilesInFolder(folder.data, extension=".nc")
    
    times = []
    cloudTops = {}
    cloudBases = {}
    cloudCovers = {}
    cloudCovers1 = {}
    cloudCovers2 = {}
    cloudFractions = {}
    cloudFractions1 = {}
    cloudFractions2 = {}
    cloudFractions1sigma1 = {}
    cloudFractions2sigma2 = {}
    
    for i,file in enumerate(files):
        print(f"\nProcessing 3D file: {file} (file {i+1} of {len(files)})")
        
        # Get Large Eddy Simulation data
        les = getLesData(
            file, 
            id = id,
            indicatorFunction = indicatorFunction
        )
    
        # Create plots for each snapshot in time
        for n in range(len(les.t)):
            print("\nProcessing timestep {} (t = {:.2f}hrs,  t = {:.1f}s)".format(n+1, float(les.t[n])/3600., float(les.t[n])))
            
            time = int(les.t[n])
            folderTime = os.path.join(folder.outputs, f"time_{time}")
            if not os.path.isdir(folderTime):
                os.makedirs(folderTime)
            
            snapshot = les.data[n]
            
            z = snapshot.z
            cloud = snapshot.ql.field > 1e-5
            cloudz = np.max(snapshot.ql.field, axis=snapshot.ql.axisXY) > 1e-5
            cloudFraction = horizontalAverage(cloud, axis=snapshot.ql.axisXY)
            cloudFraction1 = conditionalAverage(cloud, np.invert(snapshot.I2.field), axis=snapshot.ql.axisXY)
            cloudFraction2 = conditionalAverage(cloud, snapshot.I2.field, axis=snapshot.ql.axisXY)
            cloudFraction1sigma1 = cloudFraction1*(1-snapshot.I2.av)
            cloudFraction2sigma2 = cloudFraction2*snapshot.I2.av
            
            times.append(time)
            if not True in cloudz:
                cloudTops[time] = 0.
                cloudBases[time] = 0.
            else:
                cloudTops[time] = np.max(z[cloudz])
                cloudBases[time] = np.min(z[cloudz])
            cloudCovers[time]  = calculateCloudCover(cloud, axis=(snapshot.keys.zi))
            cloudCovers1[time] = calculateCloudCover(cloud * np.invert(snapshot.I2.field), axis=(snapshot.keys.zi))
            cloudCovers2[time] = calculateCloudCover(cloud * snapshot.I2.field, axis=(snapshot.keys.zi))
            cloudFractions[time]  = cloudFraction
            cloudFractions1[time] = cloudFraction1
            cloudFractions2[time] = cloudFraction2
            cloudFractions1sigma1[time] = cloudFraction1sigma1
            cloudFractions2sigma2[time] = cloudFraction2sigma2
            
            print("Cloud cover: {:.3f}".format(cloudCovers[time]))
            print("Cloud base: {:.1f}m".format(cloudBases[time]))
            print("Cloud top: {:.1f}m".format(cloudTops[time]))
            
            '''
            plotCloudFraction(
                snapshot.z,
                cloudFraction,
                id = "all",
                folder = folderTime
            )
            
            plotCloudFraction(
                snapshot.z,
                cloudFraction1,
                id = "1",
                folder = folderTime
            )
            
            plotCloudFraction(
                snapshot.z,
                cloudFraction2,
                id = "2",
                folder = folderTime
            )
            '''
            
            
        del les
        del snapshot
    
    cloudTop = np.zeros_like(times, dtype=float)
    cloudBase = np.zeros_like(times, dtype=float)
    cloudCover = np.zeros_like(times, dtype=float)
    cloudCover1 = np.zeros_like(times, dtype=float)
    cloudCover2 = np.zeros_like(times, dtype=float)
    cloudFraction  = np.zeros((len(cloudFractions[times[0]]),  len(times)))
    cloudFraction1 = np.zeros((len(cloudFractions1[times[0]]), len(times)))
    cloudFraction2 = np.zeros((len(cloudFractions2[times[0]]), len(times)))
    cloudFraction1sigma1 = np.zeros((len(cloudFractions1sigma1[times[0]]), len(times)))
    cloudFraction2sigma2 = np.zeros((len(cloudFractions2sigma2[times[0]]), len(times)))
    
    times = sorted(times)
    for n in range(len(times)):
        time = times[n]
        cloudTop[n]  = cloudTops[time]
        cloudBase[n]  = cloudBases[time]
        cloudCover[n]  = cloudCovers[time]
        cloudCover1[n] = cloudCovers1[time]
        cloudCover2[n] = cloudCovers2[time]
        cloudFraction[:,n] = cloudFractions[time]
        cloudFraction1[:,n] = cloudFractions1[time]
        cloudFraction2[:,n] = cloudFractions2[time]
        cloudFraction1sigma1[:,n] = cloudFractions1sigma1[time]
        cloudFraction2sigma2[:,n] = cloudFractions2sigma2[time]
    
    data = {}
    data["t_cloud_fraction"] = np.array(times)
    data["z_cloud_fraction"] = z
    data["cloud_top"]  = cloudTop
    data["cloud_base"]  = cloudBase
    data["cloud_cover"]  = cloudCover
    data["cloud_cover1"] = cloudCover1
    data["cloud_cover2"] = cloudCover2
    data["cloud_fraction"]  = cloudFraction
    data["cloud_fraction1"] = cloudFraction1
    data["cloud_fraction2"] = cloudFraction2
    data["cloud_fraction1_sigma1"] = cloudFraction1sigma1
    data["cloud_fraction2_sigma2"] = cloudFraction2sigma2
    
    folder = os.path.join(folder.outputs, "cloudContour")
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    savemat(os.path.join(folder, "cloud_fraction.mat"), data)
    
    

if __name__ == "__main__":
    id = "LEM"
    # id = "MONC"
    
    netcdfFile = None
    # netcdfFile = "mov0235_ALL_01-_.nc"
    # netcdfFile = "mov0235_ALL_01-z.nc"
    # netcdfFile = "diagnostics_3d_ts_30000.nc"
    
    cloudFractionContour(id=id, indicatorFunction="plume", netcdfFile=netcdfFile)
