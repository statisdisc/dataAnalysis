import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as mtick
import os
import sys

#Generate colorbar where different years are represented by slightly different colors.
def save_colorbar(my_cmap,cmap_min,cmap_max,label,filename,color_over="",color_under=""):
    a = np.array([[cmap_min,cmap_max]])

    plt.figure(figsize=(12, 1))
    
    plt.style.use("dark_background")
    plt.rcParams["font.family"] = "serif"
    img = plt.imshow(a, cmap=my_cmap)
    
    plt.gca().set_visible(False)
    cax = plt.axes([0.1, 0.5, 0.8, 0.3])
    
    if color_over == "" and color_under == "":
        cbar = plt.colorbar(orientation="horizontal", cax=cax)
    else:
        cbar = plt.colorbar(orientation="horizontal", cax=cax, extend="both")
    
    cbar.ax.set_xlabel(label,size=16)
    cbar.set_ticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
    xticks = ["2015", "2016", "2017", "2018", "2019", "2020"]
    cbar.ax.set_xticklabels(xticks, fontsize=16, weight='bold')
    
    if color_under != "":
        cbar.cmap.set_under(color_under)
    if color_over != "":
        cbar.cmap.set_over(color_over)
    
    plt.savefig(os.path.join(sys.path[0],"colorbar_horizontal_{}.png".format(filename)))
    plt.close()


#Define colors in colormap
cmap_colors = []
bins = 6000
orange = np.array([255, 145, 0, 255])/255.
red = np.array([255, 0, 0, 255])/255.
magenta = np.array([255, 0, 255, 255])/255.
blue = np.array([0, 0, 255, 255])/255.
cyan = np.array([0, 255, 255, 255])/255.
green = np.array([0, 255, 0, 255])/255.
colors = [orange, red, magenta, blue, cyan, green]
for i in xrange(bins):
    shade = 1. - (0.5/bins + 1.*i/float(bins))
    cmap_colors.append( (colors[i/1000][0], colors[i/1000][1], colors[i/1000][2]) )
cm = LinearSegmentedColormap.from_list("just_grey",cmap_colors,bins)

save_colorbar(cm,0.,6.,"","anualVar1")