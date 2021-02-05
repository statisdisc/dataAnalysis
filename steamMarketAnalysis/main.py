import sys
import os
from src import readData
from src import sortData
from src import processData
from src import manipulateData
from src import eventInfo
from src import plotFuncs

'''
This code looks at how the prices of cases have changed over time,
with a particular focus on what happens to the prices of existing
cases when a new case is introduced.
'''

    

def main(startTime, folderCaseData):
    #Get data to analyse
    cases = readData.readData(folderCaseData)

    #Sort data by oldest items
    casesReleased, timesReleased = sortData.sortData(cases)

    #Remove noisy spikes from data
    entries, timestamps = processData.processData(cases, casesReleased, timesReleased, startTime)
        
    #Add all compatible data sets together
    timestamps, meanPrice = manipulateData.sumItemData(timestamps, entries)

    #Add smoothing filter to data
    meanPriceSmooth = manipulateData.smoothData(meanPrice, smoothingRange=7)

    #Get dates of significant events
    sales, events = eventInfo.eventInfo()
    
    
    #Generate polar plot of how prices vary over time
    filename = os.path.join(folderMain, "polarPriceTimeseries.png")
    plotFuncs.plotPriceTimeseries(startTime, timestamps, meanPrice, meanPriceSmooth, filename=filename)
    
    
    #Generate polar plot of how prices vary over annually
    filename = os.path.join(folderMain, "polarAnnualVariation.png")
    plotFuncs.plotAnnualVariation(startTime, timestamps, meanPrice, meanPriceSmooth, sales, events, filename=filename)


folderMain = os.path.dirname(os.path.realpath(__file__))
folderCaseData = os.path.join(folderMain, "data")
execfile(os.path.join(folderMain, "makeColorbar1.py"))
execfile(os.path.join(folderMain, "makeColorbar2.py"))


#Do not consider data from before the below timestamp
# startTime = time.time() - 5*365.25*24*60*60
startTime = 1591723618 - 5*365.25*24*60*60

main(startTime, folderCaseData)

