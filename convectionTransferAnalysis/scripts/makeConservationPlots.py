'''
Create the energy and momentum conservation plots for numerical methods for transferring
mass, momentum and heat between fluids in a multi-fluid convection model.
These plots are found in McIntyre et a. (2020), https://doi.org/10.1002/qj.3728
'''
import os
import sys
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.scale as mscale


# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.objects.squareRootScale import squareRootScale
mscale.register_scale(squareRootScale)
from src.utilities.energy import *

def main():
    
    # Fetch folders for code structure
    folder = folders(
        folderScripts=os.path.dirname(os.path.realpath(__file__)),
        folderData="/mnt/f/Desktop/LES_Data"
    )
    
    # Spacial and temporal discretisation
    dt = np.linspace(0.,2.,21)
    dt = np.linspace(0.,2.,51)
    xf = np.linspace(0.,1.,21)[:-1]
    xc = xf + (xf[1]-xf[0])/2.
    
    # Choose whether to have co-located grid (A-grid) or staggered grid (C-grid)
    velocity_face = False
    
    # Set resolution of parameter space to sample. 
    # Note that processing time scales as resolution^3
    resolution = 50
    resolution = 11

    eta1_arr = np.linspace(0.01,2.,resolution)
    u1_arr = np.linspace(0.,2.,resolution)
    S10_arr = np.linspace(0.,1.,resolution)

    eta1_arr = np.linspace(1e-8,2.,resolution)
    u1_arr = np.linspace(-150.,150.,resolution)
    S10_arr = np.linspace(0.,1.,resolution)
    # S10_arr = np.array([1.])

    # Placeholder arrays which will be multiplied by a factor later on
    eta0 = np.ones(len(xc))
    eta1 = np.ones(len(xc))
    theta0 = 300.*np.ones(len(xc))
    theta1 = 301.*np.ones(len(xc))
    u0 = np.ones(len(xf))
    u1 = np.ones(len(xf))
    S01 = np.ones(len(xc))
    S10 = np.ones(len(xc))
    
    # Make transfers like a square wave to test stability at steep gradients
    # Only necessary for staggered grids.
    for j in xrange(len(S01)):
        if xc[j] < 0.2 or xc[j] > 0.8:
            S01[j] = 0.
            S10[j] = 0.

    # Allowed numerical schemes
    # test_cases = [["flux","n","n",0,0],["flux","n+1","n+1",1,1]]
    test_cases = [["advective","n","n",0,1],["advective","n","n+1",0,0],["advective","n+1","n",1,1],["advective","n+1","n+1",1,0]]
    
    delta_ke_list = []
    for test_case in test_cases:
        momentum_eq = test_case[0]
        q = test_case[1]
        r = test_case[2]
        
        delta_ke_min =  1e+16*np.ones((2,2,len(dt)))
        delta_ke_max = -1e+16*np.ones((2,2,len(dt)))
        delta_ke_mean = np.zeros((2,2,len(dt)))
        delta_f_min =  1e+16*np.ones((2,2,len(dt)))
        delta_f_max = -1e+16*np.ones((2,2,len(dt)))
        delta_f_mean = np.zeros((2,2,len(dt)))
        
        # Try different timesteps. Explicit schemes tend to become unstable for large dt.
        for n in xrange(len(dt)):
            print dt[n]
            
            # Cycle over all parameter space
            for ie in eta1_arr:
                for iu in u1_arr:
                    for iS in S10_arr:
                        # eta = [(1-eta1_arr[ie])*eta0.copy(), eta1_arr[ie]*eta1.copy()]
                        eta = [eta0.copy(), ie*eta1.copy()]
                        theta = [theta0.copy(), theta1.copy()]
                        u = [u0.copy(),iu*u1.copy()]
                        S = [[0*S01,S01],[iS*S10,0*S10]]
                        
                        # Canculate energy, momentum and velocity changes
                        delta_ke_00,delta_f_00,u_new_00 = deltaE(eta, theta, u, dt[n], S, 0, 0, 0, q, r, velocity_face=velocity_face, momentum_eq=momentum_eq)
                        delta_ke_01,delta_f_01,u_new_01 = deltaE(eta, theta, u, dt[n], S, 0, 1, 1, q, r, velocity_face=velocity_face, momentum_eq=momentum_eq)
                        delta_ke_10,delta_f_10,u_new_10 = deltaE(eta, theta, u, dt[n], S, 1, 0, 0, q, r, velocity_face=velocity_face, momentum_eq=momentum_eq)
                        delta_ke_11,delta_f_11,u_new_11 = deltaE(eta, theta, u, dt[n], S, 1, 1, 1, q, r, velocity_face=velocity_face, momentum_eq=momentum_eq)
                        
                        # Update maximum recorded maxima and minima
                        delta_ke_min[0][0][n] = min(delta_ke_min[0][0][n], np.min(delta_ke_00))
                        delta_ke_max[0][0][n] = max(delta_ke_max[0][0][n], np.max(delta_ke_00))
                        delta_ke_mean[0][0][n] += np.mean(delta_ke_00)/(1.*resolution**3)
                        
                        delta_ke_min[0][1][n] = min(delta_ke_min[0][1][n], np.min(delta_ke_01))
                        delta_ke_max[0][1][n] = max(delta_ke_max[0][1][n], np.max(delta_ke_01))
                        delta_ke_mean[0][1][n] += np.mean(delta_ke_01)/(1.*resolution**3)
                        
                        delta_ke_min[1][0][n] = min(delta_ke_min[1][0][n], np.min(delta_ke_10))
                        delta_ke_max[1][0][n] = max(delta_ke_max[1][0][n], np.max(delta_ke_10))
                        delta_ke_mean[1][0][n] += np.mean(delta_ke_10)/(1.*resolution**3)
                        
                        delta_ke_min[1][1][n] = min(delta_ke_min[1][1][n], np.min(delta_ke_11))
                        delta_ke_max[1][1][n] = max(delta_ke_max[1][1][n], np.max(delta_ke_11))
                        delta_ke_mean[1][1][n] += np.mean(delta_ke_11)/(1.*resolution**3)
                        
                        delta_f_min[0][0][n] = min(delta_f_min[0][0][n], np.min(delta_f_00))
                        delta_f_max[0][0][n] = max(delta_f_max[0][0][n], np.max(delta_f_00))
                        delta_f_mean[0][0][n] += np.mean(delta_f_00)/(1.*resolution**3)
                        
                        delta_f_min[0][1][n] = min(delta_f_min[0][1][n], np.min(delta_f_01))
                        delta_f_max[0][1][n] = max(delta_f_max[0][1][n], np.max(delta_f_01))
                        delta_f_mean[0][1][n] += np.mean(delta_f_01)/(1.*resolution**3)
                        
                        delta_f_min[1][0][n] = min(delta_f_min[1][0][n], np.min(delta_f_10))
                        delta_f_max[1][0][n] = max(delta_f_max[1][0][n], np.max(delta_f_10))
                        delta_f_mean[1][0][n] += np.mean(delta_f_10)/(1.*resolution**3)
                        
                        delta_f_min[1][1][n] = min(delta_f_min[1][1][n], np.min(delta_f_11))
                        delta_f_max[1][1][n] = max(delta_f_max[1][1][n], np.max(delta_f_11))
                        delta_f_mean[1][1][n] += np.mean(delta_f_11)/(1.*resolution**3)
                        
                        
                        
        
        # Define colors and linestyles necessary to distinguish between similar profiles
        colors = [["#7a7a7a","b"],["r","k"]]
        linestyles = ["-","--",":","-."]
        linestyles = ["-","-","-","-"]
        
        # plt.figure(figsize=(5,5))
        plt.figure(figsize=(9,4))
        
        spread = np.zeros((4))
        for i in xrange(2):
            for j in xrange(2):
                spread[2*i+j] = np.max(delta_ke_max[i][j]-delta_ke_min[i][j])
        spread_index = spread.argsort()[::-1]
        
        # Fill region between maximum and minimum regions
        for n in spread_index:
            j = n%2
            i = (n-j)/2
            
            delta_ke_min[i][j] = delta_ke_min[i][j].clip(min=-1e2)
            delta_ke_max[i][j] = delta_ke_max[i][j].clip(max= 1e2)
            for k in xrange(len(delta_ke_min[i][j])):
                if delta_ke_min[i][j][k] < 1e-13 and delta_ke_min[i][j][k] > -1e-13:
                    delta_ke_min[i][j][k] = 0.
                if delta_ke_max[i][j][k] < 1e-13 and delta_ke_max[i][j][k] > -1e-13:
                    delta_ke_max[i][j][k] = 0.
            
            y1 = delta_ke_min[i][j]
            y2 = delta_ke_max[i][j]
            if i == j:
                plt.fill_between(dt, y1, y2, where= y2 >= y1, facecolor=colors[i][j], interpolate=True, linewidth=0., alpha = 0.5)
                
                
        
        for n in xrange(len(spread_index)):
            j = spread_index[n]%2
            i = (spread_index[n]-j)/2
            
            # If maximum value is 0 (to numerical precision), indicate the energy-diminishing properties
            linewidth = 3.
            linestyle = "--"
            if np.max(delta_ke_max[i][j]) < 1e-13:
                linestyle = "-"

            if i == j:
                plt.plot(dt,delta_ke_min[i][j],color=colors[i][j], linestyle=linestyle, linewidth=linewidth)
                plt.plot(dt,delta_ke_max[i][j],color=colors[i][j], linestyle=linestyle, linewidth=linewidth)
                
        
        plt.plot(dt,0*dt,":",color="w")
        
        # Labels and formating
        plt.xlabel("$\\Delta t$ $S_{01}$",fontsize=20)
        plt.ylabel("Rel. Energy change, $\\Delta E_{REL}$",fontsize=20)
        plt.xlim(dt[0],dt[-1])
        plt.ylim(-3.9999e-2,3.9999e-2)
        plt.xscale("sqrt2")
        plt.yscale("sqrt2")
        
        filename = "conservation_ke_{}_q_{}_r_{}.png".format(test_case[0],q.replace("+","p"),r.replace("+","p"))
        plt.savefig( 
            os.path.join(folder.outputs,  filename), 
            bbox_inches='tight', 
            dpi=200
        )
        plt.close()
        
        
        # Save profiles for final energy plot
        if q == "n" and r == "n":
            delta_ke_list.append( [delta_ke_min[0][1], delta_ke_max[0][1], "b"] )
        if q == "n+1" and r == "n":
            delta_ke_list.append( [delta_ke_min[1][1], delta_ke_max[1][1], "k"] )
        if q == "n" and r == "n+1":
            delta_ke_list.append( [delta_ke_min[0][0], delta_ke_max[0][0], "#7a7a7a"] )
        if q == "n+1" and r == "n+1":
            delta_ke_list.append( [delta_ke_min[1][0], delta_ke_max[1][0], "r"] )
        
        
        # plt.figure(figsize=(5,5))
        plt.figure(figsize=(9,4))
        
        spread = np.zeros((4))
        for i in xrange(2):
            for j in xrange(2):
                spread[2*i+j] = np.max(delta_f_max[i][j]-delta_f_min[i][j])
        spread_index = spread.argsort()[::-1]
        
        for n in spread_index:
            j = n%2
            i = (n-j)/2
            
            delta_f_min[i][j] = delta_f_min[i][j].clip(min=-1e2)
            delta_f_max[i][j] = delta_f_max[i][j].clip(max= 1e2)
            for k in xrange(len(delta_f_min[i][j])):
                if delta_f_min[i][j][k] < 1e-13 and delta_f_min[i][j][k] > -1e-13:
                    delta_f_min[i][j][k] = 0.
                if delta_f_max[i][j][k] < 1e-13 and delta_f_max[i][j][k] > -1e-13:
                    delta_f_max[i][j][k] = 0.
            
            y1 = delta_f_min[i][j]
            y2 = delta_f_max[i][j]
            plt.fill_between(dt, y1, y2, facecolor=colors[i][j], interpolate=True, alpha = 0.5, linewidth=0.)
            
        for n in xrange(len(spread_index)):
            j = spread_index[n]%2
            i = (spread_index[n]-j)/2
            
            linewidth = 3.
            if n == 0:
                linewidth = 4.
            
            # Indicate whether a scheme conserves momentum to numerical precision
            linestyle = "--"
            if np.max(delta_f_max[i][j]) <= 1e-2 and np.min(delta_f_min[i][j]) >= -1e-2:
                linestyle = "-"

            plt.plot(dt,delta_f_min[i][j],color=colors[i][j], linestyle=linestyle, linewidth=linewidth)
            plt.plot(dt,delta_f_max[i][j],color=colors[i][j], linestyle=linestyle, linewidth=linewidth)
        
        plt.plot(dt,0*dt,":",color="w")
        
        # Labels and formating
        plt.xlabel("$\\Delta t$ $S_{01}$",fontsize=20)
        plt.ylabel("Rel. mom. change, $\\Delta F_{REL}$",fontsize=20)
        plt.xlim(dt[0],dt[-1])
        plt.ylim(-40.,40.)
        plt.xscale("sqrt2")
        plt.yscale("sqrt2")
        
        filename = "conservation_f_{}_q_{}_r_{}.png".format(test_case[0],q.replace("+","p"),r.replace("+","p"))
        plt.savefig( 
            os.path.join(folder.outputs,  filename), 
            bbox_inches='tight', 
            dpi=200
        )
        plt.close()
    
    
    
    # Plot energy profiles of hand-selected schemes
    plt.figure(figsize=(9,4))
    
    for n in xrange(len(delta_ke_list)):
        y1 = delta_ke_list[n][0]
        y2 = delta_ke_list[n][1]
        plt.fill_between(dt, y1, y2, facecolor=delta_ke_list[n][2], interpolate=True, linewidth=0., alpha = 0.5)
            
            

    for n in xrange(len(delta_ke_list)):
        linestyle = "--"
        if np.max(delta_ke_list[n][1]) < 1e-13:
            linestyle = "-"
        plt.plot(dt,delta_ke_list[n][0],color=delta_ke_list[n][2], linestyle=linestyle, linewidth=3.)
        plt.plot(dt,delta_ke_list[n][1],color=delta_ke_list[n][2], linestyle=linestyle, linewidth=3.)
            

    plt.plot(dt,0*dt,":",color="w")

    plt.xlabel("$\\Delta t$ $S_{01}$",fontsize=20)
    plt.ylabel("Rel. Energy change, $\\Delta E_{REL}$",fontsize=20)

    plt.xlim(dt[0],dt[-1])
    plt.ylim(-3.9999e-2,3.9999e-2)
    plt.xscale("sqrt2")
    plt.yscale("sqrt2")

    plt.savefig(os.path.join(folder.outputs, "conservation_ke.png") , bbox_inches='tight', dpi=200)
    plt.close()
    

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)
