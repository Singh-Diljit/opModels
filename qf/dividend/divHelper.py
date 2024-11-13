"""Supporting functions for Dividend.py"""

import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import helperFunctions.helperFunctions as hf

def discCand(discrete, times, dates):
    """Return if dividend type may be discrete."""
    if not(discrete is None):
        res = discrete
    elif (times is None) and (dates is None):
        res = False
    else:
        res = True

    return res

def extractDiv(div, discrete, times, dates):
    """Return dividend and dividend type (discrete or continuous).

    Parameters
    ----------
    div      : array_like, float : Dividend payment quantity.
    discrete : bool      , None  : Dividend type.
    times    : array_like, None  : Ascending time until disbursements.
    dates    : array_like, None  : Dates of future disbursements.

    Returns
    -------
    res : tuple : Dividend type (bool) and dividend (np.array or float).

    Notes
    -----
    For definition of array_like, see relevant numpy documentation.

    """
    div_, cont = hf.makeArray(div), False
    discrete = discCand(discrete, times, dates)
    
    if not(discrete):
        res = (cont, np.sum(div_))
    elif np.sum(div_) == 0:
        res = (cont, 0)
    else:
        res = (discrete, div_)
        
    return res

def timeDif(date1, date2):
    """Return the number of days from start of date1 to start of date2.

    Parameters
    ----------
    date1 : datetime64 : Start date.
    date2 : datetime64 : End date.

    Returns
    -------
    - : int : Number of days between two dates.

    Example(s)
    ----------
    >>> timeDif(np.datetime64('today'), np.datetime64('today'))
    >>> 0

    """
    splitDateDiff = str(date2 - date1).split(' ')
    return int(splitDateDiff[0])

def getTimes(discrete, times, dates, startDate):
    """Return an array of times in years of dividend payouts.

    Parameters
    ----------
    discrete   : bool             : If dividend is discrete.
    times      : array_like, None : Ascending times (years) until disbursements.
    dates      : array_like, None : Dates of future disbursements.
    startDate  : date_like , None : Start date.

    Returns
    -------
    res : array : Array of times in years of dividend payouts.

    Notes
    -----
    The inputs 'times' and 'dates' are not both 'None'.
    
    For definition of array_like, see relevant numpy documentation.

    For definition of date_like, see this project's time module. Generally,
    ISO8601 compliant strings are accepted, in addition to all other forms
    accepted by numpy's datetime64 module. For more robust input options
    see parseDate function in time.offline.

    """
    if not discrete:
        res = np.array([np.inf])
    elif times:
        res = np.array(times)
    else:
        date_ = np.datetime64(startDate)
        res = np.array([timeDif(date_, np.datetime64(d)) for d in dates])/365

    return res
