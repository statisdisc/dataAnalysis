import numpy as np

def getBrightColors():
    "Returns array of bright colours useful for distinguishing between multiple lines in plots."

    white = np.array([255, 255, 255, 255])/255.
    yellow = np.array([255, 255, 0, 255])/255.
    orange = np.array([255, 145, 0, 255])/255.
    red = np.array([255, 0, 0, 255])/255.
    magenta = np.array([255, 0, 255, 255])/255.
    purple = np.array([155, 0, 155, 255])/255.
    blue = np.array([0, 0, 255, 255])/255.
    cyan = np.array([0, 255, 255, 255])/255.
    green = np.array([0, 255, 0, 255])/255.
    grey = np.array([155, 155, 155, 255])/255.
    colors = [white, yellow, orange, red, magenta, purple, blue, cyan, green, grey]

    return colors