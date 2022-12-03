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