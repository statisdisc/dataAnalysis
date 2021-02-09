'''
Script for producing contour plots which show the location of clouds.
Some plots also show the thermal structure - the roots of the clouds.
Some plots show all regions of ascending air.
'''
import os
import sys
import time

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.makeGif import makeGif
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
        
        # Which layers of the 3D data set do we want to plot?
        imagesIndices = range(0, min(len(snapshot.x),len(snapshot.y)), 10)
        
        # Plot slices at fixed locations on the y-axis
        for j in imagesIndices:
            layer = snapshot.y[j]*1e-3
            title = "y = {:.2f}km (id={})".format(layer, j+1)
            print "XZ layer {} ({})".format(j+1, title)
            
            # Plot with only clouds
            plotThermalContour(
                snapshot.x*1e-3,
                snapshot.z*1e-3,
                snapshot.ql.field[:,j,:],
                id="{}_xz_cloud".format(j),
                title=title,
                xlabel="x (km)",
                folder=folderTime
            )
            
            # Plot including structure of thermals below clouds
            plotThermalContour(
                snapshot.x*1e-3,
                snapshot.z*1e-3,
                snapshot.ql.field[:,j,:],
                id="{}_xz_cloud+thermal".format(j),
                title=title,
                xlabel="x (km)",
                folder=folderTime,
                I2=snapshot.I2.field[:,j,:]
            )
            
            # Plot including structure of thermals and vertical velocity
            plotThermalContour(
                snapshot.x*1e-3,
                snapshot.z*1e-3,
                snapshot.ql.field[:,j,:],
                id="{}_xz_cloud+thermal+updraft".format(j),
                title=title,
                xlabel="x (km)",
                folder=folderTime,
                I2=snapshot.I2.field[:,j,:],
                w=snapshot.w.field[:,j,:]
            )
            
            # break
        
        # Plot slices at fixed locations on the x-axis
        for i in imagesIndices:
            layer = snapshot.x[i]*1e-3
            title = "x = {:.2f}km (id={})".format(layer, i+1)
            print "YZ layer {} ({})".format(i+1, title)
            
            # Plot with only clouds
            plotThermalContour(
                snapshot.y*1e-3,
                snapshot.z*1e-3,
                snapshot.ql.field[:,:,i],
                id="{}_yz_cloud".format(i),
                title=title,
                xlabel="y (km)",
                folder=folderTime
            )
            
            # Plot including structure of thermals below clouds
            plotThermalContour(
                snapshot.y*1e-3,
                snapshot.z*1e-3,
                snapshot.ql.field[:,:,i],
                id="{}_yz_cloud+thermal".format(i),
                title=title,
                xlabel="y (km)",
                folder=folderTime,
                I2=snapshot.I2.field[:,:,i]
            )
            
            # Plot including structure of thermals and vertical velocity
            plotThermalContour(
                snapshot.y*1e-3,
                snapshot.z*1e-3,
                snapshot.ql.field[:,:,i],
                id="{}_yz_cloud+thermal+updraft".format(i),
                title=title,
                xlabel="y (km)",
                folder=folderTime,
                I2=snapshot.I2.field[:,:,i],
                w=snapshot.w.field[:,:,i]
            )
    
    
    # Remove les data to clear memory
    totalTimesteps = len(les.t)
    del les
    del snapshot
    
    # Create gif animations for generated plots
    for n in xrange(totalTimesteps):
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        imageListContourXZ = []
        imageListContourYZ = []
        
        for k in imagesIndices:
            print k
            imageListContourXZ = []
            imageListContourYZ = []
            
            imageListContourXZ.append(
                os.path.join(
                    os.path.join(folderTime, "contourCloud"), 
                    "contour_{}_xz_cloud.png".format(k)
                )
            )
            imageListContourXZ.append(
                os.path.join(
                    os.path.join(folderTime, "contourCloud"), 
                    "contour_{}_xz_cloud+thermal.png".format(k)
                )
            )
            imageListContourXZ.append(
                os.path.join(
                    os.path.join(folderTime, "contourCloud"), 
                    "contour_{}_xz_cloud+thermal+updraft.png".format(k)
                )
            )
            
            imageListContourYZ.append(
                os.path.join(
                    os.path.join(folderTime, "contourCloud"), 
                    "contour_{}_yz_cloud.png".format(k)
                )
            )
            imageListContourYZ.append(
                os.path.join(
                    os.path.join(folderTime, "contourCloud"), 
                    "contour_{}_yz_cloud+thermal.png".format(k)
                )
            )
            imageListContourYZ.append(
                os.path.join(
                    os.path.join(folderTime, "contourCloud"), 
                    "contour_{}_yz_cloud+thermal+updraft.png".format(k)
                )
            )
        
            makeGif("contour_{}_xz.gif".format(k), imageListContourXZ, folder=folderTime, delay=200)
            makeGif("contour_{}_yz.gif".format(k), imageListContourYZ, folder=folderTime, delay=200)

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
