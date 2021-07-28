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
from src.plots.plotLEMvsMONC import plotVolumeFractionComparison
from src.plots.plotLEMvsMONC import plotVerticalProfileComparison
from src.plots.plotVerticalProfileComparison import plotVerticalFluxes


def main(
        indicatorLEM  = "plume", 
        indicatorMONC = "plume", 
        timesLEM  = [14000],
        timesMONC = [13800]
    ):
    # Fetch folders for code structure
    folder = folders(
        folderScripts = os.path.dirname(os.path.realpath(__file__))
    )
    
    variables = ["ql", "qv", "theta", "u", "v", "w"]
    
    # Create plots for each snapshot in time
    for n in range(min(len(timesLEM), len(timesMONC))):
        print("Processing timestep {} of {}".format(n+1, min(len(timesLEM), len(timesMONC))))
        
        folderTimeLEM  = os.path.join(folder.lem,  "time_{}".format(timesLEM[n]),  "profilesMean", indicatorLEM)
        folderTimeMONC = os.path.join(folder.monc, "time_{}".format(timesMONC[n]), "profilesMean", indicatorMONC)
        folderTime = os.path.join(folder.outputs, "lem_{}_monc_{}".format(timesLEM[n], timesMONC[n]), "profilesMean")
        
        '''
        Plot comparisons of vertical profiles
        '''
        plotVolumeFractionComparison(
            folderTimeLEM,
            folderTimeMONC,
            title="Volume fraction", 
            folder=folderTime
        )
        
        plotVerticalProfileComparison(
            "u",
            folderTimeLEM,
            folderTimeMONC,
            title="Horizontal velocity", 
            xlabel="u (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "v", 
            folderTimeLEM,
            folderTimeMONC,
            title="Horizontal velocity", 
            xlabel="v (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "w", 
            folderTimeLEM,
            folderTimeMONC,
            title="Vertical velocity", 
            xlabel="w (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "theta", 
            folderTimeLEM,
            folderTimeMONC,
            title="Potential temperature", 
            xlabel="$\\theta$ (K)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "qv", 
            folderTimeLEM,
            folderTimeMONC,
            title="Water vapour", 
            xlabel="$q_v$ (kg/kg)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "ql", 
            folderTimeLEM,
            folderTimeMONC,
            title="Liquid water", 
            xlabel="$q_l$ (kg/kg)", 
            folder=folderTime,
            plotZero=True
        )
        
        
        

if __name__ == "__main__":
    timeInit = time.time()
    main(
        timesLEM  = range(14000, 43400, 600),
        timesMONC = range(13800, 43200, 600)
    )
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
