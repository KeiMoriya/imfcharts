'''
2026-02-23

Examples of adding watermark.

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

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120],
               watermark='Confidential')

# Save
chart1.save(outdir + '/watermark_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. Add separately
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add watermark
chart1.watermark('Confidential')

# Save
chart1.save(outdir + '/watermark_2_watermark.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. color, linewidth, linecolor, linestyle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120],
               watermark='Confidential',
               wmx=0.3, wmy=0.3, 
               wmangle=45, wmsize=30, wmcolor='red', wmalpha=0.7, wmfont='serif')
# Save
chart1.save(outdir + '/watermark_3_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. zorder
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120],
               watermark='Confidential',
               wmx=0.3, wmy=0.3, 
               wmangle=45, wmsize=30, wmcolor='red', wmalpha=0.7, wmfont='serif', wmz=0)
# Save
chart1.save(outdir + '/watermark_4_zorder.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecols,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Add watermark
kwargs = {'x' : 0.3, 'y' : 0.3, 'angle' : 45, 'size' : 30, 'color' : 'red', 'alpha' : 0.7, 'font' : 'serif', 'z' : 0}
chart1.watermark(**kwargs)

# Save
chart1.save(outdir + '/watermark_5_kwargs.pdf')


#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/watermark.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/watermark*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
