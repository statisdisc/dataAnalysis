'''
Object to store all Large Eddy Simulation data for all timesteps.
'''

import os
import sys
from .dataLabel import dataLabel
from .lesDataSnapshot import lesDataSnapshot

class lesDataMonc1D:
    def __init__(self, data, id="MONC1D"):
        # Keys for data set
        self.keys = dataLabel(id=id)
        
        # Time snapshots available in data
        self.t = data.variables[self.keys.t][:]*1
        
        self.data = {}
        # Get all time slices of data
        for i,t in enumerate(self.t):
            self.data[t] = {}
            
            for key in data.variables:
                self.data[t][key] = data.variables[key][:][i]