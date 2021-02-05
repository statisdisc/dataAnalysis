def eventInfo():
    print '''
    SETTING UP ADDITIONAL DATA/INFO
    '''
    
    #Steam sale events
    sales = {}
    sales["Winter Sale 2015"] = ["2015-12-22", "2016-01-04"]
    sales["Winter Sale 2016"] = ["2016-12-22", "2017-01-02"]
    sales["Winter Sale 2017"] = ["2017-12-21", "2018-01-04"]
    sales["Winter Sale 2018"] = ["2018-12-20", "2019-01-03"]
    sales["Winter Sale 2019"] = ["2019-12-19", "2020-01-02"]
    sales["Summer Sale 2015"] = ["2015-06-11", "2015-06-21"]
    sales["Summer Sale 2016"] = ["2016-06-23", "2016-07-04"]
    sales["Summer Sale 2017"] = ["2017-06-22", "2017-07-05"]
    sales["Summer Sale 2018"] = ["2018-06-21", "2018-07-05"]
    sales["Summer Sale 2019"] = ["2019-06-25", "2019-07-09"]
    
    #Major tournaments
    events = []
    events.append( ["Dreamhack Winter Jonkoping 2013", "DHW 2013", "28/11/2013", "30/11/2013"] )
    events.append( ["ESL One Katowice 2014", "Katowice 2014", "13/03/2014", "16/03/2014"] )
    events.append( ["ESL One Cologne 2014", "Cologne 2014", "14/08/2014", "17/08/2014"] )
    events.append( ["Dreamhack Winter Jonkoping 2014", "DHW 2014", "27/11/2014", "29/11/2014"] )
    events.append( ["ESL One Katwice 2015", "Katowice 2015", "12/03/2015", "15/03/2015"] )
    events.append( ["ESL One Cologne 2015", "Cologne 2015", "20/08/2015", "23/08/2015"] )
    events.append( ["Dreamhack Open Cluj-Napoca 2015", "Cluj 2015", "28/10/2015", "01/11/2015"] )
    events.append( ["MLG Columbus 2016", "Columbus 2016", "29/03/2016", "03/04/2016"] )
    events.append( ["ESL One Cologne 2016", "Cologne 2016", "05/07/2016", "10/07/2016"] )
    events.append( ["ELEAGUE Atlanta 2017", "Atlanta 2017", "22/01/2017", "29/01/2017"] )
    events.append( ["PGL Krakow 2017", "Krakow 2017", "16/07/2017", "23/07/2017"] )
    events.append( ["ELEAGUE Boston 2018", "Boston 2018", "12/01/2018", "28/01/2018"] )
    events.append( ["FACEIT London 2018", "London 2018", "05/09/2018", "23/09/2018"] )
    events.append( ["IEM Katowice 2019", "Katowice 2019", "13/02/2019", "03/03/2019"] )
    events.append( ["StarLadder Berlin 2019", "Berlin 2019", "20/08/2019", "08/09/2019"] )
    
    return sales, events