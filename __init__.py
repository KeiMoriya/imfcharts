
import locale
import platform

import matplotlib.pyplot as plt

from .charts import Chart
from .charts import read

from .mpl import *

# Define IMF colors
AXISGREY  = '#B3B3B3'
AXISGRAY  = '#B3B3B3'
IMFBLUE   = '#4B82AD'
IMFGREEN  = '#96BA79'
IMFRED    = '#C00000'
IMFGREY   = '#A6A8AC'
IMFGRAY   = '#A6A8AC'
IMFBLACK  = '#000000'

# IMF colors from IMF Brand Guide
FUNDBLUE = '#004C97'
FUNDPACIFICBLUE = '#009CDE'
FUNDGREEN = '#78BE20'
FUNDYELLOW = '#F2A900'
FUNDORANGE = '#FF8200'
FUNDDARKORANGE = '#DA291C'
FUNDPURPLE = '#8031A7'
FUNDRED = '#DA291C'
FUNDGREY = '#B1B3B3'
FUNDGRAY = '#B1B3B3'
FUNDSNOWFALL = '#D8D9D9'
FUNDMUTEDGREY = '#707372'
FUNDMUTEDGRAY = '#707372'
FUNDCOOLBLACK = '#001E60'

# Set up commonly used styles so they can be easily used.
# Usage:
# Make sure to copy, otherwise will modify original
# style = LINE_AND_MARKER.copy()
# dict_attrs = {col : style}
# chart = Chart(df, linecols=linecols, dict_attrs=dict_attrs)
REDCIRCLES = {'linewidth' : 0,
              'color' : IMFRED,
              'linestyle' : '-',
              'marker' : 'o',
              'markersize' : 10,
              'markerfacecolor' : AXISGRAY,
              'markeredgewidth' : 0,
              'markeredgecolor' : AXISGRAY}

# Set default style
try:
    set_style('imf-articleiv')
except Exception as e:
    print('Could not set style with exception:')
    print(e)




def lang(lang_code: str = "en") -> str:
    """
    Set LC_TIME based on a 2-letter language code and the current OS.

    Parameters
    ----------
    lang_code : str, default "en"
        Two-letter language code such as "en", "fr", "de", "ja".
        Common aliases like "jp" are normalized to "ja".

    Returns
    -------
    str
        The locale string that was successfully set.

    Raises
    ------
    ValueError
        If the language code is not supported by this function.
    locale.Error
        If no matching locale could be set on the current system.
    """

    lang = (lang_code or "en").strip().lower()

    # Normalize common aliases
    aliases = {
        "jp": "ja",
        "cn": "zh",
    }
    lang = aliases.get(lang, lang)

    system = platform.system()

    # OS-specific locale candidates, in order of preference
    locale_map = {
        "en": {
            "Windows": ["English_United States", "English", "en-US"],
            "Darwin": ["en_US.UTF-8", "en_US", "C"],
            "Linux": ["en_US.UTF-8", "en_US", "C"],
        },
        "fr": {
            "Windows": ["French_France", "French", "fr-FR"],
            "Darwin": ["fr_FR.UTF-8", "fr_FR"],
            "Linux": ["fr_FR.UTF-8", "fr_FR"],
        },
        "de": {
            "Windows": ["German_Germany", "German", "de-DE"],
            "Darwin": ["de_DE.UTF-8", "de_DE"],
            "Linux": ["de_DE.UTF-8", "de_DE"],
        },
        "es": {
            "Windows": ["Spanish_Spain", "Spanish", "es-ES"],
            "Darwin": ["es_ES.UTF-8", "es_ES"],
            "Linux": ["es_ES.UTF-8", "es_ES"],
        },
        "it": {
            "Windows": ["Italian_Italy", "Italian", "it-IT"],
            "Darwin": ["it_IT.UTF-8", "it_IT"],
            "Linux": ["it_IT.UTF-8", "it_IT"],
        },
        "pt": {
            "Windows": ["Portuguese_Brazil", "Portuguese", "pt-BR", "pt-PT"],
            "Darwin": ["pt_BR.UTF-8", "pt_PT.UTF-8", "pt_BR", "pt_PT"],
            "Linux": ["pt_BR.UTF-8", "pt_PT.UTF-8", "pt_BR", "pt_PT"],
        },
        "ja": {
            "Windows": ["Japanese_Japan", "Japanese", "ja-JP"],
            "Darwin": ["ja_JP.UTF-8", "ja_JP"],
            "Linux": ["ja_JP.UTF-8", "ja_JP"],
        },
        "zh": {
            "Windows": ["Chinese_China", "Chinese", "zh-CN"],
            "Darwin": ["zh_CN.UTF-8", "zh_CN"],
            "Linux": ["zh_CN.UTF-8", "zh_CN"],
        },
        "ko": {
            "Windows": ["Korean_Korea", "Korean", "ko-KR"],
            "Darwin": ["ko_KR.UTF-8", "ko_KR"],
            "Linux": ["ko_KR.UTF-8", "ko_KR"],
        },
    }

    if lang not in locale_map:
        raise ValueError(f"Unsupported language code: {lang_code!r}")

    candidates = locale_map[lang].get(system, []) + ["C"]

    def _set_category(category):
        last_error = None
        for loc in candidates:
            try:
                return locale.setlocale(category, loc)
            except locale.Error as e:
                last_error = e
        raise locale.Error(
            f"Could not set locale category {category} for language code "
            f"{lang_code!r} on {system}. Tried: {candidates}"
        ) from last_error

    time_result = _set_category(locale.LC_TIME)
    numeric_result = _set_category(locale.LC_NUMERIC)

    # This is necessary for Matplotlib 3.8.0 so that y-aixs values
    # do not show as 40{,}000 etc.
    plt.rcParams["axes.formatter.use_mathtext"] = True

    return {
        "LC_TIME": time_result,
        "LC_NUMERIC": numeric_result,
    }
