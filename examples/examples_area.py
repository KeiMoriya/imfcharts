'''
2026-01-02

Examples of adding area.

Data files are created by get_data_turkey_page5.py
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
# p. 5 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart6_gross_international_reserves.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
df.dropna(axis=0, how='all', inplace=True)

# Create Chart object
gircol = 'Gross International Reserves (GIR) (rhs)'
bankcol = 'GIR, net of liabilities to banks'
corecol = 'Core NIR (rhs)'
attrs = {gircol : {'color' : '#416FA6'},
         bankcol : {'color' : '#004C97', 'linewidth' : 4, 'linestyle' : 'imfround'},
         corecol : {'color' : '#DA291C'},
         'Gold' : {'color' : '#CAEDFE'},
         'FX' : {'color' : '#009CDE'}}
#==========================================================================================================
# fill
#==========================================================================================================

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol, areacols=['FX', 'Gold'],
               title='no options',
               xrange='2022-01:', yrange=[0, 200], ryrange=[-120, 60])

# Save
chart6.save(outdir + '/area_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. Right axis
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart6 = Chart(df, rlinecols=[bankcol, gircol], linecols=corecol,
               areacols=['FX', 'Gold'], areaaxis='right',
               title='right y-axis',
               xrange='2022-01:', ryrange=[0, 200], yrange=[-120, 60])

# Save
chart6.save(outdir + '/area_2_right.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. colorcycle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol,
               areacols=['FX', 'Gold'],
               colorcycle=['red', 'blue', 'green', 'purple', 'brown', 'black'],
               title='color cycle',
               xrange='2022-01:', yrange=[0, 200], ryrange=[-120, 60])

# Save
chart6.save(outdir + '/area_3_colorcycle.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. no stack
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol,
               areacols=['FX', 'Gold'],
               areastack=False, attrs = {'FX' : {'alpha' : 0.3}, 'Gold' : {'alpha' : 0.3}},
               title='no stack',
               xrange='2022-01:', yrange=[0, 200], ryrange=[-120, 60])

# Save
chart6.save(outdir + '/area_4_nostack.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. area edge color
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol,
               areacols=['FX', 'Gold'], areaedgecolor='purple', arealinewidth=3,
               title='edge color',
               xrange='2022-01:', yrange=[0, 200], ryrange=[-120, 60])

# Save
chart6.save(outdir + '/area_5_edgecolor.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. hatches
# ---------------------------------------------------------------------------------------------------------
attrs = {'FX' : {'color' : 'yellow',
                 'hatchcolor' : 'red',
                 'hatch' : '////',
                 'hatchwidth' : 3,
                 'edgecolor' : 'purple'},
         'Gold' : {'color' : 'grey',
                   'hatch' : 'blue',
                   'hatch' : '\\\\',
                   'hatchwidth' : 2,
                   'edgecolor' : 'brown',
                   'alpha' : 0.3}
         }
# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol,
               areacols=['FX', 'Gold'],
               attrs=attrs,
               topxaxis='right',
               title='hatches',
               xrange='2022-01:', yrange=[-0.5, 200], ryrange=[-120, 60])

# Save
chart6.save(outdir + '/area_6_hatches.pdf')

# ---------------------------------------------------------------------------------------------------------
# 7. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol,
               topxaxis='right',
               title='kwargs',
               xrange='2022-01:', yrange=[-0.5, 200], ryrange=[-120, 60])

kwargs = {'data' : df,
          'cols' : ['FX', 'Gold'],
          'alpha' : 0.3,
          'linewidth' : 3,
          'edgecolor' : 'pink',
          'attrs' : attrs,
          'xrange' : '2022-01:',
          # 'debug' : True
          }
chart6.area(**kwargs)

# Save
chart6.save(outdir + '/area_7_kwargs.pdf')

# ---------------------------------------------------------------------------------------------------------
# 8. legend
# ---------------------------------------------------------------------------------------------------------
attrs = {'FX' : {'color' : 'yellow',
                 'hatchcolor' : 'red',
                 'hatch' : '////',
                 'hatchwidth' : 3,
                 'edgecolor' : 'purple',
                 'legend' : False},
         'Gold' : {'color' : 'grey',
                   'hatch' : 'blue',
                   'hatch' : '\\\\',
                   'hatchwidth' : 2,
                   'edgecolor' : 'brown',
                   'alpha' : 0.3}
         }

# Create Chart object
chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol,
               areacols=['FX', 'Gold'],
               attrs=attrs,
               topxaxis='right',
               title='legend False',
               xrange='2022-01:', yrange=[-0.5, 200], ryrange=[-120, 60])

# Save
chart6.save(outdir + '/area_8_legend.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/area.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/*area*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
