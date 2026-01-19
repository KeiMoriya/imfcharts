'''
2025-12-27

Examples of adding lines and rects.

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

#==========================================================================================================
# hrect
#==========================================================================================================

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hline no options',
               xrange='2017-01:', yrange=[0, 120])

# Add hline
chart1.hline(y=20)

# Save
chart1.save(outdir + '/hlines_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. xrange
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hline xrange',
               xrange='2017-01:', yrange=[0, 120])

# Add hline
chart1.hline(y=20, xrange='2020-03:2025-04')

# Save
chart1.save(outdir + '/hlines_2_xrange.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. color, linewidth, linecolor, linestyle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hline attrs',
               xrange='2017-01:', yrange=[0, 120])

# Add hline
chart1.hline(y=20, xrange='2020-03:2025-04',
             color='blue', linewidth=1.5, linestyle='--', alpha=0.3)

# Save
chart1.save(outdir + '/hlines_3_line_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. zorder
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hline zorder',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.hline(y=20, xrange='2020-03:2025-04',
             zorder=3) # , dashes=[10, 4]

# Save
chart1.save(outdir + '/hlines_4_zorder.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hline legend',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.hline(y=20, xrange='2020-03:2025-04',
             label='horizontal line', legend=True,
             color='grey', linewidth=0.5, linestyle='--', alpha=0.2)

# Save
chart1.save(outdir + '/hlines_5_legend.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hline kwargs',
               xrange='2017-01:', yrange=[0, 120])

# Add hline
kwargs = {'y' : 20, 'xrange' : '2020-03:2025-04',
          'label' : 'horizontal line', 'legend' : True,
          'color' : 'grey', 'linewidth' : 0.5, 'linestyle' : '--', 'alpha' : 0.2}
chart1.hline(**kwargs)

# Save
chart1.save(outdir + '/hlines_6_kwargs.pdf')

#==========================================================================================================
# vline
#==========================================================================================================

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vline no options',
               xrange='2017-01:', yrange=[0, 120])

# Add vline
chart1.vline(x='2020-03')

# Save
chart1.save(outdir + '/vlines_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. xrange
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vline xrange',
               xrange='2017-01:', yrange=[0, 120])

# Add vline
chart1.vline(x='2020-03', yrange=[30, 60])

# Save
chart1.save(outdir + '/vlines_2_xrange.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. color, linewidth, linecolor, linestyle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vline attrs',
               xrange='2017-01:', yrange=[0, 120])

# Add vline
chart1.vline(x='2020-03', yrange=[30, 60],
             color='blue', linewidth=1.5, linestyle='--', alpha=0.3)

# Save
chart1.save(outdir + '/vlines_3_line_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. zorder
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vline zorder',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vline(x='2020-03',
             zorder=3) # , dashes=[10, 4]

# Save
chart1.save(outdir + '/vlines_4_zorder.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vline legend',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vline(x='2020-03', yrange=[30, 60],
             label='vertical line', legend=True,
             color='grey', linewidth=2.5, linestyle='--', alpha=0.7)

# Save
chart1.save(outdir + '/vlines_5_legend.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vline kwargs',
               xrange='2017-01:', yrange=[0, 120])

# Add vline
kwargs = {'x' : '2020-03', 'yrange' : [30, 60],
          'label' : 'vertical line', 'legend' : True,
          'color' : 'grey', 'linewidth' : 2.5, 'linestyle' : '--', 'alpha' : 0.7}
chart1.vline(**kwargs)

# Save
chart1.save(outdir + '/vlines_6_kwargs.pdf')

#==========================================================================================================
# hrect
#==========================================================================================================

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hrect no options',
               xrange='2017-01:', yrange=[0, 120])

# Add hrect
chart1.hrect(ymin=20, ymax=100)

# Save
chart1.save(outdir + '/hrects_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. xrange
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hrect xrange',
               xrange='2017-01:', yrange=[0, 120])

# Add hrect
chart1.hrect(ymin=20, ymax=100, xrange='2020-03:2025-04')

# Save
chart1.save(outdir + '/hrects_2_xrange.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. color, linewidth, linecolor, linestyle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hrect attrs',
               xrange='2017-01:', yrange=[0, 120])

# Add hrect
chart1.hrect(ymin=20, ymax=100, xrange='2020-03:2025-04',
             hatch='//',
             color='blue', linewidth=1.5, linecolor='red', linestyle='--', alpha=0.3)

# Save
chart1.save(outdir + '/hrects_3_line_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. zorder
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hrect zorder',
               xrange='2017-01:', yrange=[0, 120])

# Add hrect
chart1.hrect(ymin=20, ymax=100, xrange='2020-03:2025-04',
             hatch='++',
             color='grey', linewidth=0.5, linecolor='black', linestyle='--', alpha=0.9,
             zorder=3) # , dashes=[10, 4]

# Save
chart1.save(outdir + '/hrects_4_zorder.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hrect legend',
               xrange='2017-01:', yrange=[0, 120])

# Add hrect
chart1.hrect(ymin=20, ymax=100, xrange='2020-03:2025-04',
             hatch='++',
             label='horizontal rectangle', legend=True,
             color='grey', linewidth=0.5, linecolor='black', linestyle='--', alpha=0.2)

# Save
chart1.save(outdir + '/hrects_5_legend.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='hrect kwargs',
               xrange='2017-01:', yrange=[0, 120])

# Add hrect
kwargs = {'ymin' : 20, 'ymax' : 100, 'yrange' : '2020-03:2025-04',
          'hatch' : '++',
          'label' : 'horizontal rectangle', 'legend' : True,
          'color' : 'grey', 'linewidth' : 0.5, 'linestyle' : '--', 'alpha' : 0.2}
chart1.hrect(**kwargs)

# Save
chart1.save(outdir + '/hrects_6_kwargs.pdf')

#==========================================================================================================
# vrect
#==========================================================================================================

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vrect no options',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vrect(xmin='2019-06', xmax='2024-02')

# Save
chart1.save(outdir + '/vrects_1_no_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. xrange
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vrect xrange',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vrect(xmin='2019-06', xmax='2024-02', yrange=[30, 90])

# Save
chart1.save(outdir + '/vrects_2_xrange.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. color, linewidth, linecolor, linestyle
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vrect attrs',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vrect(xmin='2019-06', xmax='2024-02', yrange=[30, 90],
             hatch='//',
             color='blue', linewidth=1.5, linecolor='red', linestyle='--', alpha=0.3)

# Save
chart1.save(outdir + '/vrects_3_line_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. zorder
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vrect zorder',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vrect(xmin='2019-06', xmax='2024-02', yrange=[30, 90],
             hatch='++',
             color='grey', linewidth=0.5, linecolor='black', linestyle='--', alpha=0.9,
             zorder=3) # , dashes=[10, 4]

# Save
chart1.save(outdir + '/vrects_4_zorder.pdf')


# ---------------------------------------------------------------------------------------------------------
# 5. legend
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vrect legend',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
chart1.vrect(xmin='2019-06', xmax='2024-02', yrange=[30, 90],
             hatch='++',
             color='grey', linewidth=0.5, linecolor='black', linestyle='--', alpha=0.2,
             label='vertical rectangle', legend=True)

# Save
chart1.save(outdir + '/vrects_5_legend.pdf')

# ---------------------------------------------------------------------------------------------------------
# 6. kwargs
# ---------------------------------------------------------------------------------------------------------
# Create Chart object
chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='vrect kwargs',
               xrange='2017-01:', yrange=[0, 120])

# Add vrect
kwargs = {'xmin' : '2019-06', 'xmax' : '2024-02', 'yrange' : [30, 90],
          'hatch' : '++',
          'label' : 'vertical rectangle', 'legend' : True,
          'color' : 'grey', 'linewidth' : 0.5, 'linestyle' : '--', 'alpha' : 0.2}
chart1.vrect(**kwargs)

# Save
chart1.save(outdir + '/vrects_6_kwargs.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/lines_rects.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)
    
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/*rects*.pdf') + glob.glob(outdir + '/*hlines*.pdf') + glob.glob(outdir + '/*vlines*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
