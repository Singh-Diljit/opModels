"""Solve for IV in Black's approximation."""

from scipy.stats import norm
import numpy as np

def freqVol(vol, rootTime, logChange, adjS, adjK, call=True):
    """Return Black's Approximation when volatility is the only variable."""
    stdDev = vol * rootTime
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else: #pricing a put
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS

    return max(value), stdDev

def freqVega(h, prA, stdDev, rootTime, logChange, adjS, adjK, call=True):
    """Return vega when volatility is the only variable."""
    stdDev += h * rootTime
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else: #pricing a put
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS

    prB = max(value)
    diffQ = (prB - prA) / h
    
    return diffQ

def vol(opPr, S, K, r, T, q, dYr, call=True, volEst=.1, eps=10**(-5), maxIts=200):
    """Compute the implied volatility of an option via Black's Approximation.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility..

    Parameters
    ----------
    opPr   : Price of contract.
    S      : Current price of stock.
    K      : Strike price of the option.
    r      : Annualized risk-free interest rate, continuously compounded.
    T      : Time, in years, until maturity.
    vol    : Volatility of the stock.
    q      : Array of dividend payment(s).
    dYr    : Time, in years, of dividend payout(s).
    call   : If pricing call.
    volEst : Initial guess at volatility.
    eps    : Accepted error in optionPrice error.
        (Not the same as error in IV.)
    maxIts    : Maximum number of iterations function will perfrom.

    Returns
    -------
    The implied volatility.
    
    Example(s)
    ----------
    >>> qdiv, qtimes = np.array([.7, .7]), np.array([[3/12, 5/12]])
    >>> vol(opPr=2.6756877949596003, S=50, K=55, r=.1, T=.5, q=qdiv, dYr=qtimes)
    >>> 0.30000000067408783

    >>> qdiv, qtimes = np.array([.7, .7]), np.array([[3/12, 5/12]])
    >>> vol(opPr=1.8991667424392134, S=55, K=50, r=.1, T=.5, q=qdiv, dYr=qtimes, call=False)
    >>> 0.3000000010474237

    #An example where early ex. is optimal.
    >>> qdiv, qtimes = np.array([.1, 10]), np.array([[3/12, 5/12]])
    >>> vol(opPr=1.5769675819620286, S=50, K=55, r=.1, T=.5, q=qdiv, dYr=qtimes)
    >>> 0.3000002376937799

    """
    dYr, div = np.append(dYr, T), np.append(q, 0)
    rateTime = r * dYr
    disc = np.exp(-rateTime)
    adjS = S - np.cumsum(disc * div)
    adjK = K * disc
    rootTime = np.sqrt(dYr)
    logChange = np.log(adjS / K) + rateTime

    h = .05
    for _ in range(maxIts):
        prEst, stdDev = freqVol(volEst, rootTime, logChange, adjS, adjK, call)
        error = opPr - prEst
        if abs(error) < eps:
            break
        vega = freqVega(h, prEst, stdDev, rootTime, logChange, adjS, adjK, call)
        h = error / vega
        volEst += h
    
    return volEst
