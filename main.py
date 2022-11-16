import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import convolve
import particle
import houghcircle


#select directory
rootdir = '..\\SMB Image Processing\\50-50'
rootdirlist = os.listdir(rootdir)
print(rootdirlist)

#pick directory choice
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


#read all files in dir
choice = rootdir

# iterate over files in
# that directory

global filecount
filecount = 0

global totalcircles
totalcircles = 0

def circlefindhough(filename):

    # Read image.
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.medianBlur(gray, 7)
    # gray_blurred = gray

    #Threshold
    th3 = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 12)

    th3 = cv2.threshold(gray_blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 0.5, 15,
                                        param1=300, param2=1, minRadius=2, maxRadius=5)

    global circles_count
    circles_count = 0


    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

            #add to circle counter
            circles_count += 1

        global totalcircles
        totalcircles += circles_count
    else:
        print("No circles detected.")

# Show Images here
    cv2.imshow(f"Detected Circle for {filename}", th3)
    cv2.waitKey(0)
    cv2.imshow(f"Original Image for {filename}", img)
    cv2.imwrite('out.tif', img)
    cv2.waitKey(0)
    print("showing circles")

    print(f"Circles detected: {circles_count}.")


    #Outputs
    cv2.imshow(f"Detected Circle for {filename}", th3)
    cv2.waitKey(0)
    cv2.imshow(f"Original Image for {filename}", img)
    cv2.imwrite('out.tif', img)
    cv2.waitKey(0)
    print("showing circles")
    
    print(f"Circles detected: {circles_count}.")

#Run Program
for filename in os.listdir(subdir):
    f = os.path.join(subdir, filename)
    print(f)
    # checking if it is a file
    if os.path.isfile(f):
        particle.circlefindparticle(f)
        filecount += 1
        print(f)
    else:
        print("Not a file.")

##User parameters
volume_per_square = 6.25 #nanoliters
volume_per_slide = volume_per_square * 2.262

dilution_correction = 75/25 * 130/100
averagecirc = totalcircles/filecount
circspernl = averagecirc/volume_per_slide
circsperml = circspernl * 1000000
corrected_circ_conc = circsperml * dilution_correction


print(f"Total number of circles counted was: {totalcircles}.")
print(f"Number of images counted was: {filecount}.")
print(f"Concentration of blood MBs is: {corrected_circ_conc} per mL.")