"""Implement Black's Approximation."""

import numpy as np
from scipy.stats import norm

def blacksApproximation(S, K, r, T, vol, q, dYr, call=True):
    """Price an American option paying discrete dividends.

    Parameters
    ----------
    S   : float : Current price of stock.
    K   : float : Strike price of the option.
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    vol : float : Volatility of the stock.
    q   : array : Dividend payment(s).
    dYr : array : Time, in years, of dividend payout(s).
    call: bool, optional : If pricing call.

    Returns
    -------
    optionValue : float : Value of option.

    Example(s)
    ----------
    >>> qdiv, qtimes = np.array([.7, .7]), np.array([[3/12, 5/12]])
    >>> blacksApproximation(S=50, K=55, r=.1, T=.5, vol=.3,
                            q=qdiv, dYr=qtimes)
    >>> 2.6756877949596003

    >>> blacksApproximation(S=55, K=50, r=.1, T=.5, vol=.3,
                            q=qdiv, dYr=qtimes, call=False)
    >>> 1.8991667424392134
    
    """
    dYr, div = np.append(dYr, T), np.append(q, 0)
    rateTime = r * dYr
    disc = np.exp(-rateTime)
    adjS = S - np.cumsum(disc * div)
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
    
    return max(value)
