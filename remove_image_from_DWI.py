#!/usr/bin/env python
# encoding: utf-8
"""
This is a script to remove one image from a DWI image with multiple images. For instance, I want to remove a b0 image from 24 images in my DWIs.

Created by Richard Yaxley on 2012-06-25.
"""

import sys
import os
import subprocess
import commands
import glob
import re
import numpy as np
import fileinput
import shutil



if (len(sys.argv) == 1):
    sys.exit('Please specify the name of your image and the image to remove: $ remove_image_fromDWI.py 001_dwi.nhdr 8')
else:
    image = sys.argv[1]
    image_to_remove = sys.argv[2]




datapath = os.path.dirname(os.path.abspath(image))

opath = os.path.join(datapath, 'EditedImage')
if not os.path.isdir(opath):
    os.makedirs(opath)

# open raw header file from temp/ directory output of CoregisterDWI.
fid = open(image)
hdr = fid.readlines()
fid.close()
# Edit header
temp = []
for line in hdr:
    
    # Change size of image from 24 to 23
    if re.search('sizes', line, re.I):
        line = line.replace('24','23') # if only one image removed, can make smarter
        
    if re.search('data file:', line):
        # line = line.replace('???_dwi_split_P%03d_transformed.raw.gz', '011_dwi_split_P%03d_transformed.raw.gz')
        line = line.replace('0 23 1', '0 22 1')
        line = line.replace('011_dwi_','')
        line = line.replace('_transformed.raw.gz','.raw')
        # line = line.replace('011_dwi_split_P%03d_transformed_edited.raw.gz','split_P%03d.raw')
        # z = line
        print line

    # Remove gradient
    if re.search('DWMRI_gradient_'+image_to_remove.zfill(4), line, re.I):
        line = ''
        
    # Change numbering (shift by -1) of subsequent gradients
    if re.search('DWMRI_gradient', line, re.I):
        if int(line.split(':')[0][-4:]) > int(image_to_remove):
            line = line.replace(line.split(':')[0][-4:], str(int(line.split(':')[0][-4:])-1).zfill(4))
    
    temp.append(line)
    
    x = open(os.path.join(opath, image.replace('.nhdr','_edited.nhdr')), 'w')
    x.writelines(temp)
    x.close()


# Renumber files that comprise each DWI
for i in sorted(glob.glob(os.path.join(datapath, 'split_*.raw'))):
    print i
    if int(os.path.basename(i).split('.')[0][-3:]) < int(image_to_remove):
        src = i
        tgt = os.path.join(opath, os.path.basename(i))
    elif int(os.path.basename(i).split('.')[0][-3:]) == int(image_to_remove):
        print 'SKIPPING THIS FILE:', i
    elif int(os.path.basename(i).split('.')[0][-3:]) > int(image_to_remove):
        src = i
        fid = os.path.basename(i)
        fid = fid.replace(fid.split('.')[0][-3:],  str(int(fid.split('.')[0][-3:])-1).zfill(3))
        tgt = os.path.join(opath, fid)
    
    shutil.copyfile(src,tgt)
    
# write out a new image using unu save
ifid = os.path.join(opath, '*_edited.nhdr')
ofid = os.path.join(opath, 'Edited.nrrd')
cmd = 'unu save -e gzip -f nrrd -i %s -o %s' % (ifid, ofid)
print cmd
subprocess.call(cmd, shell=True) 