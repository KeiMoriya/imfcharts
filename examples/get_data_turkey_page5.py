'''
2025-11-15

Get data for Turkey page 5.
'''

import os
import sys

import numpy as np
import pandas as pd

import imf_datatools
from imf_datatools.dataframe_utilities import *

import imfplotly
objects = []

outdir = 'data/turkey_page5'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

# -----------------------------------------------------
# 1. Current Account
# -----------------------------------------------------
dict_series = {'N186BC@EMERGEMA' : 'Current Account Balance',
               'N186BCGN@EMERGEMA' : 'Gold',
               'N186BCST@EMERGEMA' : 'transport',
               'N186BCSR@EMERGEMA' : 'travel',
               'N186IX3@EMERGEMA' : 'exports',
               'N186IM3@EMERGEMA' : 'imports'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
df['Tourism & Transport'] = df['transport'] + df['travel']
df['Energy Balance'] = df['exports'] - df['imports']
df['Other'] = df['Current Account Balance'] - df[['Gold', 'Tourism & Transport', 'Energy Balance']].sum(axis=1)

# Drop unnecessary cols
df.drop(['transport', 'travel', 'exports', 'imports'], axis=1, inplace=True)
cols = df.columns

# Read in data for GDP and FX which was hardcoded in Excel
infilename = 'gdp_fx.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
gdp_fx = pd.read_csv(infilename, index_col=0, parse_dates=[0])
gdp_fx['gdp_usd'] = gdp_fx['gdp'] / gdp_fx['fx']

# Normalize by GDP
df = calc_m2q(df, 'sum')
df = df.merge(gdp_fx[['gdp_usd']], left_index=True, right_index=True, how='outer')
for col in cols:
    df[col] = 100. * df[col] / gdp_fx['gdp_usd']
df.drop('gdp_usd', axis=1, inplace=True)
df.dropna(axis=0, how='any', inplace=True)
        
fig = imfplotly.create_fig(df, linecols=df.columns[0], barcols=df.columns[1:],
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig5_chart1_current_account.csv')

# -----------------------------------------------------
# 2. Current Account
# -----------------------------------------------------
cacol = 'Current account'
dict_series = {'N186BC@EMERGEMA' : cacol,
               'N186IX3@EMERGEMA' : 'export_fuel',
	       'N186IM3@EMERGEMA' : 'import_fuel',
               'N186BGXN@EMERGEMA' : 'export_gold',
	       'N186BGMN@EMERGEMA' : 'import_gold'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
df['Excluding fuel'] = df[cacol] - (df['export_fuel'] - df['import_fuel'])
df['Excluding fuel & gold'] = df[cacol] - (df['export_fuel'] - df['import_fuel']) - (df['export_gold'] - df['import_gold'])
df['Excluding gold'] = df[cacol] - (df['export_gold'] - df['import_gold'])
df.drop(['export_fuel', 'import_fuel', 'export_gold', 'import_gold'], axis=1, inplace=True)

# Take 12-month moving sum and divide by 1000
df = df.rolling(12).sum() / 1000

fig = imfplotly.create_fig(df, linecols=df.columns,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig5_chart2_current_account_mms.csv')

# -----------------------------------------------------
# 3. Terms of Trade Shock, 2025Q2 or Latest
# -----------------------------------------------------

dict_series = {'N186PFTT@EMERGEMA' : 'TUR',
               'N273PFTT@EMERGELA' : 'MEX',
               'N935PFTT@EMERGECW' : 'CZE',
               'N223PFTT@EMERGELA' : 'BRA 1/',
               'N536PFTT@EMERGEPR' : 'IDN',
               'N228PFTT@EMERGELA' : 'CHL 1/',
               'N944PFTT@EMERGECW' : 'HDN 1/',
               'N918PFTT@EMERGECW' : 'BGR 1/',
               'N548IUT@EMERGEPR' : 'MYS',
               'N542IBT@EMERGEPR' : 'KOR',
               'N968PFTT@EMERGECW' : 'ROU 1/',
               'N534PFTT@EMERGEPR' : 'IND 1/',
               'N578PFTT@EMERGEPR' : 'THA',
               'N964PFTT@EMERGECW' : 'POL 1/',
               'N924PFTT@EMERGEPR' : 'CHN',
               'N233PFTT@EMERGELA' : 'COL'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

# Calculate mean for each country in 2023
mean_2023 = df.loc['2023'].mean()

# For each country, calculate 100 * (latest available data / 2022 mean - 1)
_df = pd.DataFrame(index=df.columns)
_df['shock'] = np.nan
for country in _df.index:
    mean = mean_2023.loc[country]
    # Check freq of data and if monthly convert to quarterly
    if len(df.loc['2023', country].dropna()) == 4:
        data = df[country].dropna()
    elif len(df.loc['2023', country].dropna()) in [11, 12]:
        data = calc_m2q(df[country], 'mean').dropna()
    else:
        print('Something wrong for ' + country)
        sys.exit()
        
    # Calculate deviation from 2023 mean
    _df.loc[country, 'shock'] = 100. * (data.values[-1] / mean - 1.)
        
fig = imfplotly.create_fig(_df, barcols=_df.columns)
objects.append(fig)
_df.to_csv(outdir + '/fig5_chart3_terms_of_trade.csv')

# -----------------------------------------------------
# 4. Current Account Financing
# -----------------------------------------------------
dict_series = {'N186BC@EMERGEMA' : 'Current Account Balance',
	       'N186BFP@EMERGEMA' : 'Portfolio',
	       'N186BFRA@EMERGEMA' : 'Reserves (+ = drawdown)',
               'N186BFI@EMERGEMA' : 'direct_investment',
               'N186BFO@EMERGEMA' : 'other_investment'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
df['Other Inv. & FDI'] = df['direct_investment'] + df['other_investment']
df['E&O'] = df['Current Account Balance'] - df[['Portfolio', 'Reserves (+ = drawdown)', 'Other Inv. & FDI']].sum(axis=1)
df.drop(['direct_investment', 'other_investment'], axis=1, inplace=True)

# Read in data for GDP and FX which was hardcoded in Excel
infilename = 'gdp_fx.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
gdp_fx = pd.read_csv(infilename, index_col=0, parse_dates=[0])
gdp_fx['gdp_usd'] = gdp_fx['gdp'] / gdp_fx['fx']

# Normalize by GDP
df_q = - calc_m2q(df, 'sum')
cols = df_q.columns
df_q = df_q.merge(gdp_fx[['gdp_usd']], left_index=True, right_index=True, how='outer')
for col in cols:
    df_q[col] = 100. * df_q[col] / gdp_fx['gdp_usd']
df_q.drop('gdp_usd', axis=1, inplace=True)
df_q.dropna(axis=0, how='any', inplace=True)

barcols = [c for c in df_q.columns if c != 'Current Account Balance']
fig = imfplotly.create_fig(df_q, linecols='Current Account Balance',
                           barcols=barcols,
                           xrange='2022-01:')
objects.append(fig)
df_q.to_csv(outdir + '/fig5_chart4_current_account_financing.csv')

# -----------------------------------------------------
# 5. Financial Account 2/
# -----------------------------------------------------
dict_series = {'N186BFP@EMERGEMA' : 'Portfolio investment',
	       'N186BFI@EMERGEMA' : 'Direct investment',
	       'N186BFO@EMERGEMA' : 'Other investment',
               'N186BFN@EMERGEMA' : 'Financial account'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

# Calculate 3-month moving average
# and take negative
df = - df.rolling(3).mean() / 1000.

fincol = 'Financial account'
barcols = [c for c in df.columns if c != fincol]
fig = imfplotly.create_fig(df, linecols=fincol, barcols=barcols,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig5_chart5_financial_account.csv')

# -----------------------------------------------------
# 6. Gross International Reserves
# -----------------------------------------------------

gircol = 'Gross International Reserves (GIR) (rhs)'
dict_series = {'N186LFRG@EMERGEMA' : gircol,
	       'N186LFG@EMERGEMA' : 'Gold',
               'N186CLDB@EMERGEMA' : 'banking_deposits',
               'N186XUSN@EMERGEMA' : 'fx'}
df = None
for series in dict_series:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

df['FX'] = df[gircol] - df['Gold']
bankcol = 'GIR, net of liabilities to banks'
df[bankcol] = df[gircol] - df['banking_deposits'] / df['fx']
df.drop(['banking_deposits', 'fx'], axis=1, inplace=True)
df /= 1000.

# Read in corecol
corecol = 'Core NIR (rhs)'
infilename = 'Figure 5 Codes.xlsx'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
core = pd.read_excel(infilename, sheet_name='C6.Trans', skiprows=6, index_col=0, parse_dates=[0])
core = core[['Core NIR']].rename({'Core NIR' : corecol}, axis=1).dropna()
core.index = pd.to_datetime(core.index, format="%b-%y")

# Merge with df
df = df.merge(core, left_index=True, right_index=True, how='outer')
barcols = ['FX', 'Gold']

fig = imfplotly.create_fig(df, linecols=[bankcol, gircol], rlinecols=[corecol], barcols=barcols,
                           xrange='2022-01:')
objects.append(fig)
df.to_csv(outdir + '/fig5_chart6_gross_international_reserves.csv')

# -----------------------------------------------------
# Create HTML
# -----------------------------------------------------
imfplotly.create_html('turkey_page5.html', objects)
