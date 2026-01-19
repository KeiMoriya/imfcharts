'''
2026-01-05

Example of bars

Data files are created by get_data_turkey_page4.py
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
# p. 4 Chart 1
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page4/fig4_chart1_exp.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
cols = df.columns
linecol = 'Primary exp.'
barcols = list(df.columns)
barcols.remove(linecol)

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               title='no options',
               xrange='2018-01:', # yrange=[0, 30],
               ncol_legend=2)

# Save
chart1.save(outdir + '/bars_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. color cycle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               colorcycle=['red', 'green', 'blue', 'black'],
               title='color cycle',
               xrange='2018-01:', yrange=[0, 30],
               ncol_legend=2)

# Save
chart1.save(outdir + '/bars_2_colorcycle.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. axis right
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               title='axis right',
               baraxis='right',
               xrange='2018-01:', yrange=[0, 30],
               ncol_legend=2)

# Save
chart1.save(outdir + '/bars_3_right.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. baredgecolor
# ---------------------------------------------------------------------------------------------------------

# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               baredgecolor='gold',
               title='baredgecolor',
               xrange='2018-01:', yrange=[0, 30],
               ncol_legend=2)

# Save
chart1.save(outdir + '/bars_4_baredgecolor.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. margins
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               title='margins',
               margins=120,
               xrange='2018-01:', yrange=[0, 30],
               ncol_legend=2)

# Save
chart1.save(outdir + '/bars_5_margins.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. attrs
# ---------------------------------------------------------------------------------------------------------
attrs = {linecol : {'linewidth' : 4, 'color' : IMFBLACK},
         'Personnel' : {'color' : '#004C97', 'baredgecolor' : 'red'},
         'Goods & services' : {'color' : '#009CDE'},
         'Current transfers' : {'color' : '#CAEDFE'},
         'Capital exp.' : {'color' : '#FF8200'},
         'Other' : {'color' : '#DA291C'},                         
         }

# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               title='attrs',
               attrs=attrs,
               xrange='2018-01:', yrange=[0, 30],
               ncol_legend=2)

# Save
chart1.save(outdir + '/bars_6_attrs.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart3 = Chart(title='kwargs', yrange=[0, 30],
               ncol_legend=2)
kwargs = {'data' : df,
          'cols' : barcols,
          'attrs' : attrs,
          'xrange' : '2018-01:',
          # 'debug' : True
          }
chart3.bars(**kwargs)

kwargs = {'cols' : linecol,
          'attrs' : {linecol : {'color' : 'black',
                                'linewidth' : 4}}
          }
chart3.lines(**kwargs)
# Save
chart3.save(outdir + '/bars_7_kwargs.pdf')

# Switch kwargs to be for area
chart3 = Chart(title='kwargs for area', yrange=[0, 30],
               ncol_legend=2)
kwargs = {'data' : df,
          'cols' : barcols,
          'attrs' : attrs,
          'xrange' : '2018-01:',
          # 'debug' : True
          }
chart3.area(**kwargs)

kwargs = {'cols' : linecol,
          'attrs' : {linecol : {'color' : 'black',
                                'linewidth' : 4}}
          }
chart3.lines(**kwargs)
# Save
chart3.save(outdir + '/bars_7_kwargs_switch_to_bars.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/bars.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted([f for f in glob.glob(outdir + '/bars*.pdf') if f.find('rects') == -1])
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
