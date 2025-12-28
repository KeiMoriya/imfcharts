'''
2025-10-05

Generate charts.
'''

import os
import sys
import itertools
import warnings

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.colors as mplcolors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.patches import Patch

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

def guess_freq(df):
    '''
    Guess frequency of a series given a DataFrame.
    Checks differences in days between index and tries go guess.
    '''

    # If df is None, return '?', just a holder
    if df is None:
        return '?'

    # Not enough data to check differences.
    # Return daily freq.
    if len(df) < 2:
        return 'D'
    else:
        idx_types = {type(idx) for idx in df.index}
        if idx_types in [{pd.Timestamp}, {pd.Period}]:
            if (df.index[1] - df.index[0]).days < 6:
                return 'D'
            elif (df.index[1] - df.index[0]).days < 10:
                return 'W'
            elif (df.index[1] - df.index[0]).days < 32:
                return 'M'
            elif (df.index[1] - df.index[0]).days < 93:
                return 'Q'
            elif (df.index[1] - df.index[0]).days < 370:
                return 'A'
            else:
                return 'D'
        else:
            # If not time series, return '?'
            return '?'

class Chart:
    '''
    Class that generates and modifies charts.

    Provides easy way to generate custom charts using custom styles
    and contains internal matplotlib.Figure object for further manipulation.
    Able to save internal figure object.
    '''

    def __init__(self, data=None, indexcol=None,
                 # plotting options
                 linecols=None, barcols=None, rlinecols=None,
                 # whether to remove breaks in line charts
                 linebreaks=False,
                 # bar options
                 stack=True, area=False, barwidth=None, baraxis='left',
                 total_barwidth=None,
                 barlinewidth=None,
                 baredgecolor='black',
                 title=None,
                 subtitle = None,
                 xtitle='', ytitle='',
                 xtitlesize=14, ytitlesize=14,
                 xtickfontsize=14, ytickfontsize=14,
                 xticklength=None, yticklength=None,
                 xtickangle=0,
                 nxticks=7,
                 xformat='auto',
                 dict_legend=None,
                 dict_xaxis=None,
                 dict_yaxis=None,
                 # style
                 style='default',
                 # individual look of each column in data
                 attrs=None,
                 xrange=None, yrange=None, ryrange=None,
                 xmargins='auto',
                 width=10, height=6,
                 topxaxis='left',
                 hlines=[], vlines=[], hrects=[], vrects=[],
                 ncol_legend=1,
                 legend_spacing=0.5,
                 legend_fontsize=14,
                 legend_header='',
                 legend_left=0.04, legend_bottom=0.85, legend_width=0.70, legend_height=0.15,
                 legend_mode='expand',
                 show_legend=True,
                 debug=False):

        # ------------------------------------------------------------------------------
        # Set attributes
        self.debug = debug
        self.data = data

        # Set self.indexcol
        self.indexcol= indexcol
        if self.indexcol is not None:
            if self.data is not None and type(self.data) == pd.DataFrame:
                if indexcol not in self.data.columns:
                    print('indexcol specified as "' + str(indexcol) + '" but not found in data:')
                    print(data)
                    sys.exit()
                else:
                    if self.debug:
                        print('Setting index to ' + str(indexcol))
                    self.data.set_index(indexcol, inplace=True)
                    # If possible, convert to datetime index
                    try:
                        self.data.index = pd.to_datetime(self.data.index)
                    except Exception:
                        pass
            else:
                print('WARNING: indexcol specified but data is not DataFrame')

        # If barlinewidth was specified, use it
        if barlinewidth is not None:
            self.barlinewidth = barlinewidth
        # Otherwise get from style
        else:
            self.barlinewidth = matplotlib.rcParams['patch.linewidth']
        self.baredgecolor = baredgecolor
                
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

        self.xticklength = xticklength
        self.yticklength = yticklength
        
        self.xtickangle = xtickangle
        self.nxticks = nxticks

        self.xformat = xformat
        self.xmargins = xmargins

        self.ncol_legend = ncol_legend
        self.legend_fontsize = legend_fontsize
        self.legend_header = legend_header

        # Whether left or right x-axis should be drawn on top.
        # Use self.set_top_xaxis() to set.
        self.topxaxis = topxaxis

        # ------------------------------------------------------------------------------
        # Entries, labels for legend
        self.legend_entries = []
        self.legend_labels = []

        self.legend_left = legend_left
        self.legend_bottom = legend_bottom
        self.legend_width = legend_width
        self.legend_height = legend_height
        self.legend_mode = legend_mode
        self.legend_spacing = legend_spacing
        self.show_legend = show_legend

        # Check whether index of data is datetime
        self.xaxis_type = 'datetime'
        if self.data is not None and type(self.data) == pd.DataFrame:
            # Try to convert to datetime axis
            try:
                # Ignore pandas warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    self.data.index = pd.to_datetime(self.data.index)
            except:
                pass
            
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
        self.ax_right = None
        if self.debug:
            print('Created self.fig, self.ax')

        # Add title, subtitle
        self.set_title(self.title)
        self.set_subtitle(self.subtitle)

        # Add x, y title
        self.set_xtitle(self.xtitle, self.xtitlesize)
        self.set_ytitle(self.ytitle, self.ytitlesize)

        # Set x, y tick font size
        self.set_xticks(size=self.xtickfontsize, length=self.xticklength, angle=self.xtickangle)
        self.set_yticks(size=self.ytickfontsize, length=self.yticklength)

        # Get xrange and trim data as needed
        self.xrange = self._parse_xrange(xrange, debug=self.debug)
        self._trim_data(self.xrange)

        # Set whether to allow breaks in line charts.
        # If linebreaks is True, NA values will have a break in lines.
        self.linebreaks = linebreaks

        # ---------------------------------------------------------------------------------------------------
        # Draw lines, bars
        if barcols is not None:
            barcols = _parse_cols(barcols)
            self.add_bars(self.data, barcols, indexcol=self.indexcol, stack=stack, total_barwidth=total_barwidth,
                          baraxis=baraxis, xrange=self.xrange, barlinewidth=self.barlinewidth, baredgecolor=self.baredgecolor,
                          attrs=attrs, debug=self.debug)
            
        if linecols is not None:
            linecols = _parse_cols(linecols)
            self.add_lines(self.data, linecols, indexcol=self.indexcol, linebreaks=self.linebreaks, xrange=self.xrange, attrs=attrs, debug=self.debug)

        if rlinecols is not None:
            rlinecols = _parse_cols(rlinecols)
            self.add_lines(self.data, rlinecols, indexcol=self.indexcol, axis='right', linebreaks=self.linebreaks, xrange=self.xrange, attrs=attrs, debug=self.debug)
        
        # Create legend
        legend_header = ''
        if self.debug:
            print('self.legend_entries:')
            print(self.legend_entries)
            print('self.legend_labels:')
            print(self.legend_labels)
        if self.show_legend:
            self.update_legend()

        # Parse y-axis ranges
        self.yrange = self._parse_yrange(yrange)
        self.ryrange = self._parse_yrange(ryrange)

        # Set x-, y-axis ranges
        if self.data is not None:
            self.set_xrange(self.xrange, self.xmargins)
            self.set_yrange(self.yrange)
            self.set_ryrange(self.ryrange)

        # Set x-axis formatting
        self.set_date_format()

        # Set number of x-axis ticks
        if self.xaxis_type == 'datetime':
            self.set_nxticks(self.nxticks)

        # Set which x-axis is drawn on top
        self.set_top_xaxis(self.topxaxis)
                
    def apply(self, style):
        '''
        Apply style to this Chart.
        '''
        
        pass

    def _parse_xrange(self, xrange, debug=False):
        '''
        Utility function to parse x-axis range.
        This can either be a date range or a number range.
        Returns a list of two elements, the elements are one of
        - a number
        - a str interpretible as a date
        - None
        '''

        if debug:
            print('start of _parse_xrange with xrange:')
            print(xrange)

        if xrange is None:
            if debug:
                print('returning [None, None]')
            return [None, None]

        # Special case of two floats or ints, just return original.
        try:
            x0, x1 = xrange
            if type(x0) in [float, int] and type(x1) in [float, int]:
                if debug:
                    print('returning:')
                    print(xrange)
                return xrange
        except Exception:
            pass
        
        if type(xrange) == str and xrange.find(':') != -1:
            xrange = [x.strip() for x in xrange.split(':', 1)]
            xrange = [x if x != '' else None for x in xrange]
            if debug:
                print('xrange here:')
                print(xrange)

        if self.xaxis_type == 'datetime':
            try:
                xrange = [pd.Timestamp(str(x)) if x is not None else None for x in xrange]
                if debug:
                    print('returning:')
                    print(xrange)
            except ValueError:
                print('Could not convert xrange = ' + str(xrange) + ' to pd.Timestamp')
                sys.exit()
            
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

        if yrange is None:
            return [None, None]

        return [yrange[0], yrange[1]]

    def _trim_data(self, xrange):
        '''
        Trim self.data using xrange.
        '''
        
        if type(self.data) == pd.DataFrame:
            if self.xrange[0] is None and self.xrange[1] is None:
                # Don't trim if nothing specified
                pass
            elif self.xrange[0] is None:
                # Trim start only
                self.data = self.data.loc[:str(self.xrange[1]), :]
            elif self.xrange[1] is None:
                # Trim end only
                self.data = self.data.loc[str(self.xrange[0]):, :]
            else:
                # Trim both
                self.data = self.data.loc[str(self.xrange[0]):str(self.xrange[1]), :]

    def set_title(self, title, loc='left', y=1.05, fontweight='bold', fontname='Segoe UI'):
        if title is not None:
            self.ax.set_title(str(title), loc=loc, y=y,
                              fontweight=fontweight, fontname=fontname)

    def set_subtitle(self, subtitle):
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

    def set_xticks(self, size=None, length=None, angle=0):
        # If size is specified, update internal value
        if size is not None:
            self.xtickfontsize = size
            
        # If length is given as default None, get from rcParams
        if length is None:
            length = matplotlib.rcParams['xtick.major.size']

        # Set
        self.ax.tick_params(axis='x', which='major', length=length, labelsize=size, labelrotation=angle)

    def set_yticks(self, size=None, length=None):
        # If size is specified, update internal value
        if size is not None:
            self.ytickfontsize = size

        # If length is given as default None, get from rcParams
        if length is None:
            length = matplotlib.rcParams['ytick.major.size']

        # Set
        self.ax.tick_params(axis='y', which='major', labelsize=size)
        if self.ax_right:
            self.ax_right.tick_params(axis='y', length=length, which='major', labelsize=size)

    def set_nxticks(self, nxticks):
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=nxticks))

        # From freq try to specify location of ticks
        freq = guess_freq(self.data)
        if freq == 'D':
            if len(self.data) <= 30:
                self.ax.xaxis.set_major_locator(mdates.DayLocator([1, 8, 15, 22, 29]))
            elif 30 < len(self.data) and len(self.data) <= 90:
                self.ax.xaxis.set_major_locator(mdates.DayLocator([1, 15]))
            elif len(self.data) <= 180:
                self.ax.xaxis.set_major_locator(mdates.DayLocator([1]))
            else:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1, 7]))
        elif freq == 'W':
            if len(self.data) <= 42:
                self.ax.xaxis.set_major_locator(mdates.DayLocator([1, 8, 15, 22]))
            elif 42 < len(self.data) and len(self.data) <= 310:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1, 7]))
            else:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1]))
        elif freq == 'M':
            if len(self.data) <= 12:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1, 3, 5, 7, 9]))
            elif 12 < len(self.data) and len(self.data) <= 24:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1, 4, 7, 10]))
            elif len(self.data) <= 48:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1, 7]))
            elif len(self.data) < 70:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1]))
            else:
                self.ax.xaxis.set_major_locator(mdates.YearLocator(base=2))
                formatter = mdates.DateFormatter('%b-%y')
                self.ax.xaxis.set_major_formatter(formatter)
        elif freq == 'Q':
            if len(self.data) < 12:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1, 7]))
            elif len(self.data) < 30:
                self.ax.xaxis.set_major_locator(mdates.MonthLocator([1]))
            else:
                self.ax.xaxis.set_major_locator(mdates.YearLocator(base=2))
                def quarter_formatter(x, pos):
                    date = mdates.num2date(x)
                    quarter = (date.month - 1) // 3 + 1
                    return f"{date.year}Q{quarter}"
                formatter = FuncFormatter(quarter_formatter)
                self.ax.xaxis.set_major_formatter(formatter)
        elif freq == 'A':
            if len(self.data) < 8:
                self.ax.xaxis.set_major_locator(mdates.YearLocator(base=1))
            elif len(self.data) < 20:
                self.ax.xaxis.set_major_locator(mdates.YearLocator(base=2))
            else:
                base = int(len(self.data) / 6)
                self.ax.xaxis.set_major_locator(mdates.YearLocator(base=base))
            
    def set_xrange(self, xrange, margins='auto', debug=False):
        '''
        Set x-axis range of fig.
        '''

        if debug:
            print('start of set_xrange() for xrange = ' + str(xrange))
        xrange = self._parse_xrange(xrange)
        if debug:
            print('xrange after calling _parse_xrange():')
            print(xrange)

        # If margins is "auto", try to guess from freq of data
        if margins == 'auto':
            freq = guess_freq(self.data)
            if freq == 'D':
                margins = 1
            elif freq == 'W':
                margins = 5
            elif freq == 'M':
                margins = 30
            elif freq == 'Q':
                margins = 85
            elif freq == 'A':
                margins = 335
            elif freq == '?':
                margins = 0
            else:
                print('Unknown freq ' + freq)
                sys.exit()
        else:
            if type(margins) == int:
                # Use input int as-is
                pass
            else:
                print('set_xrange: margins of type ' + str(type(margins)) + ' not allowed')
                sys.exit()

        if self.xaxis_type == 'datetime':
            if xrange[0] is None:
                xrange[0] = self.data.index.min()
            if xrange[1] is None:
                xrange[1] = self.data.index.max()
        elif self.xaxis_type == 'categorical':
            if xrange[0] is None:
                xrange[0] = 0
            if xrange[1] is None:
                xrange[1] = len(self.data)
        elif self.xaxis_type == 'numerical':
            if xrange[0] is None:
                xrange[0] = self.data.index.min()
            if xrange[1] is None:
                xrange[1] = self.data.index.max()
        else:
            print('self.axis_type of ' + str(self.axis_type) + ' not implemented for set_xrange()')
            sys.exit()
            
        if debug:
            print('xrange before setting xlim:')
            print(xrange)

        # Trim the data based on xrange
        if self.xaxis_type == 'datetime':
            self._trim_data(xrange)
            
            # Try to interpret xrange as dates and add margin
            try:
                x1, x2 = pd.Timestamp(xrange[0]) - pd.Timedelta(days=margins), pd.Timestamp(xrange[1]) + pd.Timedelta(days=margins)
                self.ax.set_xlim(x1, x2)
                if debug:
                    print('Set xlim to Timestamps')
            # If fails, use xrange as-is.
            except ValueError:
                self.ax.set_xlim(xrange[0],xrange[1])
                if debug:
                    print('Set xlim to xrange as-is')
        elif self.xaxis_type == 'categorical':
            self.ax.set_xlim(xrange[0] - 0.5, xrange[1] - 0.5)
        elif self.xaxis_type == 'numerical':
            # Add 3% margin
            total = np.abs(xrange[1] - xrange[0])
            self.ax.set_xlim(xrange[0] - 0.03 * total, xrange[1] + 0.03 * total)
        else:
            print('self.axis_type of ' + str(self.axis_type) + ' not implemented for set_xrange()')
            sys.exit()

    def set_yrange(self, yrange):
        '''
        Set y-axis range of fig.
        '''

        # Get values from self.ax
        ymin, ymax = self.ax.get_ylim()

        if yrange is None:
            return

        # Set ymin, ymax if they are specified
        if yrange[0] is not None:
            ymin = yrange[0]
            
        if yrange[1] is not None:
            ymax = yrange[1]

        try:
            self.ax.set_ylim(ymin, ymax)
        except Exception as e:
            print('Could not apply set_yrange() for yrange = ' + str(yrange))
            sys.exit()

    def set_ryrange(self, ryrange):
        '''
        Set y-axis range of fig.
        '''

        if self.ax_right is None:
            return

        # Get values from self.ax_right
        ymin, ymax = self.ax_right.get_ylim()

        if ryrange is None:
            return

        # Set ymin, ymax if they are specified
        if ryrange[0] is not None:
            ymin = ryrange[0]
            
        if ryrange[1] is not None:
            ymax = ryrange[1]

        try:
            self.ax_right.set_ylim(ymin, ymax)
        except Exception as e:
            print('Could not apply set_ryrange() for yrange = ' + str(yrange))
            sys.exit()

    def set_date_format(self, xformat='auto', debug=False):
        '''
        Set formatting for datetime x-axis.
        `formatter` should be something like a
        mdates.DateFormatter().

        If default `auto` is chosen, freq of data is used.
        Specify special options "D", "W", "M", "Q", "A" to set to these frequencies.
        '''

        if debug:
            print('Start of set_date_format()')

        # If self.xaxis_type is not "datetime", skip
        if self.xaxis_type != 'datetime':
            if debug:
                print('self.xaxis_type = ' + str(self.xaxis_type) + ', returning')
            return

        # If default, guess from freq of data.
        if xformat == 'auto':
             # If length of data is less than 2, cannot calculate difference,
            # use date
            if type(self.data) == pd.DataFrame:
                freq = guess_freq(self.data)
                if freq == 'D':
                    formatter = mdates.DateFormatter('%m/%d/%Y')
                elif freq == 'W':
                    formatter = mdates.DateFormatter('%m/%d/%Y')
                elif freq == 'M':
                    formatter = mdates.DateFormatter('%b-%y')
                elif freq == 'Q':
                    def quarter_formatter(x, pos):
                        date = mdates.num2date(x)
                        quarter = (date.month - 1) // 3 + 1
                        return f"{date.year}Q{quarter}"
                    formatter = FuncFormatter(quarter_formatter)
                    # Below does not work
                    # formatter = mdates.DateFormatter('%YQ%q')
                # Annual
                elif freq == 'A':
                    formatter = mdates.DateFormatter('%Y')
                elif freq == '?':
                    pass
            else:
                print('Cannot determine formatter for xformat = auto')
                sys.exit()
        elif xformat in ['D', 'W']:
            # IMF default for daily
            formatter = mdates.DateFormatter('%m/%d/%Y')
            if debug:
                print('formatter for D:')
                print(formatter)
        elif xformat == 'M':
            # IMF default for monthly
            formatter = mdates.DateFormatter('%b-%y')
            if debug:
                print('formatter for M:')
                print(formatter)
        elif xformat == 'Q':
            # IMF default for quarterly
            def quarter_formatter(x, pos):
                date = mdates.num2date(x)
                quarter = (date.month - 1) // 3 + 1
                return f"{date.year}Q{quarter}"
            formatter = mdates.FuncFormatter(quarter_formatter)
            # Below does not work
            # formatter = mdates.DateFormatter('%YQ%q')
            if debug:
                print('formatter for Q:')
                print(formatter)
        elif xformat == 'A':
            formatter = mdates.DateFormatter('%Y')
            if debug:
                print('formatter for A:')
                print(formatter)
        # Otherwise if specified
        elif type(xformat) == str:
            try:
                formatter = mdates.DateFormatter(xformat)
                if debug:
                    print('formatter for str:')
                    print(formatter)
            except Exception as e:
                print('Cannot specify mdates.DateFormatter with xformat ="' + xformat + '"')
                sys.exit()
        else:
            print('set_date_format():')
            print('xformat of "' + str(xformat) + '" of type ' + str(type(xformat)) + ' not allowed')
            sys.exit()
        
        self.ax.xaxis.set_major_formatter(formatter)

    def add_lines(self, data, colname, indexcol=None, axis='left', linebreaks=False, xrange=None, attrs=None, debug=False):
        '''
        Add line to chart
        '''

        if debug:
            print('Calling add_lines on "' + str(colname) + '"')

        if indexcol is not None:
            if type(data) == pd.DataFrame:
                # Check if index has already been set for data
                if data.index.name == indexcol:
                    pass

                # Otherwise try to set index to indexcol
                elif indexcol not in data.columns:
                    print('indexcol specified as "' + str(indexcol) + '" but not found in data:')
                    print(data)
                    sys.exit()
                else:
                    data.set_index(indexcol, inplace=True)
                    # If possible, convert to datetime index
                    try:
                        data.index = pd.to_datetime(data.index)
                    except Exception:
                        pass
            else:
                print('WARNING: indexcol specified but data is not DataFrame')
            
        linecols = _parse_cols(colname)
        # Don't try to plot indexcol if it was given since this is now the index
        if indexcol is not None:
            if indexcol in linecols:
                linecols.remove(indexcol)
        if debug:
            print('linecols:')
            print(linecols)

        # Set self.data to be input data
        self.data = data
        # Set x-axis limits and trim data as needed
        if xrange is not None:
            xrange = self._parse_xrange(xrange, debug=debug)
            self._trim_data(xrange)
            
        for linecol in linecols:
            if debug:
                print('adding line for "' + linecol + '"')

            if linecol not in data.columns:
                print('"' + linecol + '" is not in data')
                raise ValueError

            # Get default settings from stylefile
            marker = matplotlib.rcParams['lines.marker']
            markersize = matplotlib.rcParams['lines.markersize']
            markerfacecolor = matplotlib.rcParams['lines.markerfacecolor']
            markeredgecolor = matplotlib.rcParams['lines.markeredgecolor']
            markeredgewidth = matplotlib.rcParams['lines.markeredgewidth']
            linewidth = matplotlib.rcParams['lines.linewidth']
            linestyle = matplotlib.rcParams['lines.linestyle']
            color = None
            # Add legend for this entry
            legend = True

            dashes = None
            dash_capstyle = None
            
            # Get any attributes that were assigned to this column
            if attrs is not None and linecol in attrs:
                # This should be a dict containing attributes for this column
                _attrs = attrs[linecol]
                if debug:
                    print(_attrs)

                # If any were specified, overwrite stylefile
                if 'marker' in _attrs:
                    marker = _attrs['marker']
                    
                if 'markersize' in _attrs:
                    markersize = _attrs['markersize']

                if 'markerfacecolor' in _attrs:
                    markerfacecolor = _attrs['markerfacecolor']

                if 'markeredgecolor' in _attrs:
                    markeredgecolor = _attrs['markeredgecolor']

                if 'markeredgewidth' in _attrs:
                    markeredgewidth = _attrs['markeredgewidth']
                    
                if 'linewidth' in _attrs:
                    linewidth = _attrs['linewidth']

                if 'linestyle' in _attrs:
                    linestyle = _attrs['linestyle']
                    # If spcecial case, implement
                    if linestyle == 'imfdash':
                        linestyle = '--'
                        dashes = [10, 3]
                    elif linestyle == 'imfround':
                        linestyle = '-'
                        dashes = (0.5, 5)
                        dash_capstyle = 'round'                        

                if 'color' in _attrs:
                    color = _attrs['color']

                if 'dashes' in _attrs:
                    dashes = _attrs['dashes']
                    
                if 'dash_capstyle' in _attrs:
                    dash_capstyle = _attrs['dash_capstyle']

                if 'legend' in _attrs:
                    legend = _attrs['legend']
            # end of linecol is in attrs

            if marker.strip().lower() == 'none':
                marker = None

            # Make a copy of this column self.data[linecol] and decide whether to remove NA points.
            # This will prevent chart from being broken up if there are NA values.
            if linebreaks:
                # Just make a copy of the original, don't remove NA
                _df = self.data[[linecol]]
            else:
                # Remove NA points
                _df = self.data[[linecol]].dropna()
                
            if axis == 'left':
                # Allow iteration over multiple markers into one legend
                entries = []
                
                if marker is None:
                    if dashes or dash_capstyle:
                        entry = self.ax.plot(_df.index, _df[linecol], label=linecol,
                                             markersize=markersize, marker=marker,
                                             markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                             markeredgewidth=markeredgewidth,
                                             linestyle=linestyle, linewidth=linewidth, color=color,
                                             dashes=dashes, dash_capstyle=dash_capstyle)
                    else:
                        entry = self.ax.plot(_df.index, _df[linecol], label=linecol,
                                             markersize=markersize, marker=marker,
                                             markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                             markeredgewidth=markeredgewidth,
                                             linestyle=linestyle, linewidth=linewidth, color=color)
                    entries.append(entry[0])
                else:
                    # Iterate over all specified markers and put in one legend entry
                    for _marker in marker:
                        if dashes or dash_capstyle:
                            entry = self.ax.plot(_df.index, _df[linecol], label=linecol,
                                                 markersize=markersize, marker=_marker,
                                                 markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                                 markeredgewidth=markeredgewidth,
                                                 linestyle=linestyle, linewidth=linewidth, color=color,
                                                 dashes=dashes, dash_capstyle=dash_capstyle)
                        else:
                            entry = self.ax.plot(_df.index, _df[linecol], label=linecol,
                                                 markersize=markersize, marker=_marker,
                                                 markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                                 markeredgewidth=markeredgewidth,
                                                 linestyle=linestyle, linewidth=linewidth, color=color)
                            
                        if legend:
                            entries.append(entry[0])
                    # end of loop over marker
                
                if legend:
                    self.legend_entries.append(tuple(entries))
                    self.legend_labels.append(linecol)
            elif axis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                    
                # Allow iteration over multiple markers into one legend
                entries = []
                
                if marker is None:
                    if dashes or dash_capstyle:
                        entry = self.ax_right.plot(_df.index, _df[linecol], label=linecol,
                                                   markersize=markersize, marker=marker,
                                                   markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                                   markeredgewidth=markeredgewidth,
                                                   linestyle=linestyle, linewidth=linewidth, color=color,
                                                   dashes=dashes, dash_capstyle=dash_capstyle)
                    else:
                        entry = self.ax_right.plot(_df.index, _df[linecol], label=linecol,
                                                   markersize=markersize, marker=marker,
                                                   markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                                   markeredgewidth=markeredgewidth,
                                                   linestyle=linestyle, linewidth=linewidth, color=color)
                    entries.append(entry[0])
                else:
                    # Iterate over all specified markers and put in one legend entry
                    for _marker in marker:
                        if dashes or dash_capstyle:
                            entry = self.ax_right.plot(_df.index, _df[linecol], label=linecol,
                                                       markersize=markersize, marker=_marker,
                                                       markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                                       markeredgewidth=markeredgewidth,
                                                       linestyle=linestyle, linewidth=linewidth, color=color,
                                                       dashes=dashes, dash_capstyle=dash_capstyle)
                        else:
                            entry = self.ax_right.plot(_df.index, _df[linecol], label=linecol,
                                                       markersize=markersize, marker=_marker,
                                                       markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                                       markeredgewidth=markeredgewidth,
                                                       linestyle=linestyle, linewidth=linewidth, color=color)

                        if legend:
                            entries.append(entry[0])
                    # end of loop over marker
                        
                if legend:
                    self.legend_entries.append(tuple(entries))
                    self.legend_labels.append(linecol)
            else:
                print('axis must be left or right, given ' + str(axis))
                raise VaueError
        # end of loop over linecols

        # Re-create legend
        if self.show_legend:
            self.update_legend()
            if debug:
                print('called update_legend()')

        # Set x-axis range if specified
        if xrange is not None:
            if debug:
                print('before calling set_xrange()')
                print(xrange)
            self.set_xrange(xrange, debug=debug)
            if debug:
                print('after calling set_xrange()')

    def add_bars(self, data, colname, indexcol=None, baraxis='left', stack=True, total_barwidth=None, barlinewidth=None, baredgecolor=None, xrange=None, attrs=None, debug=False):
        '''
        Add bar to chart
        '''

        if debug:
            print('Calling add_bars on "' + str(colname) + '"')
            
        if indexcol is not None:
            if type(data) == pd.DataFrame:
                # Check if index has already been set for data
                if data.index.name == indexcol:
                    pass

                # Otherwise try to set index to indexcol
                elif indexcol not in data.columns:
                    print('indexcol specified as "' + str(indexcol) + '" but not found in data:')
                    print(data)
                    sys.exit()
                else:
                    data.set_index(indexcol, inplace=True)
                    # If possible, convert to datetime index
                    try:
                        data.index = pd.to_datetime(data.index)
                    except Exception:
                        pass
            else:
                print('WARNING: indexcol specified but data is not DataFrame')
                
        barcols = _parse_cols(colname)
        # Don't try to plot indexcol if it was given since this is now the index
        if indexcol is not None:
            barcols.remove(indexcol)

        # Line width of bar borders for all bars.
        # If specified as input arg, use
        if barlinewidth is not None:
            _barlinewidth = barlinewidth
        # Otherwise use class settings
        else:
            _barlinewidth = self.barlinewidth
        
        # Set self.data to be input data
        self.data = data
        # Set x-axis limits and trim data as needed
        if xrange is not None:
            xrange = self._parse_xrange(xrange)
            self._trim_data(xrange)

        # If total_barwidth is default of None,
        # set depending on self.xaxis_type
        if total_barwidth is None:
            if self.xaxis_type in ['numerical', 'categorical']:
                total_barwidth = 0.9
            elif self.xaxis_type == 'datetime':
                # Set below based on freq
                pass
            else:
                print('total_barwdith not implemented for self.xaxis_type of ' + str(self.xaxis_type))
                sys.exit()

        # Guess freq of data and set bar width.
        # This can be overridden later for each individual bar from attrs.
        if self.xaxis_type == 'datetime':
            freq = guess_freq(self.data)
            if freq == 'D':
                barwidth = 1
            elif freq == 'W':
                barwidth = 3
            elif freq == 'M':
                barwidth = 20
            elif freq == 'Q':
                barwidth = 70
            elif freq == 'A':
                barwidth =300
            elif freq == '?':
                barwidth = 1
            else:
                print('Unknown frequency ' + freq)
                sys.exit()

            # If stack=False, need to divide each barwidth by number of bars.
            # If total_barwidth
            if not stack:
                if total_barwidth is None:
                    # Set to total barwdith
                    total_barwidth = barwidth
                    
                # Set each bar to be 1 / len(barcols)
                barwidth /= len(barcols)

                
        elif self.xaxis_type in ['categorical', 'numerical']:
            # Split barwidth among barcols.
            # This can be overridden later for each individual bar from attrs.
            barwidth = total_barwidth / len(barcols)
        else:
            print('self.xaxis_type of ' + str(self.xaxis_type) + ' not implemented')
            sys.exit()

        # Iterate over barcols and plot each bar.
        prop_cycle = plt.rcParams['axes.prop_cycle']
        cycle = itertools.cycle(prop_cycle)
        used_colors = []

        # Need to keep track of positive and negative offsets if stacked.
        pos_offset = [0] * len(self.data)
        neg_offset = [0] * len(self.data)

        # For stack=False, need offset for x-axis.
        # Default is to start from half the total barwidth and half a bar width in the negative direction,
        # this centers the bars.
        if not stack:
            total_offset = - total_barwidth / 2. - total_barwidth / len(barcols) / 2.

        # Keep track of all patches from previous barcols so that
        # if individual bar colors are specified for a barcol,
        # we do not color other bars.
        previous_patches = []
            
        for ibarcol, barcol in enumerate(barcols):
            if debug:
                print('-' * 40)
                print('barcol = "' + barcol + '"')
                
            if barcol not in data.columns:
                print('"' + barcol + '" is not in data')
                raise ValueError

            # Get default settings from stylefile
            # The patch.edgecolor is used for both the hatch line color
            # and the bar edge color.
            # For IMF charts use this as the hatch line color
            # and draw bar again with edgecolor set to black.
            barhatchcolor = matplotlib.rcParams['patch.edgecolor']
            barhatch = None
            barhatchwidth = matplotlib.rcParams['hatch.linewidth']
            # Local copy for this column, can be overwritten with attrs
            # If baredgecolor has not been set, use default
            if baredgecolor is None:
                _baredgecolor = self.baredgecolor
            else:
                _baredgecolor = baredgecolor

            # Individual bar colors
            barcolors = None

            # Add legend for this entry
            legend = True

            # Flag for whether offset was specified for this column.
            # If not specified, default to fixed offset for each col in barcols.
            offset_specified = False

            # Get any attributes that were assigned to this column
            if attrs is not None and barcol in attrs:
                # This should be a dict containing attributes for this column
                _attrs = attrs[barcol]
                if debug:
                    print(_attrs)

                # If any were specified, overwrite stylefile

                # Hatch colors
                if 'barhatchcolor' in _attrs:
                    barhatchcolor = _attrs['barhatchcolor']

                # Hatch pattern in bars
                if 'barhatch' in _attrs:
                    barhatch = _attrs['barhatch']

                # Line width of hatches
                if 'barhatchwidth' in _attrs:
                    barhatchwidth = _attrs['barhatchwidth']

                # Color of bar edges
                if 'baredgecolor' in _attrs:
                    _baredgecolor = _attrs['baredgecolor']
                    
                # If offset is specified for when stack=False, use it
                if 'offset' in _attrs:
                    offset = _attrs['offset']
                    offset_specified = True

                # If barwidth is specified, use it
                if 'barwidth' in _attrs:
                    barwidth = _attrs['barwidth']
                    
                # Add legend entry
                if 'legend' in _attrs:
                    legend = _attrs['legend']

                # Get individual bar colors
                if 'barcolors' in _attrs:
                    barcolors = _attrs['barcolors']

            # end of attrs existing for this barcol

            # Set offset for this bar.
            # Whether the offset is specified or not,
            # the barwidth is added into the offset.
            # Since all offses are cumulative, adding an offset
            # to the first bar will just shift all bars.
            # Adding additional offsets to other bars will
            # add spacing in between bars.
            if not offset_specified:
                offset = barwidth
            else:
                offset += barwidth
                
            # For color, if it is specified use it,
            # otherwise get the next color from the color cycle.
            if attrs is not None and barcol in attrs and 'color' in attrs[barcol]:
                color = attrs[barcol]['color']
                used_colors.append(color)
                if debug:
                    print('1. setting color for ' + barcol + ' to ' + color)
            else:
                itry = 0
                color = next(cycle)['color']
                if debug:
                    print('itry = ' + str(itry) + ', color = ' + color)
                while 1:
                    itry += 1
                    
                    if color in used_colors:
                        # Break out if all colors in the cycle have been used
                        if itry == len(prop_cycle):
                            color = next(cycle)['color']
                            if debug:
                                print('Reached max of cycle at itry = ' + str(itry) + ', setting color for ' + barcol + ' to ' + color)
                            break
                        
                        # Otherwise keep trying
                        color = next(cycle)['color']
                        if debug:
                            print('itry = ' + str(itry) + ', color is now ' + color)
                    else:
                        used_colors.append(color)
                        if debug:
                            print('2. color not used, setting color for ' + barcol + ' to ' + color)
                        break

            if debug:
                if attrs is not None and barcol in attrs:
                    print('attrs:')
                    print(attrs[barcol])
                print('barhatch = ' + str(barhatch))
                print('barlinewidth = ' + str(_barlinewidth))
                print('_baredgecolor = ' + str(_baredgecolor))
                print('barhatchcolor = ' + str(barhatchcolor))
                print('color = ' + str(color))

            # Make copy of positive and negative parts.
            # Set mask to NA so that they don't show up with lines in the chart,
            # but when saving to pos_offset and neg_offset, set values to 0.
            _df_pos = self.data[[barcol]].copy()
            mask = _df_pos[barcol] < 0
            _df_pos.loc[mask, barcol] = np.nan
                
            _df_neg = self.data[[barcol]].copy()
            mask = _df_neg[barcol] > 0
            _df_neg.loc[mask, barcol] = np.nan

            # Set offset when stack=False
            if not stack:
                total_offset += offset
                # If stack=False, need to set _x to be coordinates
                # of where bars are.
                if self.xaxis_type == 'categorical':
                    _x = np.arange(len(self.data)) + total_offset
                else:
                    _x = self.data.index + pd.Timedelta(days=total_offset)

                if debug:
                    print('-' * 40)
                    print(barcol)
                    print('barwidth = ' + str(barwidth) + ' offset = ' + str(offset))
                    print('_x:')
                    print(_x)
            
            if baraxis == 'left':
                if stack:
                    # No direct way to set hatch line widths in ax.bar,
                    # need to use plt.rc_context()
                    with plt.rc_context({"hatch.linewidth": barhatchwidth}):
                        if ibarcol == 0:
                            # Draw negative first
                            entry = self.ax.bar(self.data.index, _df_neg[barcol],
                                                width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                zorder=1, label=barcol)
                            # Draw positive
                            entry = self.ax.bar(self.data.index, _df_pos[barcol],
                                                width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                zorder=1, label=barcol)
                        else:
                            # Draw negative first
                            entry = self.ax.bar(self.data.index, _df_neg[barcol],
                                                bottom=neg_offset,
                                                width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                zorder=1, label=barcol)
                            # Draw positive
                            entry = self.ax.bar(self.data.index, _df_pos[barcol],
                                                bottom=pos_offset,
                                                width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                zorder=1, label=barcol)
                            
                        # Draw again with black edgecolor
                        entry2 = self.ax.bar(self.data.index, _df_pos[barcol],
                                             width=barwidth, color='none', edgecolor=_baredgecolor, linewidth=_barlinewidth,
                                             bottom=pos_offset,
                                             zorder=2)
                        _ = self.ax.bar(self.data.index, _df_neg[barcol],
                                        bottom=neg_offset,
                                        width=barwidth, color='none', edgecolor=_baredgecolor, linewidth=_barlinewidth,
                                        zorder=2)

                        # If barcolors was specified, get all patches for this barcol,
                        # and if the index matches, set color for the corresponding bar.
                        patches = [p for p in self.ax.patches if p not in previous_patches]
                        if debug:
                            print('len(patches) = ' + str(len(patches)))

                        # Add individually specified colors
                        if barcolors is not None:
                            color_bars(barcolors, patches, self.data.index, stack=True, debug=debug)
                        
                        # Add current patches to previous_patches
                        previous_patches += patches
                    # end of plt.rc_context()
                # end of stack
                else:
                    entry = self.ax.bar(_x, self.data[barcol],
                                        width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                        zorder=1, label=barcol)

                    # Draw again with black edgecolor
                    entry2 = self.ax.bar(_x, self.data[barcol],
                                         width=barwidth, color='none', edgecolor=_baredgecolor, linewidth=_barlinewidth,
                                         zorder=2)
                    
                    # Set x-axis categories from self.data.index
                    self.ax.set_xticks(np.arange(len(self.data)), labels=self.data.index)

                    # If barcolors was specified, get all patches for this barcol,
                    # and if the index matches, set color for the corresponding bar.
                    patches = [p for p in self.ax.patches if p not in previous_patches]
                    if debug:
                        print('len(patches) = ' + str(len(patches)))

                    # Add individually specified colors
                    if barcolors is not None:
                        color_bars(barcolors, patches, self.data.index, stack=False, debug=debug)
                        
                    # Add current patches to previous_patches
                    previous_patches += patches
                    
                # end of stack=False
            # end of baraxis == 'left'
                    
            elif baraxis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                    
                # No direct way to set hatch line widths in ax.bar,
                # need to use plt.rc_context()
                if stack:
                    with plt.rc_context({"hatch.linewidth": barhatchwidth}):
                        if ibarcol == 0:
                            # Draw negative first
                            entry = self.ax_right.bar(self.data.index, _df_neg[barcol],
                                                      width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                      zorder=1, label=barcol)
                            # Draw positive
                            entry = self.ax_right.bar(self.data.index, _df_pos[barcol],
                                                      width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                      zorder=1, label=barcol)
                        else:
                            # Draw negative first
                            entry = self.ax_right.bar(self.data.index, _df_neg[barcol],
                                                      bottom=neg_offset,
                                                      width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                      zorder=1, label=barcol)
                            # Draw positive
                            entry = self.ax_right.bar(self.data.index, _df_pos[barcol],
                                                      bottom=pos_offset,
                                                      width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                      zorder=1, label=barcol)
                            
                        # Draw again with black edgecolor
                        entry2 = self.ax_right.bar(self.data.index, _df_pos[barcol],
                                                   width=barwidth, color='none', edgecolor='black', linewidth=_barlinewidth,
                                                   bottom=pos_offset,
                                                   zorder=2)
                        _ = self.ax_right.bar(self.data.index, _df_neg[barcol],
                                              bottom=neg_offset,
                                              width=barwidth, color='none', edgecolor='black', linewidth=_barlinewidth,
                                              zorder=2)

                        # If barcolors was specified, get all patches for this barcol,
                        # and if the index matches, set color for the corresponding bar.
                        patches = [p for p in self.ax_right.patches if p not in previous_patches]
                        if debug:
                            print('len(patches) = ' + str(len(patches)))

                        # Add individually specified colors
                        if barcolors is not None:
                            color_bars(barcolors, patches, self.data.index, stack=True, debug=debug)
                        
                        # Add current patches to previous_patches
                        previous_patches += patches
                    # end of plt.rc_context()
                # end of stack
                else:
                    entry = self.ax_right.bar(_x, self.data[barcol],
                                              width=barwidth, color=color, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                              zorder=1, label=barcol)
                    
                    # Draw again with black edgecolor
                    entry2 = self.ax_right.bar(_x, self.data[barcol],
                                               width=barwidth, color='none', edgecolor='black', linewidth=_barlinewidth,
                                               zorder=2)
                    # Set x-axis categories from self.data.index
                    self.ax_right.set_xticks(np.arange(len(self.data)), labels=self.data.index)

                    # If barcolors was specified, get all patches for this barcol,
                    # and if the index matches, set color for the corresponding bar.
                    patches = [p for p in self.ax_right.patches if p not in previous_patches]
                    if debug:
                        print('len(patches) = ' + str(len(patches)))

                    # Add individually specified colors
                    if barcolors is not None:
                        color_bars(barcolors, patches, self.data.index, stack=False, debug=debug)
                        
                    # Add current patches to previous_patches
                    previous_patches += patches
                    
                # end of stack=False
            # end of baraxis == 'right'
            
            # Adjust offsets
            neg_offset += _df_neg[barcol].replace(np.nan, 0).values
            pos_offset += _df_pos[barcol].replace(np.nan, 0).values

            if legend:
                # Combine entries for entry without and with border line
                self.legend_entries.append(tuple([entry[0], entry2[0]]))
                self.legend_labels.append(barcol)
        # end of loop over barcols

        # Re-create legend
        if self.show_legend:
            self.update_legend()
        
        # Set x-axis range if specified
        if xrange is not None:
            self.set_xrange(xrange, debug=debug)
        
    def add_scatter(self, data, colname, indexcol=None, attrs=None, debug=False):
        '''
        Add scatter to chart
        '''

        if debug:
            print('Calling add_lines on "' + str(colname) + '"')

        if indexcol is not None:
            if type(data) == pd.DataFrame:
                # Check if index has already been set for data
                if data.index.name == indexcol:
                    pass

                # Otherwise try to set index to indexcol
                elif indexcol not in data.columns:
                    print('indexcol specified as "' + str(indexcol) + '" but not found in data:')
                    print(data)
                    sys.exit()
                else:
                    data.set_index(indexcol, inplace=True)
            else:
                print('WARNING: indexcol specified but data is not DataFrame')

    def set_top_xaxis(self, topxaxis='left'):
        '''
        Set which x-axis is drawn on top.
        '''

        if topxaxis == 'left':
            if self.ax_right:
                self.ax.set_zorder(self.ax_right.get_zorder() + 1)
                self.ax.patch.set_visible(False)
        elif topxaxis == 'right':
            if self.ax_right:
                self.ax_right.set_zorder(self.ax.get_zorder() + 1)
                self.ax_right.patch.set_visible(False)
        else:
            print('WARNING:')
            print('Chart.topxaxis must be "left" or "right", given ' + str(topxaxis))

    def add_hline(self, y, xrange=None, coordinates='data', color='red', linewidth=1, linestyle='-', alpha=1, dashes=None, dash_capstyle=None,
                  label='', legend=False,
                  debug=False, **kwarg):
        '''
        Add horizontal line across figure.

        If xrange is None, a horizontal line will be drawn across the entire chart.
        Otherwise range should be a list of two values or a str that has form "start:end".

        `coordinates` is either "data" or "axis", for "data" xrange is converted to data coordinates.
        For "axis" the fraction of the self.ax is used.
        '''

        xrange = self._parse_xrange(xrange)
        if debug:
            print('xrange:')
            print(xrange)
            
        # No xrange
        if xrange == [None, None]:
            if debug:
                print('adding hline with no xrange')
            # dashes or dash_capstyle specified
            if dashes or dash_capstyle:
                entry = self.ax.axhline(y=y, color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha,
                                        dashes=dashes, dash_capstyle=dash_capstyle)
            # no dashes or dash_capstyle specified
            else:
                entry = self.ax.axhline(y=y, color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha)

        # xrange given
        else:
            if debug:
                print('adding hline with xrange')

            # If xrange is given as Timestamps, need to calculate fraction of x-axis range.
            if coordinates == 'data' and type(xrange[0]) == pd.Timestamp and type(xrange[1]) == pd.Timestamp:
                # Get axis range, this will be in ordinals
                xmin, xmax = self.ax.get_xlim()
                # Get fraction of xrange[0], xrange[1]
                xrange[0] = (xrange[0] - pd.Timestamp('1970-01-01')).days
                xrange[1] = (xrange[1] - pd.Timestamp('1970-01-01')).days
                             
                xrange[0] = (xrange[0] - xmin) / (xmax - xmin)
                xrange[1] = (xrange[1] - xmin) / (xmax - xmin)
                if debug:
                    print('xrange:')
                    print(xrange)
                
            # dashes or dash_capstyle specified
            if dashes or dash_capstyle:
                entry = self.ax.axhline(y=y, xmin=xrange[0], xmax=xrange[1],
                                        color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha,
                                        dashes=dashes, dash_capstyle=dash_capstyle)
            # no dashes or dash_capstyle specified
            else:
                entry = self.ax.axhline(y=y, xmin=xrange[0], xmax=xrange[1],
                                        color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha)

        # If adding to legend
        if legend:
            self.legend_entries.append(entry)
            self.legend_labels.append(label)

        # Re-create legend
        if self.show_legend:
            self.update_legend()
            if debug:
                print('called update_legend()')
            
    def add_vline(self, x, yrange=None, coordinates='data', width=1, color='red', linewidth=1, linestyle='-', alpha=1, dashes=None, dash_capstyle=None,
                  label='', legend=False,
                  debug=False, **kwarg):
        '''
        Add vertical line across figure.
        If yrange is None, a vertical line will be drawn across the entire chart.
        Otherwise range should be a list of two values.
        
        `coordinates` is either "data" or "axis", for "data" xrange is converted to data coordinates.
        For "axis" the fraction of the self.ax is used.
        '''

        yrange = self._parse_yrange(yrange)

        # If x-axis is datetime, make sure to convert x to datetime
        if self.xaxis_type == 'datetime':
            try:
                x = pd.Timestamp(x)
            except ValueError:
                print('Could not convert ' + str(x) + ' to pd.Timestamp')
                raise ValueError

        # Convert yrange to fraction of self.ax range as needed
        if coordinates == 'data' and yrange != [None, None]:
            # Get axis range, this will be in ordinals
            ymin, ymax = self.ax.get_ylim()

            # Get fraction of xrange[0], xrange[1]
            yrange[0] = (yrange[0] - ymin) / (ymax - ymin)
            yrange[1] = (yrange[1] - ymin) / (ymax - ymin)

        # No yrange
        if yrange == [None, None]:
            # dashes or dash_capstyle specified
            if dashes or dash_capstyle:
                entry = self.ax.axvline(x=x, color=color, linewidth=linewidth, linestyle=linestyle, dashes=dashes, alpha=alpha,
                                        dash_capstyle=dash_capstyle)
                # no dashes or dash_capstyle specified
            else:
                entry = self.ax.axvline(x=x, color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha)

        # yrange given
        else:
            # dashes or dash_capstyle specified
            if dashes or dash_capstyle:
                entry = self.ax.axvline(x=x, ymin=yrange[0], ymax=yrange[1],
                                        color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha,
                                        dashes=dashes, dash_capstyle=dash_capstyle)
                # no dashes or dash_capstyle specified
            else:
                entry = self.ax.axvline(x=x, ymin=yrange[0], ymax=yrange[1],
                                        color=color, linewidth=linewidth, linestyle=linestyle, alpha=alpha)


        # If adding to legend
        if legend:
            self.legend_entries.append(entry)
            self.legend_labels.append(label)

        # Re-create legend
        if self.show_legend:
            self.update_legend()
            if debug:
                print('called update_legend()')
                
    def add_hrect(self, ymin=0, ymax=0, xrange=None, coordinates='data', color='red', linecolor='none', linewidth=0, linestyle='-', alpha=0.3,
                  dash_capstyle=None,
                  hatch=None, # hatchlinewidth=None,
                  label='', legend=False,
                  zorder=1,
                  debug=False, **kwarg):
        '''
        Add horizontal rectangle across figure.

        If xrange is None, a horizontal rectangle will be drawn across the entire chart.
        Otherwise range should be a list of two values or a str that has form "start:end".

        `coordinates` is either "data" or "axis", for "data" xrange is converted to data coordinates.
        For "axis" the fraction of the self.ax is used.
        '''

        xrange = self._parse_xrange(xrange)
        if debug:
            print('xrange:')
            print(xrange)
            
        # No xrange
        if xrange == [None, None]:
            if debug:
                print('adding rect with no xrange')
            xrange = [0, 1]
        # xrange given
        else:
            if debug:
                print('adding hline with xrange')

            # If xrange is given as Timestamps, need to calculate fraction of x-axis range.
            if coordinates == 'data' and type(xrange[0]) == pd.Timestamp and type(xrange[1]) == pd.Timestamp:
                # Get axis range, this will be in ordinals
                xmin, xmax = self.ax.get_xlim()
                # Get fraction of xrange[0], xrange[1]
                xrange[0] = (xrange[0] - pd.Timestamp('1970-01-01')).days
                xrange[1] = (xrange[1] - pd.Timestamp('1970-01-01')).days
                             
                xrange[0] = (xrange[0] - xmin) / (xmax - xmin)
                xrange[1] = (xrange[1] - xmin) / (xmax - xmin)
                if debug:
                    print('xrange:')
                    print(xrange)

        # dash_capstyle specified
        if dash_capstyle:
            entry = self.ax.axhspan(ymin, ymax, xmin=xrange[0], xmax=xrange[1],
                                    facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                    hatch=hatch,
                                    zorder=zorder,
                                    dash_capstyle=dash_capstyle)
        # no dash_capstyle specified
        else:
            entry = self.ax.axhspan(ymin, ymax, xmin=xrange[0], xmax=xrange[1],
                                    facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                    hatch=hatch,
                                    zorder=zorder)

        # If adding to legend
        if legend:
            # Create a Patch that has the same characteristics
            # that can be added to the legend entries.
            entry = Patch(
                facecolor=color,
                edgecolor=linecolor,
                hatch=hatch,
                label=label)
            self.legend_entries.append(entry)
            self.legend_labels.append(label)

        # Re-create legend
        if self.show_legend:
            self.update_legend()
            if debug:
                print('called update_legend()')
            
#        # As of Matplotlib 3.8.0, changing the hatch linewidth does not work.
#        # It is possible to set the rcParams temporarily,
#        # but once it is restored to the original value that value takes over.
#        # Below is code in case this is fixed in the future.
#
#        # If hatch_linewdith is set, use it.
#        # Otherwise default to rcParams
#        hatchlinewidth_rc = matplotlib.rcParams["hatch.linewidth"]
#        if hatchlinewidth is None:
#            hatchlinewidth = hatchlinewidth_rc
#
#        # The following try-finally is so that matplotlib.rcParams["hatch.linewidth"]
#        # is always resstored to original value.
#        try:
#            # Set value to hatchlinewidth
#            matplotlib.rcParams["hatch.linewidth"] = hatchlinewidth
#
#            # Add ax.axhspan here
#        finally:
#            # Set mpl.rcParams back to original value.
#            # For Matplotlib 3.8.0, this negates the effect of setting hatch.linewidth
#            # and the resulting figure will always have the hatch linewidth of rcParams.
#            matplotlib.rcParams["hatch.linewidth"] = hatchlinewidth_rc

    def add_vrect(self, xmin=0, xmax=0, yrange=None, coordinates='data', color='red', linecolor='none', linewidth=0, linestyle='-', alpha=0.3,
                  dash_capstyle=None,
                  hatch=None, # hatchlinewidth=None,
                  label='', legend=False,
                  zorder=1,
                  debug=False, **kwarg):
        '''
        Add vertical rectangle across figure.

        If yrange is None, a vertical rectangle will be drawn across the entire chart.
        Otherwise range should be a list of two values or a str that has form "start:end".

        `coordinates` is either "data" or "axis", for "data" xrange is converted to data coordinates.
        For "axis" the fraction of the self.ax is used.
        '''

        yrange = self._parse_yrange(yrange)
        if debug:
            print('yrange:')
            print(yrange)
            
        # No yrange
        if yrange == [None, None]:
            if debug:
                print('adding rect with no yrange')
            yrange = [0, 1]
        # yrange given
        else:
            if debug:
                print('adding hline with yrange')

            # If yrange is given, need to calculate fraction of x-axis range.
            if coordinates == 'data':
                # Get axis range
                _ymin, _ymax = self.ax.get_ylim()
                # Get fraction of yrange[0], yrange[1]
                yrange[0] = (yrange[0] - _ymin) / (_ymax - _ymin)
                yrange[1] = (yrange[1] - _ymin) / (_ymax - _ymin)
                if debug:
                    print('yrange:')
                    print(yrange)

        # Parse x-axis range
        xmin, xmax = self._parse_xrange([xmin, xmax])

        # dash_capstyle specified
        if dash_capstyle:
            entry = self.ax.axvspan(xmin, xmax, ymin=yrange[0], ymax=yrange[1],
                                    facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                    hatch=hatch,
                                    zorder=zorder,
                                    dash_capstyle=dash_capstyle)
        # no dash_capstyle specified
        else:
            entry = self.ax.axvspan(xmin, xmax, ymin=yrange[0], ymax=yrange[1],
                                    facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                    hatch=hatch,
                                    zorder=zorder)
            
        # If adding to legend
        if legend:
            # Create a Patch that has the same characteristics
            # that can be added to the legend entries.
            entry = Patch(
                facecolor=color,
                edgecolor=linecolor,
                hatch=hatch,
                label=label)
            self.legend_entries.append(entry)
            self.legend_labels.append(label)

        # Re-create legend
        if self.show_legend:
            self.update_legend()
            if debug:
                print('called update_legend()')
            
#        # As of Matplotlib 3.8.0, changing the hatch linewidth does not work.
#        # It is possible to set the rcParams temporarily,
#        # but once it is restored to the original value that value takes over.
#        # Below is code in case this is fixed in the future.
#
#        # If hatch_linewdith is set, use it.
#        # Otherwise default to rcParams
#        hatchlinewidth_rc = matplotlib.rcParams["hatch.linewidth"]
#        if hatchlinewidth is None:
#            hatchlinewidth = hatchlinewidth_rc
#
#        # The following try-finally is so that matplotlib.rcParams["hatch.linewidth"]
#        # is always resstored to original value.
#        try:
#            # Set value to hatchlinewidth
#            matplotlib.rcParams["hatch.linewidth"] = hatchlinewidth
#
#            # Add ax.axhspan here
#        finally:
#            # Set mpl.rcParams back to original value.
#            # For Matplotlib 3.8.0, this negates the effect of setting hatch.linewidth
#            # and the resulting figure will always have the hatch linewidth of rcParams.
#            matplotlib.rcParams["hatch.linewidth"] = hatchlinewidth_rc

    def add_text(self, x, y, text='', xycoords='data', color='black',
                 fontsize=14, fontfamily='Segoe UI', fontweight='normal',
                 va='top', ha='left'):
        '''
        Add text.

        va='top' will align the top of the text to the specified value.
        ha='left' will align the left of the text to the specified value.
        '''

        if self.xaxis_type == 'datetime':
            try:
                x = pd.Timestamp(x)
            except Exception:
                print('WARNING: Could not convert ' + str(x) + ' to pd.Timestamp')

        self.ax.text(x, y, text,
                     color=color,
                     fontsize=fontsize, fontfamily=fontfamily, fontweight=fontweight,
                     va=va, ha=ha)
    
    def add_arrow(self, head=(0, 0), tail=(1, 1),
                  color='black', width=4, headwidth=15, headlength=15, shrink=0.05, arrowstyle='->', edgecolor=None, edgewidth=0,
                  va='top', ha='left',
                  text='', xycoords='data', textcoords='data'):
        '''
        Add arrow and text.

        va='top' will align the top of the arrow to the specified value.
        ha='left' will align the left of the arrow to the specified value.
        '''

        if self.xaxis_type == 'datetime' and xycoords=='data':
            try:
                head[0] = pd.Timestamp(head[0])
            except Exception:
                print('WARNING: Could not convert ' + str(head[0]) + ' to pd.Timestamp')

            try:
                tail[0] = pd.Timestamp(tail[0])
            except Exception:
                print('WARNING: Could not convert ' + str(tail) + ' to pd.Timestamp')
                
            self.ax.annotate(xy=head, xytext=tail,
                             arrowprops=dict(
                                 facecolor=color,      # Color of the arrow
                                 edgecolor=edgecolor,  # Color of arrow outline
                                 linewidth=edgewidth,  # Width of arrow edges
                                 shrink=shrink,        # Distance from point and text
                                 width=width,          # Width of the arrow tail in points
                                 headwidth=headwidth,  # Width of the arrow head base in points
                                 headlength=headlength # Length of the arrow head in points
                             ),
                             va=va, ha=ha,
                             text=text, xycoords=xycoords, textcoords=textcoords)

    def update_legend(self,
                      ncol_legend=None, legend_spacing=None,
                      legend_left=None, legend_bottom=None, legend_width=None, legend_height=None, legend_mode=None):
        '''
        Update legend of Chart.
        Some options can be specified as inputs, if they are provided as None the class  attributes are used.
        '''

        # Use inputs if they are specified, otherwise default to class attributes
        if ncol_legend is None:
            ncol_legend = self.ncol_legend
        if legend_left is None:
            legend_left = self.legend_left
        if legend_bottom is None:
            legend_bottom = self.legend_bottom
        if legend_width is None:
            legend_width = self.legend_width
        if legend_height is None:
            legend_height = self.legend_height
        if legend_mode is None:
            legend_mode = self.legend_mode
        if legend_spacing is None:
            legend_spacing = self.legend_spacing
        
        self.legend = self.ax.legend(self.legend_entries, self.legend_labels,
                                     loc='upper left',
                                     labelspacing=legend_spacing,
                                     bbox_transform=self.ax.transAxes,
                                     bbox_to_anchor=(legend_left,legend_bottom,legend_width,legend_height),
                                     mode=legend_mode, borderaxespad=0,
                                     ncol=ncol_legend, fontsize=self.legend_fontsize, frameon=False, title=self.legend_header, numpoints=1
        )

    def save(self, filename, dpi=250):
        '''
        Save information on chart.
        '''

        # Besides saving chart as file,
        # would be nice to have options to
        # - save data
        # - save style, settings
        # so that chart can be re-generated.

        # Get dirname and create as necessary
        dirname = os.path.dirname(filename)
        if not dirname == '' and not os.path.isdir(dirname):
            try:
                os.makedirs(dirname)
            except Exception as e:
                print('Could not create dir ' + dirname + ' for filename ' + filename)

        try:
            self.fig.savefig(filename, dpi=dpi)
        except Exception as e:
            print('WARNING: Could not create file ' + filename + ' with exception:')
            print(e)

    def show(self, debug=False):
        '''
        Show chart.
        '''

        if debug:
            print('Calling show')

        # This is necessary to update charts after they have been shown.
        self.fig.canvas.draw()
        
        self.fig.show()

    def set_show_legend(self, option):
        if option:
            self.show_legend = True
        else:
            self.show_legend = False

def color_bars(barcolors, patches, dataindex, stack=False, debug=False):
    '''
    Color individual bars given a list of dicts of the form
    [{idx1 : color1}, {idx2 : color2}, ...]
    and a list of patches for bars and the data's index.

    Treat patches differently based on whether this is a stacked bar chart or not.
    '''

    if debug:
        print('start of color_bars():')
        print('barcolors:')
        print(barcolors)

    if stack:
        # barcolors should be a list of dicts of form
        # [{'idx1' : 'blue'}, {'idx2' : 'red'}]
        for dict_idx_color in barcolors:
            idx = list(dict_idx_color.keys())[0]
            color = dict_idx_color[idx]
            
            if debug:
                print('idx: ' + str(idx) + ', color = ' + str(color))

            # Find matching index number
            try:
                matching_idx = dataindex.get_loc(idx)
                if debug:
                    print('matching_idx = ' + str(matching_idx))
        
                # Get corresponding patch and change color.
                # If stack=True, there will be 4 patches,
                # positive with, without edge color,
                # negative with, without edge color.
                start = matching_idx.start
                matching_patches = [(ip, p) for ip, p in enumerate(patches) if ip % len(dataindex) == start]
                for ip, p in matching_patches:
                    if debug:
                        hex = mplcolors.to_hex(p.get_facecolor()[:3], keep_alpha=False)
                        print('Filling patch color for ip = ' + str(ip) + ', color = ' + hex)
                        print('x = ' + str(p.get_x()) + ', y = ' + str(p.get_y()) + ', height = ' + str(p.get_height()))
                    p.set_facecolor(color)

                    
            except KeyError:
                print('WARNING: barcolors specified for ' + str(idx) + ' but not found in data')
                continue
        # end of loop over barcolors
    # end of stack

    else:
        # barcolors should be a list of dicts of form
        # [{'idx1' : 'blue'}, {'idx2' : 'red'}]
        for dict_idx_color in barcolors:
            idx = list(dict_idx_color.keys())[0]
            color = dict_idx_color[idx]

            if debug:
                print('idx: ' + str(idx) + ', color = ' + str(color))

            # Find matching index number
            try:
                matching_idx = dataindex.get_loc(idx)
                if debug:
                    print('matching_idx = ' + str(matching_idx))
            
                # Get corresponding patch and change color.
                # If stack=False and no duplicate index values, only one patch should match
                if type(matching_idx) == int:
                    p = patches[matching_idx]
                    if debug:
                        print('matching patches: ' + str(p))
                    p.set_facecolor(color)
                # If there are duplicate index values, matching_idx
                # will be a list of [False, False, True, False, True, ...]
                # where True corresponds to matching indexes.
                elif type(matching_idx) == np.ndarray:
                    for iidx, idx in enumerate(matching_idx):
                        print('iidx = ' + str(iidx) + ' idx = ' + str(idx))
                        if idx:
                            p = patches[iidx]
                            if debug:
                                print('Setting color for patch with iidx = ' + str(iidx))
                                print('x = ' + str(p.get_x()) + ', y = ' + str(p.get_y()) + ', height = ' + str(p.get_height()))
                            p.set_facecolor(color)
                else:
                    print('type of matching_idx is ' + str(type(matching_idx)))
                    sys.exit()
            except KeyError:
                print('WARNING: barcolors specified for ' + str(idx) + ' but not found in data')
                continue
        # end of loop over barcolors
    # end of stack=False

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

