'''
2026-01-12

Examples of adding text, arrows.

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
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])
cols = df.columns
linecol = cols[0]

# Create a forecast for the next 4 quarters
p = df.index.max() + 3 * pd.offsets.MonthBegin()
lastval = df.loc[df.index.max(), linecol]
dates = pd.date_range(start=p, freq='3MS', end=p + pd.Timedelta(days=600))
for idate, date in enumerate(dates):
    forecast = lastval + 0.5 + np.random.normal(scale=0.3)
    df.loc[date, 'forecast'] = forecast
    df.loc[date, '25%'] = forecast - 1.5 - (0.3 + 0.8 * idate) * np.random.random()
    df.loc[date, '75%'] = forecast + 1.5 + (0.3 + 0.8 * idate) * np.random.random()
    df.loc[date, '10%'] = forecast - 4.5 - (0.3 + 0.5 * idate) * np.random.random()
    df.loc[date, '90%'] = forecast + 4.5 + (0.3 + 0.5 * idate) * np.random.random()

# ---------------------------------------------------------------------------------------------------------
# 1. No options
# ---------------------------------------------------------------------------------------------------------
chart1 = Chart(df, linecols=[linecol, 'forecast'],
               title='No options',
               xrange='2023Q1:', yrange=[-5, 9.5])

# Add hline with hline()
chart1.hline(y=1.4, xrange='2023Q1:' + df.index[-1].strftime('%Y-%m'),
             color=IMFBLACK, linewidth=2.5, linestyle='--', dashes=[10, 4])

text = '''Real GDP growth
long-run average
(1.4 q/q)'''

# Add text with text()
chart1.text(pd.Timestamp('2024Q3'), 6.5, text=text)

# Add fill
chart1.fill('25%', '75%')

# Add arrow with arrow()
chart1.arrow(head=[pd.Timestamp('2025Q1'), 1.5],
             tail=[pd.Timestamp('2025Q1'), 5])
# Save
chart1.save(outdir + '/text_arrow_fill_1_nooptions.pdf')

# ---------------------------------------------------------------------------------------------------------
# 2. With options
# ---------------------------------------------------------------------------------------------------------
attrs = {linecol : {'linewidth' : 4,
                    'color' : '#004C97',
                    # 'linestyle' : '--',
                    'marker' : 'o',
                    'markersize' : 10,
                    'markerfacecolor' : 'white',
                    'markeredgewidth' : 4,
                    'markeredgecolor' : '#004C97'},
         'forecast' : {'marker' : 'x',
                       'markersize' : 12,
                       'linestyle' : '--',
                       'linewidth' : 0.8,
                       'color' : 'red'}
         }

kw_hline = {'y' : 1.4, 'xrange' : '2020Q1:' + df.index[-1].strftime('%Y-%m'),
            'color' : IMFBLACK, 'linewidth' : 2.5, 'linestyle' : '--', 'dashes' : [10, 4]}


text = '''Real GDP growth
long-run average
(1.4 q/q)'''

kw_text = {'x' : pd.Timestamp('2024Q3'), 'y' : 6.5, 'text' : text,
           'fontweight' : 'bold', 'color' : '#004C97'}

kw_arrow = {'head' : [pd.Timestamp('2025Q1'), 1.5],
            'tail' : [pd.Timestamp('2025Q1'), 5],
            'color' : '#004C97'}

chart1 = Chart(df, linecols=[linecol, 'forecast'],
               attrs=attrs,
               topaxis='left',
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

# Add fill
chart1.fill('25%', '75%')

# Add arrow with arrow()
chart1.arrow(head=[pd.Timestamp('2025Q1'), 1.5],
             tail=[pd.Timestamp('2025Q1'), 5],
             color='#004C97')
# Save
chart1.save(outdir + '/text_arrow_fill_2_options.pdf')

# ---------------------------------------------------------------------------------------------------------
# 3. With axes fractions
# ---------------------------------------------------------------------------------------------------------
chart1 = Chart(df, linecols=[linecol, 'forecast'],
               title='axes fraction',
               xrange='2023Q1:', yrange=[-5, 9.5])

# Add hline
chart1.hline(y=1.4, xrange='2023Q1:' + df.index[-1].strftime('%Y-%m'),
             color=IMFGREEN, linewidth=2.5, linestyle='-.', dashes=[10, 4])

# Add fill for two columns in data.
chart1.fill('25%', '75%', color='yellow', alpha=0.3, linecolor='orange', linewidth=1.5, linestyle='--')

# Add text
text = '''Real GDP growth\nlong-run average\n(1.4 q/q)'''
chart1.text(pd.Timestamp('2024Q3'), 6.5, text=text, fontsize=18, fontfamily='cursive', fontweight='bold')

# Add arrow
chart1.arrow(head=[0.60, 0.45], tail=[0.60, 0.65], coords='axes fraction',
             color='pink', edgecolor='red', edgewidth=3,
             width=6, headwidth=7, headlength=20)

# Add arrow
chart1.arrow(head=[0.5, 0.8], tail=[0.9, 0.8], coords='figure fraction',
             color='pink', edgecolor='red',
             edgewidth=3, width=6, headwidth=7, headlength=20)

# Save
# Specify bbox_inches=None and pad_inches=None to not remove any white spacing.
chart1.save(outdir + '/text_arrow_fill_axes_3_fractions.pdf', bbox_inches=None, pad_inches=None)

# ---------------------------------------------------------------------------------------------------------
# 3. Arrow Options
# ---------------------------------------------------------------------------------------------------------
chart1 = Chart(df, linecols=[linecol, 'forecast'],
               title='arrow options',
               xrange='2023Q1:', yrange=[-5, 9.5])

# Add hline
chart1.hline(y=1.4, xrange='2023Q1:' + df.index[-1].strftime('%Y-%m'),
             color=IMFGREEN, linewidth=2.5, linestyle='-.', dashes=[10, 4])

# Add fill for two columns in data.
chart1.fill('25%', '75%', color='yellow', alpha=0.3, linecolor='orange', linewidth=1.5, linestyle='--')

# Add vertical lines at each year
for year in range(2023, 2027+1):
    chart1.vline(x=str(year)+'-01', color='red', alpha=0.7, linestyle='--')

# Add arrow
chart1.arrow(tail=['2023Q1', -4], head=['2024Q1', -4], coords='data')
chart1.text(pd.Timestamp('2023Q1'), -4.5, 'default',
            fontsize=6)
    
# Add arrow
chart1.arrow(tail=['2023Q1', -2], head=['2024Q1', -2], coords='data',
             color='pink', edgecolor='red', edgewidth=1, 
             width=1, headwidth=5, headlength=5, shrink=0)
chart1.text(pd.Timestamp('2023Q1'), -1.5, 'width=1, headwidth=5, headlength=5, shrink=0',
            fontsize=6)

# Add arrow
chart1.arrow(tail=['2024Q1', -2], head=['2025Q1', -2], coords='data',
             color='pink', edgecolor='yellow', edgewidth=1, 
             width=1, headwidth=15, headlength=5, shrink=0.05)
chart1.text(pd.Timestamp('2024Q1'), -2.5, 'width=1, headwidth=15, headlength=5, shrink=0.05',
            fontsize=6)

# Add arrow
chart1.arrow(tail=['2025Q1', -2], head=['2026Q1', -2], coords='data',
             color='pink', edgecolor='green', edgewidth=2,
             width=2, headwidth=5, headlength=15, shrink=0)
chart1.text(pd.Timestamp('2025Q1'), -1.5, 'width=2, headwidth=5, headlength=15, shrink=0',
            fontsize=6)

# Add arrow
chart1.arrow(tail=['2026Q1', -2], head=['2027Q1', -2], coords='data',
             color='blue', edgewidth=0,
             width=5, headwidth=15, headlength=15, shrink=0, zorder=-1)
chart1.text(pd.Timestamp('2026Q1'), -2.5, 'edgewidth=0,\n width=5, headwidth=15, headlength=15, shrink=0',
            fontsize=6)

# Save
chart1.save(outdir + '/text_arrow_fill_axes_4_arrowoptions.pdf')

# ---------------------------------------------------------------------------------------------------------
# 4. Multiple Bands
# ---------------------------------------------------------------------------------------------------------

chart1 = Chart(df, linecols=[linecol, 'forecast'],
               title='Multiple bands',
               xrange='2023Q1:', yrange=[-5, 9.5])

# Add fill for 25-75 percentile
chart1.fill('25%', '75%', color='grey', alpha=0.7)

# Add fill between 10-25 percentile
chart1.fill('10%', '25%', color='grey', alpha=0.3)

# Add fill between 75-90 percentile
chart1.fill('75%', '90%', color='grey', alpha=0.3)

# Save
chart1.save(outdir + '/text_arrow_fill_axes_5_multiple.pdf')

# ---------------------------------------------------------------------------------------------------------
# 5. Dicts as input
# ---------------------------------------------------------------------------------------------------------

kw_hline = {'y' : 1.4, 'xrange' : '2020Q1:' + df.index[-1].strftime('%Y-%m'),
            'color' : IMFBLACK, 'linewidth' : 2.5, 'linestyle' : '--', 'dashes' : [10, 4]}


text = '''Real GDP growth
long-run average
(1.4 q/q)'''

kw_text = {'x' : pd.Timestamp('2024Q3'), 'y' : 6.5, 'text' : text,
           'fontweight' : 'bold', 'color' : '#004C97'}

kw_arrow = {'head' : [pd.Timestamp('2025Q1'), 1.5],
            'tail' : [pd.Timestamp('2025Q1'), 5],
            'color' : '#004C97'}

kw_fills_mid = {'lo' : '25%', 'hi' : '75%',
                'color' : 'grey', 'alpha' : 0.7,
                'label' : r'$1 \sigma$', 'legend' : True}

kw_fills_lo = {'lo' : '10%', 'hi' : '25%',
                'color' : 'grey', 'alpha' : 0.3,
                'label' : r'$2 \sigma$', 'legend' : True}

kw_fills_hi = {'lo' : '75%', 'hi' : '90%',
                'color' : 'grey', 'alpha' : 0.3}

chart1 = Chart(df, linecols=[linecol, 'forecast'],
               hlines=[kw_hline], # Add hline via kwargs
               texts = [kw_text], # Add text via kwargs
               arrows = [kw_arrow], # Add arrow via kwargs
               fills=[kw_fills_mid, kw_fills_lo, kw_fills_hi],
               title='dict inputs',
               xrange='2023Q1:', yrange=[-5, 9.5])

# Save
chart1.save(outdir + '/text_arrow_fill_axes_6_kwargs.pdf')

#==========================================================================================================
# Merge all files
#==========================================================================================================
from PyPDF2 import PdfWriter
mergedfilename = outdir + '/text_arrow_fill.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/text_arrow_fill*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)
