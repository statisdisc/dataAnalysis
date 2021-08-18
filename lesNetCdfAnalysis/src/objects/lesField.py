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
        t  = None, 
        x  = None, 
        y  = None, 
        z  = None, 
        I2 = None, 
        w  = None, 
        dataOverride = None
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
        
        # Data for all cells
        if dataOverride is None:
            self.field = data.variables[key][:][indexTime]*1
        else:
            self.field = dataOverride
        
        self.calculateVerticalProfiles(I2=I2, w=w)
    
    def calculateVerticalProfiles(self, I2=None, w=None):
        '''
        Calculate all vertical (horizontally averaged) profiles
        '''
        self.calculateMeans(I2=I2)
        self.calculateMinMax(I2=I2)
        self.calculateVariances(I2=I2)
        self.calculateCovariances(I2=I2, w=w)
    
    def calculateMeans(self, I2=None):
        '''
        Calculate the horizontal mean profiles.
        :param I2: Indicator function for fluid 2 with same dimensions as self.field, np.ndarray.
        :return: None.
        '''
        # Horizontally averaged field
        self.av = self.horizontalAverage()
        
        # Horizontally averaged fields for fluids 1 and 2
        self.fluid1 = None
        self.fluid2 = None
        if I2 is not None:
            self.fluid1 = self.conditionalAverage(1-I2.field)
            self.fluid2 = self.conditionalAverage(  I2.field)
    
    def calculateMinMax(self, I2=None):
        # Global minima and maxima
        self.min = np.min(self.field)
        self.max = np.max(self.field)
        
        # Minima and maxima in each fluid
        self.fluid1Min, self.fluid1Max = None, None
        self.fluid2Min, self.fluid2Max = None, None
        if I2 is not None:
            self.fluid1Min, self.fluid1Max = self.conditionalMinMax(1-I2.field)
            self.fluid2Min, self.fluid2Max = self.conditionalMinMax(  I2.field)
    
    def calculateVariances(self, I2=None):
        '''
        Calculate the horizontally averaged variance profiles.
        :param I2: Indicator function for fluid 2 with same dimensions as self.field, np.ndarray.
        :return: None.
        '''
        # Total flux across all fluids summed over each height level
        self.var = self.varianceAll(np.ones_like(self.field), self.av)
        self.std = np.sqrt(self.var)
        
        self.fluid1VarAll      = None
        self.fluid2VarAll      = None
        self.fluid1VarResolved = None
        self.fluid2VarResolved = None
        self.fluid1VarSubgrid  = None
        self.fluid2VarSubgrid  = None
        self.fluid1StdAll      = None
        self.fluid2StdAll      = None
        self.fluid1StdResolved = None
        self.fluid2StdResolved = None
        self.fluid1StdSubgrid  = None
        self.fluid2StdSubgrid  = None
        
        if I2 is not None:
            # The volume-fraction-weighted total fluxes summed over each height level
            self.fluid1VarAll = self.varianceAll(1-I2.field, self.av)
            self.fluid2VarAll = self.varianceAll(  I2.field, self.av)
            
            # Volume-fraction-weighted fluxes from resolved variables only (vertical profiles)
            self.fluid1VarResolved = self.varianceResolved(self.fluid1)
            self.fluid2VarResolved = self.varianceResolved(self.fluid2)
            
            # Subfilter fluxes - The un-accounted-for flux not picked up by the resolved contribution
            self.fluid1VarSubgrid = np.maximum(0, self.fluid1VarAll - self.fluid1VarResolved)
            self.fluid2VarSubgrid = np.maximum(0, self.fluid2VarAll - self.fluid2VarResolved)
            
            # Standard deviations
            self.fluid1StdAll      = np.sqrt(self.fluid1VarAll)
            self.fluid2StdAll      = np.sqrt(self.fluid2VarAll)
            self.fluid1StdResolved = np.sqrt(self.fluid1VarResolved)
            self.fluid2StdResolved = np.sqrt(self.fluid2VarResolved)
            self.fluid1StdSubgrid  = np.sqrt(self.fluid1VarSubgrid)
            self.fluid2StdSubgrid  = np.sqrt(self.fluid2VarSubgrid)
    
    def calculateCovariances(self, I2=None, w=None):
        '''
        Calculate the horizontally averaged covariance profiles.
        Currently set-up for the vertical fluxes.
        :param I2: Indicator function for fluid 2 with same dimensions as self.field, np.ndarray.
        :param w: The vertical velocity field with same dimensions as self.field, np.ndarray.
        :return: None.
        '''
        self.flux = None
        self.fluid1FluxAll = None
        self.fluid2FluxAll = None
        self.fluid1FluxResolved = None
        self.fluid2FluxResolved = None
        self.fluid1FluxSubgrid = None
        self.fluid2FluxSubgrid = None
        
        if w is not None:
            # Total flux across all fluids summed over each height level
            self.flux = self.covarianceAll(np.ones_like(self.field), self.av, w.field, w.av)
            
            if I2 is not None: 
                # The volume-fraction-weighted total fluxes summed over each height level
                self.fluid1FluxAll = (1-I2.av)*self.covarianceAll(
                    1-I2.field,
                    self.av, 
                    w.field, 
                    w.av
                )
                self.fluid2FluxAll = I2.av*self.covarianceAll(
                    I2.field, 
                    self.av, 
                    w.field, 
                    w.av
                )
                
                # Volume-fraction-weighted fluxes from resolved variables only (vertical profiles)
                self.fluid1FluxResolved = (1-I2.av)*self.covarianceResolved(self.fluid1, w.fluid1, w.av)
                self.fluid2FluxResolved =    I2.av *self.covarianceResolved(self.fluid2, w.fluid2, w.av)
                
                # Subfilter fluxes - The un-accounted-for flux not picked up by the resolved contribution
                self.fluid1FluxSubgrid = self.fluid1FluxAll - self.fluid1FluxResolved
                self.fluid2FluxSubgrid = self.fluid2FluxAll - self.fluid2FluxResolved
    
    def horizontalAverage(self):
        '''
        Return the vertical profile (horizontal mean)
        '''
        return np.mean(self.field, axis=self.axisXY)
    
    def conditionalAverage(self, I):
        '''
        Get the vertical profile for regions where the fluid is defined (I)
        '''
        return np.sum(self.field*I, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
    
    def conditionalVariance(self, I, mean):
        '''
        Get the variance profile where the fluid is defined (I)
        '''
        if len(self.field) == len(mean):
            return np.sum(I*(self.field-mean[:,None,None])**2, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
        else:
            return np.sum(I*(self.field-mean[None,None,:])**2, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
    
    def conditionalMinMax(self, I):
        '''
        Get the minimum and maximum values for regions the fluid is defined
        *Could be optimised better*
        '''
        minMaxFieldAll = max(abs(self.max), abs(self.max))
        minimum = np.min(self.field + 1e3*minMaxFieldAll*(1-I), axis=self.axisXY)
        maximum = np.max(self.field - 1e3*minMaxFieldAll*(1-I), axis=self.axisXY)
        return minimum, maximum
    
    def varianceResolved(self, fluidMean):
        '''
        Get the variance from the vertical profiles only
        '''
        return (fluidMean - self.av)**2
        
    def varianceAll(self, I, mean):
        '''
        Get the variance summed over each height level
        '''
        if len(self.field) == len(mean):
            return np.sum(I*(self.field-mean[:,None,None])**2, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
        else:
            return np.sum(I*(self.field-mean[None,None,:])**2, axis=self.axisXY)/np.sum(I, axis=self.axisXY)
    
    def covarianceResolved(self, fluidMean, phiFluidMean, phiMean):
        '''
        Get the covariance with phi from the vertical profiles only
        '''
        return (fluidMean - self.av)*(phiFluidMean - phiMean)
        
    def covarianceAll(self, I, fluidMean, phi, phiMean):
        '''
        Get the covariance with phi summed over each height level
        '''
        if len(self.field) == len(fluidMean):
            return np.sum(
                I*(self.field-fluidMean[:,None,None])*(phi - phiMean[:,None,None]), 
                axis=self.axisXY
            ) / np.sum(I, axis=self.axisXY)
        else:
            return np.sum(
                I*(self.field-fluidMean[None,None,:])*(phi - phiMean[None,None,:]), 
                axis=self.axisXY
            ) / np.sum(I, axis=self.axisXY)
    
    def covarianceResolvedAlt(self, fluidMean, phiFluidMean):
        '''
        Alternative flux formulation which use mean values of each fluid rather than overall mean
        '''
        return fluidMean*phiFluidMean
    
    def covarianceAllAlt(self, I, phi):
        '''
        Alternative flux formulation which use mean values of each fluid rather than overall mean
        '''
        return np.sum(
            I*self.field*phi, 
            axis=self.axisXY
        ) / np.sum(I, axis=self.axisXY)
    
    def updateField(self, field):
        '''
        Update the field and re-calculate the diagnostics
        '''
        self.field = field
        self.calculateVerticalProfiles()