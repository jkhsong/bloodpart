# Microparticle detection in whole blood

## Background:
Bloodpart (Bloodparticle) was developed to automate the detection and analysis of exogenous particles in large (>1,000 image) whole blood datasets.

## Rationale:
Due to the high concentration of red blood cells (RBCs) in whole blood, detection and dimensional characterization of exogenous particles using impedance (e.g. Coulter counter) or optics (e.g. flow-cytometry) is highly inaccurate.  Thus, a means of discriminating exogenous particles from a confluence of RBCs is necessary to determine the quantity, size, and shape of such microparticles.  

## How Bloodpart works:
<ul>

1. Bloodpart detects and stores the properties of refractive microparticles within a field of blood using image filtering and circle-detection methods (i.e. Hough Circle Transform).

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

> Pick choice 1-3: