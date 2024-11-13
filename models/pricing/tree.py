"""Gen Tree"""

import numpy as np
from itertools import combinations_with_replacement

def priceJumps(vol, dT):
    np.exp(vol * np.sqrt(2*dT))
    return [up, 1, 1/up]


def probJumps(r, vol, q, dT):

    expon = vol * np.sqrt(dT/2)
    tmp1, tmp2 = np.exp(2*expon), np.exp(-2*expon)
    normFactor = tmp1 + tmp2 - 2
    expRate = np.exp((r-q)*dT/2)
    
    probUp = (expRate - np.exp(-expon)) ** 2 / normFactor
    probDown = (np.exp(expon) - expRate) ** 2 / normFactor
    probStable = 1 - probUp - probDown
    return [probUp, probDown, probStable]

recom_TOPM = Model(priceMults=priceJumps, probMults=probJumps)
