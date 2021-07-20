'''
Object to store all Large Eddy Simulation data for a single timestep.
'''

import numpy as np

class lesField:
    def __init__(
        self, 
        key, 
        name, 
        data, 
        keys, 
        indexTime, 
        t = False, 
        x = False, 
        y = False, 
        z = False, 
        I2 = False, 
        w = False, 
        dataOverride = False
    ):
        print("Initialising {} ({}) at snapshot {}".format(name, key, indexTime))
        
        self.name = name
        self.key = key
        
        # Time
        self.t = t

        # Range of x, y and z values
        self.x = x
        self.y = y
        self.z = z
        
        # Axis for computing horizontal averages
        self.axisXY = (keys.xi, keys.yi)
        
        # Other input data
        I2 = I2
        w = w
        dataOverride = dataOverride
        
        # Data for all cells
        if type(dataOverride) == bool:
            self.field = data.variables[key][:][indexTime]*1
        else:
            self.field = dataOverride
        
        self.min = np.min(self.field)
        self.max = np.max(self.field)
        
        # Horizontally averaged field
        self.av = self.horizontalAverage()
        
        # Horizontally averaged fields for fluids 1 and 2
        if type(I2) != bool:
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
            
            if type(w) != bool:
                # Total flux across all fluids
                self.flux = self.fluxAll(np.ones_like(I2.field), self.av, w.field, w.av)
                
                # Resolved fluxes
                self.fluid1FluxResolved = (1-I2.av)*self.fluxResolved(self.fluid1, w.fluid1, w.av)
                self.fluid2FluxResolved =    I2.av *self.fluxResolved(self.fluid2, w.fluid2, w.av)
                
                # Subfilter fluxes
                self.fluid1FluxSubgrid = (1-I2.av)*self.fluxAll(
                    1-I2.field,
                    self.av, 
                    w.field, 
                    w.av
                ) - self.fluid1FluxResolved
                self.fluid2FluxSubgrid = I2.av*self.fluxAll(
                    I2.field, 
                    self.av, 
                    w.field, 
                    w.av
                ) - self.fluid2FluxResolved
                
                # Resolved fluxes
                # self.fluid1FluxResolved = (1-I2.av)*self.fluxResolvedAlternative(self.fluid1, w.fluid1)
                # self.fluid2FluxResolved =    I2.av *self.fluxResolvedAlternative(self.fluid2, w.fluid2)
                
                # Subfilter fluxes
                # self.fluid1FluxSubgrid = (1-I2.av)*self.fluxAllAlternative(1-I2.field, w.field) - self.fluid1FluxResolved
                # self.fluid2FluxSubgrid =    I2.av *self.fluxAllAlternative(  I2.field, w.field) - self.fluid2FluxResolved
    
    # Get the vertical profile
    def horizontalAverage(self):
        return np.mean(self.field, axis=self.axisXY)
    
    # Get the vertical profile for regions where the fluid is defined (I)
    def conditionalAverage(self, I):
        return np.sum(self.field*I, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
    
    # Get the variance profile where the fluid is defined (I)
    def conditionalVariance(self, I, mean):
        if len(self.field) == len(mean):
            return np.sum(I*(self.field-mean[:,None,None])**2, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
        else:
            return np.sum(I*(self.field-mean[None,None,:])**2, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
        
    # Get the minimum and maximum values for regions the fluid is defined
    # Could be optimised better.
    def conditionalMinMax(self, I):
        minMaxFieldAll = max(abs(self.max), abs(self.max))
        minimum = np.min(self.field + 1e3*minMaxFieldAll*(1-I), axis=self.axisXY)
        maximum = np.max(self.field - 1e3*minMaxFieldAll*(1-I), axis=self.axisXY)
        return minimum, maximum
    
    # Get the resolved fluxes
    def fluxResolved(self, fluidMean, wFluidMean, wMean):
        return (fluidMean - self.av)*(wFluidMean - wMean)
        
    # Get the total fluxes
    def fluxAll(self, I, fluidMean, w, wMean):
        if len(self.field) == len(fluidMean):
            return np.sum(
                I*(self.field-fluidMean[:,None,None])*(w - wMean[:,None,None]), 
                axis=self.axisXY
            ) / np.sum(I, axis=self.axisXY)
        else:
            return np.sum(
                I*(self.field-fluidMean[None,None,:])*(w - wMean[None,None,:]), 
                axis=self.axisXY
            ) / np.sum(I, axis=self.axisXY)
    
    # Alternative flux formulation which use mean values of each fluid rather than overall mean
    def fluxResolvedAlternative(self, fluidMean, wFluidMean):
        return fluidMean*wFluidMean
    
    def fluxAllAlternative(self, I, w):
        return np.sum(
            I*self.field*w, 
            axis=self.axisXY
        ) / np.sum(I, axis=self.axisXY)