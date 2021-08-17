'''
Plot the location of clouds.
Option to show the thermal structure (the roots of the clouds) in red.
Option to show regions of ascending air in white.
'''
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import LinearSegmentedColormap as lsc
# plt.style.use("dark_background")
# plt.rcParams["font.family"] = "serif"

def getDefaultColors():
    return dict(
        background = [0,0,0],       # Black
        text       = [1,1,1],       # White
        plume      = [1,0,0],       # Red
        updraft    = [1,1,1],       # White
        arrows     = [1,0,1],       # Magenta
        mesh       = [0,0,0],       # Black
        cloudCmap  = "binary_r"
    )

def plotThermalContour(
        x, y, ql,
        showMesh = False,
        id = "", 
        title = "", 
        xlabel = "",
        ylabel = "z (km)",
        xlim = [-10., 10.],
        ylim = [0., 3.],
        dpi = 200,
        folder = "", 
        I2 = None, 
        u = None, 
        w = None, 
        velocityVectorsOnly = False,
        cbarScale = "logarithmic",
        greyscale = False
    ):
    if len(y) != len(ql):
        ql = ql.transpose()
        
        if I2 is not None:
            I2 = I2.transpose()
        
        if w is not None:
            w = w.transpose()
        
        if u is not None:
            u = u.transpose()
    
    colors = getDefaultColors()
    if greyscale:
        colors = getGreyscaleColors()
    
    fig, ax = plt.subplots(1,1,figsize=(int(xlim[1]-xlim[0]),2*int(ylim[1]-ylim[0])))
    
    # Plot regions where clouds exist (based on liquid water, ql)
    if cbarScale == "logarithmic":
        c = ax.pcolor(x, y, np.log10(ql), cmap=colors["cloudCmap"], vmin=-5, vmax=-3)
    else:
        c = ax.pcolor(x, y, ql, cmap=colors["cloudCmap"], vmin=1e-5, vmax=1e-3)
    # fig.colorbar(c, ax=ax)
    
    # Plot contours for the structure of the thermals
    if I2 is not None:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        alpha = 0.3
        cmap = lsc.from_list("", [(0., 0., 0., 0.), colors["plume"]+[alpha]])
        ax.contourf(X, Y, I2, 2, cmap=cmap, vmin=0., vmax=1.1, linewidths=(0,0))
        
        # Outline regions
        ax.contour(X, Y, I2, levels=[0.9], colors=[colors["plume"]], linewidths=[1.])
        
    
    # Plot contours for regions of ascending air
    if w is not None and not velocityVectorsOnly:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        alpha = 0.3
        cmap = lsc.from_list("", [(0., 0., 0., 0.), colors["updraft"]+[alpha]])
        ax.contourf(X, Y, w, 2, cmap=cmap, vmin=-1e-5, vmax=1e-5, linewidths=(0,0))
        
        # Outline regions
        ax.contour(X, Y, w, levels=[0.], colors=[colors["updraft"]], linewidths=[1.])
    
    # Show the mesh for the Large Eddy Simulation
    if showMesh:
        xMin, xMax = np.min(x), np.max(x)
        yMin, yMax = np.min(y), np.max(y)
        
        for i in range(len(x)):
            ax.plot([x[i], x[i]], [yMin, yMax], colors["mesh"], linewidth=0.2, alpha=0.5)
        
        for j in range(len(y)):
            ax.plot([xMin, xMax], [y[j], y[j]], colors["mesh"], linewidth=0.2, alpha=0.5)
    
    # Show velocity vectors
    if u is not None and w is not None:
        vectorInterval = 100
        X, Y = np.meshgrid(x, y)
        plt.quiver(
            np.concatenate(X)[::vectorInterval], 
            np.concatenate(Y)[::vectorInterval], 
            np.concatenate(u)[::vectorInterval], 
            np.concatenate(w)[::vectorInterval], 
            angles='xy', 
            color=colors["arrows"], 
            scale=100, 
            headwidth=2
        )
    
    # Limits and labels
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel, color=colors["text"])
    ax.set_ylabel(ylabel, color=colors["text"])
    plt.title(title, color=colors["text"])
    
    # Ensure x and y axis are the same scale
    plt.gca().set_aspect("equal")
    
    # Create folder for image
    folderCloud = os.path.join(folder, "contourCloud")
    if not os.path.isdir(folderCloud):
        os.makedirs(folderCloud)
    
    plt.savefig(
        os.path.join(folderCloud, "contour_{}.png".format(id)), 
        bbox_inches="tight", 
        dpi=dpi
    )
    plt.close()