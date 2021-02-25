from scipy.io import loadmat

def getScmData(matlabFile):
    "Get SCM data from a MatLab file"
    
    matDict = loadmat(matlabFile)
    
    return matDict