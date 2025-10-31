'''
2025-10-05

Generate charts.
'''

import os
import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def _parse_cols(cols):
    '''
    Utility function to parse input columns.
    '''

    # Parse list ccols to get which columns to use.
    # These will be saved in use_cols.
    use_cols = []
    
    # If None is given, don't add anything
    if cols is None:
        return use_cols

    # If a str was given, check whether such a column exists and add it.
    elif type(cols) == str:
        use_cols.append(cols)
        
    # If an iterable is given, check whether valid and add.
    else:
        try:
            for col in cols:
                if type(col) == str:
                    use_cols.append(col)
                else:
                    print('cols must be given as str or iterable of str,')
                    print('given col of type ' + str(type(col)) + ':')
                    print(col)
                    raise ValueError
        except TypeError:
            print('_parse_cols: cols must be given as str or iterable of str')
            print('given type of ' + str(type(cols)) + ':')
            print(cols)
            sys.exit(-1)

    # Remove any duplicate columns
    # (using a dict in Python 3.7 onwards will guarantee original ordering)
    use_cols = list(dict.fromkeys(use_cols))

    return use_cols

class Chart:
    '''
    Class that generates and modifies charts.

    Provides easy way to generate custom charts using custom styles
    and contains internal matplotlib.Figure object for further manipulation.
    Able to save internal figure object.
    '''

    def __init__(self, data=None,
                 # plotting options
                 linecols=None, barcols=None, rlinecols=None,
                 # bar options
                 stack=True, area=False, barwidth=None, bar_right=False,
                 title=None,
                 subtitle = None,
                 xtitle='', ytitle='',
                 xtitlesize=14, ytitlesize=14,
                 xtickfontsize=8, ytickfontsize=8,
                 xformat='auto',
                 dict_legend=None,
                 dict_xaxis=None,
                 dict_yaxis=None,
                 # style
                 style='default',
                 # individual look of each column in data
                 dict_attrs=None,
                 xrange=None, yrange=None, ryrange=None,
                 width=10, height=6,
                 hlines=[], vlines=[], hrects=[], vrects=[],
                 debug=False):

        # ------------------------------------------------------------------------------
        # Set attributes
        self.data = data
        self.width = width
        self.height = height

        self.title = title
        self.subtitle = subtitle

        self.xtitle = xtitle
        self.ytitle = ytitle

        self.xtitlesize = xtitlesize
        self.ytitlesize = ytitlesize

        self.xtickfontsize = xtickfontsize
        self.ytickfontsize = ytickfontsize
        
        # ------------------------------------------------------------------------------
        # Entries, labels for legend
        self.legend_entries = []
        self.legend_labels = []

        # Check whether index of data is datetime
        self.xaxis_type = 'datetime'
        if self.data is not None and type(self.data) == pd.DataFrame:
            idx_types = {type(idx) for idx in self.data.index}
            if idx_types in [{pd.Timestamp}, {pd.Period}]:
                pass
            elif idx_types in [{int}, {float}]: 
                self.xaxis_type = 'numerical'
            else:
                self.xaxis_type = 'categorical'
        
        # Create figure
        self.fig, self.ax = plt.subplots(1, 1, figsize=(self.width, self.height))
        # Initialize self.ax_right to None, only generate as needed
        self.ax_right = self.ax.twinx()
        if debug:
            print('Created self.fig, self.ax')

        # Set color cycler to be common with the left y-axis.
        # Hack from https://github.com/matplotlib/matplotlib/issues/19479
        self.ax_right._get_lines = self.ax._get_lines

        # Add title, subtitle
        if self.title is not None:
            self.ax.set_title(str(title), loc='left', y=1.05,
                              fontweight='bold', fontname='Segoe UI')
        if self.subtitle is not None:
            font_properties = {
                'family': 'Segoe UI',
                'size': 12,
                'color': '#4B82AD'
            }
            
            self.ax.text(0., 1.03, subtitle,
                         horizontalalignment='left',
                         verticalalignment='center',
                         transform=self.ax.transAxes,
                         fontdict=font_properties)
                         # color='#4B82AD',
                         # fontsize=12)

        # Add x, y title
        self.set_xtitle(self.xtitle, self.xtitlesize)
        self.set_ytitle(self.ytitle, self.ytitlesize)

        # Set x, y tick font size
        self.set_xticks(size=self.xtickfontsize)
        self.set_yticks(size=self.ytickfontsize)

        if linecols is not None:
            linecols = _parse_cols(linecols)
            for linecol in linecols:
                self.add_line(self.data, linecol, dict_attrs=dict_attrs, debug=debug)

        if rlinecols is not None:
            rlinecols = _parse_cols(rlinecols)
            for rlinecol in rlinecols:
                self.add_line(self.data, rlinecol, axis='right', dict_attrs=dict_attrs, debug=debug)

        if barcols is not None:
            pass
        
        # Create legend
        ncol_legend = 1
        fontsize = 8
        legend_header = ''
        print('self.legend_entries:')
        print(self.legend_entries)
        print('self.legend_labels:')
        print(self.legend_labels)
        self.legend = self.ax.legend(self.legend_entries, self.legend_labels,
                                     loc='upper left',
                                     labelspacing=1.5,
                                     bbox_transform=self.ax.figure.transFigure,
                                     # bbox_to_anchor=(bottom_left,fig_top_space + 0.015,bottom_right,0.99),
                                     mode='expand', borderaxespad=0,
                                     ncol=ncol_legend, fontsize=fontsize, frameon=False, title=legend_header, numpoints=1
        )

        # Adjust x-axis, y-axis ranges
        self.xrange = self._parse_xrange(xrange)
        self.yrange = self._parse_yrange(yrange)
        self.ryrange = self._parse_yrange(ryrange)

        self.set_xrange(self.xrange)
        self.set_yrange(self.yrange)
        self.set_ryrange(self.ryrange)
                
    def apply(self, style):
        '''
        Apply style to this Chart.
        '''
        
        pass

    def _parse_xrange(self, xrange):
        '''
        Utility function to parse x-axis range.
        This can either be a date range or a number range.
        '''

        if type(xrange) == str and xrange.find(':') != -1:
            xrange = xrange.split(':', 1)

        if self.xaxis_type == 'datetime':
            xrange = [pd.Timestamp(x) for x in xrange]
            
        return [xrange[0], xrange[1]]

    def _parse_yrange(self, yrange):
        '''
        Utility function to parse y-axis range.
        This must be a number range.
        
        Input can be one of
        - None        Return None, no calculation done.
        - (y1, y2)    Returns provided values y1, y2.
                      If either is None, this side will default to available value in df.
        '''

        return [yrange[0], yrange[1]]

    def set_xtitle(self, xtitle, xtitlesize=None):
        self.xtitle = xtitle
        # If a xtitlesize was specified, save internally
        if xtitlesize is not None:
            self.xtitlesize = xtitlesize

        # Set x-axis title
        self.ax.set_xlabel(xtitle, fontsize=self.xtitlesize)

    def set_ytitle(self, ytitle, ytitlesize=None):
        self.ytitle = ytitle
        # If a ytitlesize was specified, save internally
        if ytitlesize is not None:
            self.ytitlesize = ytitlesize

        # Set y-axis title
        self.ax.set_ylabel(ytitle, fontsize=self.ytitlesize)

    def set_xticks(self, size=None):
        # If size is specified, update internal value
        if size is not None:
            self.xtickfontsize = size

        # Set
        self.ax.tick_params(axis='x', which='major', labelsize=size)

    def set_yticks(self, size=None):
        # If size is specified, update internal value
        if size is not None:
            self.ytickfontsize = size

        # Set
        self.ax.tick_params(axis='y', which='major', labelsize=size)
        if self.ax_right:
            print('setting right y-axis tick labelsize to ' + str(size))
            self.ax_right.tick_params(axis='y', which='major', labelsize=size)
        
    def set_xrange(self, xrange):
        '''
        Set x-axis range of fig.
        '''

        self.ax.set_xlim(xrange[0], xrange[1])

    def set_yrange(self, yrange):
        '''
        Set y-axis range of fig.
        '''

        self.ax.set_ylim(yrange[0], yrange[1])

    def set_ryrange(self, ryrange):
        '''
        Set y-axis range of fig.
        '''

        self.ax_right.set_ylim(ryrange[0], ryrange[1])
        
    def add_line(self, data, colname, axis='left', dict_attrs=None, debug=False):
        '''
        Add line to chart
        '''

        if debug:
            print('Calling add_line on "' + colname + '"')
            
        if colname not in data.columns:
            print('"' + colname + '" is not in data')
            raise ValueError

        if axis == 'left':
            entry = self.ax.plot(data.index, data[colname], label=colname)
            self.legend_entries.append(entry[0])
            self.legend_labels.append(colname)
        elif axis == 'right':
            entry = self.ax_right.plot(data.index, data[colname], label=colname)
            self.legend_entries.append(entry[0])
            self.legend_labels.append(colname)
        else:
            print('axis must be left or right, given ' + str(axis))
            raise VaueError
        
        # Merge with self.data

    def add_bar(self, data, colname, axis='left', dict_attrs=None, debug=False):
        '''
        Add bar to chart
        '''

        # Merge with self.data
        pass

    def add_scatter(self, data, colname, dict_attrs=None, debug=False):
        '''
        Add scatter to chart
        '''

        # Merge with self.data
        pass

    def add_hline(self, y, width=1, color='red', dash='-', opacity=1, text=''):
        '''
        Add horizontal line across figure.
        '''
        pass

    def add_vline(self, x, width=1, color='red', dash='-', opacity=1, text=''):
        '''
        Add vertical line across figure.
        '''

        pass
    
    def add_hrect(self, y0, y1, width=1, linecolor='red', fillcolor=None, dash='-', opacity=1, text=''):
        '''
        Add horizontal rectangle across figure.
        '''

        pass

    def add_vrect(self, y0, y1, width=1, linecolor='red', fillcolor=None, dash='-', opacity=1, text=''):
        '''
        Add vertical rectangle across figure.
        '''

        pass
    

    def save(self, filename):
        '''
        Save information on chart.
        '''

        # save data

        # save style, settings

        pass

    def show(self, debug=False):
        '''
        Show chart.
        '''

        if debug:
            print('Calling show')

        self.fig.show()
    

def main(argv):
    pass

def read(saved):
    '''
    Read in saved Chart object
    '''

    if not os.path.isfile(saved):
        print('File ' + saved + ' does not exist')
        sys.exit()
        
    # return chart
    pass

if __name__ == '__main__':
    main(sys.argv[1:])

