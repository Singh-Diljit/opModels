"""First order greeks for Black's approximation."""

from scipy.stats import norm
import numpy as np

def firstOrder(h, S, K, r, T, vol, div, dYr, call=True, greek='delta'):
    """Compute first order sensitivites via difference quotiant.

    Parameters
    ----------
    h    : float : Radius of paramater interval. 
    S    : float : Current price of stock.
    K    : float : Strike price of the option.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    vol  : float : Volatility of the stock.
    div  : list  : List of dividend payment(s).
    dYr  : list  : Time, in years, of dividend payout(s).
    call : bool  : If pricing call.
    greek: str   : Paramater whose sensativity is being measured.

    Returns
    -------
    float : Approximation of greek.

    Example(s)
    ---------
    >>> firstOrder(h=.1, S=50, K=55, r=.1, T=.5, vol=.3,
                            div=[.7]*2, dYr=[3/12, 5/12], greek='delta')
    >>> 0.4063443040186243
    
    """
    if greek == 'theta':
        dYr = np.array([np.append(dYr, T-h), np.append(dYr, T+h)])
    else:
        dYr = np.append(dYr, T)

    rateTime = r * dYr    
    if greek == 'rho':
        hdYr = h * dYr
        rateTime = np.array([rateTime - hdYr, rateTime + hdYr])

    disc = np.exp(-rateTime)
    div = np.append(div, 0)
    adjK = K * disc

    adjS = S - np.cumsum(disc * div)
    if greek == 'delta':
        adjS = np.array([adjS - h, adjS + h])

    rootTime = np.sqrt(dYr)
    stdDev = vol * rootTime
    if greek == 'vega':
        hrootTime = h * rootTime
        stdDev = np.array([stdDev - hrootTime, stdDev + hrootTime])
        
    logChange = np.log(adjS / K) + rateTime
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else:
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS
        
    prA, prB = np.amax(value, axis=1)
    diffQ = (prB - prA) / (2*h)
    
    return diffQ
