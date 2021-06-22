import os
import sys

def getFilesInFolder(folder, extension=""):
    '''
    Return a list of all files in a folder with a particular extension
    '''
    fileList = []
    
    for file in os.listdir(folder):
        if file.endswith(extension):
            fileList.append(os.path.join(folder, file))
    
    return fileList

def getFoldersInFolder(folder, extension=""):
    '''
    Return a list of all sub-folders in a folder
    '''
    folderList = []
    
    for file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file)):
            folderList.append(os.path.join(folder, file))
    
    return folderList