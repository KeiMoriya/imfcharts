'''
2025-11-15

Get data for Turkey page 3.
'''

import os
import sys

import numpy as np
import pandas as pd

import imf_datatools
from imf_datatools.dataframe_utilities import *

import imfplotly
objects = []

outdir = 'data/turkey_page3'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

# -----------------------------------------------------
# 1. Real Minimum Wage
# -----------------------------------------------------
dict_series = {'N186PC@EMERGEMA' : 'inflation',
	       'N186EMMW@EMERGEMA' : 'wage'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

basedate = '2015-01-01'
wage0 = df.loc[basedate, 'wage']
inflation0 = df.loc[basedate, 'inflation']
        
# Rebase so that 2015-01 is 100.
col = 'Real Minimum Wage'
df[col] = 100. * df['wage'] / df['inflation'] / (wage0 / inflation0)
        
fig = imfplotly.create_fig(df, barcols=col,
                           xrange='2015-01:')
objects.append(fig)
df.to_csv(outdir + '/fig3_chart1_wage.csv')

# -----------------------------------------------------
# 2. Real Labor Cost and Earnings Index
# -----------------------------------------------------
dict_series = {'N186PC@EMERGEMA' : 'inflation',
	       'S186EHL@EMERGEMA' : 'labor',
               'S186EH@EMERGEMA' : 'earnings'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

basedate = '2015-01-01'
labor0 = df.loc[basedate, 'labor']
earnings0 = df.loc[basedate, 'earnings']
        
# Rebase so that 2015-01 is 100.
col1 = 'Labor cost'
df[col1] = 100. * df['labor'] / df['inflation'] / (labor0 / inflation0)

col2 = 'Earnings'
df[col2] = 100. * df['earnings'] / df['inflation'] / (earnings0 / inflation0)

df = df[[col1, col2]]

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2015-01:')
objects.append(fig)
df.to_csv(outdir + '/fig3_chart2_labor.csv')

# -----------------------------------------------------
# 3. Unemployment Rate
# -----------------------------------------------------
dict_series = {'S186ELUR@EMERGEMA' : 'Total',
               'S186ELRM@EMERGEMA' : 'Male',
               'S186ELRF@EMERGEMA' : 'Female'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2015-01:')
objects.append(fig)
df.to_csv(outdir + '/fig3_chart3_unemp.csv')

# -----------------------------------------------------
# 4. Labor Force Participation Rate
# -----------------------------------------------------
dict_series = {'S186ELPR@EMERGEMA' : 'Total',
	       'S186EPRM@EMERGEMA' : 'Male',
	       'S186EPRF@EMERGEMA' : 'Female'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2015-01:')
objects.append(fig)
df.to_csv(outdir + '/fig3_chart4_participation.csv')

# -----------------------------------------------------
# 5. Labor Compensation
# -----------------------------------------------------
dict_series = {'N186NGDP@EMERGEMA' : 'gdp',
	       'N186NYCT@EMERGEMA' : 'compensation',
	       'N186NGS@EMERGEMA' : 'surplus'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

col1 = 'Compensation of employees'
df[col1] = 100. * df['compensation'].rolling(4).sum() / df['gdp'].rolling(4).sum()
col2 = 'Operating surplus'
df[col2] = 100. * df['surplus'].rolling(4).sum() / df['gdp'].rolling(4).sum()

df = df[[col1, col2]]
        
fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2015-Q1:')
objects.append(fig)
df.to_csv(outdir + '/fig3_chart5_compensation.csv')

# -----------------------------------------------------
# 6. Share of Employment: SME vs. Large Firms
# -----------------------------------------------------

# Data from Turkstat website, not available in Haver.
infilename = 'Figure 3 Codes.xlsx'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
sheetname = 'C6. Website data'
df = pd.read_excel(infilename, sheet_name=sheetname, index_col=0, parse_dates=[0])

fig = imfplotly.create_fig(df, linecols=df.columns[0], rlinecols=df.columns[1])
objects.append(fig)
df.to_csv(outdir + '/fig3_chart6_employment_share.csv')

# -----------------------------------------------------
# Create HTML
# -----------------------------------------------------
imfplotly.create_html('turkey_page3.html', objects)
