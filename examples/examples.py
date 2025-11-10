'''
2025-10-05

Examples of running imfcharts.

Data files are created by get_data_turkey_page1.py
and files are stored in data/turkey_page1/.
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

# Turn on interactive mode
# plt.ion()
# Clear all existing figures
plt.close('all')

outdir = 'pdf'

# ---------------------------------------------------------------------------------------------------------
# p. 1 Chart 1
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page1/fig1_chart1_gdp.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
cols = df.columns
linecol = cols[0]
barcols = cols[1:]

# Create Chart object
chart1 = Chart(df, linecols=linecol, barcols=barcols,
               dict_attrs={linecol : {'linewidth' : 4,
                                      # 'linestyle' : '--',
                                      'marker' : 'o',
                                      'markersize' : 10,
                                      'markerfacecolor' : 'white',
                                      'markeredgewidth' : 4,
                                      'markeredgecolor' : IMFBLUE}},
               title='Contributions to Real GDP Growth',
               subtitle='(Percent, q/q)',
               xrange='2023Q1:', yrange=[-3, 8],
               ncol_legend=2)
               # debug=True)

# Save
chart1.save(outdir + '/page1_chart1_gdp.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 1 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page1/fig1_chart2_labor.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
chart2 = Chart(df, linecols=df.columns[0], rlinecols=df.columns[1],
               title='Labor Utilization',
               subtitle='(Percent)',
               xrange='2023-01:2025-08', # yrange=[8, 11], ryrange=[10, 25],
               yrange=[8, 11],
               )
               # debug=True)

# Save
chart2.save(outdir + '/page1_chart2_labor.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 1 Chart 3
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page1/fig1_chart3_ip.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
df = df[['Industrial Production', 'Retail sales']]

# Create Chart object
chart3 = Chart(df, linecols=df.columns,
               title='Production Indicators',
               subtitle='(Percent, yoy)',
               legend_left=0.60, legend_width=0.40,
               xrange='2023-01:', yrange=[-10, 40],
               )
               # debug=True)

# Save
chart3.save(outdir + '/page1_chart3_ip.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 1 Chart 4
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page1/fig1_chart4_confidence.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
chart4 = Chart(df, linecols=df.columns,
               title='Economic Confidence Index',
               subtitle='(Seasonally adjusted, 100+=optimistic)',
               ncol_legend=2,
               xrange='2023-01:', yrange=[60, 140],
               ) # debug=True)

# Save
chart4.save(outdir + '/page1_chart4_confidence.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 1 Chart 5
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page1/fig1_chart5_partners.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
chart5 = Chart(df, linecols=df.columns,
               title='Major Trading Partner GDP Growth',
               subtitle='(Percent q/q, SAAR)',
               ncol_legend=2,
               legend_left=0.70, legend_width=0.30,
               xrange='2023-01:', yrange=[-1, 5],
               ) # debug=True)

# Save
chart5.save(outdir + '/page1_chart5_partners.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 1 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page1/fig1_chart6_trade.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
chart6 = Chart(df, linecols=df.columns,
               title='Major Trading Partner GDP Growth',
               subtitle='(Percent q/q, SAAR)',
               xrange='2019Q1:', yrange=[20, 55],
               ) # debug=True)

# Save
chart6.save(outdir + '/page1_chart6_trade.pdf')

# ---------------------------------------------------------------------------------------------------------
# Additional commands
# ---------------------------------------------------------------------------------------------------------
# Access figure object
fig = chart2.fig

# Show figure
# chart2.show()

# Add a horizontal line
chart2.add_hline(3)

# Apply style
# chart.apply(style)

# Show all charts
# plt.show()

# Delete previous merged file
mergedfilename = outdir + '/all.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
