'''
Script for producing contour plots which show the tracers used to define thermals.
'''
import os
import sys
import time

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGif import makeGif
from src.utilities.getLesData import getLesData
from src.plots.plotTracer import plotTracer



def main():
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts=os.path.dirname(os.path.realpath(__file__)),
        folderData="/mnt/f/Desktop/LES_Data"
    )
    
    # Get Large Eddy Simulation data
    les = getLesData(os.path.join(folder.data, "mov0235_ALL_01-_.nc"))
    
    # Create plots for each snapshot in time
    for n in range(len(les.t)):
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        if not os.path.isdir(folderTime):
            os.makedirs(folderTime)
        
        snapshot = les.data[n]
        
        # Which layers of the 3D data set do we want to plot?
        imagesIndices = range(0, min(len(snapshot.x),len(snapshot.y)), 10)
        
        # Plot slices at fixed locations on the y-axis
        for j in imagesIndices:
            layer = snapshot.y[j]*1e-3
            title = "y = {:.2f}km (id={})".format(layer, j+1)
            print "XZ layer {} ({})".format(j+1, title)
            
            # Plot radioactive tracer field
            plotTracer(
                snapshot.x*1e-3,
                snapshot.z*1e-3,
                snapshot.rts.field[:,j,:],
                id="{}_xz_rts".format(j),
                title=title,
                xlabel="x (km)",
                dpi=200,
                folder=folderTime
            )
            
            # Plot radioactive tracer field with plume definition contour
            plotTracer(
                snapshot.x*1e-3,
                snapshot.z*1e-3,
                snapshot.rts.field[:,j,:],
                id="{}_xz_rts+thermal".format(j),
                title=title,
                xlabel="x (km)",
                dpi=200,
                folder=folderTime,
                I2=snapshot.I2.field[:,j,:]
            )
        
        # Plot slices at fixed locations on the x-axis
        for i in imagesIndices:
            layer = snapshot.x[i]*1e-3
            title = "x = {:.2f}km (id={})".format(layer, i+1)
            print "YZ layer {} ({})".format(i+1, title)
            
            # Plot radioactive tracer field
            plotTracer(
                snapshot.y*1e-3,
                snapshot.z*1e-3,
                snapshot.rts.field[:,:,i],
                id="{}_yz_rts".format(i),
                title=title,
                xlabel="y (km)",
                dpi=200,
                folder=folderTime
            )
            
            # Plot radioactive tracer field with plume definition contour
            plotTracer(
                snapshot.y*1e-3,
                snapshot.z*1e-3,
                snapshot.rts.field[:,:,i],
                id="{}_yz_rts".format(i),
                title=title,
                xlabel="y (km)",
                dpi=200,
                folder=folderTime,
                I2=snapshot.I2.field[:,:,i]
            )
    
    
    

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
