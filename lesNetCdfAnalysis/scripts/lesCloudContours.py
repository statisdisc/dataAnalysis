'''
Script for producing contour plots which show the location of clouds.
Some plots also show the thermal structure - the roots of the clouds.
Some plots show all regions of ascending air.
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
from src.utilities.timeElapsed import timeElapsed
from src.plots.plotThermalContour import plotThermalContour


@timeElapsed
def main(generateGif=False, id="LEM", indicatorFunction="basic", netcdfFile=None):
    
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
        raise ValueError(f"id {id} is not valid. Use LEM or MONC.")
    
    if netcdfFile:
        files = [os.path.join(folder.data, netcdfFile)]
    else:
        # Find all NetCFD files in 
        files = getFilesInFolder(folder.data, extension=".nc")
    
    
    for file in files:
        print(f"\nProcessing file: {file}")
        
        # Get Large Eddy Simulation data
        les = getLesData(
            file, 
            id = id,
            indicatorFunction = indicatorFunction
        )
        
        # Create plots for each snapshot in time
        for n in range(len(les.t)):
            folderTime = os.path.join(folder.outputs, "time_{}".format(int(les.t[n])))
            if not os.path.isdir(folderTime):
                os.makedirs(folderTime)
            
            snapshot = les.data[n]
            
            # Which layers of the 3D data set do we want to plot?
            imagesIndices = range(0, min(len(snapshot.x),len(snapshot.y)), 50)
            
            '''# Plot slices at fixed locations on the z-axis
            for k in range(0, len(snapshot.z), 10):
                layer = snapshot.z[k]*1e-3
                title = "z = {:.2f}km (id={})".format(layer, k+1)
                print "XY layer {} ({})".format(k+1, title)
                
                plotThermalContour(
                    snapshot.x*1e-3,
                    snapshot.y*1e-3,
                    snapshot.ql.field[k,:,:],
                    id="{}_xy_cloud+updraft".format(k),
                    title=title,
                    xlabel="x (km)",
                    ylabel="y (km)",
                    xlim=[-10.,10.],
                    ylim=[-10.,10.],
                    velocityVectorsOnly = True,
                    folder=folderTime,
                    I2=snapshot.I2.field[k,:,:],
                    u=(snapshot.u.field-0*np.mean(snapshot.u.av))[k,:,:],
                    w=(snapshot.v.field-0*np.mean(snapshot.v.av))[k,:,:]
                )'''
            # Plot slices at fixed locations on the y-axis
            for j in imagesIndices:
                layer = snapshot.y[j]*1e-3
                title = "y = {:.2f}km (id={})".format(layer, j+1)
                print("XZ layer {} ({})".format(j+1, title))
                
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
                    # id="{}_xz_cloud+thermal+edge".format(j),
                    title=title,
                    xlabel="x (km)",
                    folder=folderTime,
                    I2=snapshot.I2.field[:,j,:]
                )
                
                # Plot including regions of positive vertical velocity (updrafts)
                plotThermalContour(
                    snapshot.x*1e-3,
                    snapshot.z*1e-3,
                    snapshot.ql.field[:,j,:],
                    id="{}_xz_cloud+updraft".format(j),
                    title=title,
                    xlabel="x (km)",
                    folder=folderTime,
                    # u=(snapshot.v.field-snapshot.v.av[:,None,None])[:,j,:],
                    w=snapshot.w.field[:,j,:]
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
                
        
        
        # Remove les data to clear memory
        totalTimesteps = len(les.t)
        del les
        del snapshot
        
        # Create gif animations for generated plots
        if generateGif:
            for n in range(totalTimesteps):
                folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
                imageListContourXZ = []
                
                for k in imagesIndices:
                    print(k)
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
                
                    makeGif("contour_{}_xz.gif".format(k), imageListContourXZ, folder=folderTime, delay=200)

if __name__ == "__main__":
    # id = "LEM"
    id = "MONC"
    
    netcdfFile = ""
    # netcdfFile = "mov0235_ALL_01-_.nc"
    # netcdfFile = "mov0235_ALL_01-z.nc"
    netcdfFile = "diagnostics_3d_ts_32400.nc"
    
    main(generateGif=False, id=id, indicatorFunction="plume", netcdfFile=netcdfFile)
    # main(generateGif=False, indicatorFunction="plumeEdge")
    # main(generateGif=False, indicatorFunction="plumeEdgeEntrain")
    # main(generateGif=False, indicatorFunction="plumeEdgeDetrain")
