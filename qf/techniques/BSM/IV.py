
from scipy.stats import norm
import numpy as np

def freqVol(vol, sqrtT, logChange, adjS, adjK, call=True):
    """Return the BSM price when volatility is the only variable."""
    stdDev = vol * sqrtT
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else: #pricing a put
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS

    return value

def freqVega(vol, sqrtT, logChange, adjS):
    """Return vega when volatility is the only variable."""
    stdDev = vol * sqrtT
    d1 = (logChange)/stdDev + stdDev/2

    return adjS * norm().pdf(d1) * sqrtT

def vol(opPr, S, K, r, T, q, call=True, volEst=.1, eps=10**(-5), maxIts=200):
    """Return the BSM implied volatility of an option.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility assuming a BSM pricing model.

    Parameters
    ----------
    [See document header]
    opPr  : float : Price of contract.
    S     : float : Current price of stock. (float)
    K     : float : Strike price of the option. (float)
    r     : float : Annualized risk-free interest rate, continuously compounded.
    T     : float : Time, in years, until maturity.
    q     : float : Continous dividend rate.
    call  : bool  : If calculating rho of a call.
    volEst: float : Initial guess at volatility.
    eps   : float : Accepted error in option price error.
        (Not the same as error in IV.)
    maxIts: float : Maximum number of iterations function will perfrom.

    Returns
    -------
    volEst : float : The BSM implied volatility.
    
    Example(s)
    ----------
    >>> vol(19.55, 172.37, 175, .0463, 1, .0055)
    >>> 0.256812757150514

    >>> vol(1.0645842934501353, 100, 90, .08, .5, .004, call=False)
    >>> 0.20000000001801496
    
    """
    rateTime, divTime = r * T, q * T
    rateDisc, divDisc = np.exp(-rateTime), np.exp(-divTime)
    adjS, adjK = S * divDisc, K * rateDisc

    sqrtT = np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)

    for _ in range(maxIts):
        prEst = freqVol(volEst, sqrtT, logChange, adjS, adjK, call)
        error = opPr - prEst
        if abs(error) < eps:
            break
        vega_ = freqVega(volEst, sqrtT, logChange, adjS)
        volEst += error / vega_
    
    return volEst
