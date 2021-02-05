import os
import sys
import numpy as np
import matplotlib.pyplot as plt
    
def sumItemData(timestamps, entries):
    meanPrice = []
    timestamps = sorted(timestamps)
    
    
    for timestamp in timestamps:
        meanPrice.append(entries[timestamp]["TotalSpent"]/entries[timestamp]["TotalSold"])

    timestamps = np.array(timestamps)
    meanPrice = np.array(meanPrice)
    
    return timestamps, meanPrice


def smoothData(data, smoothingRange=7, periodic=False):
    dataSmooth = data.copy()
    
    if periodic == True:
        for i in xrange(len(data)):
            dataSmooth[i] = np.mean( np.roll(data, 7-i)[:15] )
    else:
        for i in xrange(len(data)):
            indexMin = max(0, i-smoothingRange)
            indexMax = min(i+smoothingRange, len(dataSmooth))
            dataSmooth[i] = np.mean(data[indexMin:indexMax])
        
    return dataSmooth
    
def plotSimpleTimeseries(x, y, ySmooth, fileId="default"):
    plt.figure(figsize=(8,4))
    
    plt.plot(x, y, color="#888888")
    plt.plot(x, ySmooth, color="k", linewidth=2.)
    
    plt.xlim(np.min(x), np.max(x))
    plt.ylim(0., 0.5)
    
    plt.savefig( os.path.join(sys.path[0], "z_timeseries_{}.png".format(fileId)), dpi=200 )
    plt.close()