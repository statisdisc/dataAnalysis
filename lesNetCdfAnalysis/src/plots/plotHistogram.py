import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
plt.style.use("dark_background")
plt.rcParams["font.family"] = "serif"

def normalDist(x, xMean, xVar, amplitude=1.):
    return amplitude/np.sqrt(2*np.pi*xVar) * np.exp(-0.5*(x-xMean)**2/xVar)
    
    
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
    # tot, bins, patches = ax0.hist(updraftData, bins=100, range=(field.min, field.max), facecolor="k", edgecolor="r")
    
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

def plotHistogramWithGaussian(field, fieldI2, layer, layerIndex, title="", folder=""):
    
    # Make data 1D for use in histograms
    data = field.field[layerIndex].flatten()
    labelData = fieldI2.field[layerIndex].flatten()
    
    # Filter out cells which are in the updraft fluid and the other fluid
    dataFluid2 = labelData*data
    dataFluid2 = dataFluid2[dataFluid2 != 0]
    
    dataFluid1 = (1-labelData)*data
    dataFluid1 = dataFluid1[dataFluid1 != 0]
    
    # Volume fractions
    sigma1 = len(dataFluid1)/float(len(data))
    sigma2 = len(dataFluid2)/float(len(data))
    
    
    
    fig, (ax0, ax1) = plt.subplots(1,2,figsize=(5,4), gridspec_kw={'width_ratios': [10, 1]})
    
    # Plot histograms
    # tot, bins, patches = ax0.hist(data, bins=100, range=(field.min, field.max), facecolor="k", edgecolor="w")
    tot, bins, patches = ax0.hist(dataFluid1, bins=100, range=(field.min, field.max), facecolor="k", edgecolor="b")
    tot, bins, patches = ax0.hist(dataFluid2, bins=100, range=(field.min, field.max), facecolor="k", edgecolor="r")
    weight = (bins[1]-bins[0])*len(data)
    
    # Overlay Gaussian profiles
    x = np.linspace(field.min, field.max, 500)
    normal1 = normalDist(x, field.fluid1[layerIndex], field.fluid1Var[layerIndex], amplitude=sigma1)
    normal2 = normalDist(x, field.fluid2[layerIndex], field.fluid2Var[layerIndex], amplitude=sigma2)
    
    ax0.plot(x, normal1*weight, color="w", linewidth=1.5, linestyle="-")
    ax0.plot(x, normal1*weight, color="b", linewidth=1.5, linestyle="--")
    ax0.plot(x, normal2*weight, color="w", linewidth=1.5, linestyle="-")
    ax0.plot(x, normal2*weight, color="r", linewidth=1.5, linestyle="--")
    
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
        os.path.join(folder, "histogram+gaussian_{}_{}.png".format(field.name, layerIndex+1)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()