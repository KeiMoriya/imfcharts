'''
2025-10-03

Get data for Turkey page 1.
'''

import os
import sys

import numpy as np
import pandas as pd

import imf_datatools
from imf_datatools.dataframe_utilities import *

import imfplotly
objects = []

outdir = 'data/turkey_page1'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

# -----------------------------------------------------
# 1. GDP
# -----------------------------------------------------

dict_series = {'S186NGPC@EMERGEMA' : 'Real GDP growth',
               'S186NCYC@EMERGEMA' : 'Consumption1', # resident household
               'S186NCNC@EMERGEMA' : 'Consumption2', # nonprofit serving household
               'S186NCGC@EMERGEMA' : 'Consumption (public)',
               'S186NFC@EMERGEMA'  : 'Fixed investment',
               'S186NXC@EMERGEMA'  : 'Exports',
               'S186NMC@EMERGEMA'  : 'Imports'}

df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
df['Consumption (private)'] = df['Consumption1'] + df['Consumption2']
df['Net exports'] = df['Exports'] - df['Imports']
df['Inventories/discrepancy'] = df['Real GDP growth'] - df['Consumption (private)'] - df['Consumption (public)'] - df['Fixed investment'] - df['Net exports']

gdpcol = 'Real GDP growth'
barcols = ['Consumption (private)', 'Consumption (public)', 'Net exports', 'Inventories/discrepancy', 'Fixed investment']
df = df[[gdpcol] + barcols].copy()
# Normalize change by previous GDP value
for barcol in barcols:
    df[barcol] = 100. * df[barcol].diff() / df[gdpcol].shift()
# Calculate %pop for GDP
df[gdpcol] = calc_pop(df[gdpcol])

dict_colors = {gdpcol : {'color' : 'blue'},
               'Consumption (private)' : {'color' : 'darkblue'},
               'Consumption (public)' : {'color' : 'green'},
               'Fixed investment' : {'color' : 'lime'},
               'Net exports' : {'color' : 'gray'},
               'Inventories/discrepancy' : {'color' : 'red'}
               }

hline = imfplotly.HLine(y=1.4)
fig = imfplotly.create_fig(df, linecols=gdpcol, barcols=barcols,
                           dict_colors=dict_colors, hlines=[hline],
                           xrange='2023-07:', yrange=[-3, 8])
objects.append(fig)
df.to_csv(outdir + '/fig1_chart1_gdp.csv')

# -----------------------------------------------------
# 2. Labor
# -----------------------------------------------------
col1, col2 = 'Unemployment rate', 'Combined rate of underemployment and unemployment (rhs)'
dict_series = {'S186ELUR@EMERGEMA' : col1,
	       'S186EUDR@EMERGEMA' : col2
               }

df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
dict_colors = {col1 : {'color' : 'blue'},
               col2 : {'color' : 'red'}
               }

fig = imfplotly.create_fig(df, linecols=col1, rlinecols=col2,
                           dict_colors=dict_colors,
                           xrange='2023-01:',
                           yrange=[8, 11], ryrange=[10, 25])
objects.append(fig)
df.to_csv(outdir + '/fig1_chart2_labor.csv')

# -----------------------------------------------------
# 3. Industrial production
# -----------------------------------------------------
col1, col2 = 'Retail sales', 'Industrial Production'
dict_series = {'S186TRSC@EMERGEMA' : col1,
               'S186D@EMERGEMA' : col2
               }
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

df = calc_yoy(df)
        
dict_colors = {col1 : {'color' : 'red'},
               col2 : {'color' : 'blue'}
               }

fig = imfplotly.create_fig(df, linecols=[col1, col2],
                           dict_colors=dict_colors,
                           xrange='2023-01:',
                           yrange=[-10, 40])
objects.append(fig)
df.to_csv(outdir + '/fig1_chart3_ip.csv')

# -----------------------------------------------------
# 4. Consumer Confidence
# -----------------------------------------------------
col1, col2 = 'Consumer Confidence', 'Services Sector'
dict_series = {'S186VCC@EMERGEMA' : col1,
               'S186VSC@EMERGEMA' : col2
               }
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

dict_colors = {col1 : {'color' : 'blue'},
               col2 : {'color' : 'red'}
               }

fig = imfplotly.create_fig(df, linecols=[col1, col2],
                           dict_colors=dict_colors,
                           xrange='2023-01:',
                           yrange=[60, 140])
objects.append(fig)
df.to_csv(outdir + '/fig1_chart4_confidence.csv')

# -----------------------------------------------------
# 5. Trading Partners
# -----------------------------------------------------
col1, col2 = 'US', 'EU'
dict_series = {'PGDPQ@USNA' : col1,
               'J025GDPR@EUNA' : col2
               }
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
df[col2] = 100. * (np.power(1. + df[col2] / 100, 4) - 1)

dict_colors = {col1 : {'color' : 'blue'},
               col2 : {'color' : 'red'}
               }

fig = imfplotly.create_fig(df, linecols=[col1, col2],
                           dict_colors=dict_colors,
                           xrange='2023-01:',
                           yrange=[-1, 5])
objects.append(fig)
df.to_csv(outdir + '/fig1_chart5_partners.csv')

# -----------------------------------------------------
# 6. Trade
# -----------------------------------------------------
col1, col2 = 'Exports', 'Imports'
dict_series = {'N186NX@EMERGEMA' : col1,
               'N186NM@EMERGEMA' : col2,
               'N186NGDP@EMERGEMA' : 'GDP'
               }
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
for col in df.columns:
    if col != 'GDP':
        df[col] = 100. * df[col] / df['GDP']
df.drop('GDP', axis=1, inplace=True)

dict_colors = {col1 : {'color' : 'blue'},
               col2 : {'color' : 'red'}
               }

fig = imfplotly.create_fig(df, linecols=[col1, col2],
                           dict_colors=dict_colors,
                           xrange='2019-01:',
                           yrange=[20, 55])
objects.append(fig)
df.to_csv(outdir + '/fig1_chart6_trade.csv')

# -----------------------------------------------------
# Create HTML
# -----------------------------------------------------
imfplotly.create_html('turkey_page1.html', objects)
