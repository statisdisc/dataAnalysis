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
from src.plots.plotTransferredProperties import plotTransferredProperties
from src.plots.plotVerticalProfileComparison import plotVolumeFraction
from src.plots.plotVerticalProfileComparison import plotVerticalProfileComparison
from src.plots.plotVerticalProfileComparison import plotVerticalFluxes


def main():
    # indicatorFunction="basic"
    # indicatorFunction="plume"
    indicatorFunction="plumeEdge"
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts = os.path.dirname(os.path.realpath(__file__)),
        folderData = "/mnt/f/Desktop/LES_Data"
    )
    
    # Create plots for each snapshot in time
    t = [8.89*3600]
    for n in xrange(len(t)):
        print "Processing timestep {} (t = {:.2f}hrs)".format(n+1, float(t[n])/3600.)
        
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        
        # plotVolumeFraction(
            # snapshot.z*1e-3, snapshot.I2,
            # folder=folderTime,
            # id=indicatorFunction
        # )
        
        # Mean profiles
        # plotVerticalProfile(
            # snapshot.z*1e-3, snapshot.u,
            # title="Horizontal velocity", 
            # xlabel="u (m/s)", 
            # folder=folderTime,
            # id=indicatorFunction,
            # plotZero=True
        # )
        
        # plotVerticalProfile(
            # snapshot.z*1e-3, snapshot.v,
            # title="Horizontal velocity", 
            # xlabel="v (m/s)", 
            # folder=folderTime,
            # id=indicatorFunction,
            # plotZero=True
        # )
        
        plotVerticalProfileComparison(
            "w", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Vertical velocity", 
            xlabel="w (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        # plotVerticalProfile(
            # snapshot.z*1e-3, snapshot.theta,
            # title="Potential temperature", 
            # xlabel="theta (K)", 
            # folder=folderTime,
            # id=indicatorFunction
        # )
        
        # plotVerticalProfile(
            # snapshot.z*1e-3, snapshot.qv,
            # title="Water vapour", 
            # xlabel="$q_v$ (kg/kg)", 
            # folder=folderTime,
            # id=indicatorFunction
        # )
        
        # plotVerticalProfile(
            # snapshot.z*1e-3, snapshot.ql,
            # title="Liquid water", 
            # xlabel="$q_l$ (kg/kg)", 
            # folder=folderTime,
            # id=indicatorFunction
        # )
        
        plotTransferredProperties(
            "u", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "v", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "w", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "theta", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "qv", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "ql", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        '''# Vertical fluxes
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.u,
            title="Horizontal velocity fluxes", 
            xlabel="$\\overline{w'u'}$ (m$^2$/s$^2$)", 
            folder=folderTime,
            id=indicatorFunction
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.v,
            title="Horizontal velocity fluxes", 
            xlabel="$\\overline{w'v'}$ (m$^2$/s$^2$)", 
            folder=folderTime,
            id=indicatorFunction
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.theta,
            title="Potential temperature fluxes", 
            xlabel="$\\overline{w'\\theta'}$ (K m/s)", 
            folder=folderTime,
            id=indicatorFunction
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.qv,
            title="Water vapour fluxes", 
            xlabel="$\\overline{w'q_v'}$ (kg/kg m/s)", 
            folder=folderTime,
            id=indicatorFunction
        )
        
        plotVerticalFluxes(
            snapshot.z*1e-3, snapshot.ql,
            title="Liquid water fluxes", 
            xlabel="$\\overline{w'q_l'}$ (kg/kg m/s)", 
            folder=folderTime,
            id=indicatorFunction
        )'''

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
