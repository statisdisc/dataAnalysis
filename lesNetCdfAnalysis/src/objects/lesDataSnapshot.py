'''
Object to store all Large Eddy Simulation data for a single timestep.
'''

import warnings
import numpy as np
from .dataLabel import dataLabel
from .lesField  import lesField

class lesDataSnapshot:
    def __init__(self, data, indexTime, id="", indicatorType="shallow", indicatorFunction="plume"):
        
        # Keys for data set
        self.keys = dataLabel(id=id, indicatorType=indicatorType)
        
        # Time
        self.t = data.variables[self.keys.t][:][indexTime]*1
        
        # 3D structure
        self.shape = data.variables[self.keys.w][:][indexTime].shape

        # List of possible x, y and z values
        if self.keys.x in data.variables:
            self.x = data.variables[self.keys.x][:]*1
        else:
            self.x = np.linspace(-1e4, 1e4, self.shape[self.keys.xi])
        
        if self.keys.y in data.variables:
            self.y = data.variables[self.keys.y][:]*1
        else:
            self.y = np.linspace(-1e4, 1e4, self.shape[self.keys.yi])
        
        if self.keys.z in data.variables:
            self.z = data.variables[self.keys.z][:]*1
        else:
            self.z = np.linspace(0, 4.4e3, self.shape[self.keys.zi])
        
        # Grid spacings
        self.dx = np.abs(self.x - np.roll(self.x, 1))
        self.dy = np.abs(self.y - np.roll(self.y, 1))
        self.dz = np.abs(self.z - np.roll(self.z, 1))
        
        # Axis for computing horizontal averages
        self.axisXY = (self.keys.xi, self.keys.yi)
        
        # Definition for partitioning of fluid
        self.indicatorFunction = indicatorFunction
        
        '''
        Data for all cells
        '''
        # Diagnose indicator function which shows the locations of the updraft fluid (fluid 2)
        self.I2 = lesField(
            "I2", "I2", data, self.keys, indexTime, 
            dataOverride=self.getUpdraftIndicator(
                data.variables[self.keys.qr][indexTime],
                data.variables[self.keys.u][indexTime],
                data.variables[self.keys.v][indexTime],
                data.variables[self.keys.w][indexTime],
                data.variables[self.keys.theta][indexTime],
                data.variables[self.keys.qv][indexTime],
                data.variables[self.keys.ql][indexTime]
            ), 
            t=self.t, x=self.x, y=self.y, z=self.z
        )
        
        # Velocity component in the z-direction (vertical velocity)
        self.w = lesField(self.keys.w, "w", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2)
        # Velocity component in the x-direction
        self.u = lesField(self.keys.u, "u", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2, w=self.w)
        # Velocity component in the y-direction
        self.v = lesField(self.keys.v, "v", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2, w=self.w)
        # Potential temperature
        self.theta = lesField(self.keys.theta, "theta", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2, w=self.w)
        # Water vapour
        self.qv = lesField(self.keys.qv, "qv", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2, w=self.w)
        # Liquid water
        self.ql = lesField(self.keys.ql, "ql", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2, w=self.w)
        # Radioactive tracer for shallow convection (timescale 15 mins) or deep convection (timescale 35 mins)
        self.qr = lesField(self.keys.qr, "qr", data, self.keys, indexTime, t=self.t, x=self.x, y=self.y, z=self.z, I2=self.I2)
        
        
    
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
            qMean = np.mean(q, axis=self.axisXY)
            
            #Standard deviation of each horizontal slice
            qStdv = np.std(q, axis=self.axisXY)
            
            #Sum of all previous elements in array (including current)
            qStdvIntegral = np.cumsum(qStdv)
            
            qStdvMax = np.maximum(qStdv, 0.05*qStdvIntegral/self.z)
            
            if len(q) == len(qMean):
                qCondition = q - qMean[:,None,None] - qStdvMax[:,None,None]
            else:
                qCondition = q - qMean[None,None,:] - qStdvMax[None,None,:]
            
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
            
            thetaMean = np.mean(theta, axis=self.axisXY)
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