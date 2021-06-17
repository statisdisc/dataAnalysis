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
def plotCloudFraction(
        z, 
        cloudFraction, 
        id="",
        folder=""
    ):
    print("Plotting volume fraction")
    z = 1e-3*z.copy()
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    ax0.plot(cloudFraction, z, "r")
    ax0.plot([0.01,0.01], [z[0], z[-1]], "#888888")
    ax0.plot([0.001,0.001], [z[0], z[-1]], "#888888")
    
    # Limits and labels
    ax0.set_xlim(0., 1)
    # ax0.set_xlim(0., 0.1)
    # ax0.set_xlim(0., 0.01)
    ax0.set_ylim(np.min(z), np.max(z))
    ax0.set_xlabel("Cloud fraction")
    ax0.set_ylabel("z (km)")
    plt.title(f"Cloud fraction {id}")
    
    # Create folder for image
    folderVertical = os.path.join(folder, "profilesMean")
    if not os.path.isdir(folderVertical):
        os.makedirs(folderVertical)
    
    np.savez(
        os.path.join(folderVertical, "z_profile_cloud_fraction_{}.npz".format(id)), 
        z = z,
        cloudFraction  = cloudFraction
    )
    
    plt.savefig(
        os.path.join(folderVertical, "profile_cloud_fraction_{}.png".format(id)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()

