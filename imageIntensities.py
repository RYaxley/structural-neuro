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


if (len(sys.argv) > 1):
    image = sys.argv[1]
    # xcoord = sys.argv[2]
    # ycoord = sys.argv[3]
    # zcoord = sys.argv[4]
else:
    print "need to specify args"



xcoord = range(1,243)
ycoord = [100]
zcoord = [100]


d = []
for x in xcoord:
    for y in ycoord:
        for z in zcoord:
            cmd = 'ImageMath '+ image +' -pixelLookup '+ str(x) +','+ str(y) +','+ str(z)
            print cmd
            # subprocess.Popen(cmd).wait()
            out = commands.getoutput(cmd)
            print out
        
print 'finis'


