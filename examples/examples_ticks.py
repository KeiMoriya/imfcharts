'''
2026-01-31

Example of ticks.

Data files are created by get_data_turkey_page2.py
'''

import os
import sys
import glob

import numpy as np
import pandas as pd

from PyPDF2 import PdfWriter

import imfcharts
import imfcharts.charts
import imfcharts.mpl
import importlib
importlib.reload(imfcharts)
importlib.reload(imfcharts.charts)
importlib.reload(imfcharts.mpl)
from imfcharts import *
# set_style('fund-guide')

# Turn on interactive mode
# plt.ion()
# Clear all existing figures
plt.close('all')

outdir = 'pdf'

# ---------------------------------------------------------------------------------------------------------
# p. 5 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart2_current_account_mms.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0]).dropna(how='all', axis=0)

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='no options',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/ticks_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='options',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55,
               xtickfontsize=15, ytickfontsize=15,
               xticklength=10, yticklength=10,
               xtickpad=10, ytickpad=10,
               xtickangle=90, ytickangle=45)

# Save
chart2.save(outdir + '/ticks_2_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. Call separately
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='call ticks()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)
chart2.ticks(axis='x', size=15, length=10, angle=90, pad=10)
chart2.ticks(axis='y', size=15, length=10, angle=45, pad=10)

# Save
chart2.save(outdir + '/ticks_3_ticks.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. Set nticks as int
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='nticks as int',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55,
               xtickfontsize=15, ytickfontsize=15,
               xticklength=10, yticklength=10,
               xtickpad=10, ytickpad=10,
               xtickangle=90, ytickangle=45,
               nticksx=10, nticksy=10)

# Save
chart2.save(outdir + '/ticks_4_nticks_int.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. Call separately with int nticks
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='call ticks() with nticks int',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)
chart2.ticks(axis='x', size=15, length=10, angle=90, pad=10, nticks=10)
chart2.ticks(axis='y', size=15, length=10, angle=45, pad=10, nticks=10)

# Save
chart2.save(outdir + '/ticks_5_ticks_nticks_int.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. No x-axis range
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='call ticks() with nticks int',
               yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/ticks_6_full_xrange.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. 25 years data
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='call ticks() with nticks int',
               xrange='2000-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/ticks_7_25years.pdf')

# ---------------------------------------------------------------------------------------------------------
# 8. 10 years data
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='call ticks() with nticks int',
               xrange='2015-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/ticks_8_10years.pdf')

# ---------------------------------------------------------------------------------------------------------
# 9. 5 years data
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='call ticks() with nticks int',
               xrange='2020-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/ticks_9_5years.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/ticks.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted([f for f in glob.glob(outdir + '/ticks*.pdf') if f.find('rects') == -1])
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
