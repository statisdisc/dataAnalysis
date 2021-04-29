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
    
    # Data sets must be the same length
    minLength = min(len(profile1["z"]), len(profile2["z"]))
    p1 = {}
    p1["z"] = profile1["z"][:minLength]
    p1["fluid1"] = profile1["fluid1"][:minLength]
    p1["fluid2"] = profile1["fluid2"][:minLength]
    p1["fluid1Std"] = profile1["fluid1Std"][:minLength]
    p1["fluid2Std"] = profile1["fluid2Std"][:minLength]
    p2 = {}
    p2["z"] = profile2["z"][:minLength]
    p2["fluid1"] = profile2["fluid1"][:minLength]
    p2["fluid2"] = profile2["fluid2"][:minLength]
    p2["fluid1Std"] = profile2["fluid1Std"][:minLength]
    p2["fluid2Std"] = profile2["fluid2Std"][:minLength]
    
    conditionZero = 1e-8*((p1["fluid1"]-p1["fluid2"]) == 0. )
    b21 = (p2["fluid2"]-p1["fluid2"])/(p1["fluid1"]-p1["fluid2"] + conditionZero)
    b12 = (p2["fluid2"]-p1["fluid1"])/(p1["fluid2"]-p1["fluid1"] + conditionZero)
    
    variance = (p2["fluid2Std"]**2 + b21**2*p1["fluid1Std"]**2 + b12**2*p1["fluid2Std"]**2)/(p1["fluid1"]-p1["fluid2"] + conditionZero)**2
    stdev = np.sqrt(variance)
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    # ax0.fill_between([0,1],[0,0],[1.,1.], facecolor="#CCCCFF")
    ax0.fill_between([0,1],[1,1],[2.8,2.8], facecolor="#CCCCCC")
    for marker in yMarkers:
        ax0.plot([0.,1.], [marker,marker], "k:", linewidth=0.5)
    
    
    # Shaded regions for standard deviation range
    # ax0.fill_betweenx(
        # p1["z"], b21-stdev, b21+stdev, 
        # facecolor=(0.,0.,0.5), 
        # linewidth=0., 
        # alpha=0.2
    # )
    # ax0.fill_betweenx(
        # p1["z"], b12-stdev, b12+stdev, 
        # facecolor=(0.5,0.,0.), 
        # linewidth=0., 
        # alpha=0.2
    # )
    
    
    ax0.plot(b21, p1["z"], "b", label="$b_{21}$")
    ax0.plot(b12, p1["z"], "r", label="$b_{12}$")
    
    # Limits and labels
    ax0.set_xlim(0., 1.)
    ax0.set_ylim(0., 4.)
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel("z (km)")
    plt.title(title)
    plt.legend(loc="best")
    
    plt.savefig(
        os.path.join(folderVertical, "transferred_{}_{}_{}.png".format(id1, id2, field)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()

