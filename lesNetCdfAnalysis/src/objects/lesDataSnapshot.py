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
        
        # Diagnose indicator function which shows the locations of the updraft fluid (fluid 2)
        if indicatorType == "shallow":
            self.I2 = lesField(
                "I2", "I2", data, indexTime, 
                dataOverride=self.getUpdraftIndicator(
                    data.variables["Q03"][indexTime],
                    data.variables["W"][indexTime]
                )
            )
        elif indicatorType == "deep":
            self.I2 = lesField(
                "I2", "I2", data, indexTime, 
                dataOverride=self.getUpdraftIndicator(
                    data.variables["Q04"][indexTime],
                    data.variables["W"][indexTime]
                )
            )
        else:
            self.I2 = []
            warnings.warn("No matching indicator type '{}'. I2 not available".format(indicatorType))
        
        
        # Velocity component in the x-direction
        self.u = lesField("U", "u", data, indexTime, I2=self.I2)
        # Velocity component in the y-direction
        self.v = lesField("V", "v", data, indexTime, I2=self.I2)
        # Velocity component in the z-direction (vertical velocity)
        self.w = lesField("W", "w", data, indexTime, I2=self.I2)
        # Potential temperature
        self.theta = lesField("THETA", "theta", data, indexTime, I2=self.I2)
        # Water vapour
        self.qv = lesField("Q01", "qv", data, indexTime, I2=self.I2)
        # Liquid water
        self.ql = lesField("Q02", "ql", data, indexTime, I2=self.I2)
        # Radioactive tracer for shallow convection (timescale 15 mins)
        self.rts = lesField("Q03", "rts", data, indexTime, I2=self.I2)
        # Radioactive tracer for deep convection (timescale 35 mins)
        self.rtd = lesField("Q04", "rtd", data, indexTime, I2=self.I2)
        
        
    
    def getUpdraftIndicator(self, q, w):
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
        condition2 = w > 0.
        
        return condition1*condition2