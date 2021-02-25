def interpolateFromArray(x, xValue, y):
    "Get estimate of value of y at xValue"
    
    if len(x) != len(y):
        raise ValueError("x (length {}) and y (length {}) must be same length".format(len(x), len(y)))
    
    index = 0
    factor = 1.
    for i in xrange(1, len(x)):
        if x[i] > xValue:
            index = i
            factor = (x[i]-xValue)/float(x[i]-x[i-1])
            break
    
    return factor*y[index-1] + (1.-factor)*y[index]