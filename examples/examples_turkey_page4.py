'''
2025-12-10

Examples of running imfcharts.

Data files are created by get_data_turkey_page4.py
and files are stored in data/turkey_page4/.
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

# Create Chart object
attrs = {linecol : {'linewidth' : 4, 'color' : IMFBLACK},
         'Personnel' : {'color' : '#004C97', 'edgecolor' : 'red'},
         'Goods & services' : {'color' : '#009CDE'},
         'Current transfers' : {'color' : '#CAEDFE'},
         'Capital exp.' : {'color' : '#FF8200'},
         'Other' : {'color' : '#DA291C'},                         
         }

chart1 = Chart(df, linecols=linecol, barcols=barcols,
               attrs=attrs,
               topxaxis='left',
               title='Central Government: Primary Expenditure Components',
               subtitle='(Percent of GDP)',
               xrange='2018-01:', yrange=[0, 30],
               ncol_legend=2)

# Add marker for 2023

# Save
chart1.save(outdir + '/page4_chart1_exp.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 4 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page4/fig4_chart2_spending.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Accrual spending' : {'color' : IMFBLUE},
              'Cash spending' : {'color' : 'white', 'offset' : 30,
                                 'hatch' : '\\\\', 'hatchcolor' : IMFBLACK, 'edgecolor' : 'cyan'}
              }

# Create Chart object
chart2 = Chart(df, barcols=df.columns, barstack=False,
               attrs=attrs,
               title='Cash vs. Accrual Earthquake Spending',
               subtitle='(Percent of GDP)',
               yrange=[0, 4],
               legend_left=0.40, ncol_legend=2, legend_width=0.6, legend_bottom=0.80,
               )

# Save
chart2.save(outdir + '/page4_chart2_spending.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 4 Chart 3
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page4/fig4_chart3_revenue.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
linecol = 'Primary revenues'
barcols = list(df.columns)
barcols.remove(linecol)

attrs = {'PIT' : {'color' : '#004C97'},
         'CIT' : {'color' : '#009CDE'},
         'VAT' : {'color' : '#CAEDFE'},
         'SCT' : {'color' : '#BFBFBF'},
         'Non-tax' : {'color' : '#FF8200'},
         'Other' : {'color' : '#DA291C'},
         'Primary revenues' : {'color' : 'black'}}

# Create Chart object
chart3 = Chart(df, linecols=linecol, barcols=barcols,
               title='Central Government: Primary Revenue Components',
               subtitle='(Percent of GDP)',
               attrs=attrs,
               xrange='2018-01:2024-01', yrange=[0, 30],
               ncol_legend=2,
               )

# Save
chart3.save(outdir + '/page4_chart3_revenue.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 4 Chart 4
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page4/fig4_chart4_revenue_expenditure.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'Primary revenue' : {'color' : IMFBLUE},
         'Primary expenditure' : {'color' : IMFRED}
         }

# Create Chart object
chart4 = Chart(df, linecols=df.columns,
               title='Central Government: Primary Revenue/Expenditure',
               subtitle='(Percent, 12-month cumulative growth rate)',
               attrs=attrs,
               xrange='2018-01:', yrange=[5, 145],
               )
# Save
chart4.save(outdir + '/page4_chart4_revenue_expenditure.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 4 Chart 5
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page4/fig4_chart5_fiscal_balance.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

barcol = 'Interest payments, rhs'
linecols = ['Overall balance', 'Primary balance']

attrs = {barcol : {'color' : '#CAEDFE'},
         'Overall balance' : {'color' : '#004C97'},
         'Primary balance' : {'color' : '#DA291C'}}

# Create Chart object
chart5 = Chart(df, linecols=linecols, barcols=barcol, baraxis='right',
               barlinewidth=0,
               attrs=attrs,
               title='Central Government Fiscal Balance',
               subtitle="(Percent of GDP; 12-month cumulative, authorities' definition)",
               xrange='2018-01:', yrange=[-10, 6], ryrange=[0, 5],
               )

# Save
chart5.save(outdir + '/page4_chart5_fiscal_balance.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 4 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page4/fig4_chart6_debt.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

attrs = {'debt' : {'color' : '#004C97'},
              }

# Create Chart object
chart6 = Chart(df, barcols=df.columns,
               barlinewidth=0,
               title='General Government Gross Debt, EU Definition',
               subtitle='(Percent of GDP)',
               attrs=attrs,
               xrange='2018-01:2025-01', yrange=[0, 50],
               )

# Save
chart6.save(outdir + '/page4_chart6_debt.pdf')

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
mergedfilename = outdir + '/all_page4.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/page4*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
