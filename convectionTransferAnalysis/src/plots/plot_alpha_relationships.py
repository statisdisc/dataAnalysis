def plot_KE_against_alpha(x,y,z,filename,title="",xvar="$x$",yvar="$y$"):
    plt.figure(figsize=(10,5))
    cs = plt.pcolor(x,y,z,cmap="bwr", vmin=-0.1, vmax=0.1)
    cs.cmap.set_under((0.,0.,0.5))
    cs.cmap.set_over((0.5,0.,0.))
    # cs.set_clim(0., maximum)
    # cb = plt.colorbar(cs)
    plt.xlabel(xvar,fontsize=20)
    plt.ylabel(yvar,fontsize=20)
    plt.title(title,fontsize=24)
    plt.xlim(x[0],x[-1])
    plt.ylim(y[0],y[-1])
    plt.tight_layout()
    # plt.gca().set_aspect("equal")
    plt.savefig( os.path.join( sys.path[0], "conservation_ke_{}.png".format(filename) ) )
    plt.close()
    
def plot_F_against_alpha(x,y,z,filename,title="",xvar="$x$",yvar="$y$"):
    plt.figure(figsize=(10,5))
    cs = plt.pcolor(x,y,z,cmap="PuOr_r", vmin=-0.1, vmax=0.1)
    cs.cmap.set_under((0.,0.,0.5))
    cs.cmap.set_over((0.5,0.,0.))
    # cs.set_clim(0., maximum)
    # cb = plt.colorbar(cs)
    plt.xlabel(xvar,fontsize=20)
    plt.ylabel(yvar,fontsize=20)
    plt.title(title,fontsize=24)
    plt.xlim(x[0],x[-1])
    plt.ylim(y[0],y[-1])
    plt.tight_layout()
    # plt.gca().set_aspect("equal")
    plt.savefig( os.path.join( sys.path[0], "conservation_f_{}.png".format(filename) ) )
    plt.close()
    
def plot_u_against_alpha(alpha,u,u_news,variable,values,unit,bins,start,end,l):
    plt.figure(figsize=(10,6)) 
    plt.plot(alpha,0.*alpha+u[0],"b:",linewidth=1.5)
    plt.plot(alpha,0.*alpha+u[1],"r:",linewidth=1.5)
    
    for n in xrange(bins):
        value = values[n]
        
        line_type = ""
        if n == bins/2:
            line_type = "--"
        if n == 0 or n == bins - 1 or n == bins/2:
            plt.plot(alpha, u_news[n][0], "b"+line_type, linewidth=1.5, alpha = 0.3 + 0.7*(n+1.)/bins,label="%s $= %s$ %s" % (variable,value,unit))
            plt.plot(alpha, u_news[n][1], "r"+line_type, linewidth=1.5, alpha = 0.3 + 0.7*(n+1.)/bins,label="%s $= %s$ %s" % (variable,value,unit))
        else:
            plt.plot(alpha, u_news[n][0], "b"+line_type, linewidth=1.5, alpha = 0.3 + 0.7*(n+1.)/bins)
            plt.plot(alpha, u_news[n][1], "r"+line_type, linewidth=1.5, alpha = 0.3 + 0.7*(n+1.)/bins)

    plt.xlabel("$\\alpha$",fontsize=18)
    plt.ylabel("Velocity (ms$^{-1}$)",fontsize=16)
    plt.title(fixed_values,fontsize=12)
    plt.suptitle("Velocity change for %s $\\in [%s,%s]$ %s with interval $%s$ %s" % (variable, start, end, unit, (end-start)/(bins-1.), unit),fontsize=16)
    plt.legend(loc="best",ncol=3)
    variable = variable.replace("$","").replace("_","").replace("\\","").replace(" ","").replace("{","").replace("}","")
    plt.savefig( os.path.join( sys.path[0], "u_vs_alpha_%s_l-%s" % (variable,l.replace("+","p")) ) )
    plt.close()