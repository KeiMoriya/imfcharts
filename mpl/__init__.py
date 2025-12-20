'''
2024-10-23

__init__.py for imfcharts/mpl
'''

import os
import sys
import glob
import shutil

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

# Get available styles in this project
stylefiles = glob.glob(os.path.abspath(os.path.dirname(__file__) + '/*.mplstyle'))

# This is where mplstyle files need to be for matplotlib to find them
STYLEDIR = os.path.abspath(matplotlib.get_configdir() + '/stylelib')
if not os.path.isdir(STYLEDIR):
    os.makedirs(STYLEDIR)

def install_styles(force: bool = False, verbose: bool = False) -> list[str]:
    """
    Copy local .mplstyle files into Matplotlib's stylelib directory so that
    `plt.style.use("imf-articleiv")` works everywhere.

    Best-effort: if we can't write to STYLEDIR, we do not crash.
    Returns a list of installed/copied style filenames.
    """
    installed = []
    try:
        os.makedirs(STYLEDIR, exist_ok=True)
        for stylefile in stylefiles:
            basename = os.path.basename(stylefile)
            outfilename = os.path.abspath(os.path.join(STYLEDIR, basename))
            if force or not os.path.isfile(outfilename):
                shutil.copy(stylefile, outfilename)
                installed.append(basename)
        if installed:
            # Reload Matplotlib so style files are available
            plt.style.reload_library()
    except Exception as e:
        if verbose:
            print(f"WARNING: Could not install styles into {STYLEDIR}: {e}")
    return installed

install_styles(force=False, verbose=False)

def _local_style_path(stylename: str) -> str | None:
    """
    Return the absolute path to a local .mplstyle shipped with this package, if it exists.
    Accepts "imf-articleiv" or "imf-articleiv.mplstyle".
    """
    name = stylename
    if not name.endswith(".mplstyle"):
        name += ".mplstyle"
    p = os.path.join(os.path.dirname(__file__), name)
    return p if os.path.isfile(p) else None

def update_style(stylename):
    '''
    Copy over local mplstyles to where matplotlib can find them i f any local changes are made.
    Input is name of style file like "imf-articleiv".
    '''

    # Check input type
    if type(stylename) != str:
        print('stylename must be str, given ' + str(stylename) + ' of type ' + str(type(stylename)))
        sys.exit(-1)

    # Check style file exists
    if not stylename.endswith('.mplstyle'):
        stylename += '.mplstyle'
    infilename = os.path.join(os.path.dirname(__file__), stylename)
    if not os.path.isfile(infilename):
        print('File ' + infilename + ' does not exist')
        sys.exit(-1)

    # Copy to STYLEDIR
    outfilename = os.path.join(STYLEDIR, os.path.basename(infilename))
    try:
        shutil.copy(infilename, outfilename)
    except Exception as e:
        print('WARNING: Could not copy file ' + infilename + ' to ' + outfilename)

    # Reload Matplotlib so style files are available
    plt.style.reload_library()

def set_style(stylename):
    '''
    Set current style to specified style.
    '''

    # Check input type
    if type(stylename) != str:
        print('stylename must be str, given ' + str(stylename) + ' of type ' + str(type(stylename)))
        sys.exit(-1)
    stylename = stylename.replace('.mplstyle', '')

    # Reload Matplotlib so style files are available
    plt.style.reload_library()
    
    # Get available styles
    styles = plt.style.available + ['default']
    if stylename in styles:
        plt.style.use(stylename)
        return

    # Fallback: if style couldn't be installed (e.g., read-only config dir),
    # try loading the packaged .mplstyle directly by path.
    local_path = _local_style_path(stylename)
    if local_path:
        plt.style.use(local_path)
        return

    raise RuntimeError('Style ' + stylename + ' does not exist (not installed and no local .mplstyle found)')

    
def _rgb2hex(r, g, b):
    '''
    Custom function to return "#RRGGBB"-formatted string
    from 3 integers between 0-255.
    '''

    # Check input for r
    if type(r) != int:
        print('Type of r must be int, not ' + str(type(r)))
        sys.exit(-1)
    if r < 0 or 255 < r:
        print('r must be between 0-255, given ' + str(r))
        sys.exit(-1)

    # Check input for g
    if type(g) != int:
        print('Type of g must be int, not ' + str(type(g)))
        sys.exit(-1)
    if g < 0 or 255 < g:
        print('g must be between 0-255, given ' + str(g))
        sys.exit(-1)

    # Check input for b
    if type(b) != int:
        print('Type of b must be int, not ' + str(type(b)))
        sys.exit(-1)
    if b < 0 or 255 < b:
        print('b must be between 0-255, given ' + str(b))
        sys.exit(-1)
        
    # Convert
    return rgb2hex([r/255, g/255, b/255])[1:].upper()

def test():
    # Need imf_datatools to run
    import imf_datatools
    df = imf_datatools.get_ecos_sdmx_data('WEO_WEO_LIVE', ['111', '193', '158'], 'NGDPD')

    plt.style.use('imf-articleiv')
    fig, ax = plt.subplots(1, 1)
    df.plot(ax=ax)
    legend = ax.legend()
    plt.show()

__version__ = '0.1'

