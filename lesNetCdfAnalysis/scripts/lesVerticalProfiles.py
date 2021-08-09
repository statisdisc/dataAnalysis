'''
Plot the vertical profiles of various fields in the Large Eddy Simulation (LES) data
for comparison with Single Column Models (SCMs).
'''
import netCDF4
import os
import sys
import time

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.objects.lesDataMonc1D import lesDataMonc1D
from src.utilities.checkFolder import getFilesInFolder
from src.utilities.getLesData import getLesData
from src.plots.plotVerticalProfile import plotVolumeFraction
from src.plots.plotVerticalProfile import plotVerticalProfile
from src.plots.plotVerticalProfile import plotVerticalFluxes
from src.plots.plotVerticalProfile import plotVerticalVariances


def get1dProfiles(folderData, key=None):
    files = getFilesInFolder(folderData, extension=".nc")
    
    dataAll = {}
    for file in files:
        print(f"\nReading 1D file: {file}")
        
        # Get Large Eddy Simulation data
        data = netCDF4.Dataset(file)
        les = lesDataMonc1D(data)
        
        # Merge dictionaries dataAll and les
        dataAll = {**dataAll, **les.data}
    
    if key is not None:
        dataKey = {}
        
        for time in dataAll.keys():
            dataKey[round(time)] = dataAll[time][key]
        
        return dataKey
    
    return dataAll

def main(id="LEM", indicatorFunction="basic", netcdfFile="", thetaMean=None):
    
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
        
        thetaMean = get1dProfiles(folder.data1d, key="theta_mean")
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
            indicatorFunction = indicatorFunction,
            thetaMeanProfiles = thetaMean
        )
        
        # Create plots for each snapshot in time
        for n in range(len(les.t)):
            print("\nProcessing timestep {} (t = {:.2f}hrs,  t = {:.1f}s)".format(n+1, float(les.t[n])/3600., float(les.t[n])))
            
            folderTime = os.path.join(folder.outputs, "time_{}".format(int(les.t[n])))
            if not os.path.isdir(folderTime):
                os.makedirs(folderTime)
            
            snapshot = les.data[n]
            
            # Volume fraction of fluid 2
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
                snapshot.z, snapshot.th,
                title="Potential temperature", 
                xlabel="$\\theta$ (K)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.thv,
                title="Virtual potential temperature", 
                xlabel="$\\theta_v$ (K)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.b,
                title="Buoyancy", 
                xlabel="b (m s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            plotVerticalProfile(
                snapshot.z, snapshot.q,
                title="Water vapour", 
                xlabel="$q_t$ (kg/kg)", 
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
            
            
            
            
            # Variances
            plotVerticalVariances(
                snapshot.z, snapshot.u,
                title="Horizontal velocity variance", 
                xlabel="$\\overline{u'u'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.v,
                title="Horizontal velocity variance", 
                xlabel="$\\overline{v'v'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.w,
                title="Horizontal velocity variance", 
                xlabel="$\\overline{w'w'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.th,
                title="Potential temperature variance", 
                xlabel="$\\overline{\\theta'\\theta'}$ (K$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.thv,
                title="Virtual potential temperature variance", 
                xlabel="$\\overline{\\theta_v'\\theta_v'}$ (K$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.b,
                title="Buoyancy variance", 
                xlabel="$\\overline{b'b'}$ (m$^2$/s$^4$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.q,
                title="Total moisture variance", 
                xlabel="$\\overline{q'q'}$", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.qv,
                title="Water vapour variance", 
                xlabel="$\\overline{q_v'q_v'}$", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalVariances(
                snapshot.z, snapshot.ql,
                title="Liquid water variance", 
                xlabel="$\\overline{q_l'q_l'}$", 
                folder=folderTime,
                id=indicatorFunction
            )
            
            
            
            # Vertical fluxes
            plotVerticalFluxes(
                snapshot.z, snapshot.u,
                title="Horizontal velocity fluxes", 
                xlabel="$\\sigma_i \\overline{w'u'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.v,
                title="Horizontal velocity fluxes", 
                xlabel="$\\sigma_i \\overline{w'v'}$ (m$^2$/s$^2$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.th,
                title="Potential temperature fluxes", 
                xlabel="$\\sigma_i \\overline{w'\\theta'}$ (K m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.thv,
                title="Virtual potential temperature fluxes", 
                xlabel="$\\sigma_i \\overline{w'\\theta_v'}$ (K m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.b,
                title="Buoyancy fluxes", 
                xlabel="$\\sigma_i \\overline{w'b'}$ (m$^2$/s$^3$)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.q,
                title="Total moisture fluxes", 
                xlabel="$\\sigma_i \\overline{w'q'}$ (kg/kg m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.qv,
                title="Water vapour fluxes", 
                xlabel="$\\sigma_i \\overline{w'q_v'}$ (kg/kg m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            plotVerticalFluxes(
                snapshot.z, snapshot.ql,
                title="Liquid water fluxes", 
                xlabel="$\\sigma_i \\overline{w'q_l'}$ (kg/kg m/s)", 
                folder=folderTime,
                id=indicatorFunction
            )
            # plotVerticalFluxes(
                # snapshot.z, snapshot.qr,
                # title="Radioactive tracer fluxes", 
                # xlabel="$\\overline{w'q_r'}$ (kg/kg m/s)", 
                # folder=folderTime,
                # id=indicatorFunction
            # )

if __name__ == "__main__":
    timeInit = time.time()
    
    # id = "LEM"
    id = "MONC"
    
    netcdfFile = ""
    # netcdfFile = "mov0235_ALL_01-_.nc"
    # netcdfFile = "mov0235_ALL_01-z.nc"
    netcdfFile = "diagnostics_3d_ts_30000.nc"
    
    # main(id=id, indicatorFunction="basic", netcdfFile=netcdfFile)
    main(id=id, indicatorFunction="plume", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="plumeEdge", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="plumeEdgeEntrain", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="plumeEdgeDetrain", netcdfFile=netcdfFile)
    # main(id=id, indicatorFunction="dbdz", netcdfFile=netcdfFile)
    
    timeElapsed = time.time()
    print("Elapsed time: {:.2f}s".format(timeElapsed-timeInit))
