def getRaceLapTimes(f1db, raceId=841):
    "Return the lap times of each driver for a particular race."
    
    #Get drivers participating in this race
    cursor = f1db.cursor(dictionary=True)
    cursor.execute('''
        SELECT
            lapTimes.driverId,
            drivers.code
        FROM
            lapTimes
        LEFT JOIN
            drivers
        ON
            drivers.driverId=lapTimes.driverId
        WHERE
            lapTimes.raceId=%s
        AND
            lapTimes.lap=1
    ''' % (raceId) )

    output = cursor.fetchall()
    cursor.close()
    
    #Create column for each driver. 
    #Each row contains the laptimes for each driver for a specific lap.
    driverColumns = ""
    for row in output:
        if row != output[0]:
            driverColumns += ", "
        driverColumns += "max(CASE WHEN lapTimes.driverId=%s THEN lapTimes.milliseconds END) AS %s" % (row["driverId"], row["code"])
    
    cursor = f1db.cursor()
    cursor.execute('''
        SELECT
            lapTimes.lap,
            %s
        FROM
            lapTimes
        WHERE
            lapTimes.raceId=%s
        GROUP BY
            lapTimes.lap
        ORDER BY
            lapTimes.lap;
    ''' % (driverColumns, raceId) )

    output = cursor.fetchall()
    cursor.close()

    return output