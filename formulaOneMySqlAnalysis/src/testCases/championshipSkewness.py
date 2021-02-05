import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy.optimize import curve_fit
import src.sql.getFinalDriversChampionship as drv
import src.utilities.brightColors as col

class compareChampionshipSkewness:
    def __init__(self, f1db, folders, yearStart=2000, yearEnd=2010):
        self.f1db = f1db
        self.folders = folders

        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.years = range(yearStart, yearEnd+1)
        self.yearsTotal = len(self.years)
        self.data = {}

        for year in self.years:
            self.getChampionship(year)
        
        self.plotChamptionshipSkewness()

    def getChampionship(self, year=2010):
        
        cursor = self.f1db.cursor(dictionary=True)
        output = drv.getFinalDriversChampionship(cursor, year=year)
        cursor.close()

        totalPoints = 0.
        for row in output:
            totalPoints += row["points"]

        for row in output:
            row["pointsFraction"] = row["points"]/totalPoints
        
        self.data[year] = output

    def plotChamptionshipSkewness(self):
        
        dpi=200
        resolutionX = 1000
        resolutionY = 1000
        fig, ax = plt.subplots(figsize=(resolutionX/dpi, resolutionY/dpi), dpi=dpi)

        plt.style.use("dark_background")
        plt.rcParams["font.family"] = "serif"

        colors = col.getBrightColors()

        for i in xrange(self.yearsTotal):
            year = self.years[i]
            x = np.array([value["position"] for value in self.data[year]])
            y = np.array([value["pointsFraction"] for value in self.data[year]])

            #Calculate championship skewness parameter
            fitParameters,covariances = curve_fit(lambda t,b: y[0]*np.exp(-(t-1)*b), x, y)

            color = colors[i%len(colors)]
            label="%s: %0.2f" % (year, fitParameters[0])
            ax.plot(x, 100*y, color=color, label=label)

        # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        #Add percentage sign to y axis
        fmt = '{x:,.0f}%'
        tick = mtick.StrMethodFormatter(fmt)
        ax.yaxis.set_major_formatter(tick)

        ax.set_xlim(left=1)
        ax.set_ylim(bottom=0)

        plt.xlabel("Championship position")
        plt.ylabel("Share of championship points")
        plt.legend(loc="best")

        filename = os.path.join(self.folders["output"], "championshipSkewness_%s-%s.png" % (self.years[0], self.years[-1]))
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        plt.close()        
        