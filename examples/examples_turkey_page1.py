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
# set_style('fund-guide')

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

attrs = {linecol : {'linewidth' : 4,
                    'color' : '#004C97',
                    # 'linestyle' : '--',
                    'marker' : 'o',
                    'markersize' : 10,
                    'markerfacecolor' : 'white',
                    'markeredgewidth' : 4,
                    'markeredgecolor' : '#004C97'},
         'Consumption (private)' : {'color' : '#4B8CAD', 'hatchcolor' : IMFBLUE, 'hatch' : '\\\\'},
         'Consumption (public)' : {'color' : 'white', 'hatch' : '\\\\\\', 'hatchcolor' : IMFBLACK},
         'Net exports' : {'color' : IMFGREY},
         'Inventories/discrepancy' : {'color' : IMFRED},
         'Fixed investment' : {'color' : 'white',
                               'hatch' : '///',
                               'hatchcolor' : IMFGREEN,
                               'hatchwidth' : 10}
         }

kw_hline = {'y' : 1.4, 'xrange' : '2023Q1:' + df.index[-1].strftime('%Y-%m'),
            'color' : IMFBLACK, 'linewidth' : 2.5, 'linestyle' : '--', 'dashes' : [10, 4]}


text = '''Real GDP growth
long-run average
(1.4 q/q)'''

kw_text = {'x' : pd.Timestamp('2024Q3'), 'y' : 6.5, 'text' : text,
           'fontweight' : 'bold', 'color' : '#004C97'}

kw_arrow = {'head' : [pd.Timestamp('2025Q1'), 1.5],
            'tail' : [pd.Timestamp('2025Q1'), 5],
            'color' : '#004C97'}

chart1 = Chart(df, linecols=linecol, barcols=barcols,
               attrs=attrs,
               topxaxis='left',
               title='Contributions to Real GDP Growth',
               subtitle='(Percent, q/q)',
               xrange='2023Q1:', yrange=[-5, 9.5], ryrange=[-5, 9.5],
               hlines=[kw_hline], # Add hline via kwargs
               texts = [kw_text], # Add text via kwargs
               arrows = [kw_arrow], # Add arrow via kwargs
               ncol_legend=2)

# Add hline with hline()
# chart1.hline(y=1.4, xrange='2023Q1:' + df.index[-1].strftime('%Y-%m'),
#              # xrange=[0.05, 0.95], coordinates='axis',
#              color=IMFBLACK, linewidth=2.5, linestyle='--', dashes=[10, 4])

# Add text with text()
# chart1.text(pd.Timestamp('2024Q3'), 6.5, text=text, fontweight='bold', color='#004C97')

# Add arrow with arrow()
chart1.arrow(head=[pd.Timestamp('2025Q1'), 1.5],
             tail=[pd.Timestamp('2025Q1'), 5],
             color='#004C97')
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
# chart2.hline(3)

# Apply style
# chart.apply(style)

# Show all charts
# plt.show()

# Delete previous merged file
mergedfilename = outdir + '/all_page1.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/page1*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
