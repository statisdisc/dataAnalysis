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

def makeSmoothColormap(colorStart, colorEnd, bins=100):
    cmapColors = []
    for i in np.linspace(0, 1, bins):
        r = (1-i)*colorStart[0] + i*colorEnd[0]
        g = (1-i)*colorStart[1] + i*colorEnd[1]
        b = (1-i)*colorStart[2] + i*colorEnd[2]
        cmapColors.append( (r,g,b) )
    
    cmap = lsc.from_list("new_cmap", cmapColors, bins)
    
    return cmap

def getDefaultColors():
    return dict(
        figure     = [1, 1, 1],       # White
        background = [0.5, 0.8, 1],   # Sky blue
        text       = [0, 0, 0],       # Black
        plume      = [1, 0, 0],       # Red
        updraft    = [1, 1, 1],       # White
        arrows     = [1, 0, 1],       # Magenta
        mesh       = [0, 0, 0],       # Black
    )

def getGreyscaleColors():
    return dict(
        figure     = [1, 1, 1],       # White
        background = [0.5, 0.5, 0.5], # Grey
        text       = [0, 0, 0],       # Black
        plume      = [0, 0, 0],       # Black
        updraft    = [1, 1, 1],       # White
        arrows     = [1, 1, 1],       # White
        mesh       = [0, 0, 0],       # Black
    )

def plotThermalContour(
        x, y, ql,
        showMesh = False,
        id = "", 
        title = "", 
        xlabel = "",
        ylabel = "z (km)",
        xlim = [-9.575, 9.575],
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
    
    fig, ax = plt.subplots(
        nrows   = 1, 
        ncols   = 1,
        figsize = (int(xlim[1]-xlim[0]),2*int(ylim[1]-ylim[0]))
    )
    
    # Background colors
    fig.patch.set_facecolor(colors["figure"])
    ax.set_facecolor(colors["background"])
    
    # Plot regions where clouds exist (based on liquid water, ql)
    cmap = makeSmoothColormap(colors["background"], [1,1,1])
    cmap.set_under(colors["background"])
    
    if cbarScale == "logarithmic":
        c = ax.pcolor(x, y, np.log10(ql), cmap=cmap, vmin=-5,   vmax=-3,   shading='auto')
    else:
        c = ax.pcolor(x, y, ql,           cmap=cmap, vmin=1e-5, vmax=1e-3, shading='auto')
    # fig.colorbar(c, ax=ax)
    
    # Plot contours for the structure of the thermals
    if I2 is not None:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        if not greyscale:
            alpha = 0.3
            cmap = lsc.from_list("", [(0., 0., 0., 0.), colors["plume"]+[alpha]])
            ax.contourf(X, Y, I2, 2, cmap=cmap, vmin=0., vmax=1.1, antialiased=True)
        
        # Outline regions
        ax.contour(X, Y, I2, levels=[0.9], colors=[colors["plume"]])
        
    
    # Plot contours for regions of ascending air
    if w is not None and not velocityVectorsOnly:
        X, Y = np.meshgrid(x, y)
        
        # Fill regions
        if not greyscale:
            alpha = 0.3
            cmap = lsc.from_list("", [(0., 0., 0., 0.), colors["updraft"]+[alpha]])
            ax.contourf(X, Y, w, 2, cmap=cmap, vmin=-1e-5, vmax=1e-5, antialiased=True)
        
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
    
    filename = "contour_{}.png".format(id)
    if greyscale:
        filename = "contour_grey_{}.png".format(id)
    
    plt.savefig(
        os.path.join(folderCloud, filename), 
        bbox_inches="tight", 
        dpi=dpi
    )
    plt.close()