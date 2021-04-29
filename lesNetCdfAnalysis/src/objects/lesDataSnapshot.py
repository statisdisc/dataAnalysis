'''
Object to store all Large Eddy Simulation data for a single timestep.
'''

import warnings
import numpy as np
from .lesField import lesField

class lesDataSnapshot:
    def __init__(self, data, indexTime, indicatorType="shallow", indicatorFunction="plume"):
        # Time
        self.t = data.variables["TIME"][:][indexTime]*1

        # List of possible x, y and z values
        self.x = data.variables["X"][:]*1
        self.y = data.variables["Y"][:]*1
        self.z = data.variables["Z"][:]*1
        
        # List of possible x, y and z values in vector form
        self.xv = data.variables["X2"][:]*1
        self.yv = data.variables["Y2"][:]*1
        self.zv = data.variables["Z2"][:]*1
        
        # Grid spacings
        self.dx = np.abs(self.x - np.roll(self.x, 1))
        self.dy = np.abs(self.y - np.roll(self.y, 1))
        self.dz = np.abs(self.z - np.roll(self.z, 1))
        
        # Definition for partitioning of fluid
        self.indicatorFunction = indicatorFunction
        
        '''
        Data for all cells
        '''
        # Diagnose indicator function which shows the locations of the updraft fluid (fluid 2)
        if indicatorType == "shallow":
            self.I2 = lesField(
                "I2", "I2", data, indexTime, 
                dataOverride=self.getUpdraftIndicator(
                    data.variables["Q03"][indexTime],
                    data.variables["U"][indexTime],
                    data.variables["V"][indexTime],
                    data.variables["W"][indexTime],
                    data.variables["THETA"][indexTime],
                    data.variables["Q01"][indexTime],
                    data.variables["Q02"][indexTime]
                )
            )
        elif indicatorType == "deep":
            self.I2 = lesField(
                "I2", "I2", data, indexTime, 
                dataOverride=self.getUpdraftIndicator(
                    data.variables["Q04"][indexTime],
                    data.variables["U"][indexTime],
                    data.variables["V"][indexTime],
                    data.variables["W"][indexTime],
                    data.variables["THETA"][indexTime],
                    data.variables["Q01"][indexTime],
                    data.variables["Q02"][indexTime]
                )
            )
        else:
            self.I2 = []
            warnings.warn("No matching indicator type '{}'. I2 not available".format(indicatorType))
        
        # Velocity component in the z-direction (vertical velocity)
        self.w = lesField("W", "w", data, indexTime, I2=self.I2)
        # Velocity component in the x-direction
        self.u = lesField("U", "u", data, indexTime, I2=self.I2, w=self.w)
        # Velocity component in the y-direction
        self.v = lesField("V", "v", data, indexTime, I2=self.I2, w=self.w)
        # Potential temperature
        self.theta = lesField("THETA", "theta", data, indexTime, I2=self.I2, w=self.w)
        # Water vapour
        self.qv = lesField("Q01", "qv", data, indexTime, I2=self.I2, w=self.w)
        # Liquid water
        self.ql = lesField("Q02", "ql", data, indexTime, I2=self.I2, w=self.w)
        # Radioactive tracer for shallow convection (timescale 15 mins)
        self.rts = lesField("Q03", "rts", data, indexTime, I2=self.I2)
        # Radioactive tracer for deep convection (timescale 35 mins)
        self.rtd = lesField("Q04", "rtd", data, indexTime, I2=self.I2)
        
        
    
    def getUpdraftIndicator(self, q, u, v, w, theta, qv, ql, indicatorFunctionOverride=False):
        "Get updraft indicator function for a given radioactive tracer q."
        
        I = self.indicatorFunction
        if indicatorFunctionOverride != False:
            I = indicatorFunctionOverride
        
        if I == "none":
            # No partition of fluids
            return np.ones_like(w)
        elif I == "basic":
            # Partition fluids based on vertical velocity
            return w > 0.
        elif I == "plume":
            # Partition fluids based on clouds and thermal structures in the atmosphere
            
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
        elif I == "plumeEdge":
            I2 = self.getUpdraftIndicator(q, u, v, w, theta, qv, ql, indicatorFunctionOverride="plume")
            
            # Translate grid cells by 1 or -1 along each horizontal axis
            # If the indicator function changes, the new condition will be True
            # condition =             I2 * np.invert(np.roll(I2, 1, axis=(1)))
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(1)))
            condition =  I2 * np.invert(np.roll(I2, 1, axis=(2)))
            condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(2)))
            
            return condition
        elif I == "plumeEdgeEntrain":
            I2 = self.getUpdraftIndicator(q, u, v, w, theta, qv, ql, indicatorFunctionOverride="plume")
            
            # Translate grid cells by 1 or -1 along each horizontal axis
            # If the indicator function changes, then we are at the boundary of the plume
            # Finally, check the horizontal velocity divergence to approximately check whether 
            # air is entrering (entraining) at that location
            # condition =             I2 * np.invert(np.roll(I2, 1, axis=(1))) * ((u - np.roll(u, 1, axis=(1))) < 0)
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(1))) * ((u - np.roll(u,-1, axis=(1))) > 0)
            # condition = condition + I2 * np.invert(np.roll(I2, 1, axis=(2))) * ((v - np.roll(v, 1, axis=(2))) < 0)
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(2))) * ((v - np.roll(v,-1, axis=(2))) > 0)
            
            # condition =             I2 * np.invert(np.roll(I2, 1, axis=(1))) * ((v - np.roll(v, 1, axis=(1)) + u - np.roll(u, 1, axis=(1))) < 0)
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(1))) * ((v - np.roll(v,-1, axis=(1)) + u - np.roll(u,-1, axis=(1))) > 0)
            condition =  I2 * np.invert(np.roll(I2, 1, axis=(2))) * ((u - np.roll(u, 1, axis=(2)) + v - np.roll(v, 1, axis=(2))) < 0)
            condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(2))) * ((u - np.roll(u,-1, axis=(2)) + v - np.roll(v,-1, axis=(2))) > 0)
            
            return condition
        elif I == "plumeEdgeDetrain":
            I2 = self.getUpdraftIndicator(q, u, v, w, theta, qv, ql, indicatorFunctionOverride="plume")
            
            # Translate grid cells by 1 or -1 along each horizontal axis
            # If the indicator function changes, then we are at the boundary of the plume
            # Finally, check the horizontal velocity divergence to approximately check whether 
            # air is leaving (detraining) at that location
            # condition =             I2 * np.invert(np.roll(I2, 1, axis=(1))) * ((u - np.roll(u, 1, axis=(1))) > 0)
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(1))) * ((u - np.roll(u,-1, axis=(1))) < 0)
            # condition = condition + I2 * np.invert(np.roll(I2, 1, axis=(2))) * ((v - np.roll(v, 1, axis=(2))) > 0)
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(2))) * ((v - np.roll(v,-1, axis=(2))) < 0)
            
            # condition =             I2 * np.invert(np.roll(I2, 1, axis=(1))) * ((v - np.roll(v, 1, axis=(1)) + u - np.roll(u, 1, axis=(1))) > 0)
            # condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(1))) * ((v - np.roll(v,-1, axis=(1)) + u - np.roll(u,-1, axis=(1))) < 0)
            condition =  I2 * np.invert(np.roll(I2, 1, axis=(2))) * ((u - np.roll(u, 1, axis=(2)) + v - np.roll(v, 1, axis=(2))) > 0)
            condition = condition + I2 * np.invert(np.roll(I2,-1, axis=(2))) * ((u - np.roll(u,-1, axis=(2)) + v - np.roll(v,-1, axis=(2))) < 0)
            
            return condition
        elif I == "dbdz":
            # Virtual potential temperature
            # theta = theta*(1. + 0.61*qv/(1.-qv))
            # theta = theta*(1. + 0.61*qv/(1.-qv) - ql/(1.-ql))
            
            thetaMean = np.mean(theta, axis=(1,2))
            b = (theta - thetaMean[:,None,None])/thetaMean[:,None,None]
            
            # Air must be unstable db/dz < 0
            condition1 = (b - np.roll(b, 1, axis=(0)))/self.dz[:,None,None] < 0
            
            # Second order differential, check for positive buoyancy anomaly
            condition2Part1 = (np.roll(b, 1, axis=(2)) + np.roll(b,-1, axis=(2)) - 2*b)/self.dx[None,None,:]
            condition2Part2 = (np.roll(b, 1, axis=(1)) + np.roll(b,-1, axis=(1)) - 2*b)/self.dy[None,:,None]
            condition2Part3 = (np.roll(b, 1, axis=(0)) + np.roll(b,-1, axis=(0)) - 2*b)/self.dz[:,None,None]
            condition2 = condition2Part1 + condition2Part2 + condition2Part3 < 0
            
            # Vertical velocity divergence
            condition3 = (w - np.roll(w, 1, axis=(0)))/self.dz[:,None,None] > 0
            
            return condition1*condition2*condition3
        else:
            return np.ones_like(w)