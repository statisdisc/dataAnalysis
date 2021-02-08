'''
Simple script to learn about the structure of the LES data.
To use LES data structures from source code, see other scripts.
'''

import os
import sys
from scipy.io import netcdf
import numpy as np

def main():
    folderMain = os.path.dirname(os.path.realpath(__file__))
    folderData = folderMain
    data = netcdf.NetCDFFile(os.path.join(folderData, "mov0235_ALL_01-_.nc"), 'r')

    # Time
    t = data.variables["TIME"][:]*1

    # Range of x, y and z values
    x = data.variables["X"][:]*1
    y = data.variables["Y"][:]*1
    z = data.variables["Z"][:]*1

    # Range of x, y, and z values as vectors
    # E.g. [0, 0, 20] and [0, 0, 40]
    x2 = data.variables["X2"][:]*1
    y2 = data.variables["Y2"][:]*1
    z2 = data.variables["Z2"][:]*1

    # Velocities
    u = data.variables["U"][:]*1
    v = data.variables["V"][:]*1
    w = data.variables["W"][:]*1

    # Potential temperature
    theta = data.variables["THETA"][:]*1

    # Moisture variables
    q1 = data.variables["Q01"][:]*1     # Vapour, qv (Specific humidity)
    q2 = data.variables["Q02"][:]*1     # Liquid, ql (Specific humidity)
    q3 = data.variables["Q03"][:]*1     # Radiative tracer, q (timescale, tau=15min)
    q4 = data.variables["Q04"][:]*1     # Radiative tracer for deep convection, q (timescale, tau=35min)

    for variable in data.variables:
        print variable

    data.close()

    print "t: {}".format(len(t))
    print t

    # print "x: {}".format(len(x))
    # print x

    # print "y: {}".format(len(y))
    # print y

    # print "z: {}".format(len(z))
    # print z

    # print "x2: {}".format(len(x2))
    # print x2

    # print "y2: {}".format(len(y2))
    # print y2

    # print "z2: {}".format(len(z2))
    # print z2

    print "u: {}".format(len(u[0][0][0]))
    print "v: {}".format(len(v))
    print "w: {}".format(len(w))
    
    print "Moisture and tracers:"
    print q1[0][100][100]
    print q2[0][100][100]
    print q3[0][100][100]
    print q4[0][100][100]

if __name__ == "__main__":
    timeInit = time.time()
    main()
    timeElapsed = time.time()
    print "Elapsed time: {:.2f}s".format(timeElapsed-timeInit)