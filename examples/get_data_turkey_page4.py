'''
2025-12-10

Get data for Turkey page 4.
'''

import os
import sys

import numpy as np
import pandas as pd

import imf_datatools
from imf_datatools.dmxe_utilities import get_dmxe_metadata, get_dmxe_data
from imf_datatools.dataframe_utilities import *

import imfplotly
objects = []

dmxefilename = 'TUR_charts.dmxe'
if not os.path.isfile(dmxefilename):
    print('File ' + dmxefilename + ' does not exist')
    sys.exit()

outdir = 'data/turkey_page4'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

# -----------------------------------------------------
# 1. Central Government: Primary Expenditure Components
# -----------------------------------------------------

dict_series = {'186GCECEW_G01' : 'Personnel',
               '186GCEGS_G01'  : 'Goods & services',
               '186GCET_G01_H' : 'Current transfers',
               '186GCEK_G01'   : 'Capital exp.',
               '186GCEP_G01_H' : 'Primary exp.'}
df = None
for series in dict_series:
    _df = get_dmxe_data(dmxefilename, series, freq='M')
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

df['Other'] = df['Primary exp.'] - df[['Personnel', 'Goods & services', 'Current transfers', 'Capital exp.']].sum(axis=1)

# Take annual sum
last_month = df.index[-1].month
df = calc_m2a(df, 'sum')
# Remove last year if not complete
if last_month != 12:
    df = df.iloc[:-1]

# Get GDP series
gdpseries = '186NGDP'
df_gdp = get_dmxe_data(dmxefilename, gdpseries, freq='A')
# Merge
df = df.merge(df_gdp, left_index=True, right_index=True, how='left')
# Normalize by GDP
for col in df.columns:
    if col == gdpseries:
        continue
    df[col] = 100. * df[col] / (df[gdpseries] * 1000.)
df.drop(gdpseries, axis=1, inplace=True)

linecol = 'Primary exp.'
barcols = list(df.columns)
barcols.remove(linecol)

dict_colors = {'Personnel' : {'color' : '#004C97'},
               'Goods & services' : {'color' : '#009CDE'},
               'Current transfers' : {'color' : '#CAEDFE'},
               'Capital exp.' : {'color' : '#FF8200'},
               'Other' : {'color' : '#DA291C'},
               'Primary exp.' : {'color' : 'black'}}

fig = imfplotly.create_fig(df, linecols=linecol, barcols=barcols,
                           dict_colors=dict_colors, bar_opacity=1,
                           xrange='2018-01:', yrange=[0, 30])
objects.append(fig)
df.to_csv(outdir + '/fig4_chart1_exp.csv')

# -----------------------------------------------------
# 2. Cash spending
# -----------------------------------------------------
infilename = 'Figure 4 Codes.xlsx'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
sheetname = '2. Desk input'
df = pd.read_excel(infilename, sheet_name=sheetname, index_col=0, parse_dates=[0])

fig = imfplotly.create_fig(df, barcols=df.columns, stack=False)
objects.append(fig)
df.to_csv(outdir + '/fig4_chart2_spending.csv')

# -----------------------------------------------------
# 3. Primary Revenue Components
# -----------------------------------------------------
gdpseries = '186NGDP'
dict_series = {'186GCRTII_G01' : 'PIT',
               '186GCRTIC_G01' : 'CIT',
               '186GCRTGSGV_G01' : 'VAT',
               '186GCRTSCT_G01' : 'SCT',
               '186GCR_G01_H' : 'Primary revenues',
               '186GCRT_G01' : 'tax',
               gdpseries : gdpseries}
df = None
for series in dict_series:
    _df = get_dmxe_data(dmxefilename, series, freq='A')
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

df['Non-tax'] = df['Primary revenues'] - df['tax']
df['Other'] = df['Primary revenues'] - df[['PIT', 'CIT', 'VAT', 'SCT', 'Non-tax']].sum(axis=1)

# Normalize by GDP
for col in df.columns:
    if col == gdpseries:
        continue
    df[col] = 100. * df[col] / (df[gdpseries] * 1000.)
df.drop([gdpseries, 'tax'], axis=1, inplace=True)

linecol = 'Primary revenues'
barcols = list(df.columns)
barcols.remove(linecol)

dict_colors = {'PIT' : {'color' : '#004C97'},
               'CIT' : {'color' : '#009CDE'},
               'VAT' : {'color' : '#CAEDFE'},
               'SCT' : {'color' : '#BFBFBF'},
               'Non-tax' : {'color' : '#FF8200'},
               'Other' : {'color' : '#DA291C'},
               'Primary revenues' : {'color' : 'black'}}

fig = imfplotly.create_fig(df, linecols=linecol, barcols=barcols,
                           dict_colors=dict_colors, bar_opacity=1,
                           xrange='2018-01:2024-01',
                           yrange=[0, 30])
objects.append(fig)
df.to_csv(outdir + '/fig4_chart3_revenue.csv')

# -----------------------------------------------------
# 4. Government: Primary Revenue/Expenditure
# -----------------------------------------------------

dict_series = {'186GCR_G01_H' : 'Primary revenue',
	       '186GCEP_G01_H' : 'Primary expenditure'}
df = None
for series in dict_series:
    _df = get_dmxe_data(dmxefilename, series, freq='M')
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

# Take rolling 12-month rolling sum and %yoy
df = calc_yoy(calc_rolling(df, 12))

dict_colors = {'Primary revenue' : {'color' : 'blue'},
               'Primary expenditure' : {'color' : 'red'}}
fig = imfplotly.create_fig(df, linecols=df.columns,
                           dict_colors=dict_colors,
                           xrange='2018-01:',
                           yrange=[5, 145])
objects.append(fig)
df.to_csv(outdir + '/fig4_chart4_revenue_expenditure.csv')

# -----------------------------------------------------
# 5. Fiscal Balance
# -----------------------------------------------------

list_series = ['186GCEI_G01',
               '186GCR_G01_H',
               '186GCE_G01_H',
               '186GCEP_G01_H']
df = None
for series in list_series:
    _df = get_dmxe_data(dmxefilename, series, freq='M')
    _df.columns = [series]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
        
# Get GDP (Q) series
gdpseries = '186NGDP'
df_gdp = get_dmxe_data(dmxefilename, gdpseries, freq='Q')

# Convert to monthly
df_gdp = calc_q2m(df_gdp, 'mean')

# Merge
df = df.merge(df_gdp, left_index=True, right_index=True, how='left')

# Calculate 12-month rolling sum and normalize by GDP
df = calc_rolling(df, 12, method='sum')
df['Interest payments, rhs'] = 100. * df['186GCEI_G01'] / df[gdpseries]
df['Overall balance'] = 100. * (df['186GCR_G01_H'] - df['186GCE_G01_H']) / df[gdpseries]
df['Primary balance'] = 100. * (df['186GCR_G01_H'] - df['186GCEP_G01_H']) / df[gdpseries]

dict_colors = {'Interest payments, rhs' : {'color' : '#CAEDFE'},
               'Overall balance' : {'color' : '#004C97'},
               'Primary balance' : {'color' : '#DA291C'}}

fig = imfplotly.create_fig(df, linecols=['Overall balance', 'Primary balance'],
                           barcols='Interest payments, rhs', bar_right=True,
                           dict_colors=dict_colors, bar_opacity=1,
                           xrange='2018-01:',
                           yrange=[-10, 6], ryrange=[0, 5])
objects.append(fig)
df.to_csv(outdir + '/fig4_chart5_fiscal_balance.csv')

# -----------------------------------------------------
# 6. Gross Debt
# -----------------------------------------------------
dict_series = {'186GGXWDG_G01_GDP_MAAS' : 'debt'}
df = None
for series in dict_series:
    _df = get_dmxe_data(dmxefilename, series, freq='A')
    _df.columns = [dict_series[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')

dict_colors = {df.columns[0] : {'color' : 'blue'},
               }

fig = imfplotly.create_fig(df, barcols=df.columns,
                           dict_colors=dict_colors,
                           xrange='2018-01:2025-01',
                           yrange=[0, 50])
objects.append(fig)
df.to_csv(outdir + '/fig4_chart6_debt.csv')

# -----------------------------------------------------
# Create HTML
# -----------------------------------------------------
imfplotly.create_html('turkey_page4.html', objects)
