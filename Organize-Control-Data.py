#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import glob
import numpy as N
import scipy as S
import scipy.stats
import csv
from decimal import *
import pylab as P
import matplotlib.pyplot as P
import itertools

def adjust_spines(ax,spines):
    for loc, spine in ax.spines.iteritems():
        if loc in spines:
            spine.set_position(('outward',0)) # outward by 10 points
        else:
            spine.set_color('none') # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])

home = os.path.expanduser('~')

basedir = os.path.join(home, 'NADIA')

files = [ os.path.join(home, 'RPV1', 'Processing', '7-Stats', 'Stats-RPV1.csv' ),
          os.path.join(home, 'RPV2', 'Processing', '7-Stats', 'Stats-RPV2.csv' ),
          os.path.join(home, 'RPV3', 'Processing', '7-Stats', 'Stats-RPV3.csv' ),
          os.path.join(home, 'LJC1', 'Processing', '7-Stats-ANTS_2013Aug29-current','Stats-LJC1.csv' ),
          os.path.join(home, 'CLE', '7-Stats', 'Stats-CLE_04_2011.csv' ),
          os.path.join(home, 'NADIA_pilot', '7-Stats', 'Stats-NADIA_pilot.csv' ),
          os.path.join(home, 'LvF', '7-Stats', 'Stats-LvF-Overnight.csv' ),
        ]

output_type = ['pdf','300'] # Format, DPI


structures = { '0': "Total Brain" ,
               '1': "Hippocampus" ,
               '2': "External Capsule" ,
               '3': "Caudate, Putamen, Globus Pallidus",
               '4': "Anterior Commissure" ,
               '5': "Substantia Nigra" ,
               '6': "Internal Capsule" ,
               '7': "Thalamus" ,
               '8': "Cerebellum" ,
               '9': "Superior Colliculus" ,
              '10': "Third Ventricle" ,
              '11': "Hypothalamus" ,
              '12': "Inferior Colliculus" ,
              '13': "Central Gray" ,
              '14': "Neocortex" ,
              '15': "Amygdala" ,
              '16': "Olfactory Bulb" ,
              '17': "Brainstem" ,
              '18': "Rest of Midbrain" ,
              '19': "Rest of Forebrain" ,
              '20': "Fimbria" ,
              '21': "Fornix" ,
              '22': "VTA" ,
              '23': "Corpus Callosum" ,
              '24': "Genu" ,
              '25': "Lateral Ventricle" ,
              '26': "Aqueduct" ,
              '27': "Fourth Ventricle" ,
              '28': "External Capsule (Left)" ,
              '29': "Splenium" ,
              '30': "Anterior Piriform" ,
              '31': "Entorhinal Cortex" ,
              '32': "Rest of Cortex" ,
              '33': "Medial PFC",
              '35': "Orbital Cortex",
             }
               
                
# Read files
d = []
for i in files:
    fid = open(i, 'rU')
    reader = csv.reader(fid, delimiter=',')
    fields = reader.next()
    for row in reader:
        d.append(row)
    fid.close()
d = N.array(d)

# Controls only and reduce to volumes measures
controls = d.copy()
controls = controls[ S.nonzero(controls[:,2] == 'Control') ]

#---------------------------------------------------------------------------#
# Write all data to one comma-delimited text file
#---------------------------------------------------------------------------#
odir = os.path.join(basedir, 'Control-Data')
if not os.path.isdir(odir):
    os.mkdir(odir)
fid = open(os.path.join(odir, 'Stats-Control.csv'), 'w')
writer = csv.writer(fid, delimiter=',', quotechar='"')
writer.writerow([ 'Study', 'Subject', 'Group', 'Age', 'Label', 'Structure', 'Volume', 'Ratio', 'FA', 'MD', 'AD', 'RD' ])
for row in controls:
    writer.writerow(row)
    fid.flush()
fid.close()





#---------------------------------------------------------------------------#
# Plot settings
TitleSize = 18    
MarkerSize = 12
LabelSize = 14
PointSize = 6
CapSize = 0
width = .05
            
# Data for each structure and age
# for structure in structures.itervalues(): # All structures
for structure in [ 'Hippocampus', 'Amygdala', 'Hypothalamus', 'Cerebellum', 'Neocortex', 'Corpus Callosum', 'Caudate, Putamen, Globus Pallidus' ]:    
    
    fig = P.figure(figsize=(10,7.5))
    ax = fig.add_subplot(1,1,1)
    
    x = []
    xbars = []
    all_xdata = []
    all_ydata = []

    for age in sorted(S.unique(controls[:,3]).astype(int)):

        # Indices for age and structure, and the intersection of the two
        i_age = S.nonzero(controls[:,3] == str(age))[0]
        i_structure = S.nonzero(controls[:,5] == structure )[0]
        i_ageXstructure = S.intersect1d(i_age, i_structure)
        
        # All data for this age and this structure
        x = controls[i_ageXstructure, 6].astype(float) 
        
        # X-axis tickmark locations based on age
        x_locations = S.sort(S.unique(controls[:,3]).astype(float))/S.unique(controls[:,3]).astype(float).max()
    
        if len(x) == 0:
            xbars.append(S.nan)
            all_xdata.append(S.nan)
            all_ydata.append(S.nan)
        if len(x) > 1:
            xbar = S.stats.nanmean(x)
            xsem = S.stats.nanstd(x)/S.sqrt(len(x)) # check this formula, got rid of ddof=1
            xbars.append(xbar)
            all_xdata.append(x)
            all_ydata.append(age.repeat(len(x))) # ***
    
        print '\n', structure ,x, '\n', all_xdata

    # Plot
    P.title(structure+' Volume', fontsize=TitleSize)
    # Plot data points
    # P.scatter( [age/220.]*len(x), x, s=PointSize, marker='.', c='k', edgecolor='k')
    #     # Plot means + error bars
    #     ecolor = 'r'
    #     P.errorbar(age/220., xbar, yerr=xsem, fmt='.', linestyle='-', color=ecolor, ecolor=ecolor, capsize=CapSize, markerfacecolor=ecolor, markersize=MarkerSize, markeredgecolor=ecolor)
    # 
    #     # Borders
    #     adjust_spines(ax,['left', 'bottom'])
    #     # Y-axis
    #     # ymin, ymax = ax.get_ylim()
    #     # shift = (ymax-ymin)/10
    #     # ax.set_yticks(N.round(S.linspace(ymin+shift, ymax-shift, 7), 1))
    #     P.ylabel('Volume (mm^3)', fontsize=LabelSize)
    #     # X-axis
    #     ax.set_xlim(x_locations[0]-width, x_locations[-1]+width)
    #     P.xticks(x_locations, S.sort(S.unique(controls[:,3]).astype(int)))
    #     P.xlabel('Age (postnatal days)', fontsize=LabelSize)
    # 
    # # Plot connecting line
    # P.plot( x_locations, xbars, ':', color='.8')
    

    
    # Trendline
     # P.hold()
    # all_xdata = list(itertools.chain.from_iterable(all_xdata))
    # all_ydata = list(itertools.chain.from_iterable(all_ydata))
    # # Calculate trendline (linear fit)
    # fit = N.polyfit(all_xdata, all_ydata, 1)
    # fit_fn = N.poly1d(fit) # fit_fn is now a function which takes in x and returns an estimate for y
    # Plot trendline
    # P.plot(all_xdata, fit_fn(all_xdata), 'r-', linewidth=2)
            # # Linear regression using stats.linregress
        # (slope, intercept, rvalue, pvalue, stderr)=stats.linregress(x,y)
        # print('\n Overall Linear regression for ' + scan + plot)
        # print('parameters: slope=%.5f intercept=%.2f \nregression: r-value=%.2f p-value=%.3f, std error= %.3f' % (slope, intercept, rvalue, pvalue, stderr))
    
    # Save figure
    fname = structure + ' Volume'
    fig.savefig(os.path.join(basedir, 'Control-Data', fname+'.'+output_type[0]), dpi=output_type[1], format=output_type[0], transparent=False)
    fig.clf()
    P.close()

