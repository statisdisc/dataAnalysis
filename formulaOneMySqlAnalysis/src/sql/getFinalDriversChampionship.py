def getFinalDriversChampionship(cursor, year=2009):
    "Return the final championship positions and points for a particular season."

    cursor.execute('''
        SELECT
            driverStandings.driverId,
            drivers.forename,
            drivers.surname,
            drivers.driverRef,
            drivers.code,
            driverStandings.position,
            driverStandings.points
        FROM
            driverStandings
        LEFT JOIN
            drivers
        ON
            driverStandings.driverId = drivers.driverId
        WHERE
            driverStandings.raceId = (
                SELECT 
                    races.raceId
                FROM 
                    races
                WHERE
                    races.year='%s'
                ORDER BY
                    races.date DESC
                LIMIT 1
            )
        ORDER BY
            driverStandings.position ASC
        
    ''' % (year) )

    output = cursor.fetchall()

    cursor.close()

    return output