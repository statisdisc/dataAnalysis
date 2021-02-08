'''
Object to store all Large Eddy Simulation data for a single timestep.
'''

import warnings
import numpy as np
from lesField import lesField

class lesDataSnapshot:
    def __init__(self, data, indexTime, indicatorType="shallow"):
        # Time
        self.t = data.variables["TIME"][:][indexTime]*1

        # Range of x, y and z values
        self.x = data.variables["X"][:]*1
        self.y = data.variables["Y"][:]*1
        self.z = data.variables["Z"][:]*1
        
        # Range of x, y and z values in vector form
        self.xv = data.variables["X2"][:]*1
        self.yv = data.variables["Y2"][:]*1
        self.zv = data.variables["Z2"][:]*1
        
        # Data for all cells
        # Velocity component in the x-direction
        self.u = lesField("U", "u", data, indexTime)
        # Velocity component in the y-direction
        self.v = lesField("V", "v", data, indexTime)
        # Velocity component in the z-direction (vertical velocity)
        self.w = lesField("W", "w", data, indexTime)
        # Potential temperature
        self.theta = lesField("THETA", "theta", data, indexTime)
        # Water vapour
        self.qv = lesField("Q01", "qv", data, indexTime)
        # Liquid water
        self.ql = lesField("Q02", "ql", data, indexTime)
        # Radioactive tracer for shallow convection (timescale 15 mins)
        self.rts = lesField("Q03", "rts", data, indexTime)
        # Radioactive tracer for deep convection (timescale 35 mins)
        self.rtd = lesField("Q04", "rtd", data, indexTime)
        
        # Diagnose indicator function which shows the locations of the updraft fluid (fluid 2)
        if indicatorType == "shallow":
            self.I2 = lesField(
                "I2", "I2", data, indexTime, 
                dataOverride=self.getUpdraftIndicator(self.rts.field)
            )
        elif indicatorType == "deep":
            self.I2 = lesField(
                "I2", "I2", data, indexTime, 
                dataOverride=self.getUpdraftIndicator(self.rtd.field)
            )
        else:
            warnings.warn("No matching indicator type '{}'. I2 not available".format(indicatorType))
    
    def getUpdraftIndicator(self, q):
        "Get updraft indicator function for a given radioactive tracer q."
        
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
        
        # Conditions for updraft, from Efstathiou et al. 2019
        condition1 = qCondition > 0.
        condition2 = self.w.field > 0.
        
        return condition1*condition2