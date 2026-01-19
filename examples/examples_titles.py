'''
2026-01-16

Example of titles, subtitles.

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
chart2.save(outdir + '/titles_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. Add with function
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.title('add with title()')

# Save
chart2.save(outdir + '/titles_2_title.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. Options in Chart()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='options in Chart()',
               titlecolor='red', titlefontsize=10, titlefont='monospace', titlefontweight=900, titleloc='center', titley=0.90,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/titles_3_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. Options in title()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.title('with options title()', color='red', fontsize=10, font='monospace', fontweight=900, loc='center', y=0.90)

# Save
chart2.save(outdir + '/titles_4_title_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

kwargs = {'text' : 'kwargs',
          'color' : 'red', 'fontsize' : 10, 'font' : 'monospace', 'fontweight' : 900,
          'loc' : 'center', 'y' : 0.90}
chart2.title(**kwargs)

# Save
chart2.save(outdir + '/titles_5_title_kwargs.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               subtitle='subtitle no options',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/titles_6_subtitle_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. Add with function
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.subtitle('add with subtitle()')

# Save
chart2.save(outdir + '/titles_7_title.pdf')

# ---------------------------------------------------------------------------------------------------------
# 8. Options in Chart()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               subtitle='options in Chart()',
               subtitlecolor='red', subtitlefontsize=10, subtitlefont='monospace', subtitlefontweight=900, subtitleha='left', subtitleva='top', subtitley=0.90,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/titles_8_option.pdf')

# ---------------------------------------------------------------------------------------------------------
# 9. Options in subtitle()
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

chart2.subtitle('with options subtitle()', color='red', fontsize=10, font='monospace', fontweight=900, ha='left', va='top', y=0.90)

# Save
chart2.save(outdir + '/titles_9_1_subtitle_options.pdf')


# ---------------------------------------------------------------------------------------------------------
# 10. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

kwargs = {'text' : 'kwargs',
          'color' : 'red', 'fontsize' : 10, 'font' : 'monospace', 'fontweight' : 900,
          'ha' : 'left', 'va' : 'top', 'y' : 0.90}
chart2.subtitle(**kwargs)

# Save
chart2.save(outdir + '/titles_9_2_subtitle_kwargs.pdf')


#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/titles.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/titles*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
