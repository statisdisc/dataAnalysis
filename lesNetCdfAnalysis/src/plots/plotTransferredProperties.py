'''
Plot the vertical profiles of a field from the Large Eddy Simulation (LES) data
for comparison with Single Column Models (SCMs).
'''
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
# plt.style.use("dark_background")
# plt.rcParams["font.family"] = "serif"

# Plot the horizontally averaged volume fraction
def plotTransferredProperties(
        field,
        id1,
        id2,
        title="", 
        xlabel="", 
        yMarkers=[],
        folder="",
        plotZero=False
    ):
    print("Plotting the transferred properties for field {}".format(field))
    
    folderVertical = os.path.join(folder, "profilesMean")
    
    folderVertical1 = os.path.join(folderVertical, id1)
    profile1 = np.load(os.path.join(folderVertical1, "z_profile_{}.npz".format(field)))
    
    folderVertical2 = os.path.join(folderVertical, id2)
    profile2 = np.load(os.path.join(folderVertical2, "z_profile_{}.npz".format(field)))
    
    b21 = (profile2["fluid2"]-profile1["fluid2"])/(profile1["fluid1"]-profile1["fluid2"] + 1e-8*((profile1["fluid1"]-profile1["fluid2"]) == 0. ))
    b12 = (profile2["fluid2"]-profile1["fluid1"])/(profile1["fluid2"]-profile1["fluid1"] + 1e-8*((profile1["fluid2"]-profile1["fluid1"]) == 0. ))
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    ax0.fill_between([0,1],[0,0],[1.,1.], facecolor="#CCCCCC")
    ax0.fill_between([0,1],[1,1],[2.8,2.8], facecolor="#CCCCFF")
    for marker in yMarkers:
        ax0.plot([0.,1.], [marker,marker], "k:", linewidth=0.5)
    
    ax0.plot(b21, profile1["z"], "b", label="$b_{21}$")
    ax0.plot(b12, profile1["z"], "r", label="$b_{12}$")
    
    # Limits and labels
    ax0.set_xlim(0., 1.)
    ax0.set_ylim(np.min(profile1["z"]), np.max(profile1["z"]))
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel("z (km)")
    plt.title(title)
    plt.legend(loc="best")
    
    plt.savefig(
        os.path.join(folderVertical, "profile_transferred_{}.png".format(field)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()

