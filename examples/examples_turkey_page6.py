'''
2025-11-15

Examples of running imfcharts.

Data files are created by get_data_turkey_page6.py
and files are stored in data/turkey_page6/.
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
# p. 6 Chart 1
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page6/fig6_chart1_current_account.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
riskcol = 'Risk weighted Assets (RHS)'

dict_attrs = {riskcol : {'color' : IMFBLACK},
              'Capital' : {'color' : IMFBLUE},
              'Core capital' : {'color' : IMFRED}}

chart1 = Chart(df, linecols=['Capital', 'Core capital'], rlinecols=riskcol,
               dict_attrs=dict_attrs,
               title='Bank Capital',
               subtitle='(Percent of risk-weighted assets; RWA y/y percent change)',
               legend_left=0.4,
               xrange='2022-01:', yrange=[10, 25], ryrange=[120, 200])

# Save
chart1.save(outdir + '/page6_chart1_current_account.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 6 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page6/fig6_chart2_current_account_mms.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0]).dropna(how='all', axis=0)

dict_attrs = {'Return to asset' : {'color' : IMFBLUE},
              'Return to equity' : {'color' : IMFRED}}

# Create Chart object
chart2 = Chart(df, barcols='Return to asset', rlinecols='Return to equity', topxaxis='right',
               dict_attrs=dict_attrs,
               title='Bank Profitability 1/',
               subtitle='(Percent, 12M moving average)',
               xrange='2022-01:', yrange=[0, 3], ryrange=[0, 30],
               legend_bottom=0.75, legend_left=0.55)

# Save
chart2.save(outdir + '/page6_chart2_current_account_mms.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 6 Chart 3
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page6/fig6_chart3_non_performing.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
dict_attrs = {'Total NPL' : {'color' : IMFBLUE},
              'Consumer loan NPL' : {'color' : IMFRED},
              'SME loan NPL' : {'color' : IMFBLACK}}
chart3 = Chart(df, linecols=df.columns,
               dict_attrs=dict_attrs,
               title='Non-Performing Loans',
               subtitle='(Percent of respective loan portfolio)',
               xrange='2022-01:', yrange=[0, 6],
               legend_left=0.6)

# Save
chart3.save(outdir + '/page6_chart3_non_performing.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 6 Chart 4
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page6/fig6_chart4_required_reserves.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
dict_attrs = {'Total' : {'color' : IMFBLACK},
              'TL' : {'color' : IMFRED},
              'FX' : {'color' : IMFBLUE}}
chart4 = Chart(df, linecols=df.columns,
               dict_attrs=dict_attrs,
               title='Required Reserves',
               subtitle='(Percent of total bank deposits at CBRT)',
               xrange='2022-01:', yrange=[-0.5, 80],
               legend_left=0.15, legend_bottom=0.15)

# Save
chart4.save(outdir + '/page6_chart4_required_reserves.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 6 Chart 5
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page6/fig6_chart5_fx_position.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
dict_attrs = {'On balance sheet' : {'color' : IMFBLUE},
              'Off balance sheet' : {'color' : IMFRED},
              'Net position' : {'color' : IMFBLACK}}
chart5 = Chart(df, linecols=df.columns,
               dict_attrs=dict_attrs,
               title='Banking Sector Net FX Position',
               subtitle='(Billion of USD)',
               xrange='2022-01:', yrange=[-100, 100])

# Save
chart5.save(outdir + '/page6_chart5_fx_position.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 6 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page6/fig6_chart6_fx_exposure.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
paycol = 'Payables to banks abroad'
sharecol = 'Share of FX loans to NFCs'
dict_attrs = {paycol : {'color' : IMFBLACK},
              sharecol : {'color' : IMFBLUE}}

chart6 = Chart(df, linecols=paycol, barcols=sharecol, baraxis='right',
               dict_attrs=dict_attrs,
               title='Bank FX Exposure 2/',
               subtitle='(Payables in bln USD; share in percent)',
               xrange='2022-01:', yrange=[20, 120], ryrange=[40, 50])

# Save
chart6.save(outdir + '/page6_chart6_fx_exposure.pdf')

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
mergedfilename = outdir + '/all_page6.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/page6*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
