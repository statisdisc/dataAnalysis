import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as tr

def saveLegend(gca, name, ncols=4, folder=""):
    "Create a separate legend image according to the users specifications"
    
    # Large image size will be cropped later
    legend_fig = plt.figure(figsize=(26,26))
    # legend = plt.figlegend(*gca.get_legend_handles_labels(), loc='center', ncol=ncols, frameon=False)
    
    legend = plt.legend(handles=gca, loc='center', ncol=ncols, frameon=False)
    legend_fig.canvas.draw()
    
    # Set out legend dimensions
    bbox = legend.get_window_extent().transformed(legend_fig.dpi_scale_trans.inverted())
    ll, ur = bbox.get_points()
    x0, y0 = ll
    x1, y1 = ur
    w, h = x1 - x0, y1 - y0
    x1, y1 = x0 + w * 1.1, y0 + h * 1.1
    bbox = tr.Bbox(np.array(((x0, y0),(x1, y1))))
    
    if folder == "":
        folder = sys.path[0]
    legend_fig.savefig(os.path.join(folder, 'legend_%s.png' % (name)), bbox_inches=bbox)
    plt.close()