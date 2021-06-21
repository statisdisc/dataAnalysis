'''
Script for producing the horizontally-averaged cloud fraction
'''
import os
import sys
import time
import numpy as np

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGif import makeGif
from src.utilities.getLesData import getLesData
from src.plots.plotCloudFraction import plotCloudFraction

# Get the vertical profile
def horizontalAverage(field):
    return np.mean(field, axis=(1,2))

# Get the vertical profile for regions where the fluid is defined (I)
def conditionalAverage(field, I):
    return np.sum(field*I, axis=(1,2))/np.sum(I, axis=(1,2))

def main(generateGif=False, indicatorFunction="basic"):
    
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts = os.path.dirname(os.path.realpath(__file__)),
        folderData = "/mnt/f/Desktop/LES_Data"
    )
    
    # Get Large Eddy Simulation data
    les = getLesData(
        os.path.join(folder.data, "mov0235_ALL_01-_.nc"), 
        indicatorFunction = indicatorFunction
    )
    
    # Create plots for each snapshot in time
    for n in range(len(les.t)):
        print(les.t[n])
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        if not os.path.isdir(folderTime):
            os.makedirs(folderTime)
        
        snapshot = les.data[n]
        
        cloud = snapshot.ql.field > 1e-5
        cloudFraction = horizontalAverage(cloud)
        cloudFraction1 = conditionalAverage(cloud, np.invert(snapshot.I2.field))
        cloudFraction2 = conditionalAverage(cloud, snapshot.I2.field)
        
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
        
        
    del les
    del snapshot
    
    

if __name__ == "__main__":
    timeInit = time.time()
    
    main(indicatorFunction="plume")
    # main(indicatorFunction="plumeEdge")
    # main(indicatorFunction="plumeEdgeEntrain")
    # main(indicatorFunction="plumeEdgeDetrain")
    
    
    timeElapsed = time.time() - timeInit
    print("Elapsed time: {timeElapsed:.2f}s")
