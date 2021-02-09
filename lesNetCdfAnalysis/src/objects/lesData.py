'''
Object to store all Large Eddy Simulation data for all timesteps.
'''

import os
import sys
from lesDataSnapshot import lesDataSnapshot

class lesData:
    def __init__(self, data, indicatorType="shallow", indicatorFunction="plume"):
        # Time snapshots available in data
        self.t = data.variables["TIME"][:]*1
        
        self.data = []
        # Get all time slices of data
        for n in xrange(len(self.t)):
            self.data.append( 
                lesDataSnapshot(
                    data, 
                    n, 
                    indicatorType=indicatorType, 
                    indicatorFunction=indicatorFunction
                )
            )