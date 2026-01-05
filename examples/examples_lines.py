'''
2026-01-03

Example of lines.

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
chart2.save(outdir + '/lines_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. color cycle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               colorcycle=['red', 'green', 'blue', 'black'],
               title='color cycle',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/lines_2_colorcycle.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. linewidth
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='linewidth',
               linewidth=5,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/lines_3_linewidth.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. linebreaks
# ---------------------------------------------------------------------------------------------------------

_df = df.copy()
_df.loc['2025-07'] = np.nan
# Create Chart object
chart2 = Chart(_df, linecols=df.columns,
               title='linebreaks false',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/lines_4_1_linebreaks_false.pdf')

# Create Chart object
chart2 = Chart(_df, linecols=df.columns,
               title='linebreaks true',
               linebreaks=True,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/lines_4_2_linebreaks_true.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. margins
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='margins',
               margins=60,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/lines_5_margins.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. attrs
# ---------------------------------------------------------------------------------------------------------
attrs = {'Current account' : {'color' : IMFBLUE},
         'Excluding fuel' : {'color' : '#009CDE'},
         'Excluding gold' : {'color' : IMFRED},
         'Excluding fuel & gold' : {'color' : '#BFBFBF'}}

# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               title='attrs',
               attrs=attrs,
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/lines_6_attrs.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart3 = Chart(title='kwargs', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)
kwargs = {'data' : df,
          'cols' : df.columns,
          'attrs' : attrs,
          'xrange' : '2022-01:',
          # 'debug' : True
          }
chart3.lines(**kwargs)
# Save
chart3.save(outdir + '/lines_7_kwargs.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/lines.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted([f for f in glob.glob(outdir + '/lines*.pdf') if f.find('rects') == -1])
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
