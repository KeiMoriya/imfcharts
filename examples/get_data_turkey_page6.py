'''
2025-11-15

Get data for Turkey page 6.
'''

import os
import sys

import numpy as np
import pandas as pd

import imf_datatools
from imf_datatools.dataframe_utilities import *

import imfplotly
objects = []

outdir = 'data/turkey_page6'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

# -----------------------------------------------------
# 1. Bank Capital
# -----------------------------------------------------
riskcol = 'Risk weighted Assets (RHS)'
dict_series = {'N186ZCR@EMERGEMA' : 'Capital',
               'N186ZCC@EMERGEMA' : 'Core capital',
               'N186ZRW@EMERGEMA' : riskcol}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
for col in ['Capital', 'Core capital']:
    df[col] = df[col] / df[riskcol] * 100
df[riskcol] = df[riskcol] / df[riskcol].shift(12) * 100
        
fig = imfplotly.create_fig(df, linecols=df.columns[:2], rlinecols=riskcol,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig6_chart1_current_account.csv')

# -----------------------------------------------------
# 2. Bank Profitability
# -----------------------------------------------------
dict_series = {'N186FPAP@EMERGEMA' : 'Return to asset',
               'N186FNIE@EMERGEMA' : 'Return to equity'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

df = df.rolling(12).mean()

fig = imfplotly.create_fig(df, barcols='Return to asset', rlinecols='Return to equity',
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig6_chart2_current_account_mms.csv')

# -----------------------------------------------------
# 3. Non-Performing Loans
# -----------------------------------------------------

dict_series = {'N186ZYTT@EMERGEMA' : 'Total NPL',
               'N186FLVH@EMERGEMA' : 'consumer_loans',
               'N186CJHN@EMERGEMA' : 'np_consumer_loans',
               'N186CFSN@EMERGEMA' : 'sme_loans',
               'N186ZDNN@EMERGEMA' : 'np_sme_loans'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
concol = 'Consumer loan NPL'
df[concol] = 100. * df['np_consumer_loans'] / df['consumer_loans']
smecol = 'SME loan NPL'
df[smecol] = 100. * df['np_sme_loans'] / df['sme_loans']

df.drop(['consumer_loans', 'np_consumer_loans',
         'sme_loans', 'np_sme_loans'], axis=1, inplace=True)
        
fig = imfplotly.create_fig(df, linecols=df.columns, xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig6_chart3_non_performing.csv')

# -----------------------------------------------------
# 4. Required Reserves
# -----------------------------------------------------
dict_series = {'F186LGU@INTWKLY' : 'F186LGU@INTWKLY',
	       'F186LGX@INTWKLY' : 'F186LGX@INTWKLY',
	       'F186LGE@INTWKLY' : 'F186LGE@INTWKLY',
	       'F186LGH@INTWKLY' : 'F186LGH@INTWKLY'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
df['Total'] = (df['F186LGH@INTWKLY'] + df['F186LGX@INTWKLY']) / (df['F186LGU@INTWKLY'] + df['F186LGE@INTWKLY']) * 100.
df['TL'] = df['F186LGH@INTWKLY'] / df['F186LGE@INTWKLY'] * 100.
df['FX'] = df['F186LGX@INTWKLY'] / df['F186LGU@INTWKLY'] * 100.
df = df[['Total', 'TL', 'FX']]

# Convert to monthly
df = calc_w2m(df, 'last')

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig6_chart4_required_reserves.csv')

# -----------------------------------------------------
# 5. Banking Sector Net FX Position
# -----------------------------------------------------
dict_series = {'U186TXS@INTWKLY' : 'On balance sheet',
	       'U186TXO@INTWKLY' : 'Off balance sheet'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

df /= 1000.
df['Net position'] = df['On balance sheet'] + df['Off balance sheet']

# Convert to monthly
df = calc_w2m(df, 'last')

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig6_chart5_fx_position.csv')

# -----------------------------------------------------
# 6. Bank FX Exposure
# -----------------------------------------------------

paycol = 'Payables to banks abroad'
dict_series = {'F186DLAE@INTWKLY' : paycol,
               'D1863LP@INTWKLY' : 'D1863LP@INTWKLY',
               'D1863LM@INTWKLY' : 'D1863LM@INTWKLY'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

sharecol = 'Share of FX loans to NFCs'
df[sharecol] = df['D1863LM@INTWKLY'] / (df['D1863LP@INTWKLY'] + df['D1863LM@INTWKLY']) * 100.
df[paycol] /= 1000.
df.drop(['D1863LP@INTWKLY', 'D1863LM@INTWKLY'], axis=1, inplace=True)

# Convert to monthly
df = calc_w2m(df, 'last')

fig = imfplotly.create_fig(df, linecols=paycol, barcols=sharecol, bar_right=True,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig6_chart6_fx_exposure.csv')

# -----------------------------------------------------
# Create HTML
# -----------------------------------------------------
imfplotly.create_html('turkey_page6.html', objects)
