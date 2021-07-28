'''
Plot the vertical profiles of various fields in the Large Eddy Simulation (LES) data
for comparison with Single Column Models (SCMs).
'''
import os
import sys
import time

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.checkFolder import getFilesInFolder
from src.utilities.getLesData import getLesData
from src.plots.plotVerticalProfile import plotVolumeFraction
from src.plots.plotVerticalProfile import plotVerticalProfile
from src.plots.plotVerticalProfile import plotVerticalFluxes


def main(id="LEM", indicatorFunction="basic", netcdfFile=""):
    
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
        raise ValueError(f"id {id} is not valid.")
    
    if netcdfFile == "":
        # Find all NetCFD files in 
        files = getFilesInFolder(folder.data, extension=".nc")
    else:
        files = [os.path.join(folder.data, netcdfFile)]
    
    
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
            print(snapshot.I2.av)
            plotVolumeFraction(
                snapshot.z, snapshot.I2,
                folder=folderTime,
                id=indicatorFunction
            )
            
            # Mean profiles
            plotVerticalProfile(
                snapshot.z, snapshot.u,
                title="Horizontal velocity", 
                xlabel="u (m/s)", 
                folder=folderTime,
                id=indicatorFunction,
                plotZero=True
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.v,
                title="Horizontal velocity", 
                xlabel="v (m/s)", 
                folder=folderTime,
                id=indicatorFunction,
                plotZero=True
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.w,
                title="Vertical velocity", 
                xlabel="w (m/s)", 
                folder=folderTime,
                id=indicatorFunction,
                plotZero=True
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.theta,
                title="Potential temperature", 
                xlabel="theta (K)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.qv,
                title="Water vapour", 
                xlabel="$q_v$ (kg/kg)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.ql,
                title="Liquid water", 
                xlabel="$q_l$ (kg/kg)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.qr,
                title="Radioactive tracer", 
                xlabel="$q_r$ (kg/kg)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            # Vertical fluxes
            plotVerticalFluxes(
                snapshot.z, snapshot.u,
                title="Horizontal velocity fluxes", 
                xlabel="$\\overline{w'u'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalFluxes(
                snapshot.z, snapshot.v,
                title="Horizontal velocity fluxes", 
                xlabel="$\\overline{w'v'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalFluxes(
                snapshot.z, snapshot.theta,
                title="Potential temperature fluxes", 
                xlabel="$\\overline{w'\\theta'}$ (K m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalFluxes(
                snapshot.z, snapshot.qv,
                title="Water vapour fluxes", 
                xlabel="$\\overline{w'q_v'}$ (kg/kg m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalFluxes(
                snapshot.z, snapshot.ql,
                title="Liquid water fluxes", 
                xlabel="$\\overline{w'q_l'}$ (kg/kg m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )

if __name__ == "__main__":
    timeInit = time.time()
    
    id = "LEM"
    # id = "MONC"
    
    netcdfFile = ""
    # netcdfFile = "mov0235_ALL_01-_.nc"
    # netcdfFile = "mov0235_ALL_01-z.nc"
    # netcdfFile = "diagnostics_3d_ts_30000.nc"
    
    # main(id=id, indicatorFunction="basic", netcdfFile=netcdfFile)
    main(id=id, indicatorFunction="plume", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="plumeEdge", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="plumeEdgeEntrain", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="plumeEdgeDetrain", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="dbdz", netcdfFile=netcdfFile)
    
    timeElapsed = time.time()
    print("Elapsed time: {:.2f}s".format(timeElapsed-timeInit))
