import os
import sys
import mysql.connector
import src.utilities.dummyPlot
import src.testCases.championshipSkewness as skew
import src.sql.getRaceLapTimes as laps

'''
Experimenting with the mysql.connector module
with data from all formula one races.
'''


def main(folders):
    #Run this in command line to import database file into MySQL: 
    #mysql -u root -p f1_database < ./data/f1db.sql
    #Database file downloaded from ergast.com
    
    # password = raw_input("Please enter your MySQL password: ")

    try:
        f1db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Genericpw1!",
            # password=password,
            database="f1_database"
        )
    except mysql.connector.errors.ProgrammingError:
        sys.exit("The password is not valid.")

    #Perform analysis and output plots
    src.utilities.dummyPlot.plotDummyPlot()
    skew.compareChampionshipSkewness(f1db, folders, yearStart=2000, yearEnd=2009)
    skew.compareChampionshipSkewness(f1db, folders, yearStart=2010, yearEnd=2019)

    laps.getRaceLapTimes(f1db)


if __name__ == "__main__":
    folders = {}
    folders["main"] = os.path.dirname(os.path.realpath(__file__))
    folders["src"] = os.path.join(folders["main"], "src")
    folders["data"] = os.path.join(folders["main"], "data")
    folders["output"] = os.path.join(folders["main"], "output")
    
    main(folders)