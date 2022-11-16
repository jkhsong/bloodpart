# Microparticle detection in whole blood (BLOOD PARTICLE)

## Background:
Bloodpart (Blood Particle) was developed to automate the detection and analysis of exogenous particles in large (>1,000 image) whole blood datasets.

## Rationale:
Due to the high concentration of red blood cells (RBCs) in whole blood, detection and dimensional characterization of exogenous particles using impedance (e.g. Coulter counter) or optics (e.g. flow-cytometry) is highly inaccurate.  Thus, a means of discriminating exogenous particles from a confluence of RBCs is necessary to determine the quantity, size, and shape of such microparticles.  


## Bloodpart is a study in de-noising and edge-detection with ML
Brightfield microscopy, particularly of blood samples, can yield suboptimal images with a wide variety of image anomalies and noise types (gradients, blotchiness, uneven contrast).  

Let's take a look at a few examples below.  
  
Gaussian Thresholding vs. K-Means Clustering:
    
![example](/SMBImageProcessing/GTvsKM.png?raw=true "GTvsKM")


## Visualized particle detection:  
 ![example2](/SMBImageProcessing/conventionalcomparison.png "conventionalcomparison")

## Example outputs: 

> Total number of particles counted was: 57845088.  
> Number of images counted was: 19.  
> Microscope objective used: 20x.  
> Dilution correction was: 3.9.  
> Volume of blood per microscope slide was: 14.1375.  
> Average particle size was: 3.25 microns.  
> **Concentration of blood particles is: 839856087114.3375 per mL.  **



## How Bloodpart works:

Bloodpart extracts features by: 
1. (Channelizing) Grayscale conversion.
2. (ML Classification)  Classification of pixels by shade-of-gray.
3. (Convolve) Applying a normalization kernel to each image,
4. (Thresholding) Applying  
5. Convolvement and circle-detection methods (i.e. Hough Transform).

2. To determine the dose of particles in blood, Bloodpart relates particle counts to a calculated fluid volume represented by each image (as derived from image size, and user parameters under <code> main.py ##User Parameters##) </code>.
</ul>


## Image dataset requirements:
- An **image dataset** folder (i.e. '\\images') should contain: 
    - subfolders for **each experiment** (i.e. '\\trial 1') which should contain: 
        - subfolders for **each timepoint** within the experiment (i.e. '\\1min') which should contain: 
            - **images** taken from each timepoint.


## How to use:
### The program reads your data folder and asks you to select a specific image dataset:

> ['trial 1', 'trial 2', 'trial 3']  
> Choice 1: trial 1  
> Choice 2: trial 2  
> Choice 3: trial 3  
>  
> **Pick choice 1-3:  <enter an input> **

### Then a sub-experiment (in this case, timepoint in minutes)

> Choice 1: 1  
> Choice 2: 10  
> Choice 3: 2  
> Choice 4: 3  
> Choice 5: 4  
> Choice 6: 5  
>  
> **Pick subdirectory 1-6:  <enter an input> **

### Next, pick from the list of image filtering algorithms:

> ..\SMB Image Processing\50-50\trial 1\1  
> Pick 1 for Normalized Convolution.  
> Pick 2 for Gaussian Thresholding.   
> Pick 3 for K-Means clustering.   
> Pick 4 for Gaussian Mixture Model.    
