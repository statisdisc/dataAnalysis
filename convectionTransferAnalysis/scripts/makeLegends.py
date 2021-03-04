'''
Create legend images to accompany the conservation plots.
These plots are found in McIntyre et a. (2020), https://doi.org/10.1002/qj.3728
'''
import os
import sys
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.saveLegend import saveLegend

def customLegend(folder=""):
    x = np.linspace(0.,1.,2)
    plt.figure()
    
    # Different numerical treatments and energy changes
    p0 = Patch(facecolor="w", edgecolor="w",label=" ")
    p1 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="$\\alpha_C = 0,\\ \\alpha_M = 0$")
    p2 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="$\\alpha_C = 1,\\ \\alpha_M = 1$")
    p3 = Patch(facecolor=(0.,0.,1.,0.5), edgecolor=(0.,0.,1.),label="$\\alpha_C = 0,\\ \\alpha_M = 1$")
    p4 = Patch(facecolor=(1.,0.,0.,0.5), edgecolor=(1.,0.,0.),label="$\\alpha_C = 1,\\ \\alpha_M = 0$")
    p5 = Line2D([0.,1.],[0.,1.],color="#555555",linewidth=4.5,linestyle="-",label="$\\Delta E_r$, $\\Delta F_r$ Range")
    p6 = Line2D([0.,1.],[0.,1.],color="#555555",linewidth=2.,linestyle="--",label="$\\Delta E_r$ Mean")
    
    # Different explicit and implicit treatments of transfer terms
    l0 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label=" ")
    l1 = Line2D([0.,1.],[0.,1.],color=(0.5,0.5,0.5),linewidth=4.5,linestyle="-",label="$\\alpha_C = 0,\\ \\alpha_M = 0$")
    l2 = Line2D([0.,1.],[0.,1.],color=(0.,0.,0.),linewidth=4.5,linestyle="-",label="$\\alpha_C = 1,\\ \\alpha_M = 1$")
    l3 = Line2D([0.,1.],[0.,1.],color=(0.,0.,1.),linewidth=4.5,linestyle="-",label="$\\alpha_C = 0,\\ \\alpha_M = 1$")
    l4 = Line2D([0.,1.],[0.,1.],color=(1.,0.,0.),linewidth=4.5,linestyle="-",label="$\\alpha_C = 1,\\ \\alpha_M = 0$")
    
    # Using parameters q=m and r=n+1
    l10 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="$q=m$, $r=n+1$, $\\alpha_C = 0$, $\\alpha_M = 0$")
    p11 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="Scheme 1:")
    p12 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="$q=m$, $r=n+1$, $\\alpha_C = 1$, $\\alpha_M = 1$")
    p13 = Patch(facecolor=(0.,0.,1.,0.5), edgecolor=(0.,0.,1.),label="$q=m$, $r=n+1$, $\\alpha_C = 0$, $\\alpha_M = 1$")
    p14 = Patch(facecolor=(1.,0.,0.,0.5), edgecolor=(1.,0.,0.),label="$q=m$, $r=n+1$, $\\alpha_C = 1$, $\\alpha_M = 0$")
    
    # Using parameters q=m and r=m
    l20 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="$q=m$, $r=m$, $\\alpha_C = 0$, $\\alpha_M = 1$")
    p21 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="$q=m$, $r=m$, $\\alpha_C = 0$, $\\alpha_M = 0$")
    p22 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="$q=m$, $r=m$, $\\alpha_C = 1$, $\\alpha_M = 1$")
    p23 = Patch(facecolor=(0.,0.,1.,0.5), edgecolor=(0.,0.,1.),label="Scheme 2:")
    p24 = Patch(facecolor=(1.,0.,0.,0.5), edgecolor=(1.,0.,0.),label="$q=m$, $r=m$, $\\alpha_C = 1$, $\\alpha_M = 0$")
    
    # Using parameters q=n+1 and r=n+1
    l30 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="$q=n+1$, $r=n+1$, $\\alpha_C = 1$, $\\alpha_M = 0$")
    p31 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="$q=n+1$, $r=n+1$, $\\alpha_C = 0$, $\\alpha_M = 0$")
    p32 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="$q=n+1$, $r=n+1$, $\\alpha_C = 1$, $\\alpha_M = 1$")
    p33 = Patch(facecolor=(0.,0.,1.,0.5), edgecolor=(0.,0.,1.),label="$q=n+1$, $r=n+1$, $\\alpha_C = 0$, $\\alpha_M = 1$")
    p34 = Patch(facecolor=(1.,0.,0.,0.5), edgecolor=(1.,0.,0.),label="Scheme 3:")
    
    # Using parameters q=n+1 and r=m
    l40 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="$q=n+1$, $r=m$, $\\alpha_C = 1$, $\\alpha_M = 1$")
    p41 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="$q=n+1$, $r=m$, $\\alpha_C = 0$, $\\alpha_M = 0$")
    p42 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="Scheme 4:")
    p43 = Patch(facecolor=(0.,0.,1.,0.5), edgecolor=(0.,0.,1.),label="$q=n+1$, $r=m$, $\\alpha_C = 0$, $\\alpha_M = 1$")
    p44 = Patch(facecolor=(1.,0.,0.,0.5), edgecolor=(1.,0.,0.),label="$q=n+1$, $r=m$, $\\alpha_C = 1$, $\\alpha_M = 0$")
    
    # Special cases for total simulation energy timeseries
    lw0 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label=" ")
    lw1 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="Scheme 1")
    lw2 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="Scheme 2")
    lw3 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="Scheme 3")
    lw4 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="Scheme 4")
    lw5 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="Scheme 5")
    lw6 = Line2D([0.,1.],[0.,1.],color="w",linewidth=4.5,linestyle="-",label="Scheme 6")
    
    # Special cases (names schemes)
    ps1 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="Scheme 1")
    ps2 = Patch(facecolor=(0.,0.,1.,0.5), edgecolor=(0.,0.,1.),label="Scheme 2")
    ps3 = Patch(facecolor=(1.,0.,0.,0.5), edgecolor=(1.,0.,0.),label="Scheme 3")
    ps4 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="Scheme 4")
    ps5 = Patch(facecolor=(0.5,0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5),label="Scheme 5")
    ps6 = Patch(facecolor=(0.,0.,0.,0.5), edgecolor=(0.,0.,0.),label="Scheme 6")
    
    # Save to PNG
    saveLegend([p1,p3,p5,p2,p4,p6], "conservation1", ncols=2, folder=folder)
    saveLegend([p1,p0,p3,p5,p4,p6,p2,p0], "conservation2", ncols=4, folder=folder)
    saveLegend([p1,p3,p4,p2], "conservation3", ncols=4, folder=folder)
    saveLegend([l1,l3,l4,l2], "conservation4", ncols=4, folder=folder)
    saveLegend([p1,lw1,lw5, p3,lw2,lw0, p4,lw3,lw0, p2,lw4,lw6], "conservation5", ncols=4, folder=folder)
    saveLegend([ps1,ps2,ps3,ps4,l0,l0,l0,l0,l0], "conservation_method1", ncols=1, folder=folder)
    saveLegend([l0,ps5,ps6,l0,l0,l0,l0,l0,l0], "conservation_method2", ncols=1, folder=folder)
    saveLegend([p11,l10,p12,p13,p14,l0,l0,l0,l0], "conservation10", ncols=1, folder=folder)
    saveLegend([p21,p22,p23,l20,p24,l0,l0,l0,l0], "conservation20", ncols=1, folder=folder)
    saveLegend([p31,p32,p33,p34,l30,l0,l0,l0,l0], "conservation30", ncols=1, folder=folder)
    saveLegend([p41,p42,l40,p43,p44,l0,l0,l0,l0], "conservation40", ncols=1, folder=folder)
    
    plt.close()

def main():
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts=os.path.dirname(os.path.realpath(__file__)),
        folderData="/mnt/f/Desktop/LES_Data"
    )
    
    customLegend(folder=folder.outputs)



if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
