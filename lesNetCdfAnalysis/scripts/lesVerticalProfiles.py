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
from src.utilities.getLesData import getLesData
from src.plots.plotVerticalProfile import plotVolumeFraction
from src.plots.plotVerticalProfile import plotVerticalProfile
from src.plots.plotVerticalProfile import plotVerticalFluxes


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
        
        plotVolumeFraction(
            snapshot.z*1e-3, snapshot.I2,
            folder=folderTime
        )
        
        # Mean profiles
        plotVerticalProfile(
            snapshot.z*1e-3, snapshot.u,
            title="Horizontal velocity", 
            xlabel="u (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfile(
            snapshot.z*1e-3, snapshot.v,
            title="Horizontal velocity", 
            xlabel="v (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfile(
            snapshot.z*1e-3, snapshot.w,
            title="Vertical velocity", 
            xlabel="w (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfile(
            snapshot.z*1e-3, snapshot.theta,
            title="Potential temperature", 
            xlabel="theta (K)", 
            folder=folderTime
        )
        
        plotVerticalProfile(
            snapshot.z*1e-3, snapshot.qv,
            title="Water vapour", 
            xlabel="$q_v$ (kg/kg)", 
            folder=folderTime
        )
        
        plotVerticalProfile(
            snapshot.z*1e-3, snapshot.ql,
            title="Liquid water", 
            xlabel="$q_l$ (kg/kg)", 
            folder=folderTime
        )
        
        # Vertical fluxes
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.u,
            title="Horizontal velocity fluxes", 
            xlabel="$\\overline{w'u'}$ (m$^2$/s$^2$)", 
            folder=folderTime
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.v,
            title="Horizontal velocity fluxes", 
            xlabel="$\\overline{w'v'}$ (m$^2$/s$^2$)", 
            folder=folderTime
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.theta,
            title="Potential temperature fluxes", 
            xlabel="$\\overline{w'\\theta'}$ (K m/s)", 
            folder=folderTime
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.qv,
            title="Water vapour fluxes", 
            xlabel="$\\overline{w'q_v'}$ (kg/kg m/s)", 
            folder=folderTime
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.ql,
            title="Liquid water fluces", 
            xlabel="$\\overline{w'q_l'}$ (kg/kg m/s)", 
            folder=folderTime
        )

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
