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

def kmeans(filename, count, initial_means = None):
    '''
    As implemented in grayscale, k-means clustering initially classifies 
    pixels into k random shades of gray, or clusters. Each k-means step 1) 
    obtains a mean shade of pixels in each of the k clusters, then 2) re-
    classifies each pixel into clusters (if necessary), which shifts the 
    corresponding cluster's mean. This is continued until no change in 
    clustering occurs (that is, pixels within clusters do not shift). 
    '''
    
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ##Apply CLAHE equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    ##

    cv2.imshow(f"Edge-enhanced image for {filename}", gray)
    cv2.waitKey(0)
    #select initial means
    k = 12 #splitting into two images
    X = np.array(gray)
    X = X.flatten()
    
    rdim, cdim = np.size(gray,0), np.size(gray,1)

    clusters = np.arange(0,rdim*cdim*3).reshape(rdim*cdim, 3)
    oldclusters = np.zeros((rdim*cdim, 3))

    try:
        if initial_means == None:
            initial_means = k_means_initial(X, k)
    finally:
        while np.array_equal(clusters, oldclusters) == False:
            oldclusters = clusters
            newmeans, centindex = k_means_step(X, k, initial_means)
            clusters = newmeans[centindex]
            initial_means = newmeans
        clusters = np.asarray(clusters.reshape(rdim, cdim))

        clusters[clusters > np.min(clusters)] = 255       

        img = cv2.normalize(src=clusters, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        return detcirc(img, filename, count, 2)
    
def k_means_initial(X, k):
    randomindices = np.random.choice(np.size(X,0), size=k, replace=False)
    means = X[randomindices]
    # means = []
    # for x in range(k): ##Evenly distributing means to start instead of randomizing
    #     means.append(int((255/k)*x))
    # means = np.array(means)
    return means



def k_means_step(X, k, means):
    centlist = [] #list of clusters by centroid
    centdist = [] #distance to each centroid
    newmeans = []

    for i in range(k):
        anotherlist = X-means[i]
        centlist.append([])
        centdist.append(np.einsum('i,i->i',anotherlist,anotherlist))
    centdist = np.stack(centdist, axis = 1)
    centindex = np.argmin(centdist, axis = 1)
    
    for i in range(k):
        centlist[i] = X[np.argwhere(centindex == i)]
        newmeans.append(np.mean(centlist[i], axis = 0, dtype=np.float64))
    newmeans = np.array(newmeans)
    
    # newmeans = newmeans.reshape(k,np.size(X,1))
    clusters = centindex.reshape(np.size(X,0),1)
    
    return (newmeans, clusters)

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
    

kmeans('..\\SMB Image Processing\\50-50\\trial 1\\1\\1.TIF', 0)