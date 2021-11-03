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
def lesCloudContours(
        id                = "LEM", 
        caseStudy         = "ARM", 
        indicatorFunction = "plume", 
        netcdfFile        = None, 
        interval          = 1,
        generateGif       = False, 
        greyscale         = False,
        plotCloud         = False,
        plotThermals      = True,
        plotVelocity      = False,
        plotAll           = False
    ):
    '''
    Plot cross sections of clouds and their underlying structures.
    
    :param id: The simulation source type, set to either "ARM" or "MONC", str.
    :param caseStudy: The name of the case study to be plot, str.
    :param indicatorFunction: The type of structure to overlay onto the cloud, str.
    :param netcdfFile: Specify the netcdf file to open (all files processed if none selected), str.
    :param interval: Gap between layers to be plotted (1 means every layer plotted), int.
    :param generateGif: Compose all generated images into an animation cycling through the layers, bool.
    :param plotCloud: If True generate plot showing only the clouds, bool.
    :param plotThermals: If True generate plot showing cloud and the chosen indicatorFunction, bool.
    :param plotVelocity: If True generate plot showing cloud and the vertical velocity, bool.
    :param plotAll: If True generate plot showing all the features above, bool.
    '''
    
    # Fetch folders for code structure
    if id == "LEM":
        folder = folders(
            id = id,
            folderScripts = os.path.dirname(os.path.realpath(__file__)),
            folderData = "/mnt/f/Desktop/LES_Data"
        )
    elif id == "MONC":
        folder = folders(
            id = f"{id}_{caseStudy}",
            folderScripts = os.path.dirname(os.path.realpath(__file__)),
            folderData = f"/mnt/c/{id}_{caseStudy}"
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
            print("\nProcessing timestep {} (t = {:.2f}hrs,  t = {:.1f}s)".format(n+1, float(les.t[n])/3600., float(les.t[n])))
            
            folderTime = os.path.join(folder.outputs, "time_{}".format(int(les.t[n])))
            if not os.path.isdir(folderTime):
                os.makedirs(folderTime)
            
            snapshot = les.data[n]
            
            # Which layers of the 3D data set do we want to plot?
            imagesIndices = range(0, min(len(snapshot.x),len(snapshot.y)), interval)
            
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
                title = f"t = {float(les.t[n])/3600:.2f} hours, y = {layer:.2f} km"
                print(f"XZ layer {j+1} ({title})")
                
                # Plot with only clouds
                if plotCloud:
                    plotThermalContour(
                        snapshot.x*1e-3,
                        snapshot.z*1e-3,
                        snapshot.ql.field[:,j,:],
                        id="{}_xz_cloud".format(j),
                        title=title,
                        xlabel="x (km)",
                        folder=folderTime,
                        greyscale=greyscale
                    )
                
                # Plot including structure of thermals below clouds
                if plotThermals:
                    plotThermalContour(
                        snapshot.x*1e-3,
                        snapshot.z*1e-3,
                        snapshot.ql.field[:,j,:],
                        id="{}_xz_cloud+thermal".format(j),
                        # title=title,
                        xlabel="x (km)",
                        folder=folderTime,
                        I2=snapshot.I2.field[:,j,:],
                        greyscale=greyscale
                    )
                
                # Plot including regions of positive vertical velocity (updrafts)
                if plotVelocity:
                    plotThermalContour(
                        snapshot.x*1e-3,
                        snapshot.z*1e-3,
                        snapshot.ql.field[:,j,:],
                        id="{}_xz_cloud+updraft".format(j),
                        title=title,
                        xlabel="x (km)",
                        folder=folderTime,
                        # u=(snapshot.v.field-snapshot.v.av[:,None,None])[:,j,:],
                        w=snapshot.w.field[:,j,:],
                        greyscale=greyscale
                    )
                
                # Plot including clouds, structure of thermals and vertical velocity
                if plotAll:
                    plotThermalContour(
                        snapshot.x*1e-3,
                        snapshot.z*1e-3,
                        snapshot.ql.field[:,j,:],
                        id="{}_xz_cloud+thermal+updraft".format(j),
                        title=title,
                        xlabel="x (km)",
                        folder=folderTime,
                        I2=snapshot.I2.field[:,j,:],
                        w=snapshot.w.field[:,j,:],
                        greyscale=greyscale
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
    
    netcdfFile = None
    # netcdfFile = "mov0235_ALL_01-_.nc"
    # netcdfFile = "mov0235_ALL_01-z.nc"
    netcdfFile = "diagnostics_3d_ts_10800.nc"
    # netcdfFile = "diagnostics_3d_ts_21600.nc"
    # netcdfFile = "diagnostics_3d_ts_32400.nc"
    
    indicatorFunction="plume"
    # indicatorFunction="plumeEdge"
    
    lesCloudContours(id=id, indicatorFunction=indicatorFunction, netcdfFile=netcdfFile, greyscale=True)
    # lesCloudContours(id=id, indicatorFunction=indicatorFunction, netcdfFile=netcdfFile, greyscale=False)
