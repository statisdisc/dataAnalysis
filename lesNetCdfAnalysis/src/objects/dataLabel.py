import warnings

class dataLabel:
    '''
    Create set of labels which describe the variable ID's used by various LES models
    '''
    def __init__(self, id="", indicatorType="shallow"):
        # Time coordinate
        self.t = "t"
        # Spacial coordinate, horizontal, x-axis
        self.x = "x"
        # Spacial coordinate, horizontal, y-axis
        self.y = "y"
        # Spacial coordinate, vertical, z-axis
        self.z = "z"
        # Which index represents to x-axis in the 3D data set?
        self.xi = 0
        # Which index represents to y-axis in the 3D data set?
        self.yi = 1
        # Which index represents to z-axis in the 3D data set?
        self.zi = 2
        # Horizontal velocity, x-axis
        self.u = "u"
        # Horizontal velocity, y-axis
        self.v = "v"
        # Vertical velocity, z-axis
        self.w = "w"
        # Potential temperature
        self.theta = "theta"
        # Specific humidity, water vapour
        self.qv = "qv"
        # Specific humidity, liquid water
        self.ql = "ql"
        # Radioactive tracer concentration
        self.qr = "qr"
        
        # Large Eddy Model variable names
        if id == "LEM":
            # Time coordinate
            self.t = "TIME"
            # Spacial coordinate, horizontal, x-axis
            self.x = "X"
            # Spacial coordinate, horizontal, y-axis
            self.y = "Y"
            # Spacial coordinate, vertical, z-axis
            self.z = "Z"
            # Which index represents to x-axis in the 3D data set?
            self.xi = 2
            # Which index represents to y-axis in the 3D data set?
            self.yi = 1
            # Which index represents to z-axis in the 3D data set?
            self.zi = 0
            # Horizontal velocity, x-axis
            self.u = "U"
            # Horizontal velocity, y-axis
            self.v = "V"
            # Vertical velocity, z-axis
            self.w = "W"
            # Potential temperature
            self.theta = "THETA"
            # Specific humidity, water vapour
            self.qv = "Q01"
            # Specific humidity, liquid water
            self.ql = "Q02"
            # Radioactive tracer concentration
            if indicatorType == "shallow":
                self.qr = "Q03"
            elif indicatorType == "deep":
                self.qr = "Q04"
            else:
                warnings.warn("No matching indicator type '{}'. Using default value.".format(indicatorType))
                self.qr = "Q03"
        # MONC variable names
        elif id == "MONC":
            # Time coordinate
            self.t = "time_series_600_600"
            # Spacial coordinate, horizontal, x-axis
            self.x = False
            # Spacial coordinate, horizontal, y-axis
            self.y = False
            # Spacial coordinate, vertical, z-axis
            self.z = "z"
            # Which index represents to x-axis in the 3D data set?
            self.xi = 0
            # Which index represents to y-axis in the 3D data set?
            self.yi = 1
            # Which index represents to z-axis in the 3D data set?
            self.zi = 2
            # Horizontal velocity, x-axis
            self.u = "u"
            # Horizontal velocity, y-axis
            self.v = "v"
            # Vertical velocity, z-axis
            self.w = "w"
            # Potential temperature
            self.theta = "th"
            # Specific humidity, water vapour
            self.qv = "q_vapour"
            # Specific humidity, liquid water
            self.ql = "q_cloud_liquid_mass"
            # Radioactive tracer concentration
            self.qr = "tracer_rad1"