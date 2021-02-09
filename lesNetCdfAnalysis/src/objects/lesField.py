'''
Object to store all Large Eddy Simulation data for a single timestep.
'''

import numpy as np

class lesField:
    def __init__(self, key, name, data, indexTime, I2=[], dataOverride=[]):
        print "Initialising {} ({}) at snapshot {}".format(name, key, indexTime)
        
        self.key = key
        self.name = name
        
        # Time
        self.t = data.variables["TIME"][:][indexTime]*1

        # Range of x, y and z values
        self.x = data.variables["X"][:]*1
        self.y = data.variables["Y"][:]*1
        self.z = data.variables["Z"][:]*1
        
        # Data for all cells
        if dataOverride == []:
            self.field = data.variables[key][:][indexTime]*1
        else:
            self.field = dataOverride
        
        self.min = np.min(self.field)
        self.max = np.max(self.field)
        
        # Horizontally averaged field
        self.av = self.horizontalAverage()
        
        # Horizontally averaged fields for fluids 1 and 2
        if I2 != []:
            # Mean
            self.fluid1 = self.conditionalAverage(1-I2.field)
            self.fluid2 = self.conditionalAverage(  I2.field)
            
            # Variance
            self.fluid1Var = self.conditionalVariance(1-I2.field, self.fluid1)
            self.fluid2Var = self.conditionalVariance(  I2.field, self.fluid2)
            
            # Standard Deviation
            self.fluid1Std = np.sqrt(self.fluid1Var)
            self.fluid2Std = np.sqrt(self.fluid2Var)
            
            # Minima and Maxima
            self.fluid1Min, self.fluid1Max = self.conditionalMinMax(1-I2.field)
            self.fluid2Min, self.fluid2Max = self.conditionalMinMax(  I2.field)
    
    # Get the vertical profile
    def horizontalAverage(self):
        return np.mean(self.field, axis=(1,2))
    
    # Get the vertical profile for regions where the fluid is defined (I)
    def conditionalAverage(self, I):
        return np.sum(self.field*I, axis=(1,2))/np.sum(I, axis=(1,2))
    
    # Get the variance profile where the fluid is defined (I)
    def conditionalVariance(self, I, mean):
        mean = mean.reshape((len(mean),1))
        return np.sum(I*(self.field-mean[:,None])**2, axis=(1,2))/np.sum(I, axis=(1,2))
        
    # Get the minimum and maximum values for regions the fluid is defined
    # Could be optimised better.
    def conditionalMinMax(self, I):
        minMaxFieldAll = max(abs(self.max), abs(self.max))
        minimum = np.min(self.field + 1e3*minMaxFieldAll*(1-I), axis=(1,2))
        maximum = np.max(self.field - 1e3*minMaxFieldAll*(1-I), axis=(1,2))
        return minimum, maximum