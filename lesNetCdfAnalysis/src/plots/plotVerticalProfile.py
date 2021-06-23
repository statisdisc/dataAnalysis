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
from scipy.io import savemat

# Plot the horizontally averaged volume fraction
def plotVolumeFraction(
        z, I2, 
        title="", 
        id="",
        folder=""
    ):
    print("Plotting volume fraction")
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    ax0.plot(I2.av, z, "r")
    
    # Limits and labels
    ax0.set_xlim(0., 1.)
    ax0.set_ylim(np.min(z), np.max(z))
    ax0.set_xlabel("$\\sigma_2$")
    ax0.set_ylabel("z (km)")
    plt.title("Volume fraction")
    
    # Create folder for image
    folderVertical = os.path.join(folder, "profilesMean")
    if id != "":
        folderVertical = os.path.join(folderVertical, id)
    if not os.path.isdir(folderVertical):
        os.makedirs(folderVertical)
    
    plt.savefig(
        os.path.join(folderVertical, "profile_sigma.png"), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()
    
    # Save vertical profiles for future use
    np.savez(
        os.path.join(folderVertical, "z_profile_sigma.npz"), 
        z = z,
        sigma1 = 1.-I2.av,
        sigma2 =    I2.av
    )

# Plot horizontally averaged fields and their range of values
def plotVerticalProfile(
        z, field,
        title="", 
        xlabel="", 
        folder="",
        id="",
        plotZero=False
    ):
    print("Plotting vertical mean profiles for field {}".format(field.name))
    
    zkm = 1e-3*z
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    if plotZero:
        ax0.plot(0*zkm, zkm, "k:", linewidth=0.5)
    
    # Shaded regions for standard deviation range
    ax0.fill_betweenx(
        zkm, field.fluid1-field.fluid1Std, field.fluid1+field.fluid1Std, 
        facecolor=(0.,0.,0.5), 
        linewidth=0., 
        alpha=0.2
    )
    ax0.fill_betweenx(
        zkm, field.fluid2-field.fluid2Std, field.fluid2+field.fluid2Std, 
        facecolor=(0.5,0.,0.), 
        linewidth=0., 
        alpha=0.2
    )
    
    # Minimum and maximum range
    ax0.plot(field.fluid1Min, zkm, "b--", linewidth=0.5, alpha=0.3)
    ax0.plot(field.fluid1Max, zkm, "b--", linewidth=0.5, alpha=0.3)
    ax0.plot(field.fluid2Min, zkm, "r--", linewidth=0.5, alpha=0.3)
    ax0.plot(field.fluid2Max, zkm, "r--", linewidth=0.5, alpha=0.3)
    
    # Mean profiles
    ax0.plot(field.fluid1, zkm, "b", linewidth=2.)
    ax0.plot(field.fluid2, zkm, "r", linewidth=2.)
    ax0.plot(field.av,     zkm, "k", linewidth=1.)    
    
    # Limits and labels
    ax0.set_xlim(field.min, field.max)
    ax0.set_ylim(np.min(zkm), np.max(zkm))
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel("z (km)")
    plt.title(title)
    
    # Create folder for image
    folderVertical = os.path.join(folder, "profilesMean")
    if id != "":
        folderVertical = os.path.join(folderVertical, id)
    if not os.path.isdir(folderVertical):
        os.makedirs(folderVertical)
    
    plt.savefig(
        os.path.join(folderVertical, "profile_{}.png".format(field.name)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()
    
    # Save vertical profiles for future use
    np.savez(
        os.path.join(folderVertical, "z_{}.npz".format(field.name)), 
        z = z,
        av = field.av,
        min = field.min,
        max = field.max,
        fluid1 = field.fluid1,
        fluid2 = field.fluid2,
        fluid1Std = field.fluid1Std,
        fluid2Std = field.fluid2Std,
        fluid1Min = field.fluid1Min,
        fluid1Max = field.fluid1Max,
        fluid2Min = field.fluid2Min,
        fluid2Max = field.fluid2Max
    )
    
    # Save vertical profiles in MATLAB readable format
    if id == "plumeEdge":
        savemat(
            os.path.join(folderVertical, "z_{}.mat".format(field.name)), 
            {
                "z": z,
                "transfer12": field.fluid2,
                "transfer21": field.fluid2
            }
        )
    else:
        savemat(
            os.path.join(folderVertical, "z_{}.mat".format(field.name)), 
            {
                "z": z,
                "av": field.av,
                "min": field.min,
                "max": field.max,
                "fluid1": field.fluid1,
                "fluid2": field.fluid2,
                "fluid1Std": field.fluid1Std,
                "fluid2Std": field.fluid2Std,
                "fluid1Min": field.fluid1Min,
                "fluid1Max": field.fluid1Max,
                "fluid2Min": field.fluid2Min,
                "fluid2Max": field.fluid2Max
            }
        )

# Plot the vertical fluxes
def plotVerticalFluxes(
        z, field,
        title="", 
        xlabel="", 
        folder="",
        id="",
        plotZero=True
    ):
    print("Plotting vertical fluxes for field {}".format(field.name))
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    if plotZero:
        ax0.plot(0*z, z, "k:", linewidth=0.5)
    
    # Minimum and maximum range
    ax0.plot(field.fluid1FluxSubgrid, z, "b", linewidth=1., alpha=0.3)
    ax0.plot(field.fluid2FluxSubgrid, z, "r", linewidth=1., alpha=0.3)
    
    # Mean profiles
    ax0.plot(field.fluid1FluxResolved, z, "b", linewidth=2.)
    ax0.plot(field.fluid2FluxResolved, z, "r", linewidth=2.)
    
    # Toal fluxes (contributions should sum to the total)
    # ax0.plot(field.flux, z, "k", linewidth=2.)
    # ax0.plot(field.fluid1FluxResolved+field.fluid2FluxResolved+field.fluid1FluxSubgrid+field.fluid2FluxSubgrid, z, "#888888", linewidth=1.)
        
    
    # Limits and labels
    minMax = max(
        abs(min(np.min(field.fluid1FluxResolved), np.min(field.fluid2FluxResolved))),
        abs(max(np.max(field.fluid1FluxResolved), np.max(field.fluid2FluxResolved)))
    )
    ax0.set_xlim(-1.2*minMax, 1.2*minMax)
    ax0.set_ylim(np.min(z), np.max(z))
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel("z (km)")
    ax0.tick_params(axis='both', labelsize=6)
    plt.title(title)
    
    # Create folder for image
    folderFluxes = os.path.join(folder, "profilesFluxes")
    if id != "":
        folderFluxes = os.path.join(folderFluxes, id)
    if not os.path.isdir(folderFluxes):
        os.makedirs(folderFluxes)
    
    plt.savefig(
        os.path.join(folderFluxes, "profile_flux_{}.png".format(field.name)), 
        bbox_inches="tight", 
        dpi=200
    )
    plt.close()
    
    # Save vertical profiles for future use
    np.savez(
        os.path.join(folderFluxes, "z_profile_flux_{}.npz".format(field.name)), 
        z = z,
        fluid1FluxResolved = field.fluid1FluxResolved,
        fluid2FluxResolved = field.fluid2FluxResolved,
        fluid1FluxSubgrid = field.fluid1FluxSubgrid,
        fluid2FluxSubgrid = field.fluid2FluxSubgrid
    )
    
    # Save vertical profiles in MATLAB readable format
    savemat(
        os.path.join(folderFluxes, "z_{}.mat".format(field.name)), 
        {
            "z": z,
            "fluid1FluxResolved": field.fluid1FluxResolved,
            "fluid2FluxResolved": field.fluid2FluxResolved,
            "fluid1FluxSubgrid": field.fluid1FluxSubgrid,
            "fluid2FluxSubgrid": field.fluid2FluxSubgrid
        }
    )