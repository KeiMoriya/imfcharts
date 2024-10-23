'''
2024-10-23

Scripts to create example datasets in data/.
'''
import os

import imf_datatools

outdir = 'data'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

seriesdict = {'PGDPH@USECON' : 'GDP',
              'PTCH@USECON' : 'C',
              'PTGH@USECON' : 'G',
              'PTFH@USECON' : 'I',
              'PTVH@USECON' : 'Inventories',
              'PTXH@USECON' : 'X',
              'PTMH@USECON' : 'M'}
df = None
for series in seriesdict:
    _df = imf_datatools.get_haver_data(series)
    _df.columns = [seriesdict[series]]
    if df is None:
        df = _df
    else:
        df = df.merge(_df, left_index=True, right_index=True, how='outer')
# Make sure all cols are available
df.dropna(axis=0, how='any', inplace=True)

# Save
outfilename = outdir + '/' + 'usgdp.csv'
df.to_csv(outfilename)
print('Created file ' + outfilename + '...')

