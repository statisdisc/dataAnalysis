import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plotDummyPlot():
    "Dummy plot to correctly initialise dark colour scheme."
    
    dpi=100
    resolutionX = 100
    resolutionY = 100
    plt.subplots(figsize=(resolutionX/dpi, resolutionY/dpi), dpi=dpi)

    plt.style.use("dark_background")
    plt.rcParams["font.family"] = "serif"
    plt.close()