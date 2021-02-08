import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
plt.style.use("dark_background")
plt.rcParams["font.family"] = "serif"

def plotLayerHistogram(field, fieldI2, layer, layerIndex, title="", folder=""):
    
    # Make data 1D for use in histograms
    data = field.field[layerIndex].flatten()
    labelData = fieldI2.field[layerIndex].flatten()
    
    # Filter out cells which are in the updraft
    updraftData = (labelData*data)
    updraftData = updraftData[updraftData != 0]
    
    
    fig, (ax0, ax1) = plt.subplots(1,2,figsize=(5,4), gridspec_kw={'width_ratios': [10, 1]})
    
    # Plot histograms
    tot, bins, patches = ax0.hist(data, bins=100, range=(field.min, field.max), facecolor="k", edgecolor="w")
    tot, bins, patches = ax0.hist(updraftData, bins=100, range=(field.min, field.max), facecolor="k", edgecolor="r")
    
    # Limits and labels
    ax0.set_xlim(field.min, field.max)
    ax0.set_ylim(0.,2.5e4)
    ax0.set_xlabel("{}".format(field.name))
    ax0.set_ylabel("Frequency")
    plt.suptitle(title)
    
    # Additional subplot to visualise the height of this layer
    ax1.plot([0.,1.],[layer, layer], linewidth=2., color="#FFFFFF")
    ax1.set_xlim(0.,1.)
    ax1.set_ylim(0.,4.5)
    plt.ylabel("z (km)")
    
    # Move ticks and labels to right side
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    # Remove x labels
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    
    # Create folder for image
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    plt.savefig(
        os.path.join(folder, "histogram_{}_{}.png".format(field.name, layerIndex+1)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()