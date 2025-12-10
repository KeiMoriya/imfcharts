'''
2025-12-10

Copy necessary series from DMXe files to new file.
'''

import os
import sys

import numpy as np
import pandas as pd

from imf_datatools.dmxe_utilities import get_all_series, get_dmxe_metadata, get_dmxe_data
from imf_datatools.dmxe_writer_utilities import read_dmxe_data, save_dmxe_data, save_dmxe_metadata, delete_dmxe_data, rename_dmxe_data

# Check input files exist
macrofilename = 'TUR_Macro.dmxe'
histfilename = 'TUR_hist.dmxe'
filenames = [macrofilename, histfilename]
for filename in filenames:
    if not os.path.isfile(filename):
        print('File ' + filename + ' does not exist')
        sys.exit()

# Get available series in each file
dict_serieslist = dict()
for filename in filenames:
    dict_serieslist[filename] = get_all_series(filename)
    print('File ' + filename + ': ' + str(len(dict_serieslist[filename])) + ' series')
    
# Create output file
outfilename = 'TUR_charts.dmxe'

# Create a tuple of filename and series that can then be copied to outfilename
infolist = [
    # Chart 1
    (macrofilename, '186NGDP', 'A'),
    (histfilename, '186GCECEW_G01', 'M'),
    (histfilename, '186GCEGS_G01', 'M'),
    (histfilename,  '186GCET_G01_H', 'M'),
    (histfilename,  '186GCEK_G01', 'M'),
    (histfilename,  '186GCEP_G01_H', 'M'),
    # Chart 3
    (histfilename,  '186GCRTII_G01', 'A'),
    (histfilename,  '186GCRTIC_G01', 'A'),
    (histfilename,  '186GCRTGSGV_G01', 'A'),
    (macrofilename,  '186GCRTSCT_G01', 'A'),
    (histfilename,  '186GCR_G01_H', 'A'),
    (histfilename,  '186GCRT_G01', 'A'),
    # Chart 4
    (histfilename, '186GCR_G01_H', 'M'),
    (histfilename, '186GCEP_G01_H', 'M'),
    # Chart 5
    (histfilename, '186NGDP', 'Q'),
    (histfilename, '186GCEI_G01', 'M'),
    (histfilename, '186GCR_G01_H', 'M'),
    (histfilename, '186GCE_G01_H', 'M'),
    (histfilename, '186GCEP_G01_H', 'M'),
    # Chart 6
    (macrofilename, '186GGXWDG_G01_GDP_MAAS', 'A'),
]

for info in infolist:
    filename, series, freq = info
    df = read_dmxe_data(filename, series, freq=freq)
    if df is None:
        print('Data retrieval failed for ' + series)
        sys.exit()

    # Write out
    result = save_dmxe_data(outfilename, df)
    if result != 0:
        print('Result of writing out ' + series + ' was:')
        print(result)
        
    # Read in from outfile to check
    _df = get_dmxe_data(outfilename, series)

# Get all series in outfile
dict_serieslist[outfilename] = get_all_series(outfilename)
print('File ' + outfilename + ': ' + str(len(dict_serieslist[outfilename])) + ' series')
