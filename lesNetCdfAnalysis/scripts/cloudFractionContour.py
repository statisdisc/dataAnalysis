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
from src.plots.plotCloudFraction import plotCloudFraction

# Get the vertical profile
def horizontalAverage(field):
    return np.mean(field, axis=(1,2))

# Get the vertical profile for regions where the fluid is defined (I)
def conditionalAverage(field, I):
    return np.sum(field*I, axis=(1,2))/np.sum(I, axis=(1,2))

def main(generateGif=False, indicatorFunction="basic", netcdfFile=""):
    
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts = os.path.dirname(os.path.realpath(__file__)),
        folderData = "/mnt/f/Desktop/LES_Data"
    )
    
    if netcdfFile == "":
        # Find all NetCFD files in 
        files = getFilesInFolder(folder.data, extension=".nc")
    else:
        files = [os.path.join(folder.data, netcdfFile)]
    
    times = []
    cloudFractions = {}
    cloudFractions1 = {}
    cloudFractions2 = {}
    cloudFractions1sigma1 = {}
    cloudFractions2sigma2 = {}
    
    counter = 0
    for file in files:
        counter += 1
        # if counter == 4:
            # break
        
        print(f"\nProcessing file {counter}: {file}")
        
        # Get Large Eddy Simulation data
        les = getLesData(
            file, 
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
            cloudFraction = horizontalAverage(cloud)
            cloudFraction1 = conditionalAverage(cloud, np.invert(snapshot.I2.field))
            cloudFraction2 = conditionalAverage(cloud, snapshot.I2.field)
            cloudFraction1sigma1 = cloudFraction1*(1-snapshot.I2.av)
            cloudFraction2sigma2 = cloudFraction2*snapshot.I2.av
            
            times.append(time)
            cloudFractions[time]  = cloudFraction
            cloudFractions1[time] = cloudFraction1
            cloudFractions2[time] = cloudFraction2
            cloudFractions1sigma1[time] = cloudFraction1sigma1
            cloudFractions2sigma2[time] = cloudFraction2sigma2
            
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
    
    cloudFraction  = np.zeros((len(cloudFractions[times[0]]),  len(times)))
    cloudFraction1 = np.zeros((len(cloudFractions1[times[0]]), len(times)))
    cloudFraction2 = np.zeros((len(cloudFractions2[times[0]]), len(times)))
    cloudFraction1sigma1 = np.zeros((len(cloudFractions1sigma1[times[0]]), len(times)))
    cloudFraction2sigma2 = np.zeros((len(cloudFractions2sigma2[times[0]]), len(times)))
    
    times = sorted(times)
    for n in range(len(times)):
        time = times[n]
        cloudFraction[:,n] = cloudFractions[time]
        cloudFraction1[:,n] = cloudFractions1[time]
        cloudFraction2[:,n] = cloudFractions2[time]
        cloudFraction1sigma1[:,n] = cloudFractions1sigma1[time]
        cloudFraction2sigma2[:,n] = cloudFractions2sigma2[time]
    
    data = {}
    data["t_cloud_fraction"] = np.array(times)
    data["z_cloud_fraction"] = z
    data["cloud_fraction"] = cloudFraction
    data["cloud_fraction1"] = cloudFraction1
    data["cloud_fraction2"] = cloudFraction2
    data["cloud_fraction1_sigma1"] = cloudFraction1sigma1
    data["cloud_fraction2_sigma2"] = cloudFraction2sigma2
    
    folder = os.path.join(folder.outputs, "cloudContour")
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    savemat(os.path.join(folder, "cloud_fraction.mat"), data)
    
    for time in times:
        print(time)
    
    

if __name__ == "__main__":
    timeInit = time.time()
    
    netcdfFile = "mov0235_ALL_01-_.nc"
    
    main(indicatorFunction="plume")
    
    timeElapsed = time.time() - timeInit
    print("Elapsed time: {timeElapsed:.2f}s")
