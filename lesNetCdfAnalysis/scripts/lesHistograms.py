'''
Script for producing histograms of Large Eddy Simulation data for each height layer.
The plots also include a histogram for the updraft component.
'''
import os
import sys
import time

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGif import makeGif
from src.utilities.getLesData import getLesData
from src.plots.plotHistogram import plotLayerHistogram
from src.plots.plotHistogram import plotHistogramWithGaussian



def main():
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts=os.path.dirname(os.path.realpath(__file__)),
        folderData="/mnt/f/Desktop/LES_Data"
    )
    
    # Get Large Eddy Simulation data
    les = getLesData(os.path.join(folder.data, "mov0235_ALL_01-_.nc"))
    # les = getLesData(os.path.join(folder.data, "mov0235_ALL_01-_.nc"), indicatorFunction="basic")
    
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
    
    # Remove les data to clear memory
    totalTimesteps = len(les.t)
    totalImages = min(len(snapshot.z), 150) 
    del les
    del snapshot
    
    # Create gif animations for generated plots
    for n in xrange(totalTimesteps):
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        imageListW = []
        imageListTheta = []
        imageListQv = []
        imageListQl = []
        
        for k in xrange(totalImages):
            imageListW.append(
                os.path.join(os.path.join(folderTime, "w"), "histogram_w_{}.png".format(k+1))
            )
            imageListTheta.append(
                os.path.join(os.path.join(folderTime, "theta"), "histogram_theta_{}.png".format(k+1))
            )
            imageListQv.append(
                os.path.join(os.path.join(folderTime, "qv"), "histogram_qv_{}.png".format(k+1))
            )
            imageListQl.append(
                os.path.join(os.path.join(folderTime, "ql"), "histogram_ql_{}.png".format(k+1))
            )
        
        makeGif("histogram_w.gif", imageListW, folder=folderTime, delay=8)
        makeGif("histogram_theta.gif", imageListTheta, folder=folderTime, delay=8)
        makeGif("histogram_qv.gif", imageListQv, folder=folderTime, delay=8)
        makeGif("histogram_ql.gif", imageListQl, folder=folderTime, delay=8)



if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
