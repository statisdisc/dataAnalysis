'''
Object to store all Large Eddy Simulation data for all timesteps.
'''

import os
import sys
from .dataLabel import dataLabel
from .lesDataSnapshot import lesDataSnapshot

class lesData:
    def __init__(
        self, 
        data, 
        id = "LEM", 
        indicatorType = "shallow", 
        indicatorFunction = "plume",
        thetaMeanProfiles = None
    ):
        # Keys for data set
        self.keys = dataLabel(id=id, indicatorType=indicatorType)
        
        # Time snapshots available in data
        self.t = data.variables[self.keys.t][:]*1
        
        self.data = []
        # Get all time slices of data
        for n in range(len(self.t)):
            
            thetaMean = 0
            if thetaMeanProfiles is not None:
                if round(self.t[n]) in thetaMeanProfiles.keys():
                    thetaMean = thetaMeanProfiles[round(self.t[n])]
            
            self.data.append( 
                lesDataSnapshot(
                    data, 
                    n, 
                    id = id,
                    indicatorType = indicatorType, 
                    indicatorFunction = indicatorFunction,
                    thetaMean = thetaMean
                )
            )