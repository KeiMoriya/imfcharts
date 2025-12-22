'''
2025-11-15

Examples of running imfcharts.

Data files are created by get_data_turkey_page3.py
and files are stored in data/turkey_page3/.
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
# p. 3 Chart 1
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page3/fig3_chart1_wage.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
attrs = {'Real Minimum Wage' : {'color' : IMFBLUE}}
chart1 = Chart(df, barcols='Real Minimum Wage',
               attrs=attrs,
               title='Real Minimum Wage',
               subtitle='(Jan 2015=100)',
               show_legend=False,
               xrange='2015-01:', yrange=[0, 250])

# Save
chart1.save(outdir + '/page3_chart1_wage.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 3 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page3/fig3_chart2_labor.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0]).dropna(how='all', axis=0)

attrs = {'Labor cost' : {'color' : IMFBLUE},
         'Earnings' : {'color' : IMFRED, 'linestyle' : '--'}}

# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Real Labor Cost and Earnings Index',
               subtitle='(2015Q1=100)',
               xrange='2015-Q1:', yrange=[80, 240])

# Save
chart2.save(outdir + '/page3_chart2_labor.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 3 Chart 3
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page3/fig3_chart3_unemp.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Total' : {'color' : IMFBLUE},
         'Male' : {'color' : IMFRED},
         'Female' : {'color' : IMFBLACK}}

# Create Chart object
chart3 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Unemployment Rate',
               subtitle='(Percent)Monetary Policy Rate',
               xrange='2015-01:', yrange=[0, 20],
               legend_bottom=0.20)

# Save
chart3.save(outdir + '/page3_chart3_unemp.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 3 Chart 4
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page3/fig3_chart4_participation.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
attrs = {'Total' : {'color' : IMFBLUE},
         'Male' : {'color' : IMFRED},
         'Female' : {'color' : IMFBLACK}}
chart4 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Labor Force Participation Rate',
               subtitle='(Percent)',
               xrange='2015-01:', yrange=[0, 100])

# Save
chart4.save(outdir + '/page3_chart4_participation.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 3 Chart 5
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page3/fig3_chart5_compensation.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
attrs = {'Compensation of employees' : {'color' : IMFBLUE},
         'Operating surplus' : {'color' : IMFRED}}
chart5 = Chart(df, linecols=df.columns,
               attrs=attrs,
               title='Labor Compensation',
               subtitle='(Percent of GDP, 4-quarter moving average)',
               xrange='2015-01:', yrange=[0, 100])

# Save
chart5.save(outdir + '/page3_chart5_compensation.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 3 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page3/fig3_chart6_employment_share.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
attrs = {'SME' : {'color' : IMFBLUE},
         'Large (rhs)' : {'color' : IMFRED}}

chart6 = Chart(df, linecols='SME', rlinecols='Large (rhs)',
               attrs=attrs,
               title='Share of Employment: SME vs. Large Firms',
               subtitle='(Percent)',
               yrange=[50, 80], ryrange=[29, 37])

# Save
chart6.save(outdir + '/page3_chart6_employment_share.pdf')

# ---------------------------------------------------------------------------------------------------------
# Additional commands
# ---------------------------------------------------------------------------------------------------------
# Access figure object
fig = chart2.fig

# Show figure
# chart2.show()

# Add a horizontal line
# chart2.add_hline(3)

# Apply style
# chart.apply(style)

# Show all charts
# plt.show()

# Delete previous merged file
mergedfilename = outdir + '/all_page3.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/page3*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
