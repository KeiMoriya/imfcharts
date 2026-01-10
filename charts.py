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
                 linecols=None, barcols=None, rlinecols=None, areacols=None,
                 # iterable of colors for colorcycle
                 colorcycle=None,
                 # lines() options ----------------------------------------------
                 # Global linewidth
                 linewidth=None,
                 # whether to remove breaks in line charts
                 linebreaks=False,
                 # Set drawstyle to "steps-post" to draw step plots
                 drawstyle='default',
                 # bars() options -----------------------------------------------
                 barstack=True, barwidth=None, baraxis='left',
                 total_barwidth=None,
                 barlinewidth=None,
                 baredgecolor='black',
                 # area() options -----------------------------------------------
                 areastack=True, areaaxis='left',
                 arealinewidth=None,
                 areaedgecolor='none',
                 alpha=1,
                 # title options ------------------------------------------------
                 title=None,
                 subtitle = None,
                 # h/vlines, h/vrects, texts, arrows ----------------------------
                 hlines=None, vlines=None, hrects=None, vrects=None, fills=None, texts=None, arrows=None,
                 xtitle='', ytitle='',
                 xtitlesize=14, ytitlesize=14,
                 xtickfontsize=14, ytickfontsize=14,
                 xticklength=None, yticklength=None,
                 xtickangle=0,
                 nxticks=7,
                 # individual look of each column in data
                 attrs=None,
                 xrange=None, yrange=None, ryrange=None,
                 xformat='auto',
                 margins='auto',
                 width=10, height=6,
                 topxaxis='left',
                 # legend options -----------------------------------------------
                 ncol_legend=1,
                 legend_spacing=0.5,
                 legend_fontsize=14,
                 legend_header='', legend_header_color='black', legend_header_fontsize=16,
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

        # Set colorcycle using iterable of colors if specified
        if colorcycle is not None:
            self.colorcycle = itertools.cycle([c for c in colorcycle])
        # Otherwise default to style file
        else:
            prop_cycle = [v['color'] for v in plt.rcParams['axes.prop_cycle']]
            self.colorcycle = itertools.cycle(prop_cycle)

        # Set global linewidth, default is None.
        self.linewidth = linewidth

        # Set global line drawstyle
        self.drawstyle = drawstyle
        
        # If barlinewidth was specified, use it
        if barlinewidth is not None:
            self.barlinewidth = barlinewidth
        # Otherwise get from style
        else:
            self.barlinewidth = matplotlib.rcParams['patch.linewidth']
        self.baredgecolor = baredgecolor

        # If arealinewidth was specified, use it
        if arealinewidth is not None:
            self.arealinewidth = arealinewidth
        # Otherwise get from style
        else:
            self.arealinewidth = matplotlib.rcParams['patch.linewidth']
        self.areaedgecolor = areaedgecolor

        self.alpha = alpha
        
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
        self.margins = margins

        # self.legend is None while it does not exist or
        # if show_legend=False or set_legend(show=False) is called.
        self.legend = None
        self.ncol_legend = ncol_legend
        self.legend_fontsize = legend_fontsize
        self.legend_header = legend_header
        self.legend_header_color = legend_header_color
        self.legend_header_fontsize = legend_header_fontsize

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

        # Set self.xaxis_type based on data
        self.xaxis_type = self._set_xaxis_type()
        
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
        self._trim_data(self.xrange, debug=self.debug)

        # Set whether to allow breaks in line charts.
        # If linebreaks is True, NA values will have a break in lines.
        self.linebreaks = linebreaks
        
        # Set x-axis range.
        if self.data is not None:
            self.set_xrange(self.xrange, self.margins)

        # Set y-axis ranges if specified.
        # If yrange is None, keep as None instead of passing through _parse_yrange()
        # which will set it to (None, None), and when used set the y-axis range to
        # Matplotlib's default (0, 1).
        # Below, self.yrange and self.ryrange are always set,
        # and if None is passed in, they remain None.
        self.yrange = yrange
        if yrange is not None:
            self.yrange = self._parse_yrange(yrange)
            self.set_yrange(self.yrange)

        self.ryrange = ryrange
        if ryrange is not None:
            self.ryrange = self._parse_yrange(ryrange)
            self.set_ryrange(self.ryrange)
            
            
        # Set x-axis formatting
        self.set_xaxis_format()

        # Set number of x-axis ticks
        if self.xaxis_type == 'datetime':
            self.set_nxticks(self.nxticks)

        # Set which x-axis is drawn on top
        self.set_top_xaxis(self.topxaxis)
                
        # ---------------------------------------------------------------------------------------------------
        # Draw area, bars, lines
        if areacols is not None:
            self.area(self.data, areacols, indexcol=self.indexcol, axis=areaaxis, colorcycle=None, alpha=self.alpha,
                      stack=areastack, linewidth=self.linewidth, edgecolor=self.areaedgecolor,
                      attrs=attrs,
                      xrange=self.xrange,
                      debug=self.debug)
            
        if barcols is not None:
            self.bars(self.data, barcols, indexcol=self.indexcol, colorcycle=None, stack=barstack, total_barwidth=total_barwidth,
                      axis=baraxis, linewidth=self.barlinewidth, edgecolor=self.baredgecolor,
                      attrs=attrs,
                      xrange=self.xrange,
                      debug=self.debug)
            
        if linecols is not None:
            self.lines(self.data, linecols, indexcol=self.indexcol, colorcycle=None,
                       linewidth=self.linewidth, linebreaks=self.linebreaks, drawstyle=self.drawstyle,
                       attrs=attrs,
                       xrange=self.xrange,
                       debug=self.debug)

        if rlinecols is not None:
            self.lines(self.data, rlinecols, indexcol=self.indexcol, axis='right', colorcycle=None,
                       linewidth=self.linewidth, linebreaks=self.linebreaks, drawstyle=self.drawstyle,
                       attrs=attrs, 
                       xrange=self.xrange,
                       debug=self.debug)
            
        # If hlines, vlines, hrects, vrects, fills, texts, arrows is given, loop over.
        # Each of these should be a list of kwargs of the form
        # [{'y' : 10, 'color' : 'red'}, ...]
        if hlines is not None:
            try:
                for hline in hlines:
                    self.hline(**hline)
            except Exception as e:
                raise RuntimeError('Could not process hlines = ' + str(hlines) + ' with exception:' + str(e))

        if vlines is not None:
            try:
                for vline in vlines:
                    self.vline(**vline)
            except Exception as e:
                raise RuntimeError('Could not process vlines = ' + str(vlines) + ' with exception:' + str(e))

        if hrects is not None:
            try:
                for hrect in hrects:
                    self.hrect(**hrect)
            except Exception as e:
                raise RuntimeError('Could not process hrects = ' + str(hrects) + ' with exception:' + str(e))

        if vrects is not None:
            try:
                for vrect in vrects:
                    self.vrect(**vrect)
            except Exception as e:
                raise RuntimeError('Could not process vrects = ' + str(vrects) + ' with exception:' + str(e))

        if fills is not None:
            try:
                for fill in fills:
                    self.fill(**fill)
            except Exception as e:
                raise RuntimeError('Could not process fills = ' + str(fills) + ' with exception:' + str(e))
            
        if texts is not None:
            try:
                for text in texts:
                    self.text(**text)
            except Exception as e:
                raise RuntimeError('Could not process texts = ' + str(texts) + ' with exception:' + str(e))

        if arrows is not None:
            try:
                for arrow in arrows:
                    self.arrow(**arrow)
            except Exception as e:
                raise RuntimeError('Could not process arrows = ' + str(arrows) + ' with exception:' + str(e))

        # Create legend
        if self.debug:
            print('self.legend_entries:')
            print(self.legend_entries)
            print('self.legend_labels:')
            print(self.legend_labels)
        if self.show_legend:
            self.update_legend()

    def apply(self, style):
        '''
        Apply style to this Chart.
        '''
        
        pass

    def _set_xaxis_type(self):

        # Check whether index of data is datetime
        if self.data is not None and type(self.data) == pd.DataFrame:
            # Try to convert to datetime axis
            try:
                # Ignore pandas warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    self.data.index = pd.to_datetime(self.data.index)
                xaxis_type = 'datetime'
            except:
                pass
            
            idx_types = {type(idx) for idx in self.data.index}
            if idx_types in [{pd.Timestamp}, {pd.Period}]:
                xaxis_type = 'datetime'
            elif idx_types in [{int}, {float}]: 
                xaxis_type = 'numerical'
            else:
                xaxis_type = 'categorical'
        else:
            xaxis_type = None

        self.xaxis_type = xaxis_type
            
        # Return so it is clear what was set
        return xaxis_type

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

    def _trim_data(self, xrange, debug=False):
        '''
        Trim self.data using xrange.
        '''

        if debug:
            print('start of _trim_data() for data:')
            print(self.data)
            print('xrange = ' + str(xrange))
        
        
        if type(self.data) == pd.DataFrame:
            if xrange[0] is None and xrange[1] is None:
                # Don't trim if nothing specified
                pass
            elif xrange[0] is None:
                # Trim start only
                self.data = self.data.loc[:str(xrange[1]), :]
            elif xrange[1] is None:
                # Trim end only
                self.data = self.data.loc[str(xrange[0]):, :]
            else:
                # Trim both
                self.data = self.data.loc[str(xrange[0]):str(xrange[1]), :]

            if debug:
                print('After applying trim, self.data:')
                print(self.data)

    def set_title(self, title, loc='left', y=1.05, fontweight='bold', fontname='Segoe UI'):
        if title is not None:
            self.title = str(title)
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
            print('start of set_xrange() for xrange = ' + str(xrange) + ', margins = ' + str(margins))
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
        elif self.xaxis_type is None:
            return None
        else:
            print('self.xaxis_type of ' + str(self.axis_type) + ' not implemented for set_xrange()')
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

    def set_xaxis_format(self, xformat=None, debug=False):
        '''
        Set formatting for datetime x-axis.
        `formatter` should be something like a
        mdates.DateFormatter().

        if xformat is specified, uses it to set formatting.
        If default `auto` is chosen, freq of data is used.
        Specify special options "D", "W", "M", "Q", "A" to set to these frequencies.
        '''

        if debug:
            print('Start of set_xaxis_format()')

        # If xformat is given use it, otherwise use self.xformat
        if xformat is not None:
            pass
        else:
            xformat = self.xformat

        if debug:
            print('xformat = ' + str(xformat))

        # If self.xaxis_type is not "datetime", skip
        if self.xaxis_type != 'datetime':
            if debug:
                print('self.xaxis_type = ' + str(self.xaxis_type) + ', returning')
            return

        # If default, guess from freq of data.
        if xformat == 'auto':
            # If no data is set, don't try to set
            if self.data is None:
                return
            
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
            elif self.data is None:
                # If no data is set, format of x-axis is not set.
                formatter = None
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
            print('set_xaxis_format():')
            print('xformat of "' + str(xformat) + '" of type ' + str(type(xformat)) + ' not allowed')
            sys.exit()

        if formatter is not None:
            self.ax.xaxis.set_major_formatter(formatter)

    def lines(self, data=None, cols=None, indexcol=None, axis='left', colorcycle=None, linewidth=None, linebreaks=False, drawstyle=None,
              attrs=None,
              xrange=None, margins=None, xformat=None, yrange=None, ryrange=None,
              debug=False):
        '''
        Add line to chart
        '''

        if debug:
            print('Calling add_lines on "' + str(cols) + '"')

        # Set data.
        # If not specified use self.data.
        if data is None:
            data = self.data

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
            
        linecols = _parse_cols(cols)
        # Don't try to plot indexcol if it was given since this is now the index
        if indexcol is not None:
            if indexcol in linecols:
                linecols.remove(indexcol)
        if debug:
            print('linecols:')
            print(linecols)

        # If no data and/or linecols are available, finish.
        if data is None:
            if linecols == []:
                print('WARNING: no data given to lines()')
            else:
                print('WARNING: no data given to lines() but linecols given as ' + str(linecols))
            print('No lines will be added')
            return

        # Set self.data to be input data
        self.data = data
        # Set self.xaxis_type from self.data
        self.xaxis_type = self._set_xaxis_type()
        if debug:
            print('self.xaxis_type = ' + str(self.xaxis_type))
            
        # Set x-axis limits if specified, or use default
        if xrange is not None:
            xrange = self._parse_xrange(xrange, debug=debug)
            self.xrange = xrange
        else:
            xrange = self.xrange
        if debug:
            print('xrange:')
            print(xrange)
            
        # Trim data as needed            
        self._trim_data(xrange, debug=debug)
        if debug:
            print(self.data)

        # Create cycle if specified.
        if colorcycle is not None:
            cycle = itertools.cycle([c for c in colorcycle])
        # Otherwise use defaults
        else:
            cycle = self.colorcycle
            
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
            _linewidth = matplotlib.rcParams['lines.linewidth']
            # If linewidth was specified as function input, use it
            if linewidth is not None:
                _linewidth = linewidth

            # If drawstyle is specified use it
            if drawstyle is not None:
                _drawstyle = drawstyle
            else:
                _drawstyle = self.drawstyle
            
            linestyle = matplotlib.rcParams['lines.linestyle']
            # Initialize color as None
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
                    _linewidth = _attrs['linewidth']

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

                if 'drawstyle' in _attrs:
                    _drawstyle = _attrs['drawstyle']
                    

                if 'dashes' in _attrs:
                    dashes = _attrs['dashes']
                    
                if 'dash_capstyle' in _attrs:
                    dash_capstyle = _attrs['dash_capstyle']

                if 'legend' in _attrs:
                    legend = _attrs['legend']
            # end of linecol is in attrs

            # If color was not specified from attrs, get from color cycle
            if color is None:
                color = next(cycle)

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
                _ax = self.ax
            elif axis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                _ax = self.ax_right
            else:
                print('axis must be left or right, given ' + str(axis))
                raise VaueError

            # Allow iteration over multiple markers into one legend
            entries = []
                
            if marker is None:
                if dashes or dash_capstyle:
                    entry = _ax.plot(_df.index, _df[linecol], label=linecol,
                                     markersize=markersize, marker=marker,
                                     markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                     markeredgewidth=markeredgewidth,
                                     drawstyle=_drawstyle,
                                     linestyle=linestyle, linewidth=_linewidth, color=color,
                                     dashes=dashes, dash_capstyle=dash_capstyle)
                else:
                    entry = _ax.plot(_df.index, _df[linecol], label=linecol,
                                     markersize=markersize, marker=marker,
                                     markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                     markeredgewidth=markeredgewidth,
                                     drawstyle=_drawstyle,
                                     linestyle=linestyle, linewidth=_linewidth, color=color)
                entries.append(entry[0])
            else:
                # Iterate over all specified markers and put in one legend entry
                for _marker in marker:
                    if dashes or dash_capstyle:
                        entry = _ax.plot(_df.index, _df[linecol], label=linecol,
                                         markersize=markersize, marker=_marker,
                                         markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                         markeredgewidth=markeredgewidth,
                                         linestyle=linestyle, linewidth=_linewidth, color=color,
                                         drawstyle=_drawstyle,
                                         dashes=dashes, dash_capstyle=dash_capstyle)
                    else:
                        entry = _ax.plot(_df.index, _df[linecol], label=linecol,
                                         markersize=markersize, marker=_marker,
                                         markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                         markeredgewidth=markeredgewidth,
                                         drawstyle=_drawstyle,
                                         linestyle=linestyle, linewidth=_linewidth, color=color)
                        
                    if legend:
                        entries.append(entry[0])
                # end of loop over marker
                
            if legend:
                self.legend_entries.append(tuple(entries))
                self.legend_labels.append(linecol)
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
            # If margins is specified, set it for this chart and use it.
            if margins is not None:
                self.margins = margins
            self.set_xrange(xrange, margins=self.margins, debug=debug)
            if debug:
                print('after calling set_xrange():')
                print(self.xrange)

        # Set xaxis format.
        # If xformat was specified use it, otherwise use self.xformat
        if xformat is None:
            xformat = self.xformat
        self.set_xaxis_format(xformat=xformat, debug=debug)
        
        # Set number of x-axis ticks
        if self.xaxis_type == 'datetime':
            if debug:
                print('self.nxticks = ' + str(self.nxticks))
            self.set_nxticks(self.nxticks)

        # Set which x-axis is drawn on top
        self.set_top_xaxis(self.topxaxis)

        # If yrange is specified use it, otherwise use self.yrange
        if axis == 'left':
            if yrange is None:
                if getattr(self, 'yrange', None) is not None:
                    yrange = self.yrange

            if yrange is not None:
                self.yrange = self._parse_yrange(yrange)
                self.set_yrange(self.yrange)
        if axis == 'right':
            if ryrange is None:
                if getattr(self, 'ryrange', None) is not None:
                    ryrange = self.ryrange
                    
            if ryrange is not None:
                self.ryrange = self._parse_yrange(ryrange)
                self.set_ryrange(self.ryrange)

    def bars(self, data=None, cols=None, indexcol=None, axis='left', colorcycle=None,
             stack=True, total_barwidth=None, linewidth=None, edgecolor=None,
             attrs=None,
             xrange=None, margins=None, xformat=None, yrange=None, ryrange=None,
             debug=False):
        '''
        Add bar to chart
        '''

        if debug:
            print('Calling bars on "' + str(cols) + '"')

        # Set data.
        # If not specified use self.data.
        if data is None:
            data = self.data
            
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
                
        barcols = _parse_cols(cols)
        # Don't try to plot indexcol if it was given since this is now the index
        if indexcol is not None:
            if indexcol in barcols:
                barcols.remove(indexcol)
        if debug:
            print('barcols:')
            print(barcols)

        # If no data and/or linecols are available, finish.
        if data is None:
            if barcols == []:
                print('WARNING: no data given to bars()')
            else:
                print('WARNING: no data given to bars() but barcols given as ' + str(barcols))
            print('No bars will be added')
            return

        # Set self.data to be input data
        self.data = data
        # Set self.xaxis_type from self.data
        self.xaxis_type = self._set_xaxis_type()
        if debug:
            print('self.xaxis_type = ' + str(self.xaxis_type))

        # Set x-axis limits if specified, or use default
        if xrange is not None:
            xrange = self._parse_xrange(xrange, debug=debug)
            self.xrange = xrange
        else:
            xrange = self.xrange
        if debug:
            print('xrange:')
            print(xrange)
            
        # Trim data as needed            
        self._trim_data(xrange, debug=debug)
        if debug:
            print(self.data)
            
        # Line width of bar borders for all bars.
        # If specified as input arg, use
        if linewidth is not None:
            _linewidth = linewidth
        # Otherwise use class settings
        else:
            _linewidth = self.linewidth
        
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
        # Create cycle if specified.
        if colorcycle is not None:
            cycle = itertools.cycle([c for c in colorcycle])
        # Otherwise use defaults
        else:
            cycle = self.colorcycle
        if debug:
            print('cycle:')
            print(cycle)
            
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
            hatchcolor = matplotlib.rcParams['patch.edgecolor']
            hatch = None
            hatchwidth = matplotlib.rcParams['hatch.linewidth']
            # Local copy for this column, can be overwritten with attrs
            # If edgecolor has not been set, use default
            if edgecolor is None:
                _edgecolor = self.baredgecolor
            else:
                _edgecolor = edgecolor

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
                if 'hatchcolor' in _attrs:
                    hatchcolor = _attrs['hatchcolor']

                # Hatch pattern in bars
                if 'hatch' in _attrs:
                    hatch = _attrs['hatch']

                # Line width of hatches
                if 'hatchwidth' in _attrs:
                    hatchwidth = _attrs['hatchwidth']

                # Color of bar edges
                if 'edgecolor' in _attrs:
                    _edgecolor = _attrs['edgecolor']
                    
                # If offset is specified for when stack=False, use it
                if 'offset' in _attrs:
                    offset = _attrs['offset']
                    offset_specified = True

                # If barwidth is specified, use it
                if 'width' in _attrs:
                    width = _attrs['width']
                    
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
                if debug:
                    print('1. setting color for ' + barcol + ' to ' + color)
            else:
                color = next(cycle)

            if debug:
                if attrs is not None and barcol in attrs:
                    print('attrs:')
                    print(attrs[barcol])
                print('hatch = ' + str(hatch))
                print('linewidth = ' + str(_linewidth))
                print('_edgecolor = ' + str(_edgecolor))
                print('hatchcolor = ' + str(hatchcolor))
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
            
            if axis == 'left':
                _ax = self.ax
            elif axis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                _ax = self.ax_right
            else:
                print('axis must be left or right, given ' + str(axis))
                raise VaueError
                
            if stack:
                # No direct way to set hatch line widths in ax.bar,
                # need to use plt.rc_context()
                with plt.rc_context({"hatch.linewidth": hatchwidth}):
                    if ibarcol == 0:
                        # Draw negative first
                        entry = _ax.bar(self.data.index, _df_neg[barcol],
                                        width=barwidth, color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0,
                                        zorder=1, label=barcol)
                        # Draw positive
                        entry = _ax.bar(self.data.index, _df_pos[barcol],
                                        width=barwidth, color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0,
                                        zorder=1, label=barcol)
                    else:
                        # Draw negative first
                        entry = _ax.bar(self.data.index, _df_neg[barcol],
                                        bottom=neg_offset,
                                        width=barwidth, color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0,
                                        zorder=1, label=barcol)
                        # Draw positive
                        entry = _ax.bar(self.data.index, _df_pos[barcol],
                                        bottom=pos_offset,
                                        width=barwidth, color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0,
                                        zorder=1, label=barcol)
                            
                    # Draw again with _edgecolor
                    entry2 = _ax.bar(self.data.index, _df_pos[barcol],
                                     width=barwidth, color='none', edgecolor=_edgecolor, linewidth=_linewidth,
                                     bottom=pos_offset,
                                     zorder=2)
                    _ = _ax.bar(self.data.index, _df_neg[barcol],
                                bottom=neg_offset,
                                width=barwidth, color='none', edgecolor=_edgecolor, linewidth=_linewidth,
                                zorder=2)
                    
                    # If barcolors was specified, get all patches for this barcol,
                    # and if the index matches, set color for the corresponding bar.
                    patches = [p for p in _ax.patches if p not in previous_patches]
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
                entry = _ax.bar(_x, self.data[barcol],
                                width=barwidth, color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0,
                                zorder=1, label=barcol)
                
                # Draw again with _edgecolor
                entry2 = _ax.bar(_x, self.data[barcol],
                                 width=barwidth, color='none', edgecolor=_edgecolor, linewidth=_linewidth,
                                 zorder=2)
                    
                # Set x-axis categories from self.data.index
                _ax.set_xticks(np.arange(len(self.data)), labels=self.data.index)

                # If barcolors was specified, get all patches for this barcol,
                # and if the index matches, set color for the corresponding bar.
                patches = [p for p in _ax.patches if p not in previous_patches]
                if debug:
                    print('len(patches) = ' + str(len(patches)))

                # Add individually specified colors
                if barcolors is not None:
                    color_bars(barcolors, patches, self.data.index, stack=False, debug=debug)
                        
                # Add current patches to previous_patches
                previous_patches += patches
                    
            # end of stack=False
            
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
            if debug:
                print('before calling set_xrange()')
                print(xrange)
            # If margins is specified, set it for this chart and use it.
            if margins is not None:
                self.margins = margins
            self.set_xrange(xrange, margins=self.margins, debug=debug)
            if debug:
                print('after calling set_xrange():')
                print(self.xrange)

        # Set xaxis format.
        # If xformat was specified use it, otherwise use self.xformat
        if xformat is None:
            xformat = self.xformat
        self.set_xaxis_format(xformat=xformat, debug=debug)
        
        # Set number of x-axis ticks
        if self.xaxis_type == 'datetime':
            if debug:
                print('self.nxticks = ' + str(self.nxticks))
            self.set_nxticks(self.nxticks)

        # Set which x-axis is drawn on top
        self.set_top_xaxis(self.topxaxis)

        # If yrange is specified use it, otherwise use self.yrange
        if axis == 'left':
            if yrange is None:
                if getattr(self, 'yrange', None) is not None:
                    yrange = self.yrange

            if yrange is not None:
                self.yrange = self._parse_yrange(yrange)
                self.set_yrange(self.yrange)
        if axis == 'right':
            if ryrange is None:
                if getattr(self, 'ryrange', None) is not None:
                    ryrange = self.ryrange
                    
            if ryrange is not None:
                self.ryrange = self._parse_yrange(ryrange)
                self.set_ryrange(self.ryrange)

    def area(self, data=None, cols=None, indexcol=None, axis='left', colorcycle=None, alpha=1,
             stack=True, linewidth=None, edgecolor=None,
             attrs=None,
             xrange=None, margins=0, xformat=None, yrange=None, ryrange=None,
             debug=False):
        '''
        Add area to chart
        '''

        if debug:
            print('Calling area on "' + str(cols) + '"')
            
        # Set data.
        # If not specified use self.data.
        if data is None:
            data = self.data
            
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
                
        areacols = _parse_cols(cols)
        # Don't try to plot indexcol if it was given since this is now the index
        if indexcol is not None:
            if indexcol in areacols:
                areacols.remove(indexcol)
        if debug:
            print('areacols:')
            print(areacols)

        # If no data and/or areacols are available, finish.
        if data is None:
            if areacols == []:
                print('WARNING: no data given to areas()')
            else:
                print('WARNING: no data given to areas() but areacols given as ' + str(areacols))
            print('No areas will be added')
            return

        # Line width of area borders for all areas.
        # If specified as input arg, use
        if linewidth is not None:
            _linewidth = linewidth
        # Otherwise use class settings
        else:
            _linewidth = self.arealinewidth
            
        # Set self.data to be input data
        self.data = data
        # Set self.xaxis_type from self.data
        self.xaxis_type = self._set_xaxis_type()
        if debug:
            print('self.xaxis_type = ' + str(self.xaxis_type))
            
        # Set x-axis limits if specified, or use default
        if xrange is not None:
            xrange = self._parse_xrange(xrange, debug=debug)
            self.xrange = xrange
        else:
            xrange = self.xrange
        if debug:
            print('xrange:')
            print(xrange)
            
        # Trim data as needed            
        self._trim_data(xrange, debug=debug)
        if debug:
            print(self.data)

        # Iterate over areacols and plot each area.
        # Create cycle if specified.
        if colorcycle is not None:
            cycle = itertools.cycle([c for c in colorcycle])
        # Otherwise use defaults
        else:
            cycle = self.colorcycle
        if debug:
            print('cycle:')
            print(cycle)
            
        # Need to keep track of positive and negative offsets if stacked.
        pos_offset = [0] * len(self.data)
        neg_offset = [0] * len(self.data)

        # Keep track of whether any negative area exists.
        # If no negative area exists, then set min yrange to 0 at end.
        has_negative = False

        for iareacol, areacol in enumerate(areacols):
            if debug:
                print('-' * 40)
                print('areacol = "' + areacol + '"')
                
            if areacol not in data.columns:
                print('"' + areacol + '" is not in data')
                raise ValueError

            # Get default settings from stylefile
            # The patch.edgecolor is used for both the hatch line color
            # and the area edge color.
            # For IMF charts use this as the hatch line color
            # and draw area again with edgecolor set to black.
            hatchcolor = matplotlib.rcParams['patch.edgecolor']
            hatch = None
            hatchwidth = matplotlib.rcParams['hatch.linewidth']
            # Local copy for this column, can be overwritten with attrs
            # If areaedgecolor has not been set, use default
            if edgecolor is None:
                _edgecolor = self.areaedgecolor
            else:
                _edgecolor = edgecolor

            # Add legend for this entry
            legend = True

            # alpha
            if alpha is None:
                _alpha = self.alpha
            else:
                _alpha = alpha

            # Get any attributes that were assigned to this column
            if attrs is not None and areacol in attrs:
                # This should be a dict containing attributes for this column
                _attrs = attrs[areacol]
                if debug:
                    print(_attrs)

                # If any were specified, overwrite stylefile

                # Hatch colors
                if 'hatchcolor' in _attrs:
                    hatchcolor = _attrs['hatchcolor']

                # Hatch pattern in area
                if 'hatch' in _attrs:
                    hatch = _attrs['hatch']

                # Line width of hatches
                if 'hatchwidth' in _attrs:
                    hatchwidth = _attrs['hatchwidth']

                # Color of area edges
                if 'edgecolor' in _attrs:
                    _edgecolor = _attrs['edgecolor']

                # alpha
                if 'alpha' in _attrs:
                    _alpha = _attrs['alpha']
                    
                # Add legend entry
                if 'legend' in _attrs:
                    legend = _attrs['legend']

            # end of attrs existing for this areacol

            # For color, if it is specified use it,
            # otherwise get the next color from the color cycle.
            if attrs is not None and areacol in attrs and 'color' in attrs[areacol]:
                color = attrs[areacol]['color']
                if debug:
                    print('1. setting color for ' + areacol + ' to ' + color)
            else:
                color = next(cycle)

            if debug:
                if attrs is not None and areacol in attrs:
                    print('attrs:')
                    print(attrs[areacol])
                print('hatch = ' + str(hatch))
                print('_edgecolor = ' + str(_edgecolor))
                print('hatchcolor = ' + str(hatchcolor))
                print('color = ' + str(color))

            # Make copy of positive and negative parts
            # (for area chart we should not have negative parts).
            # Set mask to NA so that they don't show up with lines in the chart,
            # but when saving to pos_offset and neg_offset, set values to 0.
            _df_pos = self.data[[areacol]].copy()
            mask = _df_pos[areacol] < 0
            _df_pos.loc[mask, areacol] = np.nan
                
            _df_neg = self.data[[areacol]].copy()
            mask = _df_neg[areacol] > 0
            _df_neg.loc[mask, areacol] = np.nan

            if len(_df_neg[areacol].dropna()) > 0:
                has_negative = True

            if axis == 'left':
                _ax = self.ax
            elif axis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                _ax = self.ax_right
            else:
                print('axis must be left or right, given ' + str(axis))
                raise VaueError
                    
            if stack:
                # No direct way to set hatch line widths in ax.area,
                # need to use plt.rc_context()
                with plt.rc_context({"hatch.linewidth": hatchwidth}):
                    # Draw without line edges
                    # Draw negative first
                    entry = _ax.fill_between(self.data.index, y1=_df_neg[areacol] + neg_offset, y2=neg_offset,
                                             color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0, alpha=_alpha,
                                             zorder=1, label=areacol)
                    # Draw positive
                    entry = _ax.fill_between(self.data.index, y1=_df_pos[areacol] + pos_offset, y2=pos_offset,
                                             color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0, alpha=_alpha,
                                             zorder=1, label=areacol)
                        
                    # Draw again with _edgecolor
                    # positive
                    entry2 = _ax.fill_between(self.data.index, y1=_df_pos[areacol] + pos_offset, y2=pos_offset,
                                              color='none', edgecolor=_edgecolor, linewidth=_linewidth, alpha=_alpha,
                                              zorder=2)
                    # negative
                    _ = _ax.fill_between(self.data.index, y1=_df_neg[areacol] + neg_offset, y2=neg_offset,
                                         color='none', edgecolor=_edgecolor, linewidth=_linewidth, alpha=_alpha,
                                         zorder=2)

                # end of plt.rc_context()
            # end of stack
            else:
                # Draw once without edgecolor
                entry = _ax.fill_between(self.data.index, y1=self.data[areacol], y2=0,
                                         color=color, edgecolor=hatchcolor, hatch=hatch, linewidth=0, alpha=_alpha,
                                         zorder=1, label=areacol)
                
                # Draw again with _edgecolor
                entry2 = _ax.fill_between(self.data.index, y1=self.data[areacol], y2=0,
                                          color='none', edgecolor=_edgecolor, linewidth=_linewidth, alpha=_alpha,
                                          zorder=2)
                    
                # Set x-axis categories from self.data.index
                _ax.set_xticks(np.arange(len(self.data)), labels=self.data.index)
            # end of stack=False
            
            # Adjust offsets
            neg_offset += _df_neg[areacol].replace(np.nan, 0).values
            pos_offset += _df_pos[areacol].replace(np.nan, 0).values

            if debug:
                print('pos_offset:')
                print(pos_offset)
                print('neg_offset:')
                print(neg_offset)

            # If adding to legend
            if legend:
                # Create a Patch that has the same characteristics
                # that can be added to the legend entries.
                entry = Patch(
                    facecolor=color,
                    edgecolor=_edgecolor,
                    hatch=hatch,
                    alpha=_alpha,
                    label=areacols)
                self.legend_entries.append(entry)
                self.legend_labels.append(areacol)
        # end of loop over areacols

        # Re-create legend
        if self.show_legend:
            self.update_legend()
        
        # Set x-axis range if specified.
        # For area, default is to set margins=0 so that the are chart
        # does not look like it was chopped off at the edges.
        # To have same behavior as lines etc., use margins='auto'.
        if xrange is not None:
            if debug:
                print('before calling set_xrange()')
                print(xrange)
            # If margins is specified, set it for this chart and use it.
            if margins is not None:
                self.margins = margins
            self.set_xrange(xrange, margins=self.margins, debug=debug)
            if debug:
                print('after calling set_xrange():')
                print(self.xrange)

        # Set xaxis format.
        # If xformat was specified use it, otherwise use self.xformat
        if xformat is None:
            xformat = self.xformat
        self.set_xaxis_format(xformat=xformat, debug=debug)
        
        # Set number of x-axis ticks
        if self.xaxis_type == 'datetime':
            if debug:
                print('self.nxticks = ' + str(self.nxticks))
            self.set_nxticks(self.nxticks)

        # Set which x-axis is drawn on top
        self.set_top_xaxis(self.topxaxis)

        # If yrange is specified use it, otherwise use self.yrange
        if axis == 'left':
            if yrange is None:
                if getattr(self, 'yrange', None) is not None:
                    yrange = self.yrange

            if yrange is not None:
                self.yrange = self._parse_yrange(yrange)
                self.set_yrange(self.yrange)

            # If no yrange is given and data is all above 0,
            # set y-axis min to 0
            if yrange is None and not has_negative:
                self.ax.set_ylim(bottom=0)
                
        if axis == 'right':
            if ryrange is None:
                if getattr(self, 'ryrange', None) is not None:
                    ryrange = self.ryrange
                    
            if ryrange is not None:
                self.ryrange = self._parse_yrange(ryrange)
                self.set_ryrange(self.ryrange)

            # If no yrange is given and data is all above 0,
            # set y-axis min to 0
            if ryrange is None and not has_negative:
                self.ax_right.set_ylim(bottom=0)
                
    def scatter(self, data, cols, indexcol=None, attrs=None, debug=False):
        '''
        Add scatter to chart
        '''

        if debug:
            print('Calling scatter on "' + str(cols) + '"')

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

    def hline(self, y, xrange=None, coordinates='data', color='red', linewidth=1, linestyle='-', alpha=1, dashes=None, dash_capstyle=None,
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
            
    def vline(self, x, yrange=None, coordinates='data', width=1, color='red', linewidth=1, linestyle='-', alpha=1, dashes=None, dash_capstyle=None,
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
                
    def hrect(self, ymin=0, ymax=0, xrange=None, coordinates='data', color='red', linecolor='none', linewidth=0, linestyle='-', alpha=0.3,
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
                alpha=alpha,
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

    def vrect(self, xmin=0, xmax=0, yrange=None, coordinates='data', color='red', linecolor='none', linewidth=0, linestyle='-', alpha=0.3,
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
                alpha=alpha,
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

    def text(self, x, y, text='', xycoords='data', color='black',
             fontsize=14, fontfamily='Segoe UI', fontweight='normal',
             va='top', ha='left', **kwargs):
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
    
    def arrow(self, head=(0, 0), tail=(1, 1),
              color='black', width=4, headwidth=15, headlength=15, shrink=0.05, arrowstyle='->', edgecolor=None, edgewidth=0,
              va='top', ha='left',
              text='', xycoords='data', textcoords='data', **kwargs):
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

    def fill(self, lo, hi, data=None, indexcol=None, axis='left',
             color='red', linecolor='none', linewidth=0, linestyle='-', alpha=0.3,
             dash_capstyle=None,
             hatch=None, # hatchlinewidth=None,
             label='', legend=False,
             zorder=1,
             debug=False, **kwarg):

        # Set data if specified
        if data is not None:
            if type(data) != pd.DataFrame:
                raise RuntimeError('fill(): data must be pd.DataFrame, given ' + str(data) + ' of type ' + str(type(data)))
            self.data = data
            if indexcol:
                if indexcol not in self.data.columns:
                    raise RuntimeError('indexcol specified as "' + str(indexcol) + '" but not found in data:' + str(data))
                self.data.set_index(indexcol, inplace=True)

        # Check lo and hi are valid columns in self.data
        if lo not in self.data.columns:
            raise RuntimeError('lo specified as "' + str(lo) + '" but not found in data:' + str(data))
        if hi not in self.data.columns:
            raise RuntimeError('hi specified as "' + str(hi) + '" but not found in data:' + str(data))

        if axis == 'left':
            if dash_capstyle:
                entry = self.ax.fill_between(self.data.index, self.data[lo], self.data[hi],
                                             facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                             hatch=hatch,
                                             zorder=zorder,
                                             dash_capstyle=dash_capstyle)
                # no dash_capstyle specified
            else:
                entry = self.ax.fill_between(self.data.index, self.data[lo], self.data[hi],
                                             facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                             hatch=hatch,
                                             zorder=zorder)
        else:
            if self.ax_right is None:
                self.ax_right = self.ax.twinx()
                # Set color cycler to be common with the left y-axis.
                # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                self.ax_right._get_lines = self.ax._get_lines

            if dash_capstyle:
                entry = self.ax_right.fill_between(self.data.index, self.data[lo], self.data[hi],
                                                   facecolor=color, linewidth=linewidth, edgecolor=linecolor, linestyle=linestyle, alpha=alpha,
                                                   hatch=hatch,
                                                   zorder=zorder,
                                                   dash_capstyle=dash_capstyle)
                # no dash_capstyle specified
            else:
                entry = self.ax_right.fill_between(self.data.index, self.data[lo], self.data[hi],
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
                alpha=alpha,
                label=label)
            self.legend_entries.append(entry)
            self.legend_labels.append(label)

        # Re-create legend
        if self.show_legend:
            self.update_legend()
            if debug:
                print('called update_legend()')
            
    def update_legend(self,
                      ncol_legend=None, legend_spacing=None,
                      legend_left=None, legend_bottom=None, legend_width=None, legend_height=None, legend_mode=None, adjust=True,
                      legend_header=None, legend_header_color=None, legend_header_fontsize=None):
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
        if legend_header is None:
            legend_header = self.legend_header
        if legend_header_color is None:
            legend_header_color = self.legend_header_color
        if legend_header_fontsize is None:
            legend_header_fontsize = self.legend_header_fontsize

        # Make sure legend_left + legend_width is less than 1,
        # otherwise we are left with long white margin on right side.
        if adjust:
            if legend_left + legend_width > 1:
                legend_width = 1 - legend_left
                self.legend_width = legend_width
        
        self.legend = self.ax.legend(self.legend_entries, self.legend_labels,
                                     loc='upper left',
                                     labelspacing=legend_spacing,
                                     bbox_transform=self.ax.transAxes,
                                     bbox_to_anchor=(legend_left,legend_bottom,legend_width,legend_height),
                                     mode=legend_mode, borderaxespad=0,
                                     ncol=ncol_legend, fontsize=self.legend_fontsize, frameon=False,
                                     title=self.legend_header, alignment='left', title_fontsize=self.legend_header_fontsize,
                                     numpoints=1
        )

        # Need to set legend title color
        self.legend.get_title().set_color(self.legend_header_color)

        # Need to set 

    def set_legend(self, show=True):
        '''
        Show legend.
        If show=False, don't show and delete existing legend.
        '''

        # Modify self.show_legend
        if show:
            self.show_legend = True

            # Create legend if it does not exist
            if not self.legend:
                self.update_legend()
                
        else:
            self.show_legend = False

            # If a legend already exists, delete
            if self.legend:
                try:
                    self.ax.get_legend().remove()
                    self.legend = None
                except Exception as e:
                    print('WARNING: Could not remove existing legend with exception:')
                    print(e)
        
    def save(self, filename, dpi=250, pad_inches=0.02):
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
            self.fig.savefig(filename, dpi=dpi, bbox_inches="tight", pad_inches=pad_inches)
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
