'''
2025-11-15

Examples of running imfcharts.

Data files are created by get_data_turkey_page5.py
and files are stored in data/turkey_page5/.
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
# p. 5 Chart 1
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart1_current_account.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
linecol = 'Current Account Balance'
attrs = {linecol : {'color' : IMFBLACK},
         'Other' : {'color' : '#009CDE'},
         'Energy Balance' : {'color' : '#004C97'},
         'Tourism & Transport' : {'color' : '#CAEDFE',
                                  #                                       'barcolors' : [{'2023Q3' : 'gold'},
                                  #                                                      {'2022Q3' : 'silver'}]
                                  },
         'Gold' : {'color' : IMFRED,
                   #                        'barcolors' : [{'2023Q3' : 'orange'},
                   #                                       {'2022Q3' : 'green'}]
                   }
         }
barcols = ['Other', 'Energy Balance', 'Tourism & Transport', 'Gold']
chart1 = Chart(df, linecols=linecol, barcols=barcols, # baraxis='right',
               attrs=attrs,
               title='Current Account',
               subtitle='(Percent of GDP)',
               legend_bottom=0.20, legend_left=0.55,
               xrange='2022-Q1:', yrange=[-30, 25], # ryrange=[-30, 25],
               ) # debug=True

# Save
chart1.save(outdir + '/page5_chart1_current_account.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 5 Chart 2
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart2_current_account_mms.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0]).dropna(how='all', axis=0)

attrs = {'Current account' : {'color' : IMFBLUE},
         'Excluding fuel' : {'color' : '#009CDE'},
         'Excluding gold' : {'color' : IMFRED},
         'Excluding fuel & gold' : {'color' : '#BFBFBF'}}

# Create Chart object
chart2 = Chart(df, linecols=df.columns,
               barlinewidth=0,
               attrs=attrs,
               title='Current Account',
               subtitle='(Billions USD, 12mms)',
               xrange='2022-01:', yrange=[-95, 60],
               legend_bottom=0.22, legend_left=0.55)

# Save
chart2.save(outdir + '/page5_chart2_current_account_mms.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 5 Chart 3
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart3_terms_of_trade.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0)

# Add further unstacked columns
# df['shock2'] = df['shock'] / 2.
# df['shock3'] = df['shock'] * 2.

# # Add duplicate index
# idx = list(df.index)
# idx += ['COL']
# df = df.reindex(idx)
# # Reset last value
# df.iloc[-1].values[0] = 10

attrs = {'shock' : {'color' : '#BFBFBF',
                    'barcolors' : [{'TUR' : 'red'},
                                   #                                        {'KOR' : 'blue'},
                                   #                                        {'THA' : (0, 0.8, 0.8, 0.3)},
                                   #                                        {'COL' : 'gold'}
                                   ]}
}

# Create Chart object
chart3 = Chart(df, barcols=df.columns, barstack=False, # baraxis='right',
               attrs=attrs,
               barlinewidth=0, xtickangle=90, xticklength=0,
               title='Terms of Trade Shock, 2025Q2 or Latest',
               subtitle='(Percent change from 2023 average)',
               yrange=[-15, 15],
               legend=False) # , debug=True

# Save
chart3.save(outdir + '/page5_chart3_terms_of_trade.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 5 Chart 4
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart4_current_account_financing.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
attrs = {'Current Account Balance' : {'color' : IMFBLACK},
         'Portfolio' : {'color' : IMFRED},
         'Reserves (+ = drawdown)' : {'color' : IMFGREY},
         'Other Inv. & FDI' : {'color' : '#009CDE'},
         'E&O' : {'color' : '#004C97'}}

chart4 = Chart(df, linecols='Current Account Balance',
               barcols=['Portfolio', 'Reserves (+ = drawdown)',
                        'Other Inv. & FDI', 'E&O'],
               attrs=attrs,
               title='Current Account Financing',
               subtitle='(Percent of GDP)',
               xrange='2022-Q1:', yrange=[-10, 20],
               ncol_legend=2, legend_width=0.80)

# Save
chart4.save(outdir + '/page5_chart4_participation.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 5 Chart 5
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart5_financial_account.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
attrs = {'Other investment' : {'color' : '#009CDE'},
         'Direct investment' : {'color' : '#CAEDFE'},
         'Portfolio investment' : {'color' : '#004C97'},
         'Financial account' : {'color' : '#BFBFBF'}}
chart5 = Chart(df, linecols='Financial account',
               barcols=['Other investment', 'Direct investment', 'Portfolio investment'],
               attrs=attrs,
               title='Financial Account 2/',
               subtitle='(Billions USD, 3mma, NSA)',
               xrange='2022-01:', yrange=[-8, 12])

# Save
chart5.save(outdir + '/page5_chart5_compensation.pdf')

# ---------------------------------------------------------------------------------------------------------
# p. 5 Chart 6
# ---------------------------------------------------------------------------------------------------------
# Read in data
infilename = 'data/turkey_page5/fig5_chart6_gross_international_reserves.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
gircol = 'Gross International Reserves (GIR) (rhs)'
bankcol = 'GIR, net of liabilities to banks'
corecol = 'Core NIR (rhs)'
attrs = {gircol : {'color' : '#416FA6'},
         bankcol : {'color' : '#004C97', 'linewidth' : 4, 'linestyle' : 'imfround'},
         corecol : {'color' : '#DA291C'},
         'Gold' : {'color' : '#CAEDFE'},
         'FX' : {'color' : '#009CDE'}}

chart6 = Chart(df, linecols=[bankcol, gircol], rlinecols=corecol, barcols=['FX', 'Gold'],
               barlinewidth=0,
               linebreaks=False,
               attrs=attrs,
               topaxis='right',
               title='Gross International Reserves',
               subtitle='(Billions USD)',
               xrange='2022-01:', yrange=[0, 200], ryrange=[-120, 40])

# Save
chart6.save(outdir + '/page5_chart6_gross_international_reserves.pdf')

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
mergedfilename = outdir + '/all_page5.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/page5*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
