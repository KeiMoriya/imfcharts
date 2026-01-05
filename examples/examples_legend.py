'''
2026-01-05

Example of legends.

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
chart2.save(outdir + '/legends_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. ncol_legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='ncol_legend = 3',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0, legend_left=0, legend_width=0.90, ncol_legend=3)

# Save
chart2.save(outdir + '/legends_2_colorcycle.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. show_legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='show_legend = False',
               xrange='2022-01:', yrange=[-95, 60],
               show_legend=False,
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/legends_3_show_legend_false.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. set_legend
# ---------------------------------------------------------------------------------------------------------

# Create Chart object
# Draw with legend, then remove
chart2 = Chart(df, linecols=df.columns,
               title='set_legend = False',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)
# Set legend off
chart2.set_legend(show=False)

# Save
chart2.save(outdir + '/legends_4_1_set_legend_false.pdf')

# Set legend on
chart2.set_legend(show=True)
chart2.set_title('set_legend = True')

# Save
chart2.save(outdir + '/legends_4_2_legend_true.pdf')



# Draw without legend, then turn on
chart2 = Chart(df, linecols=df.columns,
               title='set_legend = False',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55,
               show_legend=False)
# Set legend on
chart2.set_legend(show=True)
chart2.set_title('set_legend = True from no legend')

# Save
chart2.save(outdir + '/legends_4_3_legend_true2.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. fontsize
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='fontsize',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55,
               legend_fontsize=18)

# Save
chart2.save(outdir + '/legends_5_fontsize.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. legend header
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='legend header',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55,
               legend_header='This is the legend header')

# Save
chart2.save(outdir + '/legends_6_attrs.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. legend spacing
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='legend_spacing=1',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55,
               legend_spacing=1)

# Save
chart2.save(outdir + '/legends_7_legend_spacing.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/legends.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/legends*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
