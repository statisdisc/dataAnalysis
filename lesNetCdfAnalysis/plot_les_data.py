import os
import sys
from scipy.io import netcdf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use("dark_background")
plt.rcParams["font.family"] = "serif"

folderMain = os.path.dirname(os.path.realpath(__file__))
folderData = folderMain
data = netcdf.NetCDFFile(os.path.join(folderData, "mov0235_ALL_01-_.nc"), 'r')

# Time
t = data.variables["TIME"][:]*1

# Range of x, y and z values
x = data.variables["X"][:]*1
y = data.variables["Y"][:]*1
z = data.variables["Z"][:]*1

variables = ["U", "V", "W", "THETA", "Q01", "Q02", "Q03", "Q04"]
variables = ["U", "V", "W", "THETA", "Q01", "Q02", "Q03"]
# variables = ["U"]
# variables = ["THETA"]

for variable in variables:
    print variable
    folderVariable = os.path.join(folderMain, variable)
    if not os.path.isdir(folderVariable):
        os.makedirs(folderVariable)
    
    variable_data = (data.variables[variable][:]*1)[0]
    
    data_min = np.min(variable_data)
    data_max = np.max(variable_data)
    
    for k in xrange(len(z)):
        layer = z[k]*1e-3
        print "Layer {} ({:.3f}km)".format(k+1, layer)
        layer_data = variable_data[k]
        
        
        fig, (ax0, ax1) = plt.subplots(1,2,figsize=(5,4), gridspec_kw={'width_ratios': [10, 1]})
        
        tot, bins, patches = ax0.hist(layer_data.flatten(), bins=100, range=(data_min, data_max), facecolor="k", edgecolor="w")
        
        ax0.set_xlim(data_min, data_max)
        ax0.set_ylim(0.,2.5e4)
        ax0.set_xlabel("{}".format(variable))
        ax0.set_ylabel("Frequency")
        plt.suptitle("z = {:.2f}km (id={})".format(layer, k+1))
        
        ax1.plot([0.,1.],[layer, layer], linewidth=2., color="#FFFFFF")
        ax1.set_xlim(0.,1.)
        ax1.set_ylim(0.,4.5)
        plt.ylabel("z (km)")
        
        ax1.yaxis.tick_right()
        ax1.yaxis.set_label_position("right")
        ax1.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        
        plt.savefig( os.path.join(folderVariable, "histogram_{}_{}.png".format(variable, k+1)), bbox_inches="tight", dpi=200 )
        plt.close()
        # break
    # break

data.close()

#Clear memory
data = 1
variable_data = 1
layer_data = 1
x = 1
y = 1
z = 1
t = 1
