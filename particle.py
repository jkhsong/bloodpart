import cv2
import numpy as np
# from matplotlib import pyplot as plt
import convolve
import os
# import imagej
# import maven
# import scyjava
# import jnius


# scyjava.config.add_option('-Xmx6g')
# ij = imagej.init(['net.imagej:imagej:2.1.0', 'net.imagej:imagej-legacy'])
# print(ij.getVersion)
# print("imported IJ")


# Draw circles that are detected.
def detcirc(img, filename, count, method):
    ''' Draw circles that are detected
    input: image file, filename for reporting, detected_circles, method type
    returns: detected circles'''
    # cv2.imshow(f"Edge-enhanced image for {filename}", img)
    # cv2.waitKey(0)
    if method == 1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 10, param1=300, param2=1, minRadius=1, maxRadius=5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    circles_count = 0
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2] ##Set circle visualization parameters

            # Draw the circumference of the circle.
            img = cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            img = cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

            #add to circle counter
            circles_count += 1

        count += circles_count
    else:
        print("No circles detected.")
# Show Images here
    # cv2.imshow(f"Detected Circle for {filename}", img)
    # cv2.waitKey(0)
    cv2.imwrite('out.tif', img)
    print("showing circles")

    print(f"Circles detected in this image: {circles_count}.")
    return count


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



def circleadaptive(filename, circles_count):
    '''Utilizes adaptive gaussian thresholds to conduct edge detection
    input: image filename, current circles count
    returns: total circle count per image'''

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

    # th3 = cv2.threshold(gray_blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Apply Hough transform on the blurred image and count
    return detcirc(th3, filename, circles_count, 2)


    # #Outputs
    cv2.imshow(f"Detected Circle for {filename}", th3)
    cv2.waitKey(0)
    # cv2.imshow(f"Original Image for {filename}", img)
    # cv2.imwrite('out.tif', img)
    # cv2.waitKey(0)
    # print("showing circles")
    
    # print(f"Circles detected: {circles_count}.")