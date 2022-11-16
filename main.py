import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import convolve
import particle as pa
import houghcircle


#select directory
rootdir = '..\\SMB Image Processing\\50-50'
rootdirlist = os.listdir(rootdir)
print(rootdirlist)

#user inputs a directory choice
counterchoice = 1
for i in rootdirlist:
    print(f"Choice {counterchoice}: {i}")
    counterchoice += 1
choice = int(input(f"Pick choice 1-{counterchoice-1}: "))
print(rootdirlist[choice-1])
choicedir = rootdir+ '\\' + rootdirlist[choice-1]
print(choicedir)

#select sub directory
choicedirlist = os.listdir(choicedir)
print(choicedirlist)

#pick subdirectory choice
counterchoice = 1
for i in choicedirlist:
    print(f"Choice {counterchoice}: {i}")
    counterchoice += 1

choice = int(input(f"Pick subdirectory 1-{counterchoice-1}: "))
print(choicedirlist[choice-1])
subdir = choicedir+ '\\' + choicedirlist[choice-1]
print(subdir)

#pick image detection methodology:
methodchoice = int(input(f"Pick 1 for Normalized Convolution \nPick 2 for Gaussian Thresholding: "))

#read all files in dir
choice = rootdir

#####
##Set counters that will pass through to detection functions
global filecount
filecount = 0 ##File count
detcount = 0 ##Detection count

#Run Program

for filename in os.listdir(subdir):
    f = os.path.join(subdir, filename)
    print(f)
    # checking if it is a file
    if os.path.isfile(f):
        if methodchoice == 1:
            detcount += pa.circlefindparticle(f, detcount)
        else:
            detcount += pa.circleadaptive(f, detcount)
        filecount += 1
        print(f)
    else:
        print("Not a file.")

##User parameters
volume_per_square = 6.25 #nanoliters
volume_per_slide = volume_per_square * 2.262

dilution_correction = 75/25 * 130/100
averagecirc = detcount/filecount
circspernl = averagecirc/volume_per_slide
circsperml = circspernl * 1000000
corrected_circ_conc = circsperml * dilution_correction


print(f"Total number of circles counted was: {detcount}.")
print(f"Number of images counted was: {filecount}.")
print(f"Concentration of blood MBs is: {corrected_circ_conc} per mL.")