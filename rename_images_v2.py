#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

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


if (len(sys.argv) == 1):
    sys.exit('Please specify the directory path to your study. For example, /Animal/rodent/Crews/NADIA/RPV3. And specify version _2014-03-26')
else:
    study = sys.argv[1]
    version = sys.argv[2]

datapath = os.path.join(study, 'Data')
if not os.path.isdir(os.path.join(datapath)):
    sys.exit("A data directory was not found. Specify a different path.")
template = os.path.join(study, 'Tools', 'HeaderTemplate.nhdr')


# Dictionary for the Scan ID : NADIA Case_ID, Series1, Series2, Series3
cases = {'20120730_crews_NADIA_FTC_RPV0004_36'     : ['036', '131073', '196609', '262145'],
         '20120731_crews_NADIA_FTC_RPV0004_35'     : ['035', '131073', '196609', '262145'],
         '20120801_crews_NADIA_FTC_RPV0004_34'     : ['034', '327681', '393217', '458753'],
         '20120803_crews_NADIA_FTC_RPV0004_32'     : ['032', '327681', '393217', '458753'],
         '20120806_crews_NADIA_FTC_RPV0004_28'     : ['028', '131073', '196609', '262145'],
         '20120809_crews_NADIA_FTC_RPV0004_23'     : ['023', '196609', '262145', '327681'],
         '20120810_crews_NADIA_FTC_PRV0004_26^^^^' : ['026', '262145', '327681', '393217'],
         '20120814_crews_NADIA_FTC_RPV0004_17^^^^' : ['017', '393217', '458753', '524289'],
         '20120816_crews_NADIA_FTC_RPV004_12^^^^'  : ['012', '262145', '327681', '393217'],
         '20120817_crews_NADIA_FTC_RPV0004_11'     : ['011', '327681', '393217', '458753'],
         '20120820_crews_NADIA_FTC_RPV004_10'      : ['010', '262145', '327681', '393217'],
         '20120822_crews_NADIA_FTC_PRV0004_9^^^^'  : ['009', '327681', '393217', '458753'],
         '20120823_crews_NADIA_FTC_RPV0004_3'      : ['003', '327681', '393217', '458753'],
         '20120826_crews_NADIA_FTC_RPV0004_1^^^^'  : ['001', '196609', '262145', '327681'],
         '20120926_crews_NADIA_FTC_RPV0004_13'     : ['013', '131073', '196609', '262145'],
         '20110525_RPV_0001_00001' :  ['001', '196609', '262145', '327681'],
         '20110606_RPV_0001_00002' :  ['002', '131073', '196609', '262145'],
         '20110614_RPV_0001_00003' :  ['003', '131074', '196610', '262146'],
         '20110628_RPV_0001_00004' :  ['004', '196609', '262145', '327681'],
         '20110519_RPV_0001_00005' :  ['005', '196609', '262145', '327681'],
         '20110705_RPV_0001_00006' :  ['006', '196609', '262145', '      '], # Exclude
         '20110707_RPV_0001_00007' :  ['007', '196609', '262145', '327681'],
         '20110802_RPV_0001_00008' :  ['008', '196609', '262145', '327681'],
         '20110805_RPV_0001_00009' :  ['009', '458753', '524289', '589825'], # Exclude
         '20110531_RPV_0001_00030' :  ['030', '131073', '196609', '262145'],
         '20110609_RPV_0001_00031' :  ['031', '131073', '196609', '262145'],
         '20110616_RPV_0001_00032' :  ['032', '655361', '720897', '786433'],
         '20110627_RPV_0001_00033' :  ['033', '196609', '262145', '327681'],
         '20110718_RPV_0001_00034' :  ['034', '262145', '327681', '393217'],
         '20110907_RPV_0001_00035' :  ['035', '196609', '262145', '327681'],
         '20110523_RPV_0001_00036' :  ['036', '131073', '196609', '262145'],
         '20110815_RPV_0001_00037' :  ['037', '196609', '262145', '327681'],
         }

# '''
# Format: Case_ID  Series1     Series2     Series3
# 
# Study: RPV1 
# 001 196609 262145 327681
# 002 131073 196609 262145
# 003 131074 196610 262146
# 004 196609 262145 327681
# 005 196609 262145 327681
# 006 196609 262145
# 007 196609 262145 327681
# 008 196609 262145 327681
# 009 458753 524289 589825
# 030 131073 196609 262145
# 031 131073 196609 262145
# 032   655361 720897 786433
# 033 196609 262145 327681
# 034 262145 327681 393217
# 035 196609 262145 327681
# 036 131073 196609 262145
# 037 196609 262145 327681
# 20110518_RPV_0001_00023.tar.gz
# 20110524_RPV_0001_00010.tar.gz
# 20110526_RPV_0001_00011.tar.gz
# 20110601_RPV_0001_00020.tar.gz
# 20110607_RPV_0001_00012.tar.gz
# 20110608_RPV_0001_00021.tar.gz
# 20110609_RPV_0001_00031.tar.gz
# 20110613_RPV_0001_00013.tar.gz
# 20110615_RPV_0001_00022.tar.gz
# 20110616_RPV_0001_00032.tar.gz
# 20110622_RPV_0001_00014.tar.gz
# 20110623_RPV_0001_00024.tar.gz
# 20110711_RPV_0001_00015.tar.gz
# 20110727_RPV_0001_00016.tar.gz
# 20110812_RPV_0001_00017.tar.gz
# #---------------------------------------------------------------------------#
# Study: LJC1
# 002ss 196609 262145 327681
# 003ss 196609 262145 327681
# 149ca 131073 196609 262145
# 150ea 131073 196609 262145
# 150eb 131073 196609 262145
# 153ca 131073 196609 262145
# 153cb 131073 196609 262145
# 168ca 131073 196609 262145 
# 169eb 131073 196609 262145 
# 169ec 131073 196609 262145 
# 170eb 131073 196609 262145 
# 178ca 196609 262145 327681
# 178cb 196609 262145 327681
# 179ea 131073 196609 262145 
# 179eb 262145 327681 393217

# #---------------------------------------------------------------------------#
# Study: WL4
# 001 131073 196609 262145
# 002 196609 262145 327681
# 004 262146 327682 393218
# 008 196610 262146 327682
# 007 262145 327681 393217
# 009 196610 262146 327682
# 010 196610 262146 327682
# 011 196609 262145 327681
# 012 393217 458753 524289
# 013 262146 327682 393218
# 014 196610 262146 327682
# 015 131074 196610 262146
# 016 327682 393218 458754
# 017 655362 720898 786434
# 018 262146 327682 393218
# 019 196611 262146 327682
# 
# '''

for i in glob.glob(os.path.join(datapath,'*gz')):
    print i

    # Extract directory name, case name, image name
    fid = os.path.basename(i)
    scanid = fid.split('.')[0]
    case = cases[scanid][0]
    # print fid, scanid, '--->', case
    
    opath = os.path.join(study,'Processing',case,'1-Converted'+version)
    
    if not os.path.exists(opath):
        os.makedirs(opath)
    
    # if case empty directory, unzip file to directory    
    if not os.listdir(opath):
        cmd = 'tar -xzvf %s -C %s' % (i, opath)
        print cmd
        subprocess.call(cmd, shell=True)
    
    # If case directory doesn't include .nhdr
    # Convert DICOM image
    if len(os.listdir(opath)) == 1:
        print os.listdir(opath)
        cmd = 'DicomConvert %s %s.nhdr' % (os.path.join(opath,scanid,'DICOM'), os.path.join(opath,case))
        print cmd
        subprocess.call(cmd, shell=True)        
    
    # Remove "FLASH" positioning images
    for file in glob.glob(os.path.join(opath, '*')):
        if re.search('FLASH', file, re.I):
            print 'Removing:', file
            os.remove(file)
            
    # Remove Bruker Images (last dimension = 1210 rather than 440)
    for file in glob.glob(os.path.join(opath, '*.nhdr')):
        fid = open(file)
        hdr = fid.readlines()
        fid.close()

        for line in hdr:
            if re.search('sizes:', line, re.I):   
                if line.split()[-1] == '1210':
                    print 'Removing:', file
                    os.remove(file)
                    z = file.replace('nhdr', 'raw.gz')
                    if os.path.isfile(z):
                        print 'Removing:', z
                        os.remove(z)
        
    # Rename DWI files based on order
    extensions = ['.nhdr', '.raw.gz']
    for ext in extensions:
        for file in glob.glob(os.path.join(opath, '*_?.??.???.*'+ext)):
            for n in [1,2,3]:
                if re.search(cases[scanid][n], file):
                    print file, scanid, cases[scanid][n]
                    newname = os.path.join(opath, case + '_' + str(n) + ext)
                    print 'Renaming:', file, n, file.split('.')[9][2:-1], '-->', newname
                    os.rename(file, newname)
     
    # Edit the .nhdr file to point to the new raw image filename (ie, dwi_1.raw.gz, dwi_2.raw.gz, dwi_3.raw.gz)      
    for file in glob.glob(os.path.join(opath, '*.nhdr')):
        temp = []
        f = open(file)
        header = f.readlines()
        f.close()
        
        for line in header:
            if re.search('data file', line):
                line = line.replace(line, 'data file: '+ os.path.basename(file).split('.')[0] + '.raw.gz')
            temp.append(line)

            
        x = open(os.path.join(file), 'w')
        x.writelines(temp)
        x.close()         


    del temp

    # Read in the HeaderTemplate.nhdr into each subject folder and rename them as CaseID#_dwi.nhdr
    f = open(template)
    header_template = f.read()
    f.close()

    temp = []

    # Read a header file from the raw data and modify it to use as an overall header file
    for file in sorted(glob.glob(os.path.join(opath, '*_1.nhdr'))):
        print file

        f = open(file)
        header = f.readlines()
        f.close()

    # Change specific lines
    for line in header:
        if re.search('dimension:', line):
            line = line.replace('3', '4')

        if re.search('sizes:', line):
            line = line.replace('440', '55 24')  

        if re.search('space directions:', line):
            line = line.strip() + ' none\n'                                      

        if re.search('kinds:', line):
            line = line.replace('domain domain domain', 'domain domain domain list')            

        if re.search('data file:', line):
            line = line.replace(line, 'data file: '+ case+ '_%d.raw.gz 1 3 1 4\n')
            
        temp.append(line)

    # Add new lines
    temp.append('modality:=DWMRI\n')
    
    # temp.append('measurement frame: (1,0,0) (0,1,0) (0,0,1)\n') # MF 1     
    # temp.append('measurement frame: (1,0,0) (0,0,1) (0,1,0)\n') # MF 2
    # temp.append('measurement frame: (0,1,0) (1,0,0) (0,0,1)\n') # MF 3     
    # temp.append('measurement frame: (0,1,0) (0,0,1) (1,0,0)\n') # MF 4
    # temp.append('measurement frame: (0,0,1) (1,0,0) (0,1,0)\n') # MF 5    
    # temp.append('measurement frame: (0,0,1) (0,1,0) (1,0,0)\n') # MF 6
    # temp.append('measurement frame: (1,0,0) (0,1,0) (0,0,-1)\n') # MF 7    
    # temp.append('measurement frame: (1,0,0) (0,0,1) (0,-1,0)\n') # MF 8 
    # temp.append('measurement frame: (0,1,0) (1,0,0) (0,0,-1)\n') # MF 9   
    # temp.append('measurement frame: (0,1,0) (0,0,1) (-1,0,0)\n') # MF 10   
    # temp.append('measurement frame: (0,0,1) (1,0,0) (0,-1,0)\n') # MF 11  
    # temp.append('measurement frame: (0,0,1) (0,1,0) (-1,0,0)\n') # MF 12
    # temp.append('measurement frame: (1,0,0) (0,-1,0) (0,0,1)\n') # MF 13
    # temp.append('measurement frame: (1,0,0) (0,0,-1) (0,1,0)\n') # MF 14   
    # temp.append('measurement frame: (0,1,0) (-1,0,0) (0,0,1)\n') # MF 15   
    # temp.append('measurement frame: (0,1,0) (0,0,-1) (1,0,0)\n') # MF 16   
    # temp.append('measurement frame: (0,0,1) (-1,0,0) (0,1,0)\n') # MF 17 
    # temp.append('measurement frame: (0,0,1) (0,-1,0) (1,0,0)\n') # MF 18
    # temp.append('measurement frame: (1,0,0) (0,-1,0) (0,0,-1)\n') # MF 19
    # temp.append('measurement frame: (1,0,0) (0,0,-1) (0,-1,0)\n') # MF 20  
    # temp.append('measurement frame: (0,1,0) (-1,0,0) (0,0,-1)\n') # MF 21 
    # temp.append('measurement frame: (0,1,0) (0,0,-1) (-1,0,0)\n') # MF 22  
    temp.append('measurement frame: (0,0,1) (-1,0,0) (0,-1,0)\n') # MF 23  
    # temp.append('measurement frame: (0,0,1) (0,-1,0) (-1,0,0)\n') # MF 24  
    
    temp.append('DWMRI_b-value:=1600\n')
    
    temp.append('DWMRI_gradient_0000:=0 0 0\n')
    temp.append('DWMRI_gradient_0001:=0.000000 -0.850350 -0.526217\n')
    temp.append('DWMRI_gradient_0002:=0.526217 0.000000 -0.850350\n')
    temp.append('DWMRI_gradient_0003:=-0.526217 0.000000 -0.850350\n')
    temp.append('DWMRI_gradient_0004:=-0.850350 0.526217 0.000000\n')
    temp.append('DWMRI_gradient_0005:=-0.850350 -0.526217 0.000000\n')
    temp.append('DWMRI_gradient_0006:=0.000000 -0.850350 0.526217\n')
    temp.append('DWMRI_gradient_0007:=-0.309006 0.500010 0.809015\n')
    temp.append('DWMRI_gradient_0008:=0 0 0\n')
    temp.append('DWMRI_gradient_0009:=-0.809015 0.309006 0.500010\n')
    temp.append('DWMRI_gradient_0010:=-0.500010 0.809015 0.309006\n')
    temp.append('DWMRI_gradient_0011:=0.000000 1.000000 0.000000\n')
    temp.append('DWMRI_gradient_0012:=-0.500010 0.809015 -0.309006\n')
    temp.append('DWMRI_gradient_0013:=-0.809015 -0.309006 0.500010\n')
    temp.append('DWMRI_gradient_0014:=-1.000000 0.000000 0.000000\n')
    temp.append('DWMRI_gradient_0015:=0.707107 0.000000 0.707107\n')
    temp.append('DWMRI_gradient_0016:=0 0 0\n')
    temp.append('DWMRI_gradient_0017:=0.309006 0.500010 0.809015\n')
    temp.append('DWMRI_gradient_0018:=0.500010 0.809015 -0.309006\n')
    temp.append('DWMRI_gradient_0019:=0.500010 0.809015 0.309006\n')
    temp.append('DWMRI_gradient_0020:=0.809015 0.309006 0.500010\n')
    temp.append('DWMRI_gradient_0021:=0.809015 -0.309006 0.500010\n')
    temp.append('DWMRI_gradient_0022:=0.309006 -0.500010 0.809015\n')
    temp.append('DWMRI_gradient_0023:=-0.309006 -0.500010 0.809015\n')
    
    x = open(os.path.join(opath, case+'_dwi.nhdr'), 'w')
    x.writelines(temp)
    x.close()   

























