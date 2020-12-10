#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import glob
import re
import csv
import scipy as S

study = 'RPV9'
version = '7-Stats-c'

home = os.path.expanduser('~')
basedir = os.path.join(home, 'NADIA', study, 'Processing')
if not os.path.isdir(basedir):
    print '''+basedir+''', 'is not accessible.'
    sys.exit()

groups = ['Control', 'AIE', 'Unmanipulated']

# Subject ID, Group, Age
subjects = { '047': ['Unmanipulated', '80', '379'],   
             '048': ['Unmanipulated', '80', '353'],   
             '049': ['Unmanipulated', '80', '392'],   
             '050': ['Unmanipulated', '80', '343'],   
             '051': ['Unmanipulated', '80', '351'],   
             '052': ['Unmanipulated', '80', '380'],   
             '053': ['Unmanipulated', '80', '407'],   
             '054': ['Unmanipulated', '80', '373'],   
             '055': ['Unmanipulated', '80', '376'],   
             '056': ['Unmanipulated', '80', '375'],   
             '002': ['Control',       '80', '451'],   
             '003': ['Control',       '80', '462'],   
             '004': ['Control',       '80', '420'],   
             '009': ['Control',       '80', '431'],   
             '010': ['Control',       '80', '465'],   
             '011': ['Control',       '80', '480'],   
             '012': ['Control',       '80', '431'],   
             '013': ['Control',       '80', '474'],   
             '015': ['Control',       '80', '454'],   
             '021': ['Control',       '80', '486'],   
             '033': ['AIE',           '80', '465'],   
             '034': ['AIE',           '80', '466'],   
             '035': ['AIE',           '80', '426'],   
             '037': ['AIE',           '80', '430'],   
             '038': ['AIE',           '80', '467'],   
             '039': ['AIE',           '80', '458'],   
             '040': ['AIE',           '80', '407'],   
             '043': ['AIE',           '80', '471'],   
             '045': ['AIE',           '80', '476'],   
             '046': ['AIE',           '80', '428'],
           }   
# Duke P80 Atlas
structures = { '0': "",
               '1': "L-01",
               '2': "L-02",
               '3': "L-03",
               '4': "L-04",
               '5': "L-05",
               '6': "L-06",
               '7': "L-07",
               '8': "R-08",
               '9': "R-09",
              '10': "R-10",
              '11': "R-11",
              '12': "R-12",
              '13': "R-13",
              '14': "R-14",
             }


#---------------------------------------------------------------------------#
# Read data from Stats files
#---------------------------------------------------------------------------#
d = []
# mask_string = 'mask_from_seg_reg_stat.txt'
seg_string  = 'histology_reg_stat.txt' #'segmentation_m_masked_cortexsplit_reg_stat.txt'


for i in sorted(glob.glob(os.path.join(basedir, '???', version, '*histology_reg_stat.txt'))):

    f = open(i)
    x = f.readlines()
    f.close()
    print i

    filename = os.path.basename(i)
    subject = filename.split('_')[0]

    # Segmentation
    if re.search(seg_string, filename):
        for line in x:
            if not ( line.startswith('#') or line.startswith('\n') ):
                measure = 'VOL' # measure = filename.split('_')[-2]
                label = line.split()[0]
                structure = structures[label]
                volume = float(line.split()[1])
                intensity = float(line.split()[2])
                group = subjects[subject][0]
                age = subjects[subject][1]
                bodyweight = subjects[subject][2]
                
                print volume

                d.append([ study, subject, group, age, bodyweight,label, structure, volume ])
                

d = S.array(d)

#---------------------------------------------------------------------------#
# Exclude groups, subjects, and/or structures
#---------------------------------------------------------------------------#
d = S.delete(d, S.where(d[:,2] == 'Unmanipulated')[0], 0)

#---------------------------------------------------------------------------#
# Write all data to one comma-delimited text file
#---------------------------------------------------------------------------#
odir = os.path.join(home, 'NADIA', study,'Results', version)
if not os.path.isdir(odir):
    os.mkdir(odir)
fid = open(os.path.join(odir, 'Stats-'+study+'-CorticalThicknessROIs.csv'), 'w')
writer = csv.writer(fid, delimiter=',', quotechar='"')
writer.writerow([ 'Study', 'Subject', 'Group', 'Age', 'Bodyweight', 'Label', 'Structure', 'Volume' ])
for row in d:
    writer.writerow(row)
    fid.flush()
fid.close()
