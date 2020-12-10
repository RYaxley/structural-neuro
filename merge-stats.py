#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import glob
import pandas as pd


# Base path to search for files
basedir = sys.argv[1]

# Filename format
version = sys.argv[2]

if not os.path.isdir(basedir):
    print '''+basedir+''', 'is not accessible.'
    sys.exit()



def read_data(i):
    f = open(i)
    content = f.readlines()
    f.close()

    temp = []

    for line in content[13:]: # Exclude header info at top of file
        line = line.strip().split()
        temp.append(line)

    return temp



def read_study_info(i):
    'read in subjects, age, bodyweight labels etc'
    return



#---------------------------------------------------------------------------#
# Read data from Stats files
#---------------------------------------------------------------------------#
d = []

mask_string = 'mask_from_seg_reg_stat.txt'
seg_string  = 'segmentation-masked-m_reg_stat.txt'


for i in sorted(glob.glob(os.path.join(basedir,'Processing','???',version,'*_stat.txt'))):

    d = read_data(i)

    df = pd.DataFrame(d,columns=['Label','Volume','Mean','SD','Min','Max','Q1','Q5','Q33','Q50','Q66','Q95','Q99'])

    df['Subject'] = os.path.basename(i).split('_')[0]
    df['Study'] = basedir.split('/')[-1]
    df['Species']
    df['Strain']
    df['Age']
    df['Structure']





### groups will be extracted as unique values in subjects dictionary
