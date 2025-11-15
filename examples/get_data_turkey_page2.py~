'''
2025-11-08

Get data for Turkey page 2.
'''

import os
import sys

import numpy as np
import pandas as pd

import imf_datatools
from imf_datatools.dataframe_utilities import *

import imfplotly
objects = []

outdir = 'data/turkey_page2'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

# -----------------------------------------------------
# 1. Inflation
# -----------------------------------------------------

dict_series = {'N186PC@EMERGEMA' : 'Inflation',
	       'N186PCI@EMERGEMA' : 'Goods',
	       'N186PCS@EMERGEMA' : 'Services'}

df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

# Apply yoy
df = calc_yoy(df)
        
fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2017-01:')
objects.append(fig)
df.to_csv(outdir + '/fig2_chart1_inflation.csv')

# -----------------------------------------------------
# 2. Sequential Inflation
# -----------------------------------------------------
dict_series = {'N186PCI@EMERGEMA' : 'Inflation'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

# Make copy
df2 = df.copy()
df2.columns = ['3-month moving average']

# Calculate pop
df = calc_pop(df)
df.columns = ['Sequential inflation']

# Calculate 3-month moving average
df2 = 100 * (calc_pow(df2 / df2.shift(3), 1./3.) - 1.)
df = df.merge(df2, left_index=True, right_index=True, how='outer')

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2017-01:')
objects.append(fig)
df.to_csv(outdir + '/fig2_chart2_sequential_inflation.csv')

# -----------------------------------------------------
# 3. Moneetary Policy Rate
# -----------------------------------------------------
dict_series = {'N186RTAR@EMERGEMA' : 'Policy rate',
               'N186PC@EMERGEMA' : 'Inflation',
               'N186VEAI@EMERGEMA' : 'Inflation expectation'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
# Apply yoy to inflation
df['Inflation'] = calc_yoy(df['Inflation'])

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2017-01:')
objects.append(fig)
df.to_csv(outdir + '/fig2_chart3_mp.csv')

# -----------------------------------------------------
# 4. CBRT's Inflation Forecast
# -----------------------------------------------------

# Hardcoded data, not available in Haver, DMXe, or website.
infilename = 'Figure 2 Codes.xlsx'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
sheetname = 'C4.Hardcoded'
df = pd.read_excel(infilename, sheet_name=sheetname, index_col=0, parse_dates=[0]).T
df.columns = [c.strftime('%b-%y') for c in df.columns]

fig = imfplotly.create_fig(df, linecols=df.columns)
objects.append(fig)
df.to_csv(outdir + '/fig2_chart4_inflation_forecast.csv')

# -----------------------------------------------------
# 5. Inflation Expectations by Sector
# -----------------------------------------------------
dict_series = {'N186VEAI@EMERGEMA' : 'Market participants',
               'N186VERI@EMERGEMA' : 'Real sector',
               'N186VEHI@EMERGEMA' : 'Households'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2017-01:')
objects.append(fig)
df.to_csv(outdir + '/fig2_chart5_inflation_expectations.csv')

# -----------------------------------------------------
# 6. Total Credit Growth
# -----------------------------------------------------

# Data from website. Column E and F are the chart data. 
infilename = 'Figure 2 Codes.xlsx'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
sheetname = 'C6. Website data'
df = pd.read_excel(infilename, sheet_name=sheetname, index_col=0, parse_dates=[0])
cols = ['4-week moving average', '13-week moving average']
df = df[cols]

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2024-01:')
objects.append(fig)
df.to_csv(outdir + '/fig2_chart6_credit.csv')

# -----------------------------------------------------
# Create HTML
# -----------------------------------------------------
imfplotly.create_html('turkey_page2.html', objects)
