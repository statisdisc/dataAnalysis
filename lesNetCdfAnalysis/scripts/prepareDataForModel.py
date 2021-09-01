'''
Get the vertical profiles output by lesVerticalProfiles.py and compile them into a single
file with all of the profiles for the selected snapshots in time.
'''
import os
import sys
import time
import numpy as np
from scipy.io import loadmat, savemat

# User-made modules
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from src.objects.folders import folders
from src.utilities.getLesData import getLesData
from src.utilities.getScmData import getScmData
from src.utilities.timeElapsed import timeElapsed
from src.plots.plotTransferredProperties import plotTransferredProperties
from src.plots.plotLEMvsMONC import plotVolumeFractionComparison
from src.plots.plotLEMvsMONC import plotVerticalProfileComparison
from src.plots.plotVerticalProfileComparison import plotVerticalFluxes

def loadProfiles(filename, folder=""):
    filename = os.path.join(folder, filename)
    if os.path.isfile(filename):
        return loadmat(filename)
    
    data = {}
    print(f"File does not exist: {filename}")
    return data

@timeElapsed
def prepareData(
        indicator = "plume", 
        id        = "MONC", 
        times     = [30000],
        cloudData = True
    ):
    # Fetch folders for code structure
    folder = folders(
        folderScripts = os.path.dirname(os.path.realpath(__file__))
    )
    
    variables = ["sigma", "q", "ql", "qv", "th", "thv", "b", "u", "v", "w"]
    
    dataAll = dict(times=[])
    # dataAll = dict(LES_times=times)
    
    # Create plots for each snapshot in time
    for i,t in enumerate(times):
        print("Processing t={}s (timestep {} of {})".format(t, i+1, len(times)))
        
        folderTimeMean      = os.path.join(folder.outputs, id,  "time_{}".format(times[i]),  "profilesMean",      indicator)
        folderTimeVariances = os.path.join(folder.outputs, id,  "time_{}".format(times[i]),  "profilesVariances", indicator)
        folderTimeFluxes    = os.path.join(folder.outputs, id,  "time_{}".format(times[i]),  "profilesFluxes",    indicator)
        
        if os.path.isdir(folderTimeMean):
            dataAll["times"].append(t)
            
            data = {}
            for variable in variables:
                dataMean      = loadProfiles(f"z_{variable}.mat",           folderTimeMean)
                dataVariances = loadProfiles(f"z_{variable}{variable}.mat", folderTimeVariances)
                dataFluxes    = loadProfiles(f"z_w{variable}.mat",          folderTimeFluxes)
                
                # Small correction to the key naming convention
                key1 = f"{variable}1"
                key2 = f"{variable}2"
                key1New = f"{variable}_1"
                key2New = f"{variable}_2"
                for key in list(dataMean.keys()):
                    if key1 in key:
                        dataMean[key.replace(key1, key1New)] = dataMean.pop(key)
                    if key2 in key:
                        dataMean[key.replace(key2, key2New)] = dataMean.pop(key)
                        # print(f"Replaced {key} with {key.replace(key2, key2New)}")
            
                data = {**data, **dataMean, **dataVariances, **dataFluxes}
            
            # Additional diagnostics
            data["e_res1"] = data["uu_res1"] + data["vv_res1"] + data["ww_res1"]
            data["e_res2"] = data["uu_res2"] + data["vv_res2"] + data["ww_res2"]
            data["e_sg1"]  = data["uu_sg1"]  + data["vv_sg1"]  + data["ww_sg1"]
            data["e_sg2"]  = data["uu_sg2"]  + data["vv_sg2"]  + data["ww_sg2"]
            data["e_1"]    = data["e_res1"]  + data["e_sg1"]
            data["e_2"]    = data["e_res2"]  + data["e_sg2"]
            data["e_res"]  = data["sigma_1"]*data["e_res1"] + data["sigma_2"]*data["e_res2"]
            data["e_sg"]   = data["sigma_1"]*data["e_sg1"]  + data["sigma_2"]*data["e_sg2"]
            data["e"]      = data["e_res"] + data["e_sg"]
            
            # Add data
            for profile in data.keys():
                if "__" not in profile:
                    
                    # Remove any ridiculous values from data set
                    data[profile][np.abs(data[profile]) > 1e10] = np.nan
                    
                    profile_name = profile
                    # profile_name = f"LES_{profile}"
                    if profile_name not in dataAll:
                        dataAll[profile_name] = data[profile][0].reshape((len(data[profile][0]), 1))
                        # if profile != "z":
                            # dataAll[profile_name] *= 0
                    elif profile != "z":
                    # elif profile != "LES_z":
                        dataAll[profile_name] = np.concatenate(
                            (
                                dataAll[profile_name], 
                                data[profile][0].reshape((len(data[profile][0]), 1))
                            ),
                            axis = -1
                        )
    
    if cloudData:
        print("Adding cloud timeseries as well")
        folderCloud = os.path.join(folder.outputs, id, "cloudContour")
        dataCloud = loadProfiles("cloud_fraction.mat", folder=folderCloud)
        
        for profile in dataCloud.keys():
            if "__" not in profile:
                profile_name = profile
                # profile_name = f"LES_{profile}"
                if profile_name not in dataAll:
                    dataAll[profile_name] = dataCloud[profile]
    
    
    print("Data preparation complete for variables: {}".format(list(dataAll.keys())))
    
    
    folderOutput = os.path.join(folder.outputs, id, indicator)
    if not os.path.isdir(folderOutput):
        os.makedirs(folderOutput)
    savemat(os.path.join(folderOutput, "profiles.mat"), dataAll)

if __name__ == "__main__":
    # prepareData(
        # id = "LEM",
        # times = range(3800, 51800, 3600)
    # )
    
    prepareData(
        id = "MONC",
        times = range(3600, 51600, 3600)
    )
    
    prepareData(
        id = "MONC",
        times = range(3600, 51600, 3600),
        indicator = "plumeEdge",
        cloudData = False
    )
