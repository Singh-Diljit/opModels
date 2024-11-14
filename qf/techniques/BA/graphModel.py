"""Graph Black's approximation."""

import numpy as np
from scipy.stats import norm
from graphingFunc import *

#Shape of dYr is off when appending T if also vbarying T.

def vars_not_divRelated(S, K, r, T, vol, q, dYr, call=True):
    """Black's Approximation with one of S, K, or vol having multiple inputs.

    Parameters
    ----------
    S   : float, array_like : Current price of stock.
    K   : float, array_like : Strike price of the option.
    r   : float, array_like :
            Annualized risk-free interest rate, continuously compounded.
    T   : float, array_like : Time, in years, until maturity.
    vol : float, array_like : Volatility of the stock.
    q   : array_like : Dividend payment(s).
    dYr : array_like : Time, in years, of dividend payout(s).
    call: bool, optional : If pricing call.

    Returns
    -------
    optionValue : array : Value of options.

    Notes
    -----
    The variable with multiple entries should be of shape:
    (1, N), N > 0 (that is 2D arrays).

    """
    dYr, div = np.append(dYr, T), np.append(q, 0)
    rateTime = r * dYr

    disc = np.exp(-rateTime)
    ax = 0 if len(disc.shape) == 1 else 1
    
    adjS = S - np.cumsum(disc * div, axis=ax)
    adjK = K * disc

    stdDev = vol * np.sqrt(dYr)
    logChange = np.log(adjS / K) + rateTime
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else:
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS

    ax = 0 if len(value.shape) == 1 else 1
    
    return np.max(value, axis=ax)

def vars_divRelated(S, K, r, T, vol, q, dYr, call=True):

    dYr, q = np.array(dYr), np.array(q)
    if len(q.shape) == 1 and len(dYr.shape) == 1:
        div = np.append(q, 0)
        dYr = np.append(dYr, T)
    elif len(q.shape) == 2:
        div = np.hstack((q, np.zeros(shape=(q.shape[0],1))))
        dYr = np.array([np.append(dYr, T) for _ in range(q.shape[0])])
    else:
        col = np.ones(shape=(q.shape[0],1)) * T
        dYr = np.hstack((dYr, col))
        div = np.array(list(np.append(dYr, 0))*dYr.shape[0])
    
    rateTime = r * dYr
    disc = np.exp(-rateTime)

    ax = 0 if len(disc.shape) == 1 else 1
    adjS = S - np.cumsum(disc * div, axis=ax)
    adjK = K * disc

    stdDev = vol * np.sqrt(dYr)
    logChange = np.log(adjS / K) + rateTime

    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else:
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS

    ax = 0 if len(value.shape) == 1 else 1
    
    return np.max(value, axis=ax)

def graphBlacksApprox(S, K, r, T, vol, q, dYr, call=True):
    labels = getLabelsBlacksApprox(S, K, r, T, vol, q, dYr, call)
    xTitle, opType = labels['xTitle'], labels['opType']
    yTitle = f'Value of {opType}'
    graphTitle = f'Price of {opType} as {xTitle} Varies'

    dic = {'Spot Price': S, 'Strike Price': K,
              'Interest Rate': r, 'Time till Maturity (Years)': T,
              'Volatility': vol, 'Dividends': q,
              'Dividend PayOut Times (Years)': dYr}
    
    xVals = dic[xTitle]
    if xTitle in ['Spot Price', 'Strike Price',
                  'Interest Rate', 'Time till Maturity (Years)',
                  'Volatility']:
        yVals = vars_not_divRelated(S, K, r, T, vol, q, dYr, call)
    else:
        yVals = vars_divRelated(S, K, r, T, vol, q, dYr, call)
        
    simpleGraph(xVals, yVals, xTitle, yTitle, graphTitle)


K = np.linspace(40, 60, num = 50)[:, np.newaxis]
T = np.linspace(.05, 1, num = 10)[:, np.newaxis]
graphBlacksApprox(50, 55, .1, T, .3, [.7, .7], [.25, .5])

