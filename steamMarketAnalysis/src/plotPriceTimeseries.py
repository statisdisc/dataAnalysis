def plotPriceTimeseries(startTime, timestamps, meanPrice, meanPriceSmooth, filename="polarPlot.png"):
    print '''
    GENERATING POLAR PLOT OF PRICE VARIATIONS WITH TIME
    '''
    
    #Pre-processing
    timestamp_start = 1420070400
    year = 365.25*24*60*60
    nYears = int((time.time() - startTime)/year) + 1
    theta = 2*np.pi*(timestamps - timestamp_start)/year + np.pi/2.
    r = meanPriceSmooth.copy()
    
    
    plt.figure()
    ax = plt.subplot(111, projection='polar')
    plt.style.use("dark_background")
    plt.rcParams["font.family"] = "serif"
    
    #Define custom colormap
    orange = np.array([255, 145, 0, 255])/255.
    red = np.array([255, 0, 0, 255])/255.
    magenta = np.array([255, 0, 255, 255])/255.
    blue = np.array([0, 0, 255, 255])/255.
    cyan = np.array([0, 255, 255, 255])/255.
    green = np.array([0, 255, 0, 255])/255.
    colors = [orange, red, magenta, blue, cyan, green]
    nColors = len(colors)
    
    #Plot each year as a different color
    for i in xrange(nYears):
        iStart = np.argmin( np.abs(timestamps - (timestamp_start+i*year)) )
        iEnd = np.argmin( np.abs(timestamps - (timestamp_start+(i+1)*year)) )
        
        ax.plot(theta[max(0,iStart-1):iEnd], meanPrice[max(0,iStart-1):iEnd], color=colors[i%nColors], linewidth=1., alpha=0.5)

    for i in xrange(nYears):
        iStart = np.argmin( np.abs(timestamps - (timestamp_start+i*year)) )
        iEnd = np.argmin( np.abs(timestamps - (timestamp_start+(i+1)*year)) )
        
        ax.plot(theta[max(0,iStart-1):iEnd], r[max(0,iStart-1):iEnd], color=colors[i%nColors], linewidth=3.5)


    # ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)
    ax.set_xticks(np.arange(0., 2*np.pi, 2*np.pi/12.))
    ax.set_xticklabels(["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"])

    ax.set_rlabel_position(90)
    ax.set_rmax(0.175)
    ax.set_rticks([0.05, 0.1, 0.15])  # less radial ticks

    #Add dollar sign to x axis
    fmt = '${x:,.2f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

    pe = [PathEffects.withStroke(linewidth=3, foreground="w")]
    pe = [PathEffects.withStroke(linewidth=3, foreground="k")]
    for l in ax.get_yticklabels():
        l.set_path_effects(pe)
        
        
    plt.savefig(filename, bbox_inches="tight", dpi=200 )
    plt.close()