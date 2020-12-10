import os
import sys
import glob
import scipy as S
import scipy.stats
import numpy

home = os.path.expanduser('~')
for i in glob.glob(os.path.join(home, 'Ares', 'LvF', 'duke', 'P28', '*.tfm')):
    
    transform = os.path.split(i)[-1]
    
    f = open(i)
    x = f.readlines()
    f.close()
    
    mat = []
    for line in x:
        if line.startswith('Parameters:'):
            a = line.split()[1:4]
            b = line.split()[4:7]
            c = line.split()[7:10]
            mat = [a,b,c]
    print transform, numpy.linalg.det(mat).round(3)
            

