#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import glob
import commands
import subprocess


study = sys.argv[1]

if not os.path.isdir(os.path.join(study, 'Data')):
    sys.exit("A data directory was not found. Specify a different path.")

if not os.path.isdir(os.path.join(study, 'Processing')):
    os.makedirs(os.path.join(study, 'Processing'))

for i in glob.glob(os.path.join(study, 'Data', '*')):
    
    ipath = os.path.join(i, 'DICOM')
    opath = os.path.join(study, 'Processing', i.split(os.path.sep)[-1])
    if not os.path.isdir(opath):
        os.makedirs(opath)
    ofile = i.split(os.path.sep)[-1]+'.nrrd'
    
    if os.path.isfile(os.path.join(opath, ofile)):
        print 'Skipping ' + ofile
    else:
        cmd = 'DicomToNrrdConverter --inputDicomDirectory %s --outputDirectory %s --outputVolume %s ' % ( ipath, opath, ofile )
        print cmd
        print 'Converting ' + ofile 
        subprocess.call(cmd, shell=True)
   
    