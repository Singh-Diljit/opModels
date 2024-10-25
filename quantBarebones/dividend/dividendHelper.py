"""Helper functions for implementation of Dividend class."""

import numpy as np
from numpy import datetime64

def timeDif(date1, date2):
    resInDays = date2 - date1
    a = str(resInDays).split(' ')
    return int(a[0])

def resolve_DiscCont(div, times, dates):
    disc = times or dates
    return disc, not(disc)

def makePayTimes(disc, times, dates, startDate):
    if not disc:
        res = np.array([np.inf])
    elif times:
        res = np.array(times)
    else:
        date_ = datetime64(startDate)
        res = np.array([timeDif(date_, datetime64(d)) for d in dates])/365
    return res
