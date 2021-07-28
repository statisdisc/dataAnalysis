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

def plotVolumeFractionComparison(
        folderLEM,
        folderMONC,
        title="", 
        folder=""
    ):
    print("Plotting vertical mean profile comparison for volume fraction")
    profileLEM = np.load(os.path.join(folderLEM, "z_profile_sigma.npz"))
    profileMONC = np.load(os.path.join(folderMONC, "z_profile_sigma.npz"))
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    # Mean profiles
    ax0.plot(profileLEM["sigma2"], profileLEM["z"], "r", linewidth=2.)
    
    ax0.plot(profileMONC["sigma2"], profileMONC["z"], "w", linewidth=1.)
    ax0.plot(profileMONC["sigma2"], profileMONC["z"], "r--", linewidth=1.)
    print(profileMONC["sigma2"])
    # ax0.plot(profile1["av"],     profile1["z"], "k", linewidth=0.5)    
    
    # Limits and labels
    # ax0.set_xlim(profile1["min"], profile1["max"])
    ax0.set_xlim(0, 1)
    ax0.set_ylim(np.min(profileLEM["z"]), np.max(profileLEM["z"]))
    ax0.set_xlabel("$\\sigma_2$")
    ax0.set_ylabel("z (km)")
    plt.title(title)
    
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    plt.savefig(
        os.path.join(folder, "lem_vs_monc_sigma.png"), 
        bbox_inches="tight", 
        dpi=300
    )
    plt.close()

# Plot horizontally averaged fields and their range of values
def plotVerticalProfileComparison(
        field,
        folderLEM,
        folderMONC,
        title="", 
        xlabel="", 
        folder="",
        plotZero=False,
        additionalLines=[]
    ):
    print("Plotting vertical mean profile comparison for field {}".format(field))
    profileLEM = np.load(os.path.join(folderLEM, "z_{}.npz".format(field)))
    profileMONC = np.load(os.path.join(folderMONC, "z_{}.npz".format(field)))
    
    fig, ax0 = plt.subplots(1,1,figsize=(5,4))
    
    if plotZero:
        ax0.plot(0*profileLEM["z"], profileLEM["z"], "k:", linewidth=0.5)
    
    # Mean profiles
    ax0.plot(profileLEM["fluid1"], profileLEM["z"], "b", linewidth=2.)
    ax0.plot(profileLEM["fluid2"], profileLEM["z"], "r", linewidth=2.)
    
    ax0.plot(profileMONC["fluid1"], profileMONC["z"], "w", linewidth=1.)
    ax0.plot(profileMONC["fluid1"], profileMONC["z"], "b--", linewidth=1.)
    ax0.plot(profileMONC["fluid2"], profileMONC["z"], "w", linewidth=1.)
    ax0.plot(profileMONC["fluid2"], profileMONC["z"], "r--", linewidth=1.)
    
    for i in range(len(additionalLines)):
        ax0.plot(additionalLines[i][0], additionalLines[i][1], color=additionalLines[i][2], linewidth=0.5)
    
    # ax0.plot(profile1["av"],     profile1["z"], "k", linewidth=0.5)    
    
    # Limits and labels
    # ax0.set_xlim(profile1["min"], profile1["max"])
    ax0.set_xlim(
        min(
            np.min(profileLEM["fluid1"][~np.isnan(profileLEM["fluid1"])]), 
            np.min(profileMONC["fluid1"][~np.isnan(profileMONC["fluid1"])])
        ), 
        max(
            np.max(profileLEM["fluid2"][~np.isnan(profileLEM["fluid2"])]), 
            np.max(profileMONC["fluid2"][~np.isnan(profileMONC["fluid2"])])
        )
    )
    ax0.set_ylim(np.min(profileLEM["z"]), np.max(profileLEM["z"]))
    ax0.set_xlabel(xlabel)
    ax0.set_ylabel("z (km)")
    plt.title(title)
    
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    plt.savefig(
        os.path.join(folder, "lem_vs_monc_{}.png".format(field)), 
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