#!/usr/bin/env python

# December 14, 2014
# Read and organize .csv data from Lucie's MeshStatistics module in Slicer.


import os
import sys
import glob
import pandas as pd
import numpy as np


# Base path to search for files
basedir = os.path.join('/Volumes/Ares/RPV9/Processing/CorticalThickness/Figure-CortexOverlay')
regions = ['ROI-L-Anterior-Cingulate', 'ROI-L-Posterior-Cingulate']

for roi in regions:
    x = []
    for i in sorted(glob.glob(os.path.join(basedir, roi, '???.csv'))):
        print i

        f = open(i)
        lines = f.readlines()
        f.close()

        try:
            header
        except NameError:
            header = lines[1].strip()

        for line in lines:
            if line.startswith('ROI'):
                if not line.strip().split(',')[1] == 'Min':
                    min = float(line.strip().split(',')[1])/1000
                    max = float(line.strip().split(',')[2])/1000
                    avg = float(line.strip().split(',')[3])/1000
                    std = float(line.strip().split(',')[4])/1000

        # get subject name from file
        subj = os.path.basename(i).split('.')[0]

        # get roi name from folder
        region = os.path.dirname(i).split('/')[-1]

        # append subject name and roi name
        x.append([subj, region, avg])

    x = np.array(x)

    # create data frame
    df = pd.DataFrame(x, columns=['Subject','ROI','Mean'])

    df.to_csv(os.path.join(basedir,region+'-thickness.csv'))


    

