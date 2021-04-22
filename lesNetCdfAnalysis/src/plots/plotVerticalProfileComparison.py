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
# plt.style.use("dark_background")
# plt.rcParams["font.family"] = "serif"

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
def plotVerticalProfileComparison(
        field,
        id1,
        id2,
        id3="",
        id4="",
        title="", 
        xlabel="", 
        folder="",
        plotZero=False
    ):
    print("Plotting vertical mean profile comparison for field {}".format(field))
    folderVertical = os.path.join(folder, "profilesMean")
    
    folderVertical1 = os.path.join(folderVertical, id1)
    profile1 = np.load(os.path.join(folderVertical1, "z_profile_{}.npz".format(field)))
    
    folderVertical2 = os.path.join(folderVertical, id2)
    profile2 = np.load(os.path.join(folderVertical2, "z_profile_{}.npz".format(field)))
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    if plotZero:
        ax0.plot(0*profile1["z"], profile1["z"], "k:", linewidth=0.5)
    
    # Shaded regions for standard deviation range
    ax0.fill_betweenx(
        profile1["z"], profile1["fluid1"]-profile1["fluid1Std"], profile1["fluid1"]+profile1["fluid1Std"], 
        facecolor=(0.,0.,0.5), 
        linewidth=0., 
        alpha=0.2
    )
    ax0.fill_betweenx(
        profile1["z"], profile1["fluid2"]-profile1["fluid2Std"], profile1["fluid2"]+profile1["fluid2Std"], 
        facecolor=(0.5,0.,0.), 
        linewidth=0., 
        alpha=0.2
    )
    
    # Minimum and maximum range
    ax0.plot(profile1["fluid1Min"], profile1["z"], "--", linewidth=0.5, color="#888888", alpha=0.5)
    ax0.plot(profile1["fluid2Max"], profile1["z"], "--", linewidth=0.5, color="#888888", alpha=0.5)
    
    # Mean profiles
    ax0.plot(profile1["fluid1"], profile1["z"], "b", linewidth=1.)
    ax0.plot(profile1["fluid2"], profile1["z"], "r", linewidth=1.)
    
    ax0.plot(profile2["fluid1"], profile2["z"], "b--", linewidth=0.5)
    ax0.plot(profile2["fluid2"], profile2["z"], "r--", linewidth=0.5)
    
    if id3 != "":
        folderVertical3 = os.path.join(folderVertical, id3)
        profile3 = np.load(os.path.join(folderVertical3, "z_profile_{}.npz".format(field)))
        
        ax0.plot(profile3["fluid2"], profile3["z"], ":", linewidth=0.5, color="k")
    
    if id4 != "":
        folderVertical4 = os.path.join(folderVertical, id4)
        profile4 = np.load(os.path.join(folderVertical4, "z_profile_{}.npz".format(field)))
        
        ax0.plot(profile4["fluid2"], profile4["z"], ":", linewidth=0.5, color="#888888")
    
    # ax0.plot(profile1["av"],     profile1["z"], "k", linewidth=0.5)    
    
    # Limits and labels
    # ax0.set_xlim(profile1["min"], profile1["max"])
    ax0.set_xlim(np.min(profile1["fluid1"]), np.max(profile1["fluid2"]))
    ax0.set_ylim(np.min(profile1["z"]), np.max(profile1["z"]))
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel("z (km)")
    plt.title(title)
    
    # Save vertical profiles for future use
    savemat(os.path.join(folderVertical, "z_plumeEdge_{}.mat").format(field), profile2)
    
    
    plt.savefig(
        os.path.join(folderVertical, "profileComparison_{}.png".format(field)), 
        bbox_inches="tight", 
        dpi=300
    )
    plt.close()

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