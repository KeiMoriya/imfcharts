'''
2025-12-28

Examples of adding fill.

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
# p. 2 Chart 1
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page2/fig2_chart1_inflation.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Inflation' : {'linewidth' : 4, 'color' : IMFBLACK},
         'Goods' : {'linewidth' : 4, 'color' : IMFBLUE, 'linestyle' : 'imfdash'},
         'Services' : {'linewidth' : 4, 'color' : IMFRED, 'linestyle' : 'imfdash'}}
linecols = df.columns

# Add columns for fill lo, hi
lo = 'lo'
hi = 'hi'
lo2 = 'lo2'
hi2 = 'hi2'
df[lo] = df['Inflation'] - 3
df[hi] = df['Inflation'] + 3
df[lo2] = df['Inflation'] - 10
df[hi2] = df['Inflation'] + 10
#==========================================================================================================
# fill
#==========================================================================================================

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add fill
chart1.add_fill(lo, hi)

# Save
chart1.save(outdir + '/fill_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. multiple
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add fill
chart1.add_fill(lo, hi)
chart1.add_fill(lo2, lo, color='blue')
chart1.add_fill(hi, hi2, color='blue')

# Save
chart1.save(outdir + '/fill_2_multiple.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. color, linewidth, linecolor, linestyle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add fill
chart1.add_fill(lo, hi, data=df)
chart1.add_fill(lo2, lo, data=df,
                color='blue', linewidth=1.5, linestyle='--', alpha=1)
chart1.add_fill(hi, hi2, data=df,
                color='orange', linewidth=2.5, linestyle='-', alpha=0.2)

# Save
chart1.save(outdir + '/fill_3_line_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. zorder
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add fill
chart1.add_fill(lo, hi, data=df)
chart1.add_fill(lo2, lo, data=df,
                color='blue', linewidth=1.5, linestyle='--', alpha=1, zorder=2)
chart1.add_fill(hi, hi2, data=df,
                color='orange', linewidth=2.5, linestyle='-', alpha=0.2, zorder=2)

# Save
chart1.save(outdir + '/fill_4_zorder.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add fill
chart1.add_fill(lo, hi, data=df, legend=True, label='base')
chart1.add_fill(lo2, lo, data=df,
                color='blue', edgecolor='orange', linewidth=1.5, linestyle='--', alpha=0.2, zorder=2,
                legend=True, label='larger error')
# No legend for higher band
chart1.add_fill(hi, hi2, data=df,
                color='blue', edgecolor='orange', linewidth=1.5, linestyle='--', alpha=0.2, zorder=2)

# Save
chart1.save(outdir + '/fill_5_legend.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/fill.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/*fill*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
