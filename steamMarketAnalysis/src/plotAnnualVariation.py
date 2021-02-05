def plotAnnualVariation(startTime, timestamps, meanPrice, meanPriceSmooth, sales, events, filename="polarPlot.png"):
    print '''
    GENERATING POLAR PLOT OF ANNUAL VARIATIONS OF PRICES
    '''
    
    #Pre-processing
    timestamp_start = 1420070400
    year = 365.25*24*60*60
    nYears = int((time.time() - startTime)/year) + 1
    theta = 2*np.pi*(timestamps - timestamp_start)/year + np.pi/2.
    r = meanPriceSmooth.copy()
    
    meanAnnualPrice = np.zeros(366)
    meanAnnualPriceN = np.zeros(366)
    index_array = 365*((timestamps - timestamp_start)%year)/year
    
    #Sum data sets for each day of the year
    for i in xrange(nYears):
        iStart = np.argmin( np.abs(timestamps - (timestamp_start+i*year)) )
        iEnd = np.argmin( np.abs(timestamps - (timestamp_start+(i+1)*year)) )
        
        if i == 0:
            iEndMean = len(meanAnnualPrice)
            iStartMean = iEndMean - min( 365, iEnd-iStart )
        else:
            iStartMean = 0
            iEndMean = min( 365, iEnd-iStart )
        
        meanAnnualPrice[iStartMean:iEndMean] = meanAnnualPrice[iStartMean:iEndMean] + meanPrice[iStart:min(iEnd, iStart+365)]
        meanAnnualPriceN[iStartMean:iEndMean] += 1
        
    meanAnnualPriceN = np.maximum(meanAnnualPriceN, np.ones(len(meanAnnualPriceN)))
    meanAnnualPrice = meanAnnualPrice/meanAnnualPriceN
    meanAnnualPrice[-1] = meanAnnualPrice[0]
    
    #Define data sets to be plotted
    rData = meanAnnualPrice
    rMean = smoothData(meanAnnualPrice, smoothingRange=7, periodic=True)
    rMean[-1] = rMean[0]
    theta = np.linspace(0., 2*np.pi, len(rData)) + np.pi/2
    minimum = np.min(rMean)
    maximum = np.max(rMean)
    
    
    plt.figure()
    ax = plt.subplot(111, projection='polar')
    plt.style.use("dark_background")
    plt.rcParams["font.family"] = "serif"

    #Add background shading indicating extra data
    for sale in sales:
        timestamp_sale_start = time.mktime(datetime.datetime.strptime(sales[sale][0], "%Y-%m-%d").timetuple())
        timestamp_sale_end = time.mktime(datetime.datetime.strptime(sales[sale][1], "%Y-%m-%d").timetuple())
        theta_sale = 2*np.pi*(timestamp_sale_start - timestamp_start)/year + np.pi/2.
        bars = plt.bar([theta_sale], [1.], width=[2*np.pi*(timestamp_sale_end-timestamp_sale_start)/year], bottom=0.0)
        for r,bar in zip(rMean, bars):
            bar.set_color((0.,0.,0.,0.))
            bar.set_linewidth(0.)
            bar.set_facecolor("w")
            bar.set_alpha(0.3)

    new_color_map = {}
    new_color_map["red"] = ((0., 1., 1.), (1., 0., 0.))
    new_color_map["green"] = ((0., 0., 0.), (1., 1., 1.))
    new_color_map["blue"] = ((0., 0., 0.), (1., 0., 0.))
    new_cmap = mcolors.LinearSegmentedColormap("new_cmap_redgreen", new_color_map)

    width = (theta[1]-theta[0])*np.ones(len(theta))
    bars = plt.bar(theta, rMean, width=width, bottom=0.0)
    for r,bar in zip(rMean, bars):
        color = (r-minimum)/(maximum-minimum)
        color = new_cmap(color)
        bar.set_color(color)
        bar.set_facecolor(color)
    
    #Annual variation of prices
    ax.plot(theta, rMean, color="w", linewidth=4.)

        
        
    ax.grid(True)
    ax.set_xticks(np.arange(0., 2*np.pi, 2*np.pi/12.))
    ax.set_xticklabels(["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"])

    ax.set_rlabel_position(26.)
    ax.set_rmin(0.05)
    ax.set_rmax(0.12)
    ax.set_rticks([0.05, 0.1])  # less radial ticks

    #Add dollar sign to x axis
    fmt = '${x:,.2f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

    pe = [PathEffects.withStroke(linewidth=3, foreground="w")]
    pe = [PathEffects.withStroke(linewidth=3, foreground="k")]
    for l in ax.get_yticklabels():
        l.set_path_effects(pe)
        
        
    #Annotations
    text = ax.text(0.725*2.*np.pi, 0.112, 'Summer sales', color='white', ha='center', va='center', size=10)
    text.set_path_effects([PathEffects.Stroke(linewidth=3, foreground='k'), PathEffects.Normal()])
    text = ax.text(0.225*2.*np.pi, 0.112, 'Winter sales', color='white', ha='center', va='center', size=10)
    text.set_path_effects([PathEffects.Stroke(linewidth=3, foreground='k'), PathEffects.Normal()])

    plt.savefig( os.path.join(sys.path[0], "polarPlotMean.png"), bbox_inches="tight", dpi=200 )
    plt.close()