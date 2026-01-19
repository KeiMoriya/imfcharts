'''
2026-01-19

Example of x-axis, y-axis titles.

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
               title='xtitle no options',
               xtitle='dates',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/axistitles_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. Add with function
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='xtitle()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.xtitle('dates')

# Save
chart2.save(outdir + '/axistitles_2_xtitle.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. Options in Chart()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='options in Chart()',
               xtitle='dates',
               xfontsize=10, xfont='monospace', xfontweight=900, xcolor='red', xpad=2, xloc='center', xrotation=30, xalpha=0.3,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/axistitles_3_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. Options in title()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='with options xtitle()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.xtitle('dates',
              fontsize=10, font='monospace', fontweight=900, color='red', pad=2, loc='center', rotation=30, alpha=0.3)

# Save
chart2.save(outdir + '/axistitles_4_xtitle_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='kwargs for xtitle()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

kwargs = {'text' : 'dates',
          'fontsize' : 10, 'font' : 'monospace', 'fontweight' : 900,
          'color' : 'red', 'pad' : 2, 'loc' : 'center', 'rotation' : 30, 'alpha' : 0.3}
chart2.xtitle(**kwargs)

# Save
chart2.save(outdir + '/axistitles_5_xtitle_kwargs.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='xtitle no options',
               ytitle='values',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/axistitles_6_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. Add with function
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='ytitle()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.ytitle('values')

# Save
chart2.save(outdir + '/axistitles_7_ytitle.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. Options in Chart()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='options in Chart()',
               ytitle='values',
               yfontsize=10, yfont='monospace', yfontweight=900, ycolor='red', ypad=2, yloc='center', yrotation=75, yalpha=0.3,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/axistitles_8_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. Options in title()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='with options xtitle()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.ytitle('values',
              fontsize=10, font='monospace', fontweight=900, color='red', pad=2, loc='center', rotation=75, alpha=0.3)

# Save
chart2.save(outdir + '/axistitles_9_1_ytitle_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='kwargs for xtitle()',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

kwargs = {'text' : 'values',
          'fontsize' : 10, 'font' : 'monospace', 'fontweight' : 900,
          'color' : 'red', 'pad' : 2, 'loc' : 'center', 'rotation' : 75, 'alpha' : 0.3}
chart2.ytitle(**kwargs)

# Save
chart2.save(outdir + '/axistitles_9_2_ytitle_kwargs.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/axistitles.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/axistitles*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
