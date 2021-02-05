import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as mtick
import os
import sys

#Generate colormap which represents variations in item prices
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
    cbar.set_ticks([0.07,0.08,0.09,0.1,0.11])
    xticks = [float(x.get_text()) for x in cbar.ax.get_xticklabels()]
    cbar.ax.set_xticklabels(['${:.2f}'.format(x) for x in xticks], fontsize=16, weight='bold')
    
    if color_under != "":
        cbar.cmap.set_under(color_under)
    if color_over != "":
        cbar.cmap.set_over(color_over)
    
    plt.savefig(os.path.join(sys.path[0],"colorbar_horizontal_{}.png".format(filename)))
    plt.close()


#Define colors in colormap
cmap_colors = []
bins = 100
for i in xrange(bins):
    shade = 1. - (0.5/bins + 1.*i/float(bins))
    cmap_colors.append( (shade, 1.-shade, 0.) )

cm = LinearSegmentedColormap.from_list("just_grey",cmap_colors,bins)
save_colorbar(cm,0.07,0.11,"","anualVar2")