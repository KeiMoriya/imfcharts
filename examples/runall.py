import os
import glob
import importlib
import shutil
import pandas as pd

from imfcharts import *
set_style('fund-guide')

import examples_turkey_page1
import examples_turkey_page2
import examples_turkey_page3
import examples_turkey_page4
import examples_turkey_page5
import examples_turkey_page6

importlib.reload(examples_turkey_page1)
importlib.reload(examples_turkey_page2)
importlib.reload(examples_turkey_page3)
importlib.reload(examples_turkey_page4)
importlib.reload(examples_turkey_page5)
importlib.reload(examples_turkey_page6)

# Combine all pdfs
from PyPDF2 import PdfWriter
outdir = 'pdf'
mergedfilename = outdir + '/all.pdf'
if os.path.isfile(mergedfilename):
    os.remove(mergedfilename)

# Merge all files
merger = PdfWriter()
filenames = sorted(glob.glob(outdir + '/all_page*.pdf'))
for filename in filenames:
    merger.append(filename)
merger.write(mergedfilename)
print('Created file ' + mergedfilename)


# Other scripts
import examples_lines
import examples_bars
import examples_area
import examples_lines_rects
import examples_titles
import examples_legend
import examples_text_arrow_fill
import examples_fill
import examples_styles
import examples_axistitles
import examples_ticks

# Copy all summary charts
datestr = pd.Timestamp.today().strftime('%Y-%m-%d')
outdir = 'pdf/summary_' + datestr
if not os.path.isdir(outdir):
    os.makedirs(outdir)

for filestem in ['all', 'lines', 'bars', 'area', 'lines_rects', 'titles', 'legends', 'text_arrow_fill', 'fill', 'ticks']:
    original = 'pdf/' + filestem + '.pdf'
    newname = outdir + '/' + filestem + '_' + datestr + '.pdf'
    shutil.copy2(original, newname)
    
