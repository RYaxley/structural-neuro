#!/usr/bin/env python
# encoding: utf-8

"""
untitled.py

Created by Richard Yaxley on 2014-02-05.
"""

import sys
import os
import glob
import re
import subprocess


datapath = os.path.join(os.path.expanduser('~'), 'NADIA', 'RPV9', 'Processing', 'CorticalThickness')
# subjects = '0??'
version = '6-Warping'


# Extract labels from segmentation
for file in glob.glob(os.path.join(datapath, '*segmentation*')):
    
    fid = os.path.basename(file)
    subjid = fid.split('_')[0]

    for label, region in (('1', 'brain'),
                          ('2', 'nc_L'),
                          ('3', 'nc_R')):
            
        cmd = 'ImageMath %s -extractLabel %s -outfile %s' % (file, label, os.path.join(os.path.dirname(file),subjid+'_'+region+'.nrrd'))
        print cmd
        # subprocess.call(cmd, shell=True)

        

# Smooth images
for file in glob.glob(os.path.join(datapath, subjects, version, '???_*.nrrd')):

    if re.search('_brain.nrrd|\d_nc_[LR].nrrd',file):

        ofid = os.path.join(os.path.dirname(file),os.path.basename(file).split('.')[0]+'_smooth.nrrd')

        cmd = 'SegPostProcess %s -Gauss -var 0.1,0.1,0.1 -o %s' % (file, ofid )
        print cmd
        # subprocess.call(cmd, shell=True)



# Subtract neocortex region from brain region so that each labelmap can be joined
for file in glob.glob(os.path.join(datapath,subjects,version,'???_brain_smooth.nrrd')):

    for region in ('nc_L','nc_R'):
        mask = re.sub('brain', region, file)

        cmd = 'ImageMath %s -sub %s -outfile %s' % (file, mask, file)
        print cmd
        subprocess.call(cmd, shell=True)

    cmd = 'ImageMath %s -threshMask 1,1 -outfile %s' % (file, file)
    print cmd
    # subprocess.call(cmd, shell=True)



# Change Label values

# Add 1 to brain image to make nonbrain = 1 and brain = 2
for file in glob.glob(os.path.join(datapath, subjects, version,'???_brain_smooth.nrrd')):

    cmd = 'ImageMath %s -constOper 0,1 -outfile %s' % (file, file)
    print cmd
    # subprocess.call(cmd, shell=True)

# Multiply image by 2 to make neocortex = 2. Later we will add it to brain image so that 2 + 1 = 3.
for file in glob.glob(os.path.join(datapath, subjects, version,'???_nc_?_smooth.nrrd')):

    cmd = 'ImageMath %s -constOper 2,2 -outfile %s' % (file, file)
    print cmd
    # subprocess.call(cmd, shell=True)



# Combine brain and neocortex images
for file in glob.glob(os.path.join(datapath, subjects, version,'???_brain_smooth.nrrd')):
    print file
    fid = os.path.basename(file)
    subjid = fid.split('_')[0]

    for region in ('nc_L_smooth','nc_R_smooth'):

        cmd = 'ImageMath %s -add %s -outfile %s' % (file,
              os.path.join(os.path.dirname(file), subjid+'_'+region+'.nrrd'),
              os.path.join(os.path.dirname(file), subjid+'_brain_'+region+'.nrrd') )

        print cmd
        # subprocess.call(cmd, shell=True)


