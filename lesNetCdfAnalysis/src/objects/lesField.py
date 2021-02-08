'''
Object to store all Large Eddy Simulation data for a single timestep.
'''

import numpy as np

class lesField:
    def __init__(self, key, name, data, indexTime, dataOverride=[]):
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