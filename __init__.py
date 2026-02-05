
import matplotlib.pyplot as plt

from .charts import Chart
from .charts import read

from .mpl import *

# Define IMF colors
AXISGREY  = '#B3B3B3'
AXISGRAY  = '#B3B3B3'
IMFBLUE   = '#4B82AD'
IMFGREEN  = '#96BA79'
IMFRED    = '#C00000'
IMFGREY   = '#A6A8AC'
IMFGRAY   = '#A6A8AC'
IMFBLACK  = '#000000'

# IMF colors from IMF Brand Guide
FUNDBLUE = '#004C97'
FUNDPACIFICBLUE = '#009CDE'
FUNDGREEN = '#78BE20'
FUNDYELLOW = '#F2A900'
FUNDORANGE = '#FF8200'
FUNDDARKORANGE = '#DA291C'
FUNDPURPLE = '#8031A7'
FUNDRED = '#DA291C'
FUNDGREY = '#B1B3B3'
FUNDGRAY = '#B1B3B3'
FUNDSNOWFALL = '#D8D9D9'
FUNDMUTEDGREY = '#707372'
FUNDMUTEDGRAY = '#707372'
FUNDCOOLBLACK = '#001E60'

# Set up commonly used styles so they can be easily used.
# Usage:
# Make sure to copy, otherwise will modify original
# style = LINE_AND_MARKER.copy()
# dict_attrs = {col : style}
# chart = Chart(df, linecols=linecols, dict_attrs=dict_attrs)
REDCIRCLES = {'linewidth' : 0,
              'color' : IMFRED,
              'linestyle' : '-',
              'marker' : 'o',
              'markersize' : 10,
              'markerfacecolor' : AXISGRAY,
              'markeredgewidth' : 0,
              'markeredgecolor' : AXISGRAY}

# Set default style
try:
    set_style('imf-articleiv')
except Exception as e:
    print('Could not set style with exception:')
    print(e)

