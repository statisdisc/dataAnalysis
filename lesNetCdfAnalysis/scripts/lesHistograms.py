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
from src.plots.plotHistogram import plotLayerHistogram



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
        
        # Create plots for each layer in the vertical
        for k in xrange(len(snapshot.z)):
            layer = snapshot.z[k]*1e-3
            title = "z = {:.2f}km (id={})".format(layer, k+1)
            print "Layer {} ({:.3f}km)".format(k+1, layer)
            
            # Histogram for vertical velocity, w
            plotLayerHistogram(
                snapshot.w, 
                snapshot.I2, 
                layer,
                k,
                title=title,
                folder=os.path.join(folderTime, snapshot.w.name)
            )
            
            # Histogram for potential temperature, theta
            plotLayerHistogram(
                snapshot.theta, 
                snapshot.I2, 
                layer,
                k,
                title=title,
                folder=os.path.join(folderTime, snapshot.theta.name)
            )
            
            # Histogram for water vapour, qv
            plotLayerHistogram(
                snapshot.qv, 
                snapshot.I2, 
                layer,
                k,
                title=title,
                folder=os.path.join(folderTime, snapshot.qv.name)
            )
            
            # Histogram for liquid water, ql
            plotLayerHistogram(
                snapshot.ql, 
                snapshot.I2, 
                layer,
                k,
                title=title,
                folder=os.path.join(folderTime, snapshot.ql.name)
            )
    

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
