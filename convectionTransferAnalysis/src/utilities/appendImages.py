import os
import sys

def appendHor(file1,file2,file3):
    "Horizontally add file2 to the right of file1."
    
    file1 = os.path.join(sys.path[0],file1)
    file2 = os.path.join(sys.path[0],file2)
    file3 = os.path.join(sys.path[0],file3)
    os.system("magick convert +append {} {} {}".format(file1,file2,file3))

def appendVer(file1,file2,file3):
    "Vertically add file2 to the bottom of file1."
    
    file1 = os.path.join(sys.path[0],file1)
    file2 = os.path.join(sys.path[0],file2)
    file3 = os.path.join(sys.path[0],file3)
    os.system("magick convert -append {} {} {}".format(file1,file2,file3))