'''
Script for producing histograms of Large Eddy Simulation data for each height layer.
The plots also include a histogram for the updraft component.
Gaussian fits are overlaid as well as comparisons with the single column model.
'''
import os
import sys
import time

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGif import makeGif
from src.utilities.getLesData import getLesData
from src.utilities.getScmData import getScmData
from src.utilities.interpolateFromArray import interpolateFromArray
from src.plots.plotHistogram import plotHistogramWithGaussian



def main():
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts=os.path.dirname(os.path.realpath(__file__)),
        folderData="/mnt/f/Desktop/LES_Data"
    )
    
    # Get Large Eddy Simulation data and Single Column Model data
    les = getLesData(os.path.join(folder.data, "mov0235_ALL_01-_.nc"))
    scm = getScmData(os.path.join(folder.data, "SCM_results.mat"))
    
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
            
            scmGaussian = {}
            scmGaussian["sigma1"] = interpolateFromArray(scm["SCM_zw"][0], snapshot.z[k], scm["SCM_sigma1w"][:,2])
            scmGaussian["sigma2"] = interpolateFromArray(scm["SCM_zw"][0], snapshot.z[k], scm["SCM_sigma2w"][:,2])
            scmGaussian["w1"] = interpolateFromArray(scm["SCM_zw"][0], snapshot.z[k], scm["SCM_w_1"][:,2])
            scmGaussian["w2"] = interpolateFromArray(scm["SCM_zw"][0], snapshot.z[k], scm["SCM_w_2"][:,2])
            scmGaussian["wVar1"] = interpolateFromArray(scm["SCM_zw"][0], snapshot.z[k], scm["SCM_ww1"][:,2])
            scmGaussian["wVar2"] = interpolateFromArray(scm["SCM_zw"][0], snapshot.z[k], scm["SCM_ww2"][:,2])
            
            # Histogram for vertical velocity, w
            plotHistogramWithGaussian(
                snapshot.w, 
                snapshot.I2, 
                layer,
                k,
                title=title,
                folder=os.path.join(folderTime, snapshot.w.name),
                scmGaussian=scmGaussian
            )
            
            # Histogram for water vapour, qv
            # plotHistogramWithGaussian(
                # snapshot.qv, 
                # snapshot.I2, 
                # layer,
                # k,
                # title=title,
                # folder=os.path.join(folderTime, snapshot.qv.name)
            # )
            
            # Histogram for liquid water, ql
            # plotHistogramWithGaussian(
                # snapshot.ql, 
                # snapshot.I2, 
                # layer,
                # k,
                # title=title,
                # folder=os.path.join(folderTime, snapshot.ql.name)
            # )
    
    # Remove les data to clear memory
    totalTimesteps = len(les.t)
    totalImages = min(len(snapshot.z), 150) 
    del les
    del snapshot
    

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
