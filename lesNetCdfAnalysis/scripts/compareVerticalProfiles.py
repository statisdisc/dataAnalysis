'''
Plot the vertical profiles of various fields in the Large Eddy Simulation (LES) data
for comparison with Single Column Models (SCMs).
'''
import os
import sys
import time
import numpy as np

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.getLesData import getLesData
from src.utilities.getScmData import getScmData
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
    
    lesDiagnostics = getScmData(os.path.join(folder.data, "LES_transfers.mat"))
    
    for key in lesDiagnostics:
        print(key)
        
    
    
    
    
    # Create plots for each snapshot in time
    t = [8.89*3600]
    for n in range(len(t)):
        print("Processing timestep {} (t = {:.2f}hrs, {}s)".format(n+1, float(t[n])/3600., t[n]))
        
        folderTime = os.path.join(folder.outputs, "timestep_{}".format(n))
        
        '''
        Plot comparisons of vertical profiles
        '''
        plotVerticalProfileComparison(
            "u", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Horizontal velocity", 
            xlabel="u (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "v", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Horizontal velocity", 
            xlabel="v (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "w", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Vertical velocity", 
            xlabel="w (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "theta", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Potential temperature", 
            xlabel="$\\theta$ (K)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "qv", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Water vapour", 
            xlabel="$q_v$ (kg/kg)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "ql", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Liquid water", 
            xlabel="$q_l$ (kg/kg)", 
            folder=folderTime,
            plotZero=True
        )
        
        
        '''
        Plot the transferred properties during entrainment and detrainment - the b_ij coefficients
        '''
        plotTransferredProperties(
            "u", "plume", "plumeEdge",
            title="Horizontal velocity", 
            xlabel="$b_{ij}$ for u",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "v", "plume", "plumeEdge",
            title="Horizontal velocity", 
            xlabel="$b_{ij}$ for v",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "w", "plume", "plumeEdge",
            title="Vertical velocity", 
            xlabel="$b_{ij}$ for w",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "theta", "plume", "plumeEdge",
            title="Potential temperature", 
            xlabel="$b_{ij}$ for $\\theta$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "qv", "plume", "plumeEdge",
            title="Water vapour", 
            xlabel="$b_{ij}$ for $q_v$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "ql", "plume", "plumeEdge",
            title="Liquid water", 
            xlabel="$b_{ij}$ for $q_l$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
