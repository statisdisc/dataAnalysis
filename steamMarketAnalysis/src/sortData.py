import datetime
import numpy as np

def sortData(cases):
    print '''
    MAKE LIST OF DATES CASES WERE RELEASED
    '''
    
    #Sort items by date released
    casesReleased = []
    timesReleased = []
    for case in cases:
        casesReleased.append(case.name)
        timesReleased.append(case.timeReleased())
        
    casesReleased = np.array(casesReleased)
    timesReleased = np.array(timesReleased)

    minToMax = timesReleased.argsort()
    casesReleased = casesReleased[minToMax]
    timesReleased = timesReleased[minToMax]
    
    #Print ordering of data sets
    for i in xrange(len(timesReleased)):
        timeReleased = timesReleased[i]
        dateReleased = datetime.datetime.utcfromtimestamp(timeReleased).strftime('%H:%M:%S %d/%m/%Y')
        print "{} was released at:\n {}".format(casesReleased[i], dateReleased)
    
    return casesReleased, timesReleased