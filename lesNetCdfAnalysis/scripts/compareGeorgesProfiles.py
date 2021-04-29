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
        
        id = "particlesEntrainDetrain"
        folderVertical = os.path.join(folderTime, "profilesMean")
        if id != "":
            folderVertical = os.path.join(folderVertical, id)
        if not os.path.isdir(folderVertical):
            os.makedirs(folderVertical)
        
        # Save vertical profiles for future use
        indexTime = np.argmin(np.abs(lesDiagnostics["times_t"][0]-t[n]))
        print("Time")
        print(indexTime)
        print(lesDiagnostics["times_t"][0][indexTime])
        np.savez(
            os.path.join(folderVertical, "z_profile_w.npz"), 
            z = lesDiagnostics["z_lev"][0][:-1]/1000.,
            fluid1 = lesDiagnostics["w_hat_up"][:,indexTime],
            fluid2 = lesDiagnostics["w_det_up"][:,indexTime],
            fluid1Std = 0*lesDiagnostics["w_hat_up"][:,indexTime],
            fluid2Std = 0*lesDiagnostics["w_det_up"][:,indexTime],
            fluid1Min = np.min(lesDiagnostics["w_hat_up"][:,indexTime]),
            fluid1Max = np.max(lesDiagnostics["w_hat_up"][:,indexTime]),
            fluid2Min = np.min(lesDiagnostics["w_det_up"][:,indexTime]),
            fluid2Max = np.max(lesDiagnostics["w_det_up"][:,indexTime])
        )
        np.savez(
            os.path.join(folderVertical, "z_profile_qv.npz"), 
            z = lesDiagnostics["z_lev"][0][:-1]/1000.,
            fluid1 = lesDiagnostics["qv_hat_up"][:,indexTime],
            fluid2 = lesDiagnostics["qv_det_up"][:,indexTime],
            fluid1Std = 0*lesDiagnostics["qv_hat_up"][:,indexTime],
            fluid2Std = 0*lesDiagnostics["qv_det_up"][:,indexTime],
            fluid1Min = np.min(lesDiagnostics["qv_hat_up"][:,indexTime]),
            fluid1Max = np.max(lesDiagnostics["qv_hat_up"][:,indexTime]),
            fluid2Min = np.min(lesDiagnostics["qv_det_up"][:,indexTime]),
            fluid2Max = np.max(lesDiagnostics["qv_det_up"][:,indexTime])
        )
        np.savez(
            os.path.join(folderVertical, "z_profile_theta.npz"), 
            z = lesDiagnostics["z_lev"][0][:-1]/1000.,
            fluid1 = lesDiagnostics["th_hat_up"][:,indexTime],
            fluid2 = lesDiagnostics["th_det_up"][:,indexTime],
            fluid1Std = 0*lesDiagnostics["th_hat_up"][:,indexTime],
            fluid2Std = 0*lesDiagnostics["th_det_up"][:,indexTime],
            fluid1Min = np.min(lesDiagnostics["th_hat_up"][:,indexTime]),
            fluid1Max = np.max(lesDiagnostics["th_hat_up"][:,indexTime]),
            fluid2Min = np.min(lesDiagnostics["th_det_up"][:,indexTime]),
            fluid2Max = np.max(lesDiagnostics["th_det_up"][:,indexTime])
        )
        
        plotVerticalProfileComparison(
            "w", "plume", "particlesEntrainDetrain",
            title="Vertical velocity", 
            xlabel="w (m/s)", 
            folder=folderTime,
            plotZero=True
        )
        
        plotVerticalProfileComparison(
            "qv", "plume", "particlesEntrainDetrain",
            title="Water vapour", 
            xlabel="$q_v$", 
            folder=folderTime,
            plotZero=True
        )
        
        # plotVerticalProfileComparison(
            # "theta", "plume", "particlesEntrainDetrain",
            # title="Potential Temperature", 
            # xlabel="$\\theta$ (K)", 
            # folder=folderTime,
            # plotZero=True
        # )
        
        
        
        plotTransferredProperties(
            "w", "plume", "particlesEntrainDetrain",
            title="Vertical velocity", 
            xlabel="$b_{ij}$ for w",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        plotTransferredProperties(
            "qv", "plume", "particlesEntrainDetrain",
            title="Water vapour", 
            xlabel="$b_{ij}$ for $q_v$",
            yMarkers=[1., 2.8],
            folder=folderTime,
            plotZero=True
        )
        
        
        
        
        
        
        
        
        
        indexTime = np.argmin(np.abs(lesDiagnostics["times_t"][0]-t[n]))
        zLes = lesDiagnostics["z_lev"][0][:-1]/1000.
        w2Les = lesDiagnostics["w_up"][:,indexTime]
        w12Les = lesDiagnostics["w_det_up"][:,indexTime]
        w21Les = lesDiagnostics["w_hat_up"][:,indexTime]
        th2Les = lesDiagnostics["th_up"][:,indexTime]
        th12Les = lesDiagnostics["th_det_up"][:,indexTime]
        th21Les = lesDiagnostics["th_hat_up"][:,indexTime]
        qv2Les = lesDiagnostics["qv_up"][:,indexTime]
        qv12Les = lesDiagnostics["qv_det_up"][:,indexTime]
        qv21Les = lesDiagnostics["qv_hat_up"][:,indexTime]
        
        plotVerticalProfileComparison(
            "w", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Vertical velocity", 
            xlabel="w (m/s)", 
            folder=folderTime,
            plotZero=True,
            # additionalLines=[[w12Les,zLes,"r"],[w21Les,zLes,"b"]]
            # additionalLines=[[w2Les,zLes,"k"]]
        )
        
        plotVerticalProfileComparison(
            "theta", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Potential temperature", 
            xlabel="$\\theta$ (K)", 
            folder=folderTime,
            plotZero=True,
            additionalLines=[[th12Les,zLes,"k"],[th21Les,zLes,"#888888"]]
        )
        
        plotVerticalProfileComparison(
            "qv", "plume", "plumeEdge",
            id3="plumeEdgeEntrain",
            id4="plumeEdgeDetrain",
            title="Water vapour", 
            xlabel="$q_v$ (kg/kg)", 
            folder=folderTime,
            plotZero=True,
            additionalLines=[[qv12Les,zLes,"r"],[qv21Les,zLes,"b"]]
        )
        

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
