#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import subprocess
import commands
import glob
import re


if (len(sys.argv) == 1):
    sys.exit('Please specify the directory path to your data. For example, ~/Experiment ')
else:
    studydir = sys.argv[1]
    if not os.path.isdir(os.path.join(studydir)):
        sys.exit("A data directory was not found. Run script again and specify a different path.")
        

protocol = os.path.join(studydir, 'Scripts', 'QC-protocol.xml')
if not os.path.isfile(protocol):
    sys.exit("A QC-protocol.xml file was not found in the ~/Experiment/Scripts/ directory.")
    
    
for casedir in sorted(glob.glob(os.path.join(studydir,'Processing', '???'))):
    
    for datadir in glob.glob(os.path.join(casedir, '1-Converted')):

        case = casedir.split('/')[-1]
        image = os.path.join(datadir, case+'_dwi_MFcorrected.nrrd')
        output_dir = os.path.join(datadir, 'QC-DTIPrep')
        
        if not os.path.isdir(output_dir):
            cmd = 'DTIPrep1.2 -w %s -p %s -f %s' % (image, protocol, output_dir)
            print 'Processing Case #', case, '\n-->', cmd
            subprocess.call(cmd, shell=True)
    
    
    


    

        
        