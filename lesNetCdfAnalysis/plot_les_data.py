import os
import sys
from scipy.io import netcdf
import numpy as np
import matplotlib as mpl
import matplotlib
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use("dark_background")
plt.rcParams["font.family"] = "serif"

folderMain = os.path.dirname(os.path.realpath(__file__))
folderData = "/mnt/f/Desktop/LES_Data"
data = netcdf.NetCDFFile(os.path.join(folderData, "mov0235_ALL_01-_.nc"), 'r')

# Time
t = data.variables["TIME"][:]*1

# Range of x, y and z values
x = data.variables["X"][:]*1
y = data.variables["Y"][:]*1
z = data.variables["Z"][:]*1

data.variables["qv"] = data.variables.pop("Q01")
data.variables["ql"] = data.variables.pop("Q02")
data.variables["q"] = data.variables.pop("Q03")


def getUpdraftIndicator(q, w):
    #Mean of each horizontal slice
    qMean = np.mean(q, axis=(1,2))
    
    #Standard deviation of each horizontal slice
    qStdv = np.std(q, axis=(1,2))
    
    #Sum of all previous elements in array (including current)
    qStdvIntegral = np.cumsum(qStdv)
    
    qStdvMax = np.maximum(qStdv, qStdvIntegral)
    
    #Transform array to be compatible with 3D array
    qMean = qMean.reshape((len(qMean),1))
    qStdv = qStdv.reshape((len(qStdv),1))
    qStdvMax = qStdv.reshape((len(qStdvMax),1))

    qCondition = q - qMean[:,None] - qStdvMax[:,None]

    # print ""
    # print qMean[0]
    # print qDash[0][0][0]
    # print qDash[0][0][1]
    # print qDash[0][1][0]

    condition1 = qCondition > 0.
    condition2 = w > 0.
    return condition1*condition2

I2 = getUpdraftIndicator(data.variables["q"][:][0], data.variables["W"][:][0])

variables = ["U", "V", "W", "THETA", "Q01", "Q02", "Q03", "Q04"]
variables = ["U", "V", "W", "THETA", "qv", "ql"]
variables = ["W"]
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
        layer_data = variable_data[k].flatten()
        label_data = I2[k].flatten()
        updraft_data = (label_data*layer_data)
        updraft_data = updraft_data[updraft_data != 0]
        
        
        fig, (ax0, ax1) = plt.subplots(1,2,figsize=(5,4), gridspec_kw={'width_ratios': [10, 1]})
        
        tot, bins, patches = ax0.hist(layer_data, bins=100, range=(data_min, data_max), facecolor="k", edgecolor="w")
        tot, bins, patches = ax0.hist(updraft_data, bins=100, range=(data_min, data_max), facecolor="k", edgecolor="r")
        
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
