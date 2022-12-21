import cv2
import numpy as np
# from methods.algo import kmeans
# import archived.convolve as convolve
# import os

def circleadaptive(filename, circles_count):
    '''Utilizes adaptive gaussian thresholds to conduct edge detection
    input: image filename, current circles count
    returns: total circle count per image'''

    # Read image.
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    cv2.imwrite('X:\Dropbox\Image Processing\partblood\sample_output\original.png', img)

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
    cv2.imwrite('\sample_output\out.tif', img) ##sample output!
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
    cv2.imshow(f"Detected Circle for {filename}", img)
    cv2.waitKey(0)

    cv2.imwrite('X:\Dropbox\Image Processing\partblood\sample_output\measured.png', img)
    print("showing circles")

    print(f"Circles detected in this image: {circles_count}.")
    return count
    

# kmeans('..\\SMB Image Processing\\50-50\\trial 1\\1\\1.TIF', 0)