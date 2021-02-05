import time
import numpy as np

def processData(cases, casesReleased, timesReleased, startTime):
    print '''
    PROCESS THE DATA BY OMITTING THE NEWEST N CASES
    '''
    
    #Define when the item after the current item was released
    N = 1
    timesNextCase = {}
    for i in xrange(len(casesReleased)):
        case = casesReleased[i]
        if i >= len(casesReleased)-N:
            timeNextCase = time.time()
        else:
            timeNextCase = timesReleased[i+N]
        
        timesNextCase[case] = timeNextCase
        
    #Add data to arrays/dicts if all filter conditions are met
    entries = {}
    timestamps = [0]
    for case in cases:
        print "Processing data, next {} cases cut-off: {}".format(N, case.name)
        
        for i in xrange(len(case.timestamps)):
            
            timestamp = case.timestamps[i]
            
            if timestamp >= startTime:
                
                #Check cutoff for each case
                if timestamp > timesNextCase[case.name]:
                
                    #Check if timestamp is new or already exists from a previous item
                    closest_timestamp = timestamps[np.argmin( np.abs(np.array(timestamps)-timestamp) )]
                    if np.abs(timestamp - closest_timestamp) > 23.9*60*60:
                        closest_timestamp = timestamp
                        if timestamps[0] == 0:
                            timestamps[0] = timestamp
                        else:
                            timestamps.append(timestamp)
                        
                        dict = {}
                        dict["TotalSpent"] = 0
                        dict["TotalSold"] = 0
                        entries[timestamp] = dict
                        
                    index = closest_timestamp
                    entries[index]["TotalSpent"] += case.prices[i]*case.quantities[i]
                    entries[index]["TotalSold"] += case.quantities[i]
    
    return entries, timestamps