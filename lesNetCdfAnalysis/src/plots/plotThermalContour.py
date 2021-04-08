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
plt.style.use("dark_background")
plt.rcParams["font.family"] = "serif"

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
        I2 = [], 
        u = [], 
        w = [], 
        velocityVectorsOnly = False,
        cbarScale = "logarithmic"
    ):
    
    fig, ax = plt.subplots(1,1,figsize=(int(xlim[1]-xlim[0]),2*int(ylim[1]-ylim[0])))
    
    # Plot regions where clouds exist (based on liquid water, ql)
    if cbarScale == "logarithmic":
        c = ax.pcolor(x, y, np.log10(ql), cmap='binary_r', vmin=-5, vmax=-3)
    else:
        c = ax.pcolor(x, y, ql, cmap='binary_r', vmin=1e-5, vmax=1e-3)
    # fig.colorbar(c, ax=ax)
    
    # Plot contours for the structure of the thermals
    if I2 != []:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(0., 0., 0., 0.), (1., 0., 0., 0.3)])
        ax.contourf(X, Y, I2, 2, cmap=cmap, vmin=0., vmax=1.1, linewidths=(0,0))
        
        # Outline regions
        ax.contour(X, Y, I2, levels=[0.9], colors=[(1.,0.,0.)], linewidths=[1.])
        
    
    # Plot contours for regions of ascending air
    if w != [] and not velocityVectorsOnly:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(0., 0., 0., 0.), (1., 1., 1., 0.3)])
        ax.contourf(X, Y, w, 2, cmap=cmap, vmin=-1e-5, vmax=1e-5, linewidths=(0,0))
        
        # Outline regions
        ax.contour(X, Y, w, levels=[0.], colors=[(1.,1.,1.)], linewidths=[1.])
    
    # Show the mesh for the Large Eddy Simulation
    if showMesh:
        xMin, xMax = np.min(x), np.max(x)
        yMin, yMax = np.min(y), np.max(y)
        
        for i in range(len(x)):
            ax.plot([x[i], x[i]], [yMin, yMax], "k", linewidth=0.2, alpha=0.5)
        
        for j in range(len(y)):
            ax.plot([xMin, xMax], [y[j], y[j]], "k", linewidth=0.2, alpha=0.5)
    
    # Show velocity vectors
    if u != [] and w != []:
        vectorInterval = 100
        X, Y = np.meshgrid(x, y)
        plt.quiver(np.concatenate(X)[::vectorInterval], np.concatenate(Y)[::vectorInterval], np.concatenate(u)[::vectorInterval], np.concatenate(w)[::vectorInterval], angles='xy', color="m", scale=100, headwidth=2)
    
    # Limits and labels
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title)
    
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