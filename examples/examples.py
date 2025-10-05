'''
2025-10-05

Examples of running imfcharts.
'''

import os
import sys

import numpy as np
import pandas as pd

import imfcharts
import imfcharts.charts
import importlib
importlib.reload(imfcharts)
importlib.reload(imfcharts.charts)
from imfcharts import *


# Read in data
infilename = 'imfcharts/data/turkey_page1/fig1_chart2_labor.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit()
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create Chart object
chart = Chart(df, linecols=df.columns[0], rlinecols=df.columns[1],
              title='Labor Utilization',
              subtitle='(Percent)',
              xrange='2023-01:2025-08', yrange=[8, 11], ryrange=[10, 25],
              debug=True)

# Access figure object
fig = chart.fig

# Show figure
chart.show()

# Add a horizontal line
chart.add_hline(3)

# Apply style
# chart.apply(style)

# Save
chart.save('labor')
