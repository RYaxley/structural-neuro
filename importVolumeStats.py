#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import glob
import scipy as S
import csv


if (len(sys.argv) > 1):
    base = sys.argv[1]
    if not os.path.isdir(os.path.dirname(base)):
        print 'Path is not available.'
        raise SystemExit
else:
    print "Enter a directory path to search."
    raise SystemExit


#---------------------------------------------------------------------------#
# Read data from Stats files
#---------------------------------------------------------------------------#
data = []
print '\nStat files found in base path:\n', 
for i in glob.glob(os.path.join(base, '*_stat.txt')):
    print i
    f = open(i)
    x = f.readlines()
    f.close()
    
    subject = os.path.split(i)[1].split('_')[0]

    for line in x:
        if line.startswith('#') or line.startswith('\n'):
            pass
        else:
            label = line.split()[0]
            volume = line.split()[1]
            data.append([subject, label, volume])

data = S.array(data)


#---------------------------------------------------------------------------#
# Write all data to one comma-delimited text file
#---------------------------------------------------------------------------#
fid = os.path.join(base, 'VolumeStats.csv')
writer = csv.writer(open(fid, 'w'), delimiter=',')
writer.writerow(['Subject', 'Group', 'Label', 'Volume'])
for row in data:
    writer.writerow(row)            
print '\nOutput:\n', fid
