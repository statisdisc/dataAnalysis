'''
Script for producing histograms of Large Eddy Simulation data for each height layer.
The plots also include a histogram for the updraft component.
'''
import os
import sys
import time
import numpy as np

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.objects.lesData import lesData
from src.utilities.getLesData import getLesData
from src.plots.plotThermalContour import plotThermalContour



def main():
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts=os.path.dirname(os.path.realpath(__file__)),
        folderData="/mnt/f/Desktop/LES_Data"
    )
    
    # Get Large Eddy Simulation data
    les = getLesData(os.path.join(folder.data, "mov0235_ALL_01-_.nc"))
    
    # Create plots for each snapshot in time
    for n in xrange(len(les.t)):
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        if not os.path.isdir(folderTime):
            os.makedirs(folderTime)
        
        snapshot = les.data[n]
        
        for j in xrange(1, len(snapshot.y), 1):
            layer = snapshot.y[j]*1e-3
            title = "y = {:.2f}km (id={})".format(layer, j+1)
            print "Layer {} ({:.3f}km)".format(j+1, layer)
            
            # Plot with only clouds
            plotThermalContour(
                snapshot.ql, 
                snapshot.I2, 
                layer,
                j,
                id="cloud",
                title=title,
                folder=folderTime,
                cloudOnly=True
            )
            
            # Plot including structure of thermals below clouds
            plotThermalContour(
                snapshot.ql, 
                snapshot.I2, 
                layer,
                j,
                id="cloud+updraft",
                title=title,
                folder=folderTime
            )

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
