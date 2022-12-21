import cv2
import numpy as np
from particle import detcirc
# import archived.convolve as convolve
# import os

def circlefindparticle(filename, count):
    '''Utilizes convolvement (kernel, normalization) to facilitate edge detection
    input: image filename, current circles count
    returns: total circle count per image'''
    # Read image.
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #convolve
    kernel = np.array([[-1, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1],
                       [-1, -1, 35, -1, -1],
                       [-1, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1]])
    normfactor = -24 + kernel[2][2]
    rownum = 0
    norm_kernel = ([[-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, 35, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1]])
    for row in kernel:
        print(row)
        itemnum = 0
        for item in row:
            print(f"{rownum}, {itemnum}")
            norm_kernel[rownum][itemnum] = kernel[rownum][itemnum]/normfactor
            itemnum += 1
        rownum += 1
    norm_kernel = np.array(norm_kernel)
    print(norm_kernel)

    # output = convolve.convolve2D(gray, kernel, padding=0)
    #Normalized convolve
    output = cv2.filter2D(img, -1, norm_kernel)
    output = cv2.filter2D(output, -1, kernel)
    (thresh, binaryimg) = cv2.threshold(output, 127, 255, cv2.THRESH_BINARY)
    binaryimg_inverted = cv2.bitwise_not(binaryimg)

    cv2.imwrite('2DConvolved.jpg', output)
    # cv2.imshow(f"Detected Circle for {filename}", binaryimg_inverted)
    # cv2.waitKey(0)
    return detcirc(output, filename, count, 1)