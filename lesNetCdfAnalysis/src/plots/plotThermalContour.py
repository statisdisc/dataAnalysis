import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.tri as tri
plt.style.use("dark_background")
plt.rcParams["font.family"] = "serif"

def plotThermalContour(ql, I2, layer, layerIndex, id="", title="", folder="", cloudOnly=False):
    
    fig, ax0 = plt.subplots(1,1,figsize=(16,4))#, gridspec_kw={'width_ratios': [10, 1]})
    
    # Plot contours
    # c = ax0.pcolor(ql.x*1e-3, ql.z*1e-3, ql.field[:,layerIndex,:], cmap='binary_r', vmin=1e-5, vmax=1e-3)
    c = ax0.pcolor(ql.x*1e-3, ql.z*1e-3, np.log10(ql.field[:,layerIndex,:]), cmap='binary_r', vmin=-5, vmax=-3)
    # fig.colorbar(c, ax=ax0)
    
    if not cloudOnly:
        X, Y = np.meshgrid(ql.x*1e-3, ql.z*1e-3)
        ax0.contour(X, Y, I2.field[:,layerIndex,:], levels=[0.9], colors=[(1.,0.,0.)], linewidths=[1.])
    
    # Limits and labels
    ax0.set_xlim(-10., 10.)
    ax0.set_ylim(0., 3.)
    ax0.set_xlabel("x (km)")
    ax0.set_ylabel("z (km)")
    plt.title(title)
    
    plt.gca().set_aspect("equal")
    
    # Create folder for image
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    plt.savefig(
        # os.path.join(folder, "contour_{}_{}.png".format(layerIndex, id)), 
        os.path.join(folder, "contour_{}_{}.png".format(id, layerIndex)), 
        bbox_inches="tight", 
        dpi=100
    )
    plt.close()