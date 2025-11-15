'''
2025-10-05

Generate charts.
'''

import os
import sys

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

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

    # If df is None, return 'A', just a holder
    if df is None:
        return 'A'

    # Not enough data to check differences.
    # Return daily freq.
    if len(df) < 2:
        return 'D'
    else:
        if (df.index[1] - df.index[0]).days < 10:
            return 'D'
        elif (df.index[1] - df.index[0]).days < 32:
            return 'M'
        elif (df.index[1] - df.index[0]).days < 93:
            return 'Q'
        elif (df.index[1] - df.index[0]).days < 370:
            return 'A'
        else:
            return 'D'

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
                 stack=True, area=False, barwidth=None, baraxis='left',
                 barlinewidth=None,
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
        self.ax_right = None
        if debug:
            print('Created self.fig, self.ax')

        # Add title, subtitle
        self.set_title(self.title)
        self.set_subtitle(self.subtitle)

        # Add x, y title
        self.set_xtitle(self.xtitle, self.xtitlesize)
        self.set_ytitle(self.ytitle, self.ytitlesize)

        # Set x, y tick font size
        self.set_xticks(size=self.xtickfontsize)
        self.set_yticks(size=self.ytickfontsize)

        # Get xrange and trim data as needed
        self.xrange = self._parse_xrange(xrange)
        self._trim_data(self.xrange)

        # ---------------------------------------------------------------------------------------------------
        # Draw lines, bars
        if barcols is not None:
            barcols = _parse_cols(barcols)
            self.add_bars(self.data, barcols, stack=stack, baraxis=baraxis, xrange=self.xrange, barlinewidth=barlinewidth,
                          dict_attrs=dict_attrs, debug=True)
            
        if linecols is not None:
            linecols = _parse_cols(linecols)
            self.add_lines(self.data, linecols, xrange=self.xrange, dict_attrs=dict_attrs, debug=debug)

        if rlinecols is not None:
            rlinecols = _parse_cols(rlinecols)
            self.add_lines(self.data, rlinecols, axis='right', xrange=self.xrange, dict_attrs=dict_attrs, debug=debug)
        
        # Create legend
        legend_header = ''
        if debug:
            print('self.legend_entries:')
            print(self.legend_entries)
            print('self.legend_labels:')
            print(self.legend_labels)
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

        # Set which x-axis is drawn on top
        self.set_top_xaxis(self.topxaxis)
                
    def apply(self, style):
        '''
        Apply style to this Chart.
        '''
        
        pass

    def _parse_xrange(self, xrange):
        '''
        Utility function to parse x-axis range.
        This can either be a date range or a number range.
        Returns a list of two elements, the elements are one of
        - a number
        - a str interpretible as a date
        - None
        '''

        if xrange is None:
            return [None, None]

        if type(xrange) == str and xrange.find(':') != -1:
            xrange = xrange.split(':', 1)
            xrange = [x if x != '' else None for x in xrange]

        if self.xaxis_type == 'datetime':
            try:
                xrange = [pd.Timestamp(str(x)) if x is not None else None for x in xrange]
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

    def set_title(self, title):
        if title is not None:
            self.ax.set_title(str(title), loc='left', y=1.05,
                              fontweight='bold', fontname='Segoe UI')

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
            self.ax_right.tick_params(axis='y', which='major', labelsize=size)
        
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
            elif freq == 'M':
                margins = 10
            elif freq == 'Q':
                margins = 30
            elif freq == 'A':
                margins = 60
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

        if xrange[0] is None:
            xrange[0] = self.data.index.min()
        if xrange[1] is None:
            xrange[1] = self.data.index.max()
            
        if debug:
            print('xrange before setting xlim:')
            print(xrange)

        # Trim the data based on xrange
        self._trim_data(xrange)
            
        # Try to interpret xrange as dates and add margin
        try:
            self.ax.set_xlim(pd.Timestamp(xrange[0]) - pd.Timedelta(days=margins), pd.Timestamp(xrange[1]) + pd.Timedelta(days=margins))
            if debug:
                print('Set xlim to Timestamps')
        # If fails, use xrange as-is.
        except ValueError:
            self.ax.set_xlim(xrange[0],xrange[1])
            if debug:
                print('Set xlim to xrange as-is')

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

    def add_lines(self, data, colname, axis='left', xrange=None, dict_attrs=None, debug=False):
        '''
        Add line to chart
        '''

        if debug:
            print('Calling add_lines on "' + str(colname) + '"')
            
        linecols = _parse_cols(colname)

        # Set self.data to be input data
        self.data = data
        # Set x-axis limits and trim data as needed
        if xrange is not None:
            xrange = self._parse_xrange(xrange)
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
            linecolor = None
            
            # Get any attributes that were assigned to this column
            if dict_attrs is not None and linecol in dict_attrs:
                # This should be a dict containing attributes for this column
                attrs = dict_attrs[linecol]
                if debug:
                    print(attrs)

                # If any were specified, overwrite stylefile
                if 'marker' in attrs:
                    marker = attrs['marker']
                    
                if 'markersize' in attrs:
                    markersize = attrs['markersize']

                if 'markerfacecolor' in attrs:
                    markerfacecolor = attrs['markerfacecolor']

                if 'markeredgecolor' in attrs:
                    markeredgecolor = attrs['markeredgecolor']

                if 'markeredgewidth' in attrs:
                    markeredgewidth = attrs['markeredgewidth']
                    
                if 'linewidth' in attrs:
                    linewidth = attrs['linewidth']

                if 'linestyle' in attrs:
                    linestyle = attrs['linestyle']

                if 'linecolor' in attrs:
                    linecolor = attrs['linecolor']
                    
            if axis == 'left':
                entry = self.ax.plot(self.data.index, self.data[linecol], label=linecol,
                                     markersize=markersize, marker=marker,
                                     markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                     markeredgewidth=markeredgewidth,
                                     linestyle=linestyle, linewidth=linewidth, color=linecolor)
                self.legend_entries.append(entry[0])
                self.legend_labels.append(linecol)
            elif axis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                    
                entry = self.ax_right.plot(self.data.index, self.data[linecol], label=linecol,
                                           markersize=markersize, marker=marker,
                                           markerfacecolor=markerfacecolor, markeredgecolor=markeredgecolor,
                                           markeredgewidth=markeredgewidth,
                                           linestyle=linestyle, linewidth=linewidth, color=linecolor)
                self.legend_entries.append(entry[0])
                self.legend_labels.append(linecol)
            else:
                print('axis must be left or right, given ' + str(axis))
                raise VaueError

        # Re-create legend
        self.update_legend()

        # Set x-axis range if specified
        if xrange is not None:
            self.set_xrange(xrange)

    def add_bars(self, data, colname, baraxis='left', stack=True, barlinewidth=None, xrange=None, dict_attrs=None, debug=False):
        '''
        Add bar to chart
        '''

        if debug:
            print('Calling add_bars on "' + str(colname) + '"')
            
        barcols = _parse_cols(colname)

        # Line width of bar borders for all bars
        if barlinewidth is None:
            barlinewidth = matplotlib.rcParams['patch.linewidth']
        
        # Set self.data to be input data
        self.data = data
        # Set x-axis limits and trim data as needed
        if xrange is not None:
            xrange = self._parse_xrange(xrange)
            self._trim_data(xrange)

        # Guess freq of data and set bar width
        freq = guess_freq(self.data)
        if freq in 'DW':
            barwidth = 3
        elif freq == 'M':
            barwidth = 25
        elif freq == 'Q':
            barwidth = 70
        elif freq == 'A':
            barwidth =300

        # Iterate over barcols and plot each bar.
        cycle = iter(plt.rcParams['axes.prop_cycle'])
        used_colors = []

        # Need to keep track of positive and negative offsets if stacked.
        pos_offset = [0] * len(self.data)
        neg_offset = [0] * len(self.data)
        
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

            # Get any attributes that were assigned to this column
            if dict_attrs is not None and barcol in dict_attrs:
                # This should be a dict containing attributes for this column
                attrs = dict_attrs[barcol]
                if debug:
                    print(attrs)

                # If any were specified, overwrite stylefile

                # Hatch colors
                if 'barhatchcolor' in attrs:
                    barhatchcolor = attrs['barhatchcolor']

                # Hatch pattern in bars
                if 'barhatch' in attrs:
                    barhatch = attrs['barhatch']

                # Line width of hatches
                if 'barhatchwidth' in attrs:
                    barhatchwidth = attrs['barhatchwidth']
                    
            # For barcolor, if it is specified use it,
            # otherwise get the next color from the color cycle.
            if dict_attrs is not None and barcol in dict_attrs and 'barcolor' in dict_attrs[barcol]:
                barcolor = dict_attrs[barcol]['barcolor']
                used_colors.append(barcolor)
                if debug:
                    print('1. setting barcolor for ' + barcol + ' to ' + barcolor)
            else:
                barcolor = next(cycle)['color']
                while 1:
                    if barcolor in used_colors:
                        barcolor = next(cycle)['color']
                    else:
                        used_colors.append(barcolor)
                        if debug:
                            print('2. setting barcolor for ' + barcol + ' to ' + barcolor)
                        break

            if debug:
                if dict_attrs is not None and barcol in dict_attrs:
                    print('dict_attrs:')
                    print(dict_attrs[barcol])
                print('barhatch = ' + str(barhatch))
                print('barlinewidth = ' + str(barlinewidth))
                print('barhatchcolor = ' + str(barhatchcolor))
                print('barcolor = ' + str(barcolor))

            # Make copy of positive and negative parts.
            # Set mask to NA so that they don't show up with lines in the chart,
            # but when saving to pos_offset and neg_offset, set values to 0.
            _df_pos = self.data[[barcol]].copy()
            mask = _df_pos[barcol] < 0
            _df_pos.loc[mask, barcol] = np.nan
                
            _df_neg = self.data[[barcol]].copy()
            mask = _df_neg[barcol] > 0
            _df_neg.loc[mask, barcol] = np.nan
            
            if baraxis == 'left':
                # No direct way to set hatch line widths in ax.bar,
                # need to use plt.rc_context()
                with plt.rc_context({"hatch.linewidth": barhatchwidth}):
                    if ibarcol == 0:
                        # Draw negative first
                        entry = self.ax.bar(self.data.index, _df_neg[barcol],
                                            width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                            zorder=1, label=barcol)
                        # Draw positive
                        entry = self.ax.bar(self.data.index, _df_pos[barcol],
                                            width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                            zorder=1, label=barcol)
                    else:
                        # Draw negative first
                        entry = self.ax.bar(self.data.index, _df_neg[barcol],
                                            bottom=neg_offset,
                                            width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                            zorder=1, label=barcol)
                        # Draw positive
                        entry = self.ax.bar(self.data.index, _df_pos[barcol],
                                            bottom=pos_offset,
                                            width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                            zorder=1, label=barcol)
                        
                    # Draw again with black edgecolor
                    _ = self.ax.bar(self.data.index, _df_pos[barcol],
                                    width=barwidth, color='none', edgecolor='black', linewidth=barlinewidth,
                                    bottom=pos_offset,
                                    zorder=2)
                    _ = self.ax.bar(self.data.index, _df_neg[barcol],
                                    bottom=neg_offset,
                                    width=barwidth, color='none', edgecolor='black', linewidth=barlinewidth,
                                    zorder=2)
            # end of baraxis == 'left'
            elif baraxis == 'right':
                if self.ax_right is None:
                    self.ax_right = self.ax.twinx()
                    # Set color cycler to be common with the left y-axis.
                    # Hack from https://github.com/matplotlib/matplotlib/issues/19479
                    self.ax_right._get_lines = self.ax._get_lines
                    
                # No direct way to set hatch line widths in ax.bar,
                # need to use plt.rc_context()
                with plt.rc_context({"hatch.linewidth": barhatchwidth}):
                    if ibarcol == 0:
                        # Draw negative first
                        entry = self.ax_right.bar(self.data.index, _df_neg[barcol],
                                                  width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                  zorder=1, label=barcol)
                        # Draw positive
                        entry = self.ax_right.bar(self.data.index, _df_pos[barcol],
                                                  width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                  zorder=1, label=barcol)
                    else:
                        # Draw negative first
                        entry = self.ax_right.bar(self.data.index, _df_neg[barcol],
                                                  bottom=neg_offset,
                                                  width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                  zorder=1, label=barcol)
                        # Draw positive
                        entry = self.ax_right.bar(self.data.index, _df_pos[barcol],
                                                  bottom=pos_offset,
                                                  width=barwidth, color=barcolor, edgecolor=barhatchcolor, hatch=barhatch, linewidth=0,
                                                  zorder=1, label=barcol)
                        
                    # Draw again with black edgecolor
                    _ = self.ax_right.bar(self.data.index, _df_pos[barcol],
                                          width=barwidth, color='none', edgecolor='black', linewidth=barlinewidth,
                                          bottom=pos_offset,
                                          zorder=2)
                    _ = self.ax_right.bar(self.data.index, _df_neg[barcol],
                                          bottom=neg_offset,
                                          width=barwidth, color='none', edgecolor='black', linewidth=barlinewidth,
                                          zorder=2)
                    
            # end of baraxis == 'left'
            
            # Adjust offsets
            neg_offset += _df_neg[barcol].replace(np.nan, 0).values
            pos_offset += _df_pos[barcol].replace(np.nan, 0).values

            self.legend_entries.append(entry[0])
            self.legend_labels.append(barcol)
        # end of loop over barcols

        # Re-create legend
        self.update_legend()
        
        # Set x-axis range if specified
        if xrange is not None:
            self.set_xrange(xrange)
        
    def add_scatter(self, data, colname, dict_attrs=None, debug=False):
        '''
        Add scatter to chart
        '''

        # Merge with self.data
        pass

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
        if not os.path.isdir(dirname):
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

