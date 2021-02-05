import os
import csv
import numpy as np
from marketItemClass import marketItem

def readData(folderCaseData):
    print '''
    READING CSV DATA
    '''
    cases = []

    for folder in os.listdir(folderCaseData):
        print "Reading data: {}".format(folder)
        #Dictionary for each case
        name = folder.replace("_", " ")
        case = marketItem(name)
        
        folder = os.path.join(folderCaseData, folder)
        filename = os.path.join(folder, "data.csv")
        
        data_csv = open( filename, 'r+' )
        data_csv_reader = csv.reader(data_csv)
        
        dates = []
        timestamps = []
        prices = []
        quantities = []
        price_tally = 0
        quantity_tally = 0
        for row in data_csv_reader:
            date = row[0]
            timestamp = int(float(row[1]))
            price = float(row[2])
            quantity = int(float(row[3]))
            
            price_tally += price*quantity
            quantity_tally += quantity
            
            # if len(timestamps) == 0:
            if True:
                dates.append( date )
                timestamps.append( timestamp )
                prices.append( price_tally/quantity_tally )
                quantities.append( quantity_tally )
                
                price_tally = 0
                quantity_tally = 0
        
        case.dates = np.array(dates)
        case.timestamps = np.array(timestamps)
        case.prices = np.array(prices)
        case.quantities = np.array(quantities)
                
        cases.append(case)
    
    return cases