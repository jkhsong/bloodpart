import cv2
import numpy as np
# from matplotlib import pyplot as plt
import convolve
import os
print(os.environ.get('JDK_HOME'))
print(os.environ.get('JRE_HOME'))
# import imagej
# import maven
# import scyjava
# import jnius


# scyjava.config.add_option('-Xmx6g')
# ij = imagej.init(['net.imagej:imagej:2.1.0', 'net.imagej:imagej-legacy'])
# print(ij.getVersion)
# print("imported IJ")

def circlefindparticle(filename):
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

    output = convolve.convolve2D(gray, kernel, padding=0)
    #Normalized convolve
    output = cv2.filter2D(img, -1, norm_kernel)
    output = cv2.filter2D(output, -1, kernel)
    (thresh, binaryimg) = cv2.threshold(output, 127, 255, cv2.THRESH_BINARY)
    binaryimg_inverted = cv2.bitwise_not(binaryimg)

    cv2.imwrite('2DConvolved.jpg', output)
    cv2.imshow(f"Detected Circle for {filename}", binaryimg_inverted)
    cv2.waitKey(0)

    #Set circle counter
    global circles_count
    circles_count = 0