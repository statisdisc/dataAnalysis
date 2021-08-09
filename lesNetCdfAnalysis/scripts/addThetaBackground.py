'''
The potential temperature (theta) from the MONC dataset comes without the environmental
mean temperature profile. This profile must therefore be added to the high resolution data set.
'''
import os
import sys
import time
import netCDF4
import numpy as np

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.objects.lesDataMonc1D import lesDataMonc1D
from src.utilities.checkFolder import getFilesInFolder
from src.utilities.timeElapsed import timeElapsed

@timeElapsed
def addThetaBackground(
        folderData = "/mnt/c/MONC_ARM",
        indicatorMONC = "plume",
        timesMONC = [13800]
    ):
    folder = folders(
        folderScripts = os.path.dirname(os.path.realpath(__file__)),
        folderData = folderData
    )
    files = getFilesInFolder(folder.data1d, extension=".nc")
    
    dataAll = {}
    for file in files:
        print(f"\nReading file: {file}")
        
        # Get Large Eddy Simulation data
        data = netCDF4.Dataset(file)
        les = lesDataMonc1D(data)
        
        # Merge dictionaries dataAll and les
        dataAll = {**dataAll, **les.data}
    
    
    # Now update the data sets
    for n,t in enumerate(timesMONC):
        print("Processing timestep {} of {}".format(n+1, len(timesMONC)))
        
        # filenameTheta = os.path.join(folder.monc, "time_{}".format(timesMONC[n]), "profilesMean", indicatorMONC, "z_th.npz")
        filenameTheta = os.path.join(folder.monc, "time_{}".format(timesMONC[n]), "profilesMean", indicatorMONC, "z_th_uncorrected.npz")
        
        dataTheta = np.load(filenameTheta)
        dataTheta = {key:dataTheta[key] for key in dataTheta}
        
        # Save old profiles for safe-keeping
        np.savez(filenameTheta.replace("z_th.npz", "z_th_uncorrected.npz"), **dataTheta)
        
        # Add the missing mean profiles to the vertical distributions
        fields = ["av", "fluid1", "fluid2", "fluid1Min", "fluid1Max", "fluid2Min", "fluid2Max"]
        thetaMoncMean = dataTheta["av"]
        for field in fields:
            dataTheta[field] = dataAll[float(t)]["theta_mean"] - thetaMoncMean + dataTheta[field]
        
        np.savez(filenameTheta.replace("z_th_uncorrected.npz", "z_th.npz"), **dataTheta)
        

if __name__ == "__main__":
    addThetaBackground(timesMONC=np.arange(600,52200,600))
