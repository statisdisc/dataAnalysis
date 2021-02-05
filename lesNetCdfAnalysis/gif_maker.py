import os,sys

folderMain = os.path.dirname(os.path.realpath(__file__))
variables = ["U", "V", "W", "THETA", "Q01", "Q02", "Q03", "Q04"]
# variables = ["U"]

indices_start = 1
indices_finish = 219
indices_step = 1
indices = range(indices_start, indices_finish, indices_step)
indices_array = []
gif_limit = 50

for i in xrange((indices_finish-indices_start)/gif_limit + 1):
    start = i*gif_limit
    finish = min((i+1)*gif_limit, len(indices))
    indices_array.append(indices[start:finish])
    
    

for variable in variables:
    print ""
    print variable
    folderVariable = os.path.join(folderMain, variable)
    
    temp_gifs = []
    for i in xrange(len(indices_array)):
        print "Making temporary gif {}".format(i+1)
        
        console = "magick convert -delay 8 "
        for j in indices_array[i]:
            filename = os.path.join(folderVariable, "histogram_{}_{}.png".format(variable, j))
            if os.path.isfile(filename):
                console += "{} ".format(filename)
                
        filenameGif = os.path.join(sys.path[0],"{}_{}.gif".format(variable, i+1))
        temp_gifs.append(filenameGif)
        console += "{} ".format(filenameGif)
        os.system(console)
        
        
    
    print "Stiching all gifs together"
    console_final = "magick convert "
    for filename in temp_gifs:
        console_final += "{} ".format(filename)
    filenameGif = os.path.join(sys.path[0],"{}.gif".format(variable))
    console_final += "{} ".format(filenameGif)
    os.system(console_final)
    
    # Delete temporary gifs
    for filename in temp_gifs:
        print "Deleting {}".format(filename)
        os.remove(filename)
