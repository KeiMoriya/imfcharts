'''
2025-11-15

Examples of running imfcharts.

Data files are created by get_data_turkey_page2.py
and files are stored in data/turkey_page2/.
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

# Create Chart object
attrs = {'Inflation' : {'linewidth' : 4, 'color' : IMFBLACK},
         'Goods' : {'linewidth' : 4, 'color' : IMFBLUE, 'linestyle' : 'imfdash'},
         'Services' : {'linewidth' : 4, 'color' : IMFRED, 'linestyle' : 'imfdash'}}

chart1 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Inflation: Goods and Services',
               subtitle='(Y/y percent change)',
               xrange='2017-01:', yrange=[0, 120])

# Save
chart1.save(outdir + '/page2_chart1_inflation.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 2 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page2/fig2_chart2_sequential_inflation.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Sequential inflation' : {'color' : IMFBLUE},
         '3-month moving average' : {'color' : IMFRED, 'linewidth' : 3}}

# Create Chart object
chart2 = Chart(df, barcols='Sequential inflation', linecols='3-month moving average',
               attrs=attrs,
               title='Sequential Inflation',
               subtitle='(M/m percent change)',
               xrange='2017-01:', yrange=[-4, 16])

# Save
chart2.save(outdir + '/page2_chart2_sequential_inflation.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 2 Chart 3
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page2/fig2_chart3_mp.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Policy rate' : {'color' : IMFBLUE},
         'Inflation' : {'color' : IMFRED},
         'Inflation expectation' : {'color' : IMFBLACK}}

# Create Chart object
chart3 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Monetary Policy Rate',
               subtitle='(Percent)',
               xrange='2017-01:', yrange=[0, 90])

# Save
chart3.save(outdir + '/page2_chart3_mp.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 2 Chart 4
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page2/fig2_chart4_inflation_forecast.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Jul-23' : {'linewidth' : 0,
                     'color' : IMFBLACK,
                     # 'linestyle' : '--',
                     'marker' : 'o',
                     'markersize' : 10,
                     'markerfacecolor' : AXISGRAY,
                     'markeredgewidth' : 0,
                     'markeredgecolor' : AXISGRAY},
         'Nov-23' : {'linewidth' : 4,
                     'color' : IMFRED,
                     # 'linestyle' : '--',
                     'marker' : 'o',
                     'markersize' : 10,
                     'markerfacecolor' : IMFRED,
                     'markeredgewidth' : 0,
                     'markeredgecolor' : IMFRED},
         'Feb-24' : {'linewidth' : 0,
                     'color' : '#89A54E',
                     # 'linestyle' : '--',
                     'marker' : '^',
                     'markersize' : 10,
                     'markerfacecolor' : '#89A54E',
                     'markeredgewidth' : 0,
                     'markeredgecolor' : '#89A54E'},
         'May-24' : {'linewidth' : 0,
                     'color' : '#6E548D',
                     # 'linestyle' : '--',
                     'marker' : 'x',
                     'markersize' : 10,
                     'markerfacecolor' : '#6E548D',
                     'markeredgewidth' : 2,
                     'markeredgecolor' : '#6E548D'},
         'Aug-24' : {'linewidth' : 0,
                     'color' : '#3D96AE',
                     # 'linestyle' : '--',
                     'marker' : 'x|',
                     'markersize' : 10,
                     'markerfacecolor' : '#3D96AE',
                     'markeredgewidth' : 2,
                     'markeredgecolor' : '#3D96AE'},
         'Nov-24' : {'linewidth' : 4,
                     'color' : '#FFC000',
                     # 'linestyle' : '--',
                     'marker' : 'o',
                     'markersize' : 10,
                     'markerfacecolor' : '#FFC000',
                     'markeredgewidth' : 0,
                     'markeredgecolor' : '#FFC000'},
         'Feb-25' : {'linewidth' : 0,
                     'color' : IMFBLACK,
                     # 'linestyle' : '--',
                     'marker' : '+',
                     'markersize' : 10,
                     'markerfacecolor' : IMFBLACK,
                     'markeredgewidth' : 2,
                     'markeredgecolor' : IMFBLACK},
         'May-25' : {'linewidth' : 0,
                     'color' : '#FFC000',
                     # 'linestyle' : '--',
                     'marker' : '_',
                     'markersize' : 10,
                     'markerfacecolor' : '#C55A11',
                     'markeredgewidth' : 1,
                     'markeredgecolor' : '#C55A11'},
         'Aug-25' : {'linewidth' : 4,
                     'color' : '#7030A0',
                     # 'linestyle' : '--',
                     'marker' : 's',
                     'markersize' : 10,
                     'markerfacecolor' : '#7030A0',
                     'markeredgewidth' : 0,
                     'markeredgecolor' : '#7030A0'},
}

# Create Chart object
chart4 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title="CBRT's Inflation Forecast",
               subtitle='(Percent, end-year inflation)',
               ncol_legend=2, legend_left=0.45, legend_width=0.40,
               yrange=[0, 70])

# For 2 columns need to add further symbols on top
attrs = {'Jul-23' : {'linewidth' : 0,
                     'color' : IMFBLACK,
                     # 'linestyle' : '--',
                     'marker' : '.',
                     'markersize' : 2,
                     'markerfacecolor' : '#4B8CAD',
                     'markeredgewidth' : 2,
                     'markeredgecolor' : '#4B8CAD'},
         'Aug-24' : {'linewidth' : 0,
                     'color' : '#3D96AE',
                     # 'linestyle' : '--',
                     'marker' : '|',
                     'markersize' : 10,
                     'markerfacecolor' : '#3D96AE',
                     'markeredgewidth' : 2,
                     'markeredgecolor' : '#3D96AE'},
}

# chart4.lines(df, ['Jul-23', 'Aug-24'],
#              attrs=attrs)

# Save
chart4.save(outdir + '/page2_chart4_inflation_forecast.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 2 Chart 5
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page2/fig2_chart5_inflation_expectations.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
attrs = {'Market participants' : {'color' : IMFBLUE},
         'Real sector' : {'color' : IMFRED},
         'Households' : {'color' : IMFBLACK}}

# Create Chart object
chart5 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Inflation Expectations by Sector',
               subtitle='(Percent, 12-month ahead annual inflation)Major Trading Partner GDP Growth',
               xrange='2017-01:', yrange=[0, 100])

# Save
chart5.save(outdir + '/page2_chart5_inflation_expectations.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 2 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page2/fig2_chart6_credit.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'4-week moving average' : {'color' : IMFBLUE},
         '13-week moving average' : {'color' : IMFRED}}

# Create Chart object
chart6 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Total Credit Growth',
               subtitle='(Percent, m/m)',
               xrange='2024-01:', yrange=[0, 7])

# Save
chart6.save(outdir + '/page2_chart6_credit.pdf')

# ---------------------------------------------------------------------------------------------------------
# Additional commands
# ---------------------------------------------------------------------------------------------------------
# Access figure object
fig = chart2.fig

# Show figure
# chart2.show()

# Add a horizontal line
# chart2.hline(3)

# Apply style
# chart.apply(style)

# Show all charts
# plt.show()

# Delete previous merged file
mergedfilename = outdir + '/all_page2.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/page2*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
