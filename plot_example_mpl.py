'''
2024-10-23

Example of using mpl library to plot example data.
'''
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

import mpl

outdir = 'figures/mpl'
if not os.path.isdir(outdir):
    os.makedirs(outdir)


# Get example data
infilename = 'data/usgdp.csv'
if not os.path.isfile(infilename):
    print('File ' + infilename + ' does not exist')
    sys.exit(-1)
df = pd.read_csv(infilename, index_col=0, parse_dates=[0])

# Create chart
mpl.set_style('imf-articleiv')
fig, ax = plt.subplots(1, 1)
df['2001':].plot(ax=ax)
legend = ax.legend()
outfilename = outdir + '/usgdp_mpl.pdf'
fig.savefig(outfilename)
print('Created file ' + outfilename)


