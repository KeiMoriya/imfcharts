import os
import glob
import importlib

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


